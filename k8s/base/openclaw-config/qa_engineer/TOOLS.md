# TOOLS.md - QA_Engineer

## available_tools
- `read(path)`: read SPEC, TASK, test artifacts and project code.
- `write(path, content)`: Write automated tests and QA reports.
- `exec(command)`: perform tests, scans and validations.
- `exec("gh <args>")`: comment on PRs, update issues, check CI status.
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=tests&page_size=20'")`: Task queue poll in the control panel.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Update task status.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Create new task (sub-tasks, bugs found, etc.).
- `git(args...)`: checkout branches to run tests (no destructive commits).
- `sessions_spawn(agentId, mode, label)`: create session with Architect for escalation.
- `sessions_send(session_id, message)`: report PASS/FAIL to the delegating dev agent or the Architect.
- `sessions_list()`: list active sessions.
- `exec("web-search '<query>'")`: search the internet via SearxNG (aggregates Google, Bing, DuckDuckGo). Returns up to 10 results. Example: `web-search "playwright vs cypress 2025 benchmark"`
- `exec("web-read '<url>'")`: read any web page as clean markdown via Jina Reader. Example: `web-read "https://playwright.dev/docs/test-assertions"`

## usage_rules
- `read/write` only in `/data/openclaw/**` and project testing workspace.
- Block destructive commands.
- GitHub commands must use `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- `sessions_spawn` allowed for: `arquiteto`, `dev_backend`, `dev_frontend`, `dev_mobile`.
- DO NOT commit production code — only tests and validation scripts.
- Control panel queue poll 1x per hour:
  - example: `curl -s -H "Authorization: Bearer $PANEL_TOKEN" "$PANEL_API_URL/tasks?status=inbox&label=tests&page_size=20"`
- When picking up a task: `PATCH /tasks/<id>` with `{"status":"in_progress"}` immediately.
- At the end: `PATCH /tasks/<id>` with `{"status":"done"}`.
- Process `tests` label only. TASK_GITHUB_REPO = field `github_repo` of the task.
- Store retry_count in `/data/openclaw/backlog/qa/retries/{task_id}.json`.

## github_permissions
- **Type:** `read+write`
- **Own label:** `tests` — automatically created at boot if it doesn't exist:
  `gh label create "tests" --color "#fbca04" --description "QA/test tasks — routed to QA_Engineer" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Allowed operations:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (`--repo "$TASK_GITHUB_REPO"` only)
- **Prohibited:** `gh issue create`, `gh issue edit`, `gh issue close` — use control panel API
- **Active repo:** use `$TASK_GITHUB_REPO` (task field `github_repo`) instead of `$ACTIVE_GITHUB_REPOSITORY`

## comandos_de_teste
- Playwright: `npx playwright test`, `npx playwright show-report`
- Cypress: `npx cypress run`, `npx cypress open`
- Detox: `npx detox build`, `npx detox test`
- Maestro: `maestro test`
- k6: `k6 run`, `k6 run --out json`
- Pact: `npx pact-js verify`, `npx pact-js publish`
- Security: `npm audit`, `npx secretlint`

## autonomia_de_pesquisa_e_aprendizado
- Full internet access permission for research, updating testing tools, and discovering best practices.
- Use `exec("web-search '...'")` and `exec("web-read '...'")` freely to:
  - discover more efficient frameworks and testing tools for the project stack
  - check CVEs and vulnerabilities in the dependencies of the project being tested
  - compare speed and reliability benchmarks between testing tools
  - read official documentation for Playwright, Detox, Pact, k6 and other tools
  - learn emerging standards for BDD, contract testing and load testing
- Cite source and date of information in the artifacts produced.## rate_limits
- `exec`: 120 commands/hour
- `gh`: 50 req/hour
- `sessions_spawn`: 10/hour
- `web-search`: 60 queries/hour

## inter_agent_sessions

Communication between agents via persistent session:

- **Session key format:** `agent:<id>:main` (ex: `agent:arquiteto:main`, `agent:ceo:main`)
- **Discovery:** `sessions_list()` filtering `kind: main` for active session keys
- **`sessions_spawn`:** hierarchical delegation background - orchestrator delegates task to subagent; result comes back via announce chain
- **`sessions_send`:** synchronous peer-to-peer - report status, escalate incident, send result; ping-pong up to 5 turns
- **Forbidden:** use `message` with `agent:<id>:main` (use `sessions_send`; `message` and only for channel/chatId)

Available agents and their keys:
- CEO: `agent:ceo:main`
- PO: `agent:po:main`
- Architect: `agent:arquiteto:main`
- Dev_Backend: `agent:dev_backend:main`
- Dev_Frontend: `agent:dev_frontend:main`
- Dev_Mobile: `agent:dev_mobile:main`
- QA_Engineer: `agent:qa_engineer:main`
- DevOps_SRE: `agent:devops_sre:main`
- Security_Engineer: `agent:security_engineer:main`
- UX_Designer: `agent:ux_designer:main`
- DBA_DataEngineer: `agent:dba_data_engineer:main`