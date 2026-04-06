# Phase 3: Monitoring + Control Panel - Context

**Gathered:** 2026-04-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver a control panel that exposes runtime health, sessions, tasks, agents, and metrics; plus CTO-managed settings.

</domain>

<decisions>
## Implementation Decisions

### UI Structure
- **D-01:** Dashboard uses tabs.
- **D-02:** Tabs: Sessions, Tasks, Agents, Metrics.
- **D-03:** List density is medium.
- **D-04:** Each tab shows 4 top cards: active sessions, tasks in progress, tokens consumed, failures.

### Metrics & Aggregations
- **D-05:** Default window: 30 minutes with selector (1h, 6h, 24h).
- **D-06:** Metrics must include MON-02 set: tokens consumed, backlog, tasks in progress, tasks completed.
- **D-07:** Aggregation default: average per task (where applicable).
- **D-08:** Updates in real time via WebSocket.

### Failure Observability
- **D-09:** Failure view shows message + stack trace + evidence (logs/diffs/tests).
- **D-10:** Default detail is summary with expand for more.
- **D-11:** Retention is configurable by CTO.

### Configuration Management
- **D-12:** CTO can change limits/flags, model/provider selection, and agent management (activate/deactivate, roles).
- **D-13:** Require confirmation/audit for: model changes, agent disable, threshold changes.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project & Requirements
- `.planning/PROJECT.md` — core value, constraints, project guardrails
- `.planning/REQUIREMENTS.md` — monitoring + control requirements (MON-01..04, CTRL-01)
- `.planning/ROADMAP.md` — phase goals and success criteria

### Codebase Context Maps
- `.planning/codebase/ARCHITECTURE.md` — system layers and data flow
- `.planning/codebase/STACK.md` — runtime/framework constraints
- `.planning/codebase/STRUCTURE.md` — where UI/API/services should live
- `.planning/codebase/CONVENTIONS.md` — logging/error handling expectations

### Internal Docs (partially outdated)
- `docs/` — internal documentation to consider during refactor

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Next.js App Router UI in `control-panel/frontend/src/app`.
- UI components in `control-panel/frontend/src/components`.
- Client libs in `control-panel/frontend/src/lib` (Axios/React Query/WebSocket manager).

### Established Patterns
- Backend FastAPI routers in `control-panel/backend/app/api`.
- Services in `control-panel/backend/app/services`.
- WebSocket metrics flow: backend `control-panel/backend/app/api/ws.py` + frontend `control-panel/frontend/src/lib/ws.ts`.

### Integration Points
- Frontend API proxy `control-panel/frontend/src/app/api/[...slug]/route.ts`.
- Backend config in `control-panel/backend/app/core/config.py`.

</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 03-monitoring-control-panel*
*Context gathered: 2026-04-06*
