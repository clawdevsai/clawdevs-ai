# 🆓 freeride — Modelos gratuitos OpenRouter

**Objetivo:** Configurar o OpenClaw para usar modelos gratuitos do OpenRouter com ranking automático, fallbacks e roteamento hierárquico (nuvem → GPU → CPU).  
**Quando usar:** Quando o Diretor quer reduzir custo de API usando modelos gratuitos, ou para ambientes de prototipagem.  
**Quem executa:** DevOps/SRE — após aprovação explícita do Diretor.  
**Referência:** `docs/22-modelos-gratuitos-openrouter-freeride.md`

---

## Pré-requisitos

```bash
# 1. Verificar OPENROUTER_API_KEY
echo $OPENROUTER_API_KEY
# Se vazia → Diretor deve definir:
export OPENROUTER_API_KEY="sk-or-v1-..."
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."

# 2. Verificar CLI freeride
which freeride
# Se não encontrar → instalar via checklist de skills (ver skill-discovery/SKILL.md)
```

---

## Passos

### 1. Configurar melhor modelo gratuito automaticamente

```bash
# Configuração automática (caso mais comum)
freeride auto

# Manter modelo primário atual, apenas adicionar fallbacks
freeride auto -f

# Configurar com mais fallbacks (padrão é 5)
freeride auto -c 10

# Reiniciar gateway para aplicar mudanças (SEMPRE após alterar config)
openclaw gateway restart
```

### 2. Verificar configuração aplicada

```bash
freeride status
# Exemplo de saída:
# Primário: openrouter/qwen/qwen3-coder:free
# Fallbacks: openrouter/free, nvidia/nemotron:free, ..., ollama/phi3:mini (CPU)
```

### 3. Explorar modelos disponíveis

```bash
freeride list           # Top 15 modelos gratuitos rankeados
freeride list -n 30     # Listar 30 modelos
freeride refresh        # Forçar atualização do cache
```

### 4. Trocar para modelo específico

```bash
freeride switch qwen3-coder
freeride switch qwen3-coder -f   # Apenas como fallback
openclaw gateway restart
```

---

## Roteamento hierárquico (anti-deadlock)

O FreeRide configura fallbacks em cascata para evitar deadlock quando nuvem e GPU estiverem saturadas:

```
Primário: openrouter/<modelo-gratuito>:free
    ↓ rate limit ou indisponível
Fallback 1: openrouter/free (roteador inteligente)
    ↓ saturado
Fallback 2: nvidia/nemotron:free (ou equivalente)
    ↓ saturado
...
Último fallback estrutural: ollama/phi3:mini (CPU only)
```

> **Atenção:** Fallback em CPU é último recurso. Com 9 agentes + K8s + Redis + LLM na CPU → risco de degradação severa. Priorizar antes pausar a fila.

---

## Hook de recuperação (freeride-watcher)

```bash
# Iniciar daemon de monitoramento
freeride-watcher --daemon

# Forçar rotação imediata
freeride-watcher --rotate

# Ver histórico de rotações
freeride-watcher --status
```

**O watcher faz:**
1. Detecta saturação de nuvem + GPU simultaneamente
2. Instrui OpenClaw a **pausar a fila do Sessions-Spawn** (evita deadlock)
3. Serializa árvore de raciocínio do sub-agente no **LanceDB** (coma controlado)
4. Monitora evento de liberação do GPU Lock via Redis
5. Recupera estado do LanceDB e retoma de onde parou — **sem perda de contexto**

---

## Roteamento preditivo por orçamento

```python
# config/agents/agents-config.yaml — configurar threshold
# Se previsão de tokens > limite diário → rotear para CPU antes de acionar freio

# O Gateway (orchestrator/gateway/gateway.py) implementa isso automaticamente
# via EfficiencyDegradation.get_model_for_ceo() quando ratio < 0.30
```

---

## Referência de comandos

| Comando | Quando usar |
|---------|-------------|
| `freeride auto` | Configurar melhor modelo gratuito (caso padrão) |
| `freeride auto -f` | Adicionar fallbacks mantendo primário atual |
| `freeride auto -c 10` | Mais fallbacks (padrão: 5) |
| `freeride list` | Ver modelos gratuitos disponíveis |
| `freeride list -n 30` | Listar 30 modelos |
| `freeride switch <modelo>` | Trocar para modelo específico |
| `freeride switch <modelo> -f` | Adicionar só como fallback |
| `freeride status` | Ver configuração atual |
| `freeride fallbacks` | Atualizar apenas fallbacks |
| `freeride refresh` | Forçar atualização do cache de modelos |
| `freeride-watcher --daemon` | Watcher contínuo (anti-deadlock) |

---

## O que é alterado na config

Somente as chaves de modelo em `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/qwen/qwen3-coder:free",
        "fallbacks": [
          "openrouter/free",
          "nvidia/nemotron:free",
          "ollama/phi3:mini"
        ]
      }
    }
  }
}
```

> O restante da config (gateway, canais, agentes nomeados, env, customInstructions) é **preservado integralmente**.

---

## Quem pode fazer o quê

| Agente | Sugerir | Executar freeride + restart gateway |
|--------|---------|-------------------------------------|
| CEO | ✅ (estratégia de custo) | ❌ — escalar ao DevOps/Diretor |
| PO | ✅ | ❌ |
| **DevOps** | ✅ | ✅ após aprovação do Diretor |
| Outros | Podem mencionar | ❌ |

---

## Aviso sobre limites

- Modelos gratuitos têm **rate limits** menores que pagos
- Qualidade pode ser inferior para tarefas complexas de arquitetura
- Recomendado para: prototipagem, tarefas simples, DevOps/UX em CPU
- **Não configurar em produção** sem aprovação explícita do Diretor
