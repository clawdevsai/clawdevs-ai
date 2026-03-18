# TOOLS.md - PO

## tools_disponiveis
- `read`: Ler arquivos concretos (Markdown, JSON, texto). Nunca ler diretórios.
- `write`: Escrever artefatos em `/data/openclaw/backlog`.
- `sessions_spawn`: Criar nova sessão com subagente (ex: `agentId='arquiteto', mode='session'`).
- `sessions_send`: Enviar mensagem para sessão existente.
- `sessions_list`: Listar sessões ativas.
- `internet_search`: Pesquisar mercado, concorrentes, regulamentações (uso limitado).
- `gh`: **Disponível** (PO pode criar/atualizar issues, PRs, labels). Usar sempre com `--repo "$GITHUB_REPOSITORY"` e `GITHUB_TOKEN`.

## regras_de_uso
- Sempre usar `sessions_spawn` com `agentId='arquiteto'` para delegação técnica.
- Ao ler, especificar caminho completo do arquivo.
- Ao escrever, salvar em `/data/openclaw/backlog` com nomes padronizados.
- Usar `internet_search` apenas para pesquisa de mercado (não para decisoes técnicas).
- Para GitHub, sempre:
  - Usar `--repo "$GITHUB_REPOSITORY"` (não hardcode owner/repo)
  - Passar labels separadamente (ex: `--label task --label P0`)
  - Incluir referências a arquivos no body da issue.
  - Vincular issue à US e IDEA.