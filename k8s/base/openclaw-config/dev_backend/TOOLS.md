# TOOLS.md - Dev_Backend

## tools_disponiveis
- `read(path)`: read task/project files (with path validation).
- `write(path, content)`: write code/tests/docs (with validation).
- `exec(command)`: run build/test/lint commands.
- `exec("gh <args>")`: update issues/PRs and consult workflow executions, checks, labels and run logs (gh run view/rerun/list).
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=back_end&page_size=20'")`: Task queue poll in the control panel.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Update task status.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Create new task (sub-tasks, bugs found, etc.).
- `git(args...)`: commit/branch/merge operations without destructive commands.
- `sessions_spawn(agentId, mode, label)`: create session with Architect.
- `sessions_send(session_id, message)`: send update.
- `sessions_list()`: list sessions.
- `exec("web-search '<query>'")`: search the internet via SearxNG (aggregates Google, Bing, DuckDuckGo). Returns up to 10 results. Example: `web-search "python asyncio best practices 2025"`
- `exec("web-read '<url>'")`: read any web page as clean markdown via Jina Reader. Example: `web-read "https://docs.python.org/3/library/asyncio.html"`

## usage_rules
- `read/write` only on `/data/openclaw/**`.
- Block destructive commands (`rm -rf`, `git push -f`, etc.).
- GitHub commands must use `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- Validate `/data/openclaw/contexts/active_repository.env` before any gh/git action.
- Interactive communication with key `agent:<id>:main` must use `sessions_send` (never `message`).
- `message` is only for channel destinations (e.g. Telegram `chatId`), never for agent session.
- Before reading stack files (`package.json`, `go.mod`, etc.), validate existence with `read` in the target directory.
- If `PROJECT_ROOT` has no source code, use `/data/openclaw/backlog/implementation` as fallback and register `standby` without error.
- `gh` with operational parity to the Architect for reading/updating CI, issues and PRs (without destructive operations).
- Control panel queue poll 1x per hour:
  - example: `curl -s -H "Authorization: Bearer $PANEL_TOKEN" "$PANEL_API_URL/tasks?status=inbox&label=back_end&page_size=20"`
- When picking up a task: `PATCH /tasks/<id>` with `{"status":"in_progress"}` immediately.
- At the end: `PATCH /tasks/<id>` with `{"status":"done"}`.
- Process `back_end` label only. TASK_GITHUB_REPO = field `github_repo` of the task.
- Always run tests before reporting completion.
- Always report the cost/performance impact of the implemented solution.
- If task brings `## Comandos`, use these commands instead of defaults.
- Internet: full access allowed for technical research, discovery of alternatives, CVEs, benchmarks and skills updating — without source restrictions.

## github_permissions
- **Type:** `read+write`
- **Own label:** `back_end` — automatically created at boot if it doesn't exist:
  `gh label create "back_end" --color "#1d76db" --description "Backend tasks — routed to Dev_Backend" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Allowed operations:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (`--repo "$TASK_GITHUB_REPO"` only)
- **Prohibited:** `gh issue create`, `gh issue edit`, `gh issue close` — use control panel API
- **Active repo:** use `$TASK_GITHUB_REPO` (task field `github_repo`) instead of `$ACTIVE_GITHUB_REPOSITORY`## autonomy_of_research_and_learning
- Full internet access permission for research, updating skills and discovering better alternatives.
- Use `exec("web-search '...'")` and `exec("web-read '...'")` freely to:
  - discover more efficient frameworks, libraries and tools for the problem
  - check updated CVEs, vulnerabilities and security advisories in dependencies
  - compare performance and cost benchmarks between technological alternatives
  - read official documentation, changelogs and release notes of the technologies used
  - learn emerging standards that reduce cost or increase performance
- Cite source and date of information in the artifacts produced.

## rate_limits
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
- **Prohibited:** using `message` with `agent:<id>:main` (this breaks on channels like Telegram with `Unknown target`)

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