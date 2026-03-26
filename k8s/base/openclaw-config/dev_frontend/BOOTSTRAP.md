# BOOTSTRAP.md - Dev_Frontend

1. Upload env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Read `README.md` the repository to understand the application, stack and flow before implementing.
3. Validate base structure:
   - `${PROJECT_ROOT}`
   - `${PROJECT_ROOT}/src` or `${PROJECT_ROOT}/app` (Next.js App Router)
   - `${PROJECT_ROOT}/components` or `${PROJECT_ROOT}/src/components`
   - if non-existent, use fallback `/data/openclaw/backlog/implementation` and mark context as `standby` (without throwing an error)
4. Detect framework by build files:
   - `next.config.js` / `next.config.ts` → Next.js
   - `vite.config.ts` → Vite / React
   - `nuxt.config.ts` → Nuxt
   - `package.json` → check `"scripts"` field to infer framework
   - before reading build files, validate that the file exists
   - if no build file exists, do not fail; operate by `technology_stack` or wait for task
5. Define default commands (install/test/lint/build) per framework.
6. Check toolchain in PATH: `node`, `npm`, `npx`.
7. Check presence of Playwright or Cypress for e2e.
8. Configure logger with `task_id` and `framework`.
9. Configure performance baseline:
   - Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
   - Bundle size budget: document by page/component
10. Check presence of UX artifacts in `/data/openclaw/backlog/ux/` before implementation.
11. Enable technical research on the internet to optimize performance and accessibility.
12. Validate `gh` authentication and active repository permissions.
13. Set up scheduling:
    - fixed interval: 60 minutes (offset: :15 of each hour)
    - work source: issues GitHub label `front_end`
14. Ready.