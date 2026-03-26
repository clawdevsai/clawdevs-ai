# BOOT.md - Dev_Backend

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md`.
3. Read `README.md` the repository to understand the application, stack and flow before implementing.
4. Load `SOUL.md`.
5. Load `INPUT_SCHEMA.json`.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/dev_backend/MEMORY.md` — recover your own relevant implementation lessons.
8. Validate `/data/openclaw/` and implementation workspace.
9. Detect language using `technology_stack` from task or project files.
10. Load default commands by language (fallback if task does not include `## Comandos`):
    - Node.js: `npm ci`, `npm test`, `npm run lint`, `npm run build`
    - Python: `pip install -r requirements.txt`, `pytest`, `flake8`
    - Java (Maven): `mvn test`, `mvn -q -DskipTests package`
    - Go: `go test ./...`, `go vet ./...`, `go build ./...`
    - Rust: `cargo test`, `cargo clippy`, `cargo build --release`
11. Validate tools: `read`, `write`, `exec`, `git`, `sessions_send`.
12. Check commands via `exec`: `gh`, `web-search`, `web-read`.
13. Load standard targets: target latency, resource consumption, cost per request.
14. When completing the session: register up to 3 learnings in `/data/openclaw/memory/dev_backend/MEMORY.md`.
15. Ready to receive task from the Architect.

##healthcheck
- `/data/openclaw/` accessible? ✅
- INPUT_SCHEMA.json loaded? ✅
- Stack detected? ✅
- Tools `read`, `write`, `exec`, `git` available? ✅
- SHARED_MEMORY.md and MEMORY.md (dev_backend) read? ✅
- `ACTIVE_GITHUB_REPOSITORY` set? ✅