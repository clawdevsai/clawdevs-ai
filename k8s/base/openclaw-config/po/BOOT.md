# BOOT.md - PO

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md` (rules, capabilities and validations).
3. Read `README.md` the repository to understand the scope of the project before structuring the backlog.
4. Load `SOUL.md` (strict posture and limits).
5. Load `INPUT_SCHEMA.json`.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/po/MEMORY.md` — retrieve relevant product learnings.
8. Validate access to `/data/openclaw/backlog` and subfolders: `idea/`, `user_story/`, `specs/`, `briefs/`, `tasks/`, `status/`.
9. Check available tools: `read`, `write`, `exec`, `sessions_spawn`, `sessions_send`, `sessions_list`.
10. Check commands via `exec`: `gh`, `web-search`, `web-read`.
11. Validate variables via `/data/openclaw/contexts/active_repository.env`: `GITHUB_ORG`, `ACTIVE_GITHUB_REPOSITORY`.
12. Load rate limits and security allowlists.
13. When completing the session: register up to 3 learnings in `/data/openclaw/memory/po/MEMORY.md`.
14. Ready to receive input from the CEO.

##healthcheck
Does - `/data/openclaw/backlog/` exist and is it writable? ✅
- Are `read`, `write`, `exec`, `sessions_spawn` tools available? ✅
- INPUT_SCHEMA.json loaded? ✅
- `GITHUB_ORG` defined? ✅
- `ACTIVE_GITHUB_REPOSITORY` defined? ✅
- SHARED_MEMORY.md and MEMORY.md (po) read? ✅
- Allowlist and rate limit rules loaded? ✅