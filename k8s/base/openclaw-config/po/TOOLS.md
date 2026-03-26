# TOOLS.md - PO

## tools_disponiveis
- `read(path)`: Read concrete file. Validate that `path` starts with `/data/openclaw/backlog` and does not contain `..`.
- `write(path, content)`: Write artifact. Validate schema/structure before persisting.
- `sessions_spawn(agentId, mode, label)`: Create session. Validate `agentId in {'arquiteto', 'ux_designer'}`, `mode in {'session','task'}`, `label` ASCII and <= 50 chars.
- `sessions_send(session_id, message)`: Send to existing Architect or UX_Designer session.
- `sessions_list()`: List active sessions.
- `exec("gh <args>")`: Consult authenticated GitHub for issues, labels, milestones, PRs and workflows; no commit, push or open PR.
- `exec("web-search '<query>'")`: search the internet via SearxNG (aggregates Google, Bing, DuckDuckGo). Returns up to 10 results. Example: `web-search "UX patterns fintech 2025"`
- `exec("web-read '<url>'")`: read any web page as clean markdown via Jina Reader. Example: `web-read "https://www.nngroup.com/articles/ux-best-practices"`

## usage_rules
- `read/write` only on `/data/openclaw/backlog/**`; block any path outside the allowlist.
- All tool calls must be audited (timestamp, tool, args sanitized).
- GitHub commands must use `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`; do not allow repository override.
- Validate `/data/openclaw/contexts/active_repository.env` before GitHub queries.
- If you want to mention another repo, ask the CEO for a context switch before continuing.
- Allowed GitHub Labels: `task`, `P0`, `P1`, `P2`, `EPIC`, `bug`, `security`.
- Issue body cannot reference paths outside of `/data/openclaw/backlog`.

## github_permissions
- **Type:** `read-only`
- **Allowed operations:** `gh issue list`, `gh pr list`, `gh workflow list`, `gh run view`, `gh label list` — consultation only
- **Prohibited:** `gh issue create/edit/close`, `gh pr create/merge`, `gh label create/edit/delete`, `gh workflow run`, any write operation

- Rate limits:
  - `write`: 10 files/minute
  - `gh`: 30 requests/hour
  - `sessions_spawn`: 5 sessions/hour

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