# Architecture

**Analysis Date:** 2026-04-02

## Pattern Overview

**Overall:** Monorepo with a split frontend (Next.js App Router) and backend (FastAPI async API) plus Dockerized runtime services.

**Key Characteristics:**
- API-centric backend with router modules per domain and service layer for domain logic.
- Frontend uses Next.js App Router pages and a server-side proxy route for backend API calls.
- Async data access via SQLModel/SQLAlchemy and background loops/services for monitoring and metrics.

## Layers

**Frontend UI (Next.js App Router):**
- Purpose: Page routing, rendering, and UI composition.
- Location: `control-panel/frontend/src/app`
- Contains: `page.tsx`, `layout.tsx`, route handlers (e.g., `route.ts`).
- Depends on: UI components and client libraries.
- Used by: Browser clients.

**Frontend Components:**
- Purpose: Reusable UI blocks and layout elements.
- Location: `control-panel/frontend/src/components`
- Contains: Feature-specific component folders and shared UI primitives.
- Depends on: UI utilities and CSS.
- Used by: App Router pages.

**Frontend Client Libraries:**
- Purpose: HTTP/WS clients and shared utilities.
- Location: `control-panel/frontend/src/lib`
- Contains: API base URL, Axios instance, React Query client, WebSocket manager.
- Depends on: Environment variables and browser APIs.
- Used by: Pages and components.

**API Layer (FastAPI Routers):**
- Purpose: HTTP/WebSocket endpoints and request/response models.
- Location: `control-panel/backend/app/api`
- Contains: `APIRouter` modules (e.g., `agents.py`, `sessions.py`, `ws.py`).
- Depends on: Core config/db, models, services.
- Used by: Frontend proxy and external callers.

**Core Infrastructure:**
- Purpose: Cross-cutting concerns (config, auth, database).
- Location: `control-panel/backend/app/core`
- Contains: `config.py`, `auth.py`, `database.py`.
- Depends on: SQLModel/SQLAlchemy, Pydantic settings.
- Used by: API layer, services, tasks.

**Domain Models:**
- Purpose: Database entities and shared constants.
- Location: `control-panel/backend/app/models`
- Contains: SQLModel models like `agent.py`, `session.py`, `task.py`.
- Depends on: SQLModel.
- Used by: API and services.

**Service Layer:**
- Purpose: Business logic and integrations (agent sync, memory, governance, monitoring).
- Location: `control-panel/backend/app/services`
- Contains: service modules like `agent_sync.py`, `health_monitor.py`, `memory_indexing.py`.
- Depends on: core config/db, external services, models.
- Used by: API handlers, startup lifecycle, tasks.

**Background Tasks:**
- Purpose: Periodic or orchestration workflows.
- Location: `control-panel/backend/app/tasks`
- Contains: task coordinators like `periodic_sync.py`, `task_orchestration.py`.
- Depends on: services and core database.
- Used by: scheduler/worker entrypoints.

**Hooks:**
- Purpose: Event-driven or lifecycle hooks for features.
- Location: `control-panel/backend/app/hooks`
- Contains: semantic optimization hooks and tool execution hooks.
- Depends on: services and models.
- Used by: API or service workflows.

## Data Flow

**UI → Backend API:**
1. Next.js pages in `control-panel/frontend/src/app` render UI and call client utilities in `control-panel/frontend/src/lib`.
2. Client requests hit the proxy route `control-panel/frontend/src/app/api/[...slug]/route.ts`.
3. Proxy forwards to backend routes under `control-panel/backend/app/api`.
4. Backend handlers use SQLModel sessions (`control-panel/backend/app/core/database.py`) to query models in `control-panel/backend/app/models`.

**WebSocket Metrics Flow:**
1. Frontend subscribes via `control-panel/frontend/src/lib/ws.ts`.
2. Backend accepts WS connections in `control-panel/backend/app/api/ws.py`.
3. Services broadcast updates through the connection manager (e.g., `control-panel/backend/app/services/context_mode_metrics_broadcaster.py`).

**Startup/Migrations Flow:**
1. App startup in `control-panel/backend/app/main.py` triggers `run_migrations()` from `control-panel/backend/app/core/database.py`.
2. Admin bootstrap and agent sync are executed via `control-panel/backend/app/main.py` calling services in `control-panel/backend/app/services`.

**State Management:**
- Backend state is persisted in PostgreSQL via SQLModel models in `control-panel/backend/app/models`.
- Frontend state is managed via React Query in `control-panel/frontend/src/lib/query-client.ts` and context providers in `control-panel/frontend/src/app/providers.tsx`.

## Key Abstractions

**Router Modules:**
- Purpose: Domain-specific endpoints.
- Examples: `control-panel/backend/app/api/agents.py`, `control-panel/backend/app/api/sessions.py`
- Pattern: `APIRouter` per domain with Pydantic response models.

**Service Modules:**
- Purpose: Encapsulate domain logic and integrations.
- Examples: `control-panel/backend/app/services/agent_sync.py`, `control-panel/backend/app/services/health_monitor.py`
- Pattern: Async functions and lightweight service classes.

**SQLModel Entities:**
- Purpose: Database schema and ORM mappings.
- Examples: `control-panel/backend/app/models/agent.py`, `control-panel/backend/app/models/task.py`
- Pattern: SQLModel classes in snake_case files.

**Proxy Route:**
- Purpose: Frontend → backend request forwarding.
- Example: `control-panel/frontend/src/app/api/[...slug]/route.ts`
- Pattern: Next.js route handler with method handlers for REST verbs.

## Entry Points

**Backend API:**
- Location: `control-panel/backend/app/main.py`
- Triggers: Uvicorn/Gunicorn service start, Docker container start.
- Responsibilities: Configure FastAPI app, register routers, startup lifecycle, middleware.

**Frontend App:**
- Location: `control-panel/frontend/src/app/layout.tsx`, `control-panel/frontend/src/app/page.tsx`
- Triggers: Next.js server render or client navigation.
- Responsibilities: Global layout, page routing, providers.

**Frontend API Proxy:**
- Location: `control-panel/frontend/src/app/api/[...slug]/route.ts`
- Triggers: `/api/*` requests from the browser.
- Responsibilities: Forward to backend and normalize response.

## Error Handling

**Strategy:** Centralized exception handler in the backend and per-request try/catch in frontend proxy.

**Patterns:**
- Backend global exception handler in `control-panel/backend/app/main.py`.
- API-level HTTP errors via `HTTPException` in modules like `control-panel/backend/app/api/agents.py`.

## Cross-Cutting Concerns

**Logging:** Python `logging` in backend (`control-panel/backend/app/main.py`, services).  
**Validation:** Pydantic models in API layer (e.g., `control-panel/backend/app/api/agents.py`).  
**Authentication:** Bearer token validation in `control-panel/backend/app/api/deps.py` and JWT helpers in `control-panel/backend/app/core/auth.py`.

---

*Architecture analysis: 2026-04-02*
