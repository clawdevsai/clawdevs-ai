# BOOTSTRAP.md - Dev_Backend

1. Upload env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Read `README.md` the repository to understand the application, stack and flow before implementing.
3. Validate base structure:
   - `${PROJECT_ROOT}`
   - `${PROJECT_ROOT}/src` or `${PROJECT_ROOT}/lib`
   - `${PROJECT_ROOT}/tests` or `${PROJECT_ROOT}/spec`
   - if non-existent, use fallback `/data/openclaw/backlog/implementation` and mark context as `standby` (without throwing an error)
4. Detect language by `technology_stack` from task or build files.
   - before reading `package.json`/`go.mod`, validate that the file exists
   - if there is no build file, do not fail; operate by `technology_stack` or wait for task
5. Define default commands (install/test/lint/build) per language.
6. Check language toolchain in PATH.
7. Configure logger with `task_id` and `language`.
8. Configure cost/performance baseline:
   - target latency p95/p99 (when task not defined)
   - CPU/memory usage limit
   - maximum expected operating cost
9. Enable technical research on the internet to optimize cost/performance.
10. Validate `gh` authentication and active repository permissions for issues, PRs and merges when the task requires it.
11. Set up scheduling:
   - fixed interval: 60 minutes
   - work source: issues GitHub label `back_end`
12. Ready.