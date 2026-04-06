# Phase 3: Monitoring + Control Panel - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-06
**Phase:** 3-monitoring-control-panel
**Areas discussed:** UI Structure, Metrics & Aggregations, Failure Observability, Configuration Management

---

## UI Structure

| Option | Description | Selected |
|--------|-------------|----------|
| Tabs | Sessions/Tasks/Agents/Metrics | ✓ |

**User's choice:** Dashboard with tabs and top cards.
**Notes:** List density medium; 4 top cards: active sessions, tasks in progress, tokens, failures.

---

## Metrics & Aggregations

| Option | Description | Selected |
|--------|-------------|----------|
| Window | 30 min + selector | ✓ |
| Metrics | MON-02 set | ✓ |
| Aggregation | Avg per task | ✓ |
| Update | WebSocket realtime | ✓ |

---

## Failure Observability

| Option | Description | Selected |
|--------|-------------|----------|
| Detail | Message + stack + evidence | ✓ |
| Default | Summary + expand | ✓ |
| Retention | Configurable | ✓ |

---

## Configuration Management

| Option | Description | Selected |
|--------|-------------|----------|
| Scope | Limits/flags + model/provider + agents | ✓ |
| Audit | Model change, disable agent, thresholds | ✓ |

---

## the agent's Discretion

None.

## Deferred Ideas

None.
