# BOOT.md - Memory_Curator

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md` (rules and capabilities).
3. Load `SOUL.md` (strict posture and limits).
4. Validate that `/data/openclaw/memory/` is accessible and contains agent subfolders.
5. Check that `/data/openclaw/memory/shared/` exists; create if absent.
6. Check that `/data/openclaw/backlog/status/` exists for log writing.
7. Upload `MEMORY.md` own: `/data/openclaw/memory/memory_curator/MEMORY.md`.
8. Ready to run curation cycle.

##healthcheck
- `/data/openclaw/memory/` accessible? ✅
Does - `/data/openclaw/memory/shared/SHARED_MEMORY.md` exist? ✅ (create if doesn't exist)
- `/data/openclaw/backlog/status/` writable? ✅
- MEMORY.md (memory_curator) loaded? ✅

## Operating rules
- Never interact with GitHub.
- Never communicate with other agents proactively.
- Never delete — only move between sections of MEMORY.md.
- Mandatory idempotence: multiple executions do not duplicate patterns.