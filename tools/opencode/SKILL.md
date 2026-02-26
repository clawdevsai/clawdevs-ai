# 💻 opencode — Controlador de sessões e fluxo Plan/Build

**Objetivo:** Controlar o OpenCode no pod do Developer para implementação de código via LLM. Todo código gerado pelo enxame passa pelo OpenCode — o orquestrador nunca escreve código diretamente.  
**Quando usar:** O Developer usa o OpenCode para implementar Issues aprovadas pelo PO/Architect.  
**Referência:** `docs/33-opencode-controller.md`

---

## Regra fundamental

> **O orquestrador não escreve código. Todo código nasce dentro do OpenCode.**

---

## Pré-voo (obrigatório antes de iniciar)

```bash
# 1. Confirmar provedor de IA e autenticação
opencode /models
# Verificar modelo ativo; se necessário autenticar:
opencode /auth                # Exibe link para autenticação
# Aguardar confirmação do Diretor se autenticação for necessária

# 2. Verificar sessões ativas
opencode /sessions
```

---

## Passos do fluxo Plan → Build

### Fase 1 — Plan (análise e proposta de plano)

```bash
# Iniciar OpenCode SEMPRE em modo Plan
opencode /agents
# Selecionar: Plan

# Apresentar a Issue ao OpenCode:
# "Issue #42: Implementar autenticação JWT
# Critérios de aceite:
# - Token de 24h com refresh rotativo de 7 dias
# - Endpoint /auth/refresh
# - Testes unitários cobrindo expiração e refresh"

# OpenCode analisa e propõe plano
# NÃO gerar código em Plan — apenas plano detalhado

# Aguardar feedback do Diretor/Architect sobre o plano
# Iterar se necessário (perguntas, ajustes)
```

### Fase 2 — Build (implementação)

```bash
# Só alternar para Build após plano aprovado
opencode /agents
# Selecionar: Build

# OpenCode implementa conforme o plano
# Monitorar progresso; intervir apenas em bloqueios
```

### Verificar e iterar

```bash
# Ver arquivos criados/modificados
opencode /status

# Se OpenCode fizer pergunta → responder com contexto da Issue
# Se OpenCode encontrar bloqueio (dependência faltando, conflito) → escalar ao Architect

# Ao concluir, criar PR via gh CLI:
gh pr create \
  --title "feat: JWT auth (#42)" \
  --body "Closes #42\n\n## Alterações\n$(opencode /summary)" \
  --base main \
  --head feat/jwt-auth \
  --draft
```

---

## Gestão de sessões

```bash
# Listar sessões ativas
opencode /sessions

# Reutilizar sessão do projeto atual (preferir a criar nova)
opencode /sessions --use <session-id>

# NUNCA criar nova sessão sem aprovação quando já há sessão ativa do projeto
# Motivo: perda de contexto e acúmulo de sessões ociosas
```

---

## Seleção de modelo no OpenCode

```bash
# Ver modelos disponíveis
opencode /models

# Modelo padrão para Developer: deepseek-coder:6.7b (Ollama local)
# Para tarefas complexas que precisam de raciocínio mais profundo: llama3:8b
# Se modelo requer autenticação externa: enviar link ao Diretor e aguardar confirmação
```

---

## Comportamento esperado em cada modo

### Modo Plan

| Situação | Ação do Developer |
|----------|------------------|
| OpenCode propõe plano | Verificar alinhamento com Issue e critérios de aceite |
| OpenCode tem dúvida técnica | Responder com contexto da documentação (docs/) |
| Plano parece subótimo | Questionar antes de aprovar; envolver Architect se necessário |
| Plano aprovado | Alternar para Build |

### Modo Build

| Situação | Ação do Developer |
|----------|------------------|
| OpenCode implementa | Monitorar; não interferir sem necessidade |
| OpenCode tem pergunta | Responder com precisão; não inventar respostas |
| Dependência não autorizada | **Parar** — escalar ao Architect/CyberSec para aprovação |
| Erro de compilação/lint | Deixar OpenCode resolver; intervir apenas após 3 tentativas |
| Build concluído | Criar PR draft e acionar pipeline de revisão |

---

## Regras do Developer com OpenCode

- **Uma Issue por vez** — nunca iniciar nova Issue sem PR anterior aprovado
- **Nunca fazer merge** do próprio código — Architect faz o merge
- **Nunca instalar bibliotecas** sem autorização de Architect + CyberSec
- **Nunca modificar** Dockerfile, YAMLs K8s ou Terraform diretamente
- **GPU Lock** antes de qualquer chamada ao Ollama (via `scripts/gpu_lock.py`)
- **Sandbox efêmero** para testes de dependências npm/pip
