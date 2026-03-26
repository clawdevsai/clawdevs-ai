# TOOLS.md - Architect

## tools_disponiveis
- `read(path)`: Read concrete file. Validate prefix `/data/openclaw/backlog` and block `..`.
- `write(path, content)`: Write artifact after structure/schema validation.
- `exec(cmd)`: Execute controlled operational commands (`git`, `gh`, `mkdir`, `mv`) for publishing pipeline.
- `sessions_spawn(agentId, mode, label)`: Create session. Validate `agentId in {'po', 'dev_backend', 'dev_frontend', 'dev_mobile', 'qa_engineer', 'devops_sre', 'security_engineer', 'dba_data_engineer'}`, `mode='session'`, `label` ASCII <= 50 chars.
- `sessions_send(session_id, message)`: Send message to valid session (PO or execution agents).
- `sessions_list()`: List active sessions.
- `exec("web-search '<query>'")`: search the internet via SearxNG (aggregates Google, Bing, DuckDuckGo). Returns up to 10 results. Example: `web-search "postgres vs cockroachdb benchmark 2025"`
- `exec("web-read '<url>'")`: read any web page as clean markdown via Jina Reader. Example: `web-read "https://www.postgresql.org/docs/current/"`
- `exec("gh <args>")`: GitHub operations with guardrails.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Create task in the control panel.
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=<label>'")`: List panel tasks.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Update status/task fields.

## usage_rules
- `read/write` only on `/data/openclaw/backlog/**`.
- Record all calls (timestamp, tool, sanitized args).
- GitHub commands must use `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`; no repository override.
- Before any `gh`, validate `/data/openclaw/contexts/active_repository.env`.
- Repository creation permitted only with explicit authorization from the CEO: `gh repo create "$GITHUB_ORG/<repo>" ...`.
- Allowed labels: `task`, `P0`, `P1`, `P2`, `ADR`, `security`, `performance`, `spike`, `back_end`, `front_end`, `mobile`, `tests`, `devops`, `dba`, `documentacao`, `ux`.
- Label routing for agent: `back_end`→Dev_Backend, `front_end`→Dev_Frontend, `mobile`→Dev_Mobile, `tests`→QA_Engineer, `devops`→DevOps_SRE, `security`→Security_Engineer, `dba`→DBA_DataEngineer.
- Body of issue cannot contain paths outside of `/data/openclaw/backlog`.
- When creating/editing an issue, use `--body-file <file.md>`; do not use `--body` inline with `\n`.
- Body must contain mandatory sections: `Objective`, `What to build`, `How to build`, `Acceptance criteria`, `Definition of done (DoD)`.
- Mandatory publication order: `docs -> commit -> panel_task -> validação -> session_finished`.
- Create tasks in the control panel via `$PANEL_API_URL/tasks` (POST) — never `gh issue create`.
- Mandatory fields when creating task: `title`, `label` (track), `github_repo` (active repo).
- After creating task: register `task_id` returned for later updates.
- Use `$PANEL_API_URL` and `$PANEL_TOKEN` from env vars — never hardcode URL or token.
- Session docs should be published on `/data/openclaw/backlog/implementation/docs`.
- Session termination should move artifacts to `/data/openclaw/backlog/session_finished/<session_id>/`.
- If commit or issue fails: notify PO immediately; do not log out.## github_permissions
- **Type:** `read+write`
- **Own label:** `task` — automatically created at boot if it does not exist:
`gh label create "task" --color "#0075ca" --description "Technical tasks — owned by Architect" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Allowed operations:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (`--repo "$ACTIVE_GITHUB_REPOSITORY"` only)
- **Prohibited:** `gh issue create`, `gh issue edit`, `gh issue close` — use control panel API
- **Prohibited:** repository override, operations outside `ACTIVE_GITHUB_REPOSITORY`

- Rate limits:
  - `write`: 20 files/hour
  - `gh`: 50 requests/hour
  - `sessions_spawn`: 10 sessions/hour
  - `web-search`: 30 queries/hour
- `research` must start timer and end in 2h with fallback.
- Internet: full access allowed for technical research, stack comparison, CVEs, benchmarks and skills updating — without source restrictions.

## inter_agent_sessions

Communication between agents via persistent session:

- **Session key format:** `agent:<id>:main` (ex: `agent:arquiteto:main`, `agent:ceo:main`)
- **Discovery:** `sessions_list()` filtering `kind: main` for active session keys
- **`sessions_spawn`:** hierarchical delegation background - orchestrator delegates task to subagent; result comes back via announce chain
- **`sessions_send`:** synchronous peer-to-peer - report status, escalate incident, send result; ping-pong up to 5 turns
- **Prohibited:** use `message` with `agent:<id>:main` (use `sessions_send`; `message` and only for channel/chatId)

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

## Create task in control panel (replaced gh issue create)

```bash
# Ler conteúdo da task e escapar para JSON
TASK_BODY=$(cat /data/openclaw/backlog/implementation/TASK-XXX.md | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

# Create task no control panel
TASK_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $PANEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"TASK-XXX: <slug>\",\"label\":\"back_end\",\"github_repo\":\"$ACTIVE_GITHUB_REPOSITORY\",\"description\":$TASK_BODY}" \
  "$PANEL_API_URL/tasks")

TASK_ID=$(echo "$TASK_RESPONSE" | jq -r '.id')
echo "Task criada: $TASK_ID"
```