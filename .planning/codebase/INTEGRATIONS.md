# External Integrations

**Analysis Date:** 2026-04-02

## APIs & External Services

**GitHub:**
- GitHub Issues API used to sync tasks in `control-panel/backend/app/services/task_sync.py`
  - SDK/Client: HTTP via `httpx` in `control-panel/backend/pyproject.toml`
  - Auth: `PANEL_GITHUB_TOKEN` (settings field `github_token`) in `control-panel/backend/app/core/config.py`

**OpenClaw Gateway:**
- OpenClaw chat/completions upstream proxy in `control-panel/frontend/src/app/openclaw/chat/stream/route.ts`
  - Client: `fetch` to `/v1/chat/completions`
  - Auth: `OPENCLAW_GATEWAY_TOKEN` or `PANEL_OPENCLAW_GATEWAY_TOKEN` in `control-panel/frontend/src/app/openclaw/chat/stream/route.ts`
  - Endpoint: `OPENCLAW_GATEWAY_URL` or `PANEL_OPENCLAW_GATEWAY_URL` in `control-panel/frontend/src/app/openclaw/chat/stream/route.ts`

**Ollama (LLM runtime):**
- Ollama health checks and semantic optimization in `control-panel/backend/app/core/config.py` and `control-panel/frontend/src/components/monitoring/ollama-health.ts`
  - Endpoint: `PANEL_OLLAMA_BASE_URL` (settings field `ollama_base_url`) in `control-panel/backend/app/core/config.py`
  - Model: `PANEL_OLLAMA_MODEL` (settings field `ollama_model`) in `control-panel/backend/app/core/config.py`

**Kubernetes:**
- K8s API client for container management in `control-panel/backend/app/services/container_client.py`
  - SDK/Client: `kubernetes` Python package in `control-panel/backend/pyproject.toml`

## Data Storage

**Databases:**
- PostgreSQL via SQLModel + asyncpg/psycopg in `control-panel/backend/pyproject.toml`
  - Connection: `PANEL_DATABASE_URL` (settings field `database_url`) in `control-panel/backend/app/core/config.py`
  - Client/ORM: SQLModel in `control-panel/backend/pyproject.toml`
- pgvector extension for vector search in `control-panel/backend/pyproject.toml`

**File Storage:**
- Not detected

**Caching:**
- Redis in `control-panel/backend/pyproject.toml`
  - Connection: `PANEL_REDIS_URL` (settings field `redis_url`) in `control-panel/backend/app/core/config.py`

## Authentication & Identity

**Auth Provider:**
- Custom JWT-based auth in `control-panel/backend/app/core/auth.py` and `control-panel/backend/app/api/auth.py`
  - Secret: `PANEL_SECRET_KEY` (settings field `secret_key`) in `control-panel/backend/app/core/config.py`

## Monitoring & Observability

**Error Tracking:**
- Not detected

**Logs:**
- Application logging in backend services (e.g., `control-panel/backend/app/services/task_sync.py`)

## CI/CD & Deployment

**Hosting:**
- Not detected

**CI Pipeline:**
- GitHub Actions workflows in `.github/workflows/publish-pod-images-on-tag.yml`, `.github/workflows/qa-logs-monitor.yml`, `.github/workflows/validate-deployment.yml`

## Environment Configuration

**Required env vars:**
- `PANEL_DATABASE_URL`, `PANEL_REDIS_URL`, `PANEL_SECRET_KEY` in `control-panel/backend/app/core/config.py`
- `PANEL_GITHUB_TOKEN`, `PANEL_GITHUB_ORG`, `PANEL_GITHUB_DEFAULT_REPOSITORY` in `control-panel/backend/app/core/config.py`
- `PANEL_OPENCLAW_GATEWAY_URL`, `PANEL_OPENCLAW_GATEWAY_TOKEN` (frontend accepts both `PANEL_*` and non-prefixed variants) in `control-panel/frontend/src/app/openclaw/chat/stream/route.ts`
- `BACKEND_URL`, `NEXT_PUBLIC_API_URL`, `API_INTERNAL_URL` in `control-panel/frontend/next.config.ts` and `control-panel/frontend/src/lib/api-base-url.ts`

**Secrets location:**
- `.env` file present (not inspected): `.env`

## Webhooks & Callbacks

**Incoming:**
- Not detected

**Outgoing:**
- GitHub Issues API calls in `control-panel/backend/app/services/task_sync.py`

---

*Integration audit: 2026-04-02*
