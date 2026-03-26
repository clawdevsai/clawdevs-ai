# BOOTSTRAP.md - QA_Engineer

1. Upload env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Read `README.md` the repository to understand stack and test commands.
3. Validate base structure:
   - `${PROJECT_ROOT}`
   - if non-existent, use fallback `/data/openclaw/backlog/implementation` and mark context as `standby` (without throwing an error)
4. Detect app type:
   - `next.config.js` / `vite.config.ts` → web (Playwright/Cypress)
   - `app.json` / `expo.json` → mobile (Detox/Maestro)
   - `package.json` + `express` / `fastapi` → API (k6 + Pact)
   - before reading build files, validate that the file exists
   - if no build file exists, do not fail; operate by `technology_stack` or wait for task
5. Check toolchain in PATH by type.
6. Configure logger with `task_id` and `test_type`.
7. Configure retry_counter storage (in memory or `/data/openclaw/backlog/qa/retries/`).
8. Validate `gh` authentication for updating issues/PRs.
9. Set up scheduling:
   - fixed interval: 60 minutes (offset: :45 of each hour)
   - work source: issues GitHub label `tests`
10. Ready.