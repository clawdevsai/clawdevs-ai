# Codebase Structure

**Analysis Date:** 2026-04-02

## Directory Layout

```
[project-root]/
├── control-panel/                 # Main product (frontend + backend)
├── docker/                        # Docker images and service configs
├── assets/                        # Static assets and binaries
├── docs/                          # Project documentation
├── scripts/                       # Dev/ops scripts
├── tests/                         # Top-level tests
├── Makefile                       # Task runner / automation
└── README.md                      # Project overview
```

## Directory Purposes

**control-panel/backend:**
- Purpose: FastAPI backend service.
- Contains: `app/` package, migrations, backend tests, Dockerfile.
- Key files: `control-panel/backend/app/main.py`, `control-panel/backend/app/core/config.py`, `control-panel/backend/app/core/database.py`

**control-panel/backend/app:**
- Purpose: Backend application code.
- Contains: `api/`, `core/`, `models/`, `services/`, `tasks/`, `hooks/`.
- Key files: `control-panel/backend/app/api`, `control-panel/backend/app/services`, `control-panel/backend/app/models`

**control-panel/frontend:**
- Purpose: Next.js frontend application.
- Contains: `src/`, `public/`, `next.config.ts`, `package.json`.
- Key files: `control-panel/frontend/src/app/layout.tsx`, `control-panel/frontend/src/app/page.tsx`

**control-panel/frontend/src:**
- Purpose: Frontend source code.
- Contains: `app/`, `components/`, `lib/`.
- Key files: `control-panel/frontend/src/app`, `control-panel/frontend/src/components`, `control-panel/frontend/src/lib`

**docker:**
- Purpose: Docker image definitions and service configs.
- Contains: Per-service directories such as `docker/clawdevs-panel-backend`, `docker/clawdevs-panel-frontend`.
- Key files: `docker/clawdevs-panel-backend`, `docker/clawdevs-panel-frontend`

**scripts:**
- Purpose: Operational and validation scripts.
- Contains: Shell and Python scripts under `scripts/`.
- Key files: `scripts/monitor-compression.sh`, `scripts/test-compression-integration.py`

## Key File Locations

**Entry Points:**
- `control-panel/backend/app/main.py`: FastAPI app initialization and router registration.
- `control-panel/frontend/src/app/layout.tsx`: Global layout and providers.
- `control-panel/frontend/src/app/page.tsx`: Frontend landing page.

**Configuration:**
- `control-panel/backend/app/core/config.py`: Backend settings.
- `control-panel/frontend/next.config.ts`: Next.js config.
- `control-panel/frontend/tsconfig.json`: TypeScript configuration.

**Core Logic:**
- `control-panel/backend/app/services`: Backend business logic.
- `control-panel/backend/app/api`: API endpoints and request/response models.
- `control-panel/frontend/src/components`: UI components.

**Testing:**
- `control-panel/backend/tests`: Backend tests.
- `control-panel/frontend/cypress`: Frontend E2E tests.
- `tests`: Top-level tests.

## Naming Conventions

**Files:**
- Backend Python files use snake_case (e.g., `control-panel/backend/app/services/agent_sync.py`).
- Next.js routes follow App Router conventions: `page.tsx`, `layout.tsx`, `route.ts` under `control-panel/frontend/src/app`.

**Directories:**
- Frontend feature routes are directory-based (e.g., `control-panel/frontend/src/app/agents`, `control-panel/frontend/src/app/sessions`).
- Backend domains are grouped by folder (e.g., `control-panel/backend/app/api`, `control-panel/backend/app/services`).

## Where to Add New Code

**New Feature:**
- Primary backend API: `control-panel/backend/app/api`
- Backend service logic: `control-panel/backend/app/services`
- Backend models: `control-panel/backend/app/models`
- Frontend page: `control-panel/frontend/src/app`
- Frontend components: `control-panel/frontend/src/components`

**New Component/Module:**
- Implementation: `control-panel/frontend/src/components`

**Utilities:**
- Shared frontend helpers: `control-panel/frontend/src/lib`
- Backend helpers: `control-panel/backend/app/core` or `control-panel/backend/app/services`

## Special Directories

**control-panel/backend/migrations:**
- Purpose: Alembic database migrations.
- Generated: Yes
- Committed: Yes

**control-panel/frontend/.next:**
- Purpose: Next.js build output.
- Generated: Yes
- Committed: No

**control-panel/backend/.venv:**
- Purpose: Python virtual environment.
- Generated: Yes
- Committed: No

---

*Structure analysis: 2026-04-02*
