# BOOT.md - DBA_DataEngineer

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md`.
3. Read `README.md` the repository to understand the application, stack and data model before modeling.
4. Load `SOUL.md`.
5. Load `INPUT_SCHEMA.json` and validate input schema.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/dba_data_engineer/MEMORY.md` — retrieve your own learning from relevant databases.
8. Validate `/data/openclaw/` and database workspace.
9. Check `active_repository.env` at `/data/openclaw/contexts/`.
10. Create working directory: `/data/openclaw/backlog/database/`.
11. Check PATH: `psql`, `flyway`, `alembic`, `prisma` available (warn if missing, do not fail).
12. When completing the session: register up to 3 learnings in `/data/openclaw/memory/dba_data_engineer/MEMORY.md`.
13. Ready to receive tasks from the Architect or Dev_Backend.

##healthcheck
- `/data/openclaw/` accessible? ✅
- INPUT_SCHEMA.json loaded? ✅
- `active_repository.env` available? ✅
- `database/` Directory created? ✅
- SHARED_MEMORY.md and MEMORY.md (dba_data_engineer) read? ✅