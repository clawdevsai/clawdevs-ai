# BOOT.md - Security_Engineer

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md`.
3. Read `README.md` the repository to understand the application, stack and dependencies.
4. Load `SOUL.md`.
5. Load `INPUT_SCHEMA.json` and validate input schema.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/security_engineer/MEMORY.md` — retrieve your own relevant safety lessons.
8. Validate `/data/openclaw/` and security workspace.
9. Detect dependency manifests present in the repository:
   - `package.json` / `package-lock.json` → Node.js/npm
   - `requirements.txt` / `Pipfile.lock` / `pyproject.toml` → Python
   - `go.mod` / `go.sum` → Go
   - `Cargo.toml` / `Cargo.lock` → Rust
   - `pom.xml` / `build.gradle` → Java/Kotlin
10. Check security tools in PATH: `semgrep`, `trivy`, `gitleaks`, `npm`, `pip-audit`, `osv-scanner`.
11. Validate `gh` authentication and permissions on the active repository via `active_repository.env`.
12. When completing the session: register up to 3 learnings in `/data/openclaw/memory/security_engineer/MEMORY.md`.
13. Ready to receive tasks from the Architect, CEO (P0) or dev agents.

##healthcheck
- `/data/openclaw/` accessible? ✅
- INPUT_SCHEMA.json loaded? ✅
- Dependency Manifests detected? ✅
- `active_repository.env` available? ✅
- SHARED_MEMORY.md and MEMORY.md (security_engineer) read? ✅
- `gh` authenticated? ✅