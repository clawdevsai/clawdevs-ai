# BOOT.md - Architect

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md` (rules, capabilities and validations).
3. Read `README.md` the repository to understand structure, stack and contracts before planning.
4. Load `SOUL.md` (strict posture and limits).
5. Load `INPUT_SCHEMA.json`.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/arquiteto/MEMORY.md` — recover your own relevant architectural learnings.
8. Validate access to `/data/openclaw/backlog` and subfolders: `idea/`, `user_story/`, `tasks/`, `architecture/`, `briefs/`, `implementation/docs/`, `session_finished/`, `specs/`, `ux/`.
9. Check available tools: `read`, `write`, `exec`, `sessions_spawn`, `sessions_send`, `sessions_list`.
10. Check commands via `exec`: `gh`, `web-search`, `web-read`.
11. Validate variables via `/data/openclaw/contexts/active_repository.env`: `GITHUB_ORG`, `ACTIVE_GITHUB_REPOSITORY`.
12. Initialize operational directories if missing: `/data/openclaw/backlog/status/`, `/data/openclaw/backlog/audit/`, `/data/openclaw/backlog/session_finished/`.
13. Load allowlists and security limits (allowed labels, rate limits, path whitelist).
14. When completing the session: register up to 3 learnings in `/data/openclaw/memory/arquiteto/MEMORY.md`.
15. Ready to receive input from PO.

##healthcheck
Does - `/data/openclaw/backlog/` exist and is it writable? ✅
- `implementation/docs/` and `session_finished/` available? ✅
- Tools `read`, `write`, `exec`, `sessions_spawn` available? ✅
- INPUT_SCHEMA.json loaded? ✅
- `GITHUB_ORG` defined? ✅
- `ACTIVE_GITHUB_REPOSITORY` defined? ✅
- SHARED_MEMORY.md and MEMORY.md (architect) read? ✅
- Allowlists and rate limits loaded? ✅

## GitHub label preparation (single boot)
```bash
gh label create "task"      --color "#0075ca" --description "Technical tasks — owned by Arquiteto"    --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "ADR"       --color "#e4e669" --description "Architecture Decision Record"             --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "security"  --color "#d93f0b" --description "Security tasks — routed to Security_Eng" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "back_end"  --color "#1d76db" --description "Backend tasks — routed to Dev_Backend"   --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "front_end" --color "#0e8a16" --description "Frontend tasks — routed to Dev_Frontend" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "mobile"    --color "#5319e7" --description "Mobile tasks — routed to Dev_Mobile"     --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "tests"     --color "#f9d0c4" --description "QA tasks — routed to QA_Engineer"        --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "devops"    --color "#006b75" --description "DevOps tasks — routed to DevOps_SRE"     --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "dba"       --color "#b60205" --description "DBA tasks — routed to DBA_DataEngineer"  --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
gh label create "ux"        --color "#e99695" --description "UX tasks — routed to UX_Designer"        --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true
```