# TOOLS.md - Arquiteto

## tools_disponiveis
- `read`: Ler arquivos concretos (Markdown, JSON, texto). Nunca ler diretórios.
- `write`: Escrever artefatos em `/data/openclaw/backlog` (tasks, ADRs, diagrams).
- `sessions_spawn`: Criar nova sessão com subagente (ex: `agentId='po', mode='session'`).
- `sessions_send`: Enviar mensagem para sessão existente.
- `sessions_list`: Listar sessões ativas.
- `internet_search`: Pesquisar boas práticas, padrões, tradeoffs (uso limitado a 2h por US).
- `gh`: **Disponível** (Arquiteto pode criar/atualizar issues, workflows). Usar sempre com `--repo "$GITHUB_REPOSITORY"` e `GITHUB_TOKEN`.

## regras_de_uso
- Sempre usar `sessions_spawn` com `agentId='po'` para delegação.
- Ao ler, especificar caminho completo do arquivo.
- Ao escrever, salvar em `/data/openclaw/backlog` com nomes padronizados.
- Usar `internet_search` apenas para validação de padrões arquiteturais (não para decisões de produto).
- Para GitHub:
  - `gh issue create` com `--label` múltiplos (ex: `--label task --label P0 --label ADR`)
  - Incluir no body: referências a TASK-XXX.md, US-XXX.md, ADR-XXX.md.
  - Vincular issues a US com `Closes #US-XXX` se aplicável.
  - Usar `gh api` para operações avançadas (ex: adicionar labels existentes).