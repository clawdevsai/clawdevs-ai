# BOOTSTRAP.md - Architect

Preparation for continuous operation:
1. Load settings:
   - `GITHUB_ORG` (`owner` format)
   - `ACTIVE_GITHUB_REPOSITORY` (`owner/repo` format)
   - `GITHUB_TOKEN` (if available)
   - `OPENCLAW_ENV` (`production` or `staging`)
   - `MAX_RESEARCH_TIME_PER_US` (default 2h)
2. Read `README.md` the repository to understand the project, stack and flow before decomposing tasks.
3. Validate `/data/openclaw/backlog` and subfolders:
   - `idea/`, `user_story/`, `tasks/`, `architecture/`, `briefs/`
   - `implementation/docs/`
   - `session_finished/`
4. Initialize operational directories:
   - `/data/openclaw/backlog/status`
   - `/data/openclaw/backlog/audit`
   - `/data/openclaw/backlog/implementation/docs`
   - `/data/openclaw/backlog/session_finished`
5. Establish logger with security and audit events.
6. Upload whitelists:
   - labels GitHub allowed
   - trusted research domains
   - agents allowed for session (`po`, `dev_backend`, `dev_frontend`, `dev_mobile`, `qa_engineer`, `devops_sre`, `security_engineer`, `ux_designer`, `dba_data_engineer`)
7. Validate required tools (`read`, `write`, `exec`, `sessions_spawn`, `sessions_send`) and commands `gh`, `web-search` and `web-read` via `exec`.
8. If any requirement is missing, abort with a clear error for the PO.
9. Ready.