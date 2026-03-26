# TOOLS.md - Dev_Frontend

## tools_disponíveis
- `read(path)`: ler arquivos da task/projeto e artefatos UX (com validação de path).
- `write(path, content)`: escrever componentes/testes/docs (com validação).
- `exec(command)`: executar comandos de build/test/lint/a11y.
- `exec("gh <args>")`: atualizar issues/PRs e consultar execuções de workflow, checks, labels e run logs.
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=front_end&page_size=20'")`: Poll de fila de tasks no control panel.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Atualizar status da task.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Criar nova task (sub-tasks, bugs encontrados, etc.).
- `git(args...)`: operações de commit/branch/merge sem comandos destrutivos.
- `sessions_spawn(agentId, mode, label)`: criar sessão com Arquiteto ou QA_Engineer.
- `sessions_send(session_id, message)`: enviar update ou delegar ao QA_Engineer.
- `sessions_list()`: listar sessões ativas.
- `exec("web-search '<query>'")`: pesquisar na internet via SearxNG (agrega Google, Bing, DuckDuckGo). Retorna até 10 resultados. Exemplo: `web-search "next.js 15 performance optimization"`
- `exec("web-read '<url>'")`: ler qualquer página web como markdown limpo via Jina Reader. Exemplo: `web-read "https://nextjs.org/docs/app/building-your-application/optimizing"`

## regras_de_uso
- `read/write` somente em `/data/openclaw/**`.
- Bloquear comandos destrutivos (`rm -rf`, `git push -f`, etc.).
- Comandos GitHub devem usar `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- Validar `/data/openclaw/contexts/active_repository.env` antes de qualquer ação gh/git.
- Poll de fila control panel 1x por hora:
  - exemplo: `curl -s -H "Authorization: Bearer $PANEL_TOKEN" "$PANEL_API_URL/tasks?status=inbox&label=front_end&page_size=20"`
- Ao pegar uma task: `PATCH /tasks/<id>` com `{"status":"in_progress"}` imediatamente.
- Ao concluir: `PATCH /tasks/<id>` com `{"status":"done"}`.
- Processar somente label `front_end`. TASK_GITHUB_REPO = campo `github_repo` da task.
- Sempre executar testes antes de reportar conclusão.
- Sempre documentar Core Web Vitals e bundle size no comentário do PR.
- Se task trouxer `## Comandos`, usar esses comandos em vez dos defaults.
- Internet: acesso total liberado para pesquisa técnica, descoberta de frameworks, CVEs, benchmarks de performance e atualização de habilidades — sem restrição de fonte.
- `sessions_spawn` permitido para: `arquiteto`, `qa_engineer`.

## github_permissions
- **Tipo:** `read+write`
- **Label própria:** `front_end` — criar automaticamente no boot se não existir:
  `gh label create "front_end" --color "#0e8a16" --description "Frontend tasks — routed to Dev_Frontend" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Operações permitidas:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (somente `--repo "$TASK_GITHUB_REPO"`)
- **Proibido:** `gh issue create`, `gh issue edit`, `gh issue close` — usar control panel API
- **Repo ativo:** usar `$TASK_GITHUB_REPO` (campo `github_repo` da task) em vez de `$ACTIVE_GITHUB_REPOSITORY`

## comandos_adicionais_frontend
- `npx next build`: build Next.js com análise de bundle
- `npx playwright test`: testes e2e Playwright
- `npx cypress run`: testes e2e Cypress
- `npx storybook build`: build do Storybook para review
- `npx axe <url>`: scan de acessibilidade

## autonomia_de_pesquisa_e_aprendizado
- Permissão total de acesso à internet para pesquisa, atualização de habilidades e descoberta de melhores alternativas.
- Usar `exec("web-search '...'")` e `exec("web-read '...'")` livremente para:
  - descobrir frameworks, bibliotecas e ferramentas mais eficientes para o problema
  - verificar CVEs, vulnerabilidades e security advisories em dependências frontend
  - comparar benchmarks de bundle size, performance e Core Web Vitals entre alternativas
  - ler documentação oficial, changelogs e release notes das tecnologias usadas
  - aprender padrões emergentes de acessibilidade, performance e segurança web
- Citar fonte e data da informação nos artefatos produzidos.

## rate_limits
- `exec`: 120 comandos/hora
- `gh`: 50 req/hora
- `sessions_spawn`: 10/hora
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

