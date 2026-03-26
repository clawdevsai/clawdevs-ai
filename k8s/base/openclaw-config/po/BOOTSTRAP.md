# BOOTSTRAP.md - PO

Preparation for continuous operation:
1. Load environment settings:
   - `DIRECTORS_NAME`
   - `GITHUB_ORG` (`owner` format)
   - `ACTIVE_GITHUB_REPOSITORY` (`owner/repo` format)
   - `OPENCLAW_ENV` (`production` or `staging`)
2. Read `README.md` the repository to understand the project and flow before structuring the backlog.
3. Validate base directory `/data/openclaw/backlog` and required subfolders:
   - `idea/`, `specs/`, `user_story/`, `tasks/`, `briefs/`
4. Initialize operational directories:
   - `/data/openclaw/backlog/status`
   - `/data/openclaw/backlog/audit`
5. Establish logger:
   - audit trail in JSONL
   - minimum level INFO, security events in WARN/ERROR
6. Upload security whitelists:
   - GitHub allowed labels
   - domains allowed for search
7. Check required tools (`read`, `write`, `sessions_spawn`, `sessions_send`, `gh`).
8. If any check fails, abort with clear error to the CEO.
9. Ready.

Operating Notes:
- `gh` can be used to consult issues, PRs, labels and workflows.
- Creation of PRs and commits remains delegated to the Architect.