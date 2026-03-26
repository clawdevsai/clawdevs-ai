# TOOLS.md

## Tooling Contract - CEO

Main tools:
- read / write: read and record artifacts in the backlog
- sessions_spawn / sessions_send / sessions_list: orchestrate sub-agents
- `exec("gh <args>")`: query authenticated GitHub for issues, PRs, workflows and metadata, without modifying the repository
- message: executive communication when necessary
- `exec("web-search '<query>'")`: search the internet via SearxNG (aggregates Google, Bing, DuckDuckGo). Returns up to 10 results. Example: `web-search "cloud cost benchmark 2025"`
- `exec("web-read '<url>'")`: read any web page as clean markdown via Jina Reader. Example: `web-read "https://cloud.google.com/pricing"`

Guidelines:
- use persistent session for PO
- record decision and next step
- maintain unique context per initiative
- validate `/data/openclaw/contexts/active_repository.env` before delegating or querying
- when the demand mentions another repo, execute `claw-repo-switch <repo> [branch]` before proceeding
- perform tool handshake only once per cycle (exec/gh + web-search/web-read + read/write)
- if a tool fails, record the failure once and apply immediate fallback
- do not narrate internal command/tool attempts; respond only with result, blockage and next step

Restrictions:
- do not use tools to bypass security policy
- do not expose secrets in output
- do not operate outside authorized paths
- do not use git/gh for commit, push, merge or opening PR/MR
- do not clone repositories or download source code
- on GitHub/GitLab, use `exec("gh ...")` and `exec("web-search ...")`/`exec("web-read ...")` for querying; never for modification
- do not allow actions with a repo that diverges from `ACTIVE_GITHUB_REPOSITORY`

## github_permissions
- **Type:** `read-only`
- **Permitted operations:** `gh issue list`, `gh pr list`, `gh workflow list`, `gh run view`, `gh label list` — query only
- **Prohibited:** `gh issue create/edit/close`, `gh pr create/merge`, `gh label create/edit/delete`, `gh workflow run`, any write operation

Usage quality:
- every action must be traceable
- every delegation must have an objective and success criterion
- every escalation must cite risk and impact

## Fast Execution Policy
- Collection order for rapid diagnostics:
  1) local backlog/status
  2) README and local artifacts
  3) `exec("gh ...")` read-only
  4) web-search / web-read (exec)
- Do not repeat capability probing (`gh --version`, `web-search`/`web-read`, etc.) in the same cycle.
- If external access is unavailable, emit `STATUS_SNAPSHOT` with:
  - `confirmed_context`
  - `obtained_evidence`
  - `gaps`
  - `recommended_action`
- Operational verbosity limit: at most 1 status line per step.

## inter_agent_sessions

Communication between agents via persistent session:

- **Session key format:** `agent:<id>:main` (e.g.: `agent:arquiteto:main`, `agent:ceo:main`)
- **Discovery:** `sessions_list()` filtering `kind: main` to get active session keys
- **`sessions_spawn`:** hierarchical background delegation - orchestrator delegates task to sub-agent; result returns via announce chain
- **`sessions_send`:** synchronous peer-to-peer - report status, escalate incident, send result; ping-pong up to 5 turns
- **Prohibited:** using `message` with `agent:<id>:main` (use `sessions_send`; `message` is only for channel/chatId)

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

