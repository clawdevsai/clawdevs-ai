# Coding Conventions

**Analysis Date:** 2026-04-02

## Naming Patterns

**Files:**
- Frontend React components use kebab-case filenames: `control-panel/frontend/src/components/layout/app-layout.tsx`, `control-panel/frontend/src/components/approvals/approval-card.tsx`
- Next.js route pages follow `src/app/<route>/page.tsx`: `control-panel/frontend/src/app/login/page.tsx`, `control-panel/frontend/src/app/chat/page.tsx`
- Backend Python modules use snake_case: `control-panel/backend/app/services/context_metrics.py`, `control-panel/backend/app/hooks/semantic_optimization_hook.py`

**Functions:**
- Python functions use snake_case: `control-panel/backend/app/core/auth.py`
- Frontend helper functions use camelCase: `control-panel/frontend/src/components/layout/app-layout.tsx`

**Variables:**
- Constants are uppercase in Python tests: `control-panel/backend/tests/conftest.py`
- Frontend uses camelCase for locals and state: `control-panel/frontend/src/app/page.tsx`

**Types:**
- Python classes use PascalCase: `control-panel/backend/app/services/context_metrics.py`
- Frontend component props interfaces use PascalCase with `Props` suffix: `control-panel/frontend/src/components/ui/badge.tsx`

## Code Style

**Formatting:**
- No explicit formatter config detected (no `.prettierrc`, `prettier.config.*`, `biome.json`)
- TypeScript uses double quotes and trailing commas in object literals: `control-panel/frontend/src/app/layout.tsx`, `control-panel/frontend/src/app/page.tsx`
- Python uses double-quoted strings and module docstrings: `control-panel/backend/app/services/context_metrics.py`

**Linting:**
- Frontend scripts use TypeScript for linting (`tsc --noEmit`): `control-panel/frontend/package.json`
- No ESLint config detected despite `eslint` dependency: `control-panel/frontend/package.json`

## Import Organization

**Order:**
1. React/third‑party imports
2. Internal components/utilities via alias
3. Local relative imports

Examples: `control-panel/frontend/src/app/page.tsx`, `control-panel/frontend/src/components/layout/app-layout.tsx`

**Path Aliases:**
- Use `@/*` for `src/*`: `control-panel/frontend/tsconfig.json`
- Example usage: `control-panel/frontend/src/app/page.tsx`

## Error Handling

**Patterns:**
- FastAPI endpoints raise `HTTPException` for auth/authorization: `control-panel/backend/app/api/auth.py`, `control-panel/backend/app/api/deps.py`
- Service methods guard failures with `try/except` and return safe defaults: `control-panel/backend/app/services/embedding_search.py`
- DB session generator logs and re-raises: `control-panel/backend/app/core/database.py`
- Global exception handler logs and returns JSON error: `control-panel/backend/app/main.py`

## Logging

**Framework:** Python `logging`

**Patterns:**
- Module-level logger via `logging.getLogger(__name__)`: `control-panel/backend/app/core/database.py`, `control-panel/backend/app/hooks/semantic_optimization_hook.py`
- App-level `logging.basicConfig(level=logging.INFO)`: `control-panel/backend/app/main.py`

## Comments

**When to Comment:**
- Use module docstrings to describe purpose: `control-panel/backend/app/services/context_metrics.py`
- Inline comments for test setup/fixtures or explain edge cases: `control-panel/backend/tests/test_context_metrics.py`

**JSDoc/TSDoc:**
- Minimal JSDoc on custom Cypress commands: `control-panel/frontend/cypress/support/commands.ts`

## Function Design

**Size:** Favor small, single-purpose async methods for services and hooks: `control-panel/backend/app/services/embedding_search.py`, `control-panel/backend/app/hooks/semantic_optimization_hook.py`

**Parameters:** Prefer typed parameters with `Annotated` for FastAPI dependencies: `control-panel/backend/app/api/auth.py`, `control-panel/backend/app/api/deps.py`

**Return Values:** Typed return dicts for service results, safe defaults on error: `control-panel/backend/app/hooks/semantic_optimization_hook.py`

## Module Design

**Exports:** Prefer named exports for frontend components and utilities: `control-panel/frontend/src/components/ui/badge.tsx`, `control-panel/frontend/src/lib/utils.ts`

**Barrel Files:** Not detected in frontend or backend modules (no `index.ts`/`__init__.py` re-exports used as barrels).

---

*Convention analysis: 2026-04-02*
