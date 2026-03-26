# BOOT.md - QA_Engineer

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md`.
3. Read `README.md` the repository to understand the application and test stack.
4. Load `SOUL.md`.
5. Load `INPUT_SCHEMA.json`.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/qa_engineer/MEMORY.md` — recover your own relevant quality learning.
8. Validate `/data/openclaw/` and testing workspace.
9. Detect application type (web/mobile/api) by project or task.
10. Check testing toolchain in PATH:
    - Web: `npx playwright`, `npx cypress`
    - Mobile: `npx detox`, `maestro`
    - Load: `k6`, `locust`
    - Contract: `pact`
11. Check presence of SPEC for delegated tasks (`/data/openclaw/backlog/specs/`).
12. When completing the session: register up to 3 learnings in `/data/openclaw/memory/qa_engineer/MEMORY.md`.
13. Ready to receive delegation from the Architect or dev agents.

##healthcheck
- `/data/openclaw/` accessible? ✅
- INPUT_SCHEMA.json loaded? ✅
- Application type detected? ✅
- SHARED_MEMORY.md and MEMORY.md (qa_engineer) read? ✅
- `ACTIVE_GITHUB_REPOSITORY` set? ✅