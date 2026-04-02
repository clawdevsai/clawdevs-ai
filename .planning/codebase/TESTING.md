# Testing Patterns

**Analysis Date:** 2026-04-02

## Test Framework

**Runner:**
- pytest 8.4.0
- Config: `control-panel/backend/pyproject.toml`

**Assertion Library:**
- pytest built-in assertions

**Run Commands:**
```bash
cd control-panel/backend && pytest
cd control-panel/backend && pytest --cov=app
cd control-panel/frontend && pnpm exec cypress run
```

## Test File Organization

**Location:**
- Backend tests under `control-panel/backend/tests`
- Frontend E2E tests under `control-panel/frontend/cypress/e2e`

**Naming:**
- Backend: `test_*.py` (e.g., `control-panel/backend/tests/test_auth.py`)
- Frontend: `*.cy.ts` (e.g., `control-panel/frontend/cypress/e2e/login.cy.ts`)

**Structure:**
```
control-panel/backend/tests/
control-panel/frontend/cypress/e2e/
```

## Test Structure

**Suite Organization:**
```python
import pytest

@pytest.mark.asyncio
async def test_login_success(client, admin_user):
    response = await client.post("/auth/login", json={...})
    assert response.status_code == 200
```

**Patterns:**
- Backend async tests use `@pytest.mark.asyncio`: `control-panel/backend/tests/test_auth.py`
- Shared fixtures in `conftest.py`: `control-panel/backend/tests/conftest.py`
- E2E suites use `describe` + `beforeEach`: `control-panel/frontend/cypress/e2e/login.cy.ts`, `control-panel/frontend/cypress/e2e/chat.cy.ts`

## Mocking

**Framework:** `unittest.mock` (`AsyncMock`, `patch`) for backend services

**Patterns:**
```python
from unittest.mock import AsyncMock, patch

with patch("aiohttp.ClientSession.post") as mock_post:
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"embeddings": [[0.1, 0.2, 0.3]]})
```

**What to Mock:**
- External HTTP calls and services: `control-panel/backend/tests/test_embedding_search.py`
- Feature flags and side-effect services: `control-panel/backend/tests/test_semantic_optimization_hook.py`

**What NOT to Mock:**
- In-memory DB interactions using SQLite test engine: `control-panel/backend/tests/conftest.py`

## Fixtures and Factories

**Test Data:**
```python
@pytest_asyncio.fixture(scope="function")
async def admin_user(db_session):
    user = User(username="admin", password_hash=..., role="admin")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
```

**Location:**
- Backend fixtures in `control-panel/backend/tests/conftest.py`

## Coverage

**Requirements:** None enforced

**View Coverage:**
```bash
cd control-panel/backend && pytest --cov=app
```

## Test Types

**Unit Tests:**
- Pure service/class logic: `control-panel/backend/tests/test_context_metrics.py`

**Integration Tests:**
- FastAPI auth flow using ASGI client + SQLite: `control-panel/backend/tests/test_auth.py`, `control-panel/backend/tests/conftest.py`

**E2E Tests:**
- Cypress for UI flows: `control-panel/frontend/cypress/e2e/login.cy.ts`, `control-panel/frontend/cypress/e2e/chat.cy.ts`

## Common Patterns

**Async Testing:**
```python
@pytest.mark.asyncio
async def test_embed_success():
    ...
```

**Error Testing:**
```python
cy.intercept("POST", "/api/auth/login", { forceNetworkError: true }).as("networkError")
cy.get('[data-testid="login-error"]').should("be.visible")
```

---

*Testing analysis: 2026-04-02*
