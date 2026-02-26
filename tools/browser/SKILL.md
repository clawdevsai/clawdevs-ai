# 🌐 agent-browser

**Objetivo:** Automação de browser para QA (E2E), Developer (validação de frontend) e UX (análise de fluxos, evidências).  
**Quando usar:** Testes de interface, submissão de formulários, capturas de tela, verificação de acessibilidade, demos gravadas.  
**Permissão:** `Bash(agent-browser:*)` — somente agentes autorizados (QA, Developer, UX).  
**Referência:** `docs/11-ferramentas-browser.md`

---

## Pré-requisitos

```bash
# Instalar (apenas após aprovação do Diretor via checklist Zero Trust)
npm install -g agent-browser
agent-browser install --with-deps

# Verificar instalação
agent-browser --version
```

> **Zero Trust:** Não navegar para URLs fora da egress whitelist do cluster sem aprovação explícita do Diretor.  
> **Sem binários:** agent-browser é instalado via npm (texto claro). Verificar `skillstracelock.json` antes de instalar.

---

## Passos

### 1. Abrir página e obter snapshot

```bash
agent-browser open <url>
agent-browser snapshot -i          # Apenas elementos interativos (recomendado)
agent-browser snapshot -i --json   # Saída JSON para parsing pelo agente
```

### 2. Interagir com elementos (usando @refs do snapshot)

```bash
agent-browser click @e1
agent-browser fill @e2 "valor"      # Limpa e digita (preferir a type)
agent-browser press Enter
agent-browser wait --load networkidle
```

### 3. Verificar resultado

```bash
agent-browser snapshot -i           # Novo snapshot após navegação
agent-browser get text @e1
agent-browser get url
```

### 4. Capturar evidência

```bash
agent-browser screenshot evidencia.png --full
agent-browser pdf relatorio.pdf
agent-browser record start demo.webm
agent-browser record stop
```

### 5. Fechar

```bash
agent-browser close
```

---

## Referência rápida de comandos

| Categoria | Comando | Descrição |
|-----------|---------|-----------|
| **Navegação** | `open <url>` | Abre URL |
| | `back` / `forward` / `reload` | Histórico |
| | `close` | Fecha browser |
| **Snapshot** | `snapshot -i` | Elementos interativos com refs |
| | `snapshot -c` | Saída compacta |
| | `snapshot -s "#main"` | Escopo por seletor CSS |
| **Interação** | `click @e1` | Clique |
| | `fill @e2 "texto"` | Digita (limpa antes) |
| | `type @e2 "texto"` | Digita sem limpar |
| | `press Enter` | Tecla |
| | `hover @e1` | Hover |
| | `check @e1` / `uncheck @e1` | Checkbox |
| | `select @e1 "valor"` | Select dropdown |
| | `scroll down 500` | Scroll |
| | `drag @e1 @e2` | Arrastar |
| **Obter dados** | `get text @e1` | Texto |
| | `get attr @e1 href` | Atributo |
| | `get url` | URL atual |
| **Esperar** | `wait @e1` | Elemento aparecer |
| | `wait --text "Sucesso"` | Texto na página |
| | `wait --url "/dashboard"` | Padrão de URL |
| | `wait --load networkidle` | Rede ociosa |
| **Evidências** | `screenshot path.png` | Screenshot |
| | `screenshot --full` | Página inteira |
| | `pdf output.pdf` | PDF |
| | `record start demo.webm` / `stop` | Vídeo |
| **Sessões** | `state save auth.json` | Salvar sessão (login) |
| | `state load auth.json` | Restaurar sessão |
| | `--session nome` | Sessão paralela isolada |
| **Debug** | `--headed` | Mostrar janela |
| | `console` | Erros de console |
| | `highlight @e1` | Destacar elemento |

---

## Localizadores semânticos (alternativa a @refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Entrar" click
agent-browser find label "Email" fill "user@test.com"
```

---

## Integração por agente

| Agente | Casos de uso |
|--------|-------------|
| **QA** | Testes E2E completos, verificação de acessibilidade, fluxos de regressão, evidências de bug |
| **Developer** | Validação de frontend durante dev, preenchimento de demos, extração de dados de UI |
| **UX** | Análise de fluxos, gravação de demos para stakeholders, verificação de responsivo |

---

## Segurança e boas práticas

- **Refs mudam após navegação:** sempre tirar novo snapshot após navegar.
- **Usar `fill` em vez de `type`** em inputs para garantir limpeza do campo.
- **Elemento não encontrado:** tirar snapshot para obter ref correta antes de tentar novamente.
- **Não navegar para URLs não validadas:** verificar egress whitelist do cluster.
- **Estado de login:** salvar em `auth.json` local; nunca commitar no repositório.
- Registrar gotchas e erros recorrentes em `memory/warm/TOOLS.md`.

---

## Exemplos completos

### E2E de login (QA)

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
# textbox "Email" [ref=e1], textbox "Senha" [ref=e2], button "Entrar" [ref=e3]
agent-browser fill @e1 "qa@example.com"
agent-browser fill @e2 "senha_teste"
agent-browser click @e3
agent-browser wait --url "/dashboard"
agent-browser snapshot -i
agent-browser screenshot evidencia-login-ok.png
agent-browser close
```

### Sessão autenticada reutilizável (Developer)

```bash
# Primeira vez: salvar estado
agent-browser open https://app.example.com/login
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "senha"
agent-browser click @e3
agent-browser wait --url "/dashboard"
agent-browser state save .auth/session.json

# Próximas sessões
agent-browser state load .auth/session.json
agent-browser open https://app.example.com/dashboard
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `command not found: agent-browser` | `npm install -g agent-browser && agent-browser install` |
| Elemento não encontrado | Tirar `snapshot -i` e usar ref correta |
| Página não carregou | Adicionar `wait --load networkidle` após `open` |
| Binário não encontrado no ARM64 | Usar caminho completo do binário |
| Timeout | Aumentar com `--timeout 10000` |
