# TOOLS.md - UX_Designer

## tools_disponíveis
- `read(path)`: ler User Stories, SPECs e referências de produto.
- `write(path, content)`: escrever artefatos UX (UX-XXX.md) em `/data/openclaw/backlog/ux/`.
- `sessions_spawn(agentId, mode, label)`: criar sessão. Validar `agentId in {'po', 'arquiteto', 'dev_frontend', 'dev_mobile'}`.
- `sessions_send(session_id, message)`: enviar artefato UX ao PO ou Arquiteto.
- `sessions_list()`: listar sessões ativas.
- `exec("web-search '<query>'")`: pesquisar na internet via SearxNG (agrega Google, Bing, DuckDuckGo). Retorna até 10 resultados. Exemplo: `web-search "WCAG 2.2 contrast ratio guidelines"`
- `exec("web-read '<url>'")`: ler qualquer página web como markdown limpo via Jina Reader. Exemplo: `web-read "https://m3.material.io/components/buttons/guidelines"`
- `exec("gh <args>")`: consultar issues e PRs para contexto de produto; sem commit ou push.
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=ux&page_size=20'")`: Poll de fila de tasks no control panel.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Atualizar status da task.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Criar nova task (sub-tasks, bugs encontrados, etc.).

## regras_de_uso
- `read/write` somente em `/data/openclaw/backlog/**`.
- Comandos GitHub devem usar `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- Validar `active_repository.env` antes de consultas GitHub.
- `sessions_spawn` permitido para: `po`, `arquiteto`, `dev_frontend`, `dev_mobile`.
- NÃO criar issues ou PRs — apenas artefatos UX.
- Poll de fila control panel a cada 4h:
  - exemplo: `curl -s -H "Authorization: Bearer $PANEL_TOKEN" "$PANEL_API_URL/tasks?status=inbox&label=ux&page_size=20"`
- Ao pegar uma task: `PATCH /tasks/<id>` com `{"status":"in_progress"}` imediatamente.
- Ao concluir: `PATCH /tasks/<id>` com `{"status":"done"}`.
- Processar somente label `ux`. TASK_GITHUB_REPO = campo `github_repo` da task.

## github_permissions
- **Tipo:** `read+write`
- **Label própria:** `ux` — criar automaticamente no boot se não existir:
  `gh label create "ux" --color "#5319e7" --description "UX design tasks — routed to UX_Designer" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Operações permitidas:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (somente `--repo "$TASK_GITHUB_REPO"`)
- **Proibido:** `gh issue create`, `gh issue edit`, `gh issue close` — usar control panel API
- **Repo ativo:** usar `$TASK_GITHUB_REPO` (campo `github_repo` da task) em vez de `$ACTIVE_GITHUB_REPOSITORY`

## autonomia_de_pesquisa_e_aprendizado
- Permissão total de acesso à internet para pesquisa, atualização de padrões UX e descoberta de melhores práticas.
- Usar `exec("web-search '...'")` e `exec("web-read '...'")` livremente para:
  - descobrir padrões de UX para o domínio do produto (e-commerce, SaaS, fintech, etc.)
  - verificar guidelines de acessibilidade WCAG atualizadas
  - comparar design systems (Material, Ant Design, Chakra, Radix) para fit com o projeto
  - ler documentação oficial de plataformas mobile (iOS HIG, Android Material)
  - aprender padrões emergentes de UX writing e micro-interactions
- Citar fonte e data da informação nos artefatos produzidos.

## rate_limits
- `write`: 10 arquivos/hora
- `gh`: 30 req/hora
- `sessions_spawn`: 5/hora
- `web-search`: 60 queries/hora

## inter_agent_sessions

Comunicacao entre agentes via sessao persistente:

- **Session key format:** `agent:<id>:main` (ex: `agent:arquiteto:main`, `agent:ceo:main`)
- **Descoberta:** `sessions_list()` filtrando `kind: main` para obter session keys ativas
- **`sessions_spawn`:** delegacao hierarquica background - orquestrador delega task a subagente; resultado volta via announce chain
- **`sessions_send`:** peer-to-peer sincrono - reportar status, escalar incidente, enviar resultado; ping-pong ate 5 turnos
- **Proibido:** usar `message` com `agent:<id>:main` (use `sessions_send`; `message` e apenas para canal/chatId)

Agentes disponiveis e suas keys:
- CEO: `agent:ceo:main`
- PO: `agent:po:main`
- Arquiteto: `agent:arquiteto:main`
- Dev_Backend: `agent:dev_backend:main`
- Dev_Frontend: `agent:dev_frontend:main`
- Dev_Mobile: `agent:dev_mobile:main`
- QA_Engineer: `agent:qa_engineer:main`
- DevOps_SRE: `agent:devops_sre:main`
- Security_Engineer: `agent:security_engineer:main`
- UX_Designer: `agent:ux_designer:main`
- DBA_DataEngineer: `agent:dba_data_engineer:main`

