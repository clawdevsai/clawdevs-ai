---
status: testing
phase: 03-monitoring-control-panel
source: [.planning/phases/03-monitoring-control-panel/03-monitoring-control-panel-01-SUMMARY.md, .planning/phases/03-monitoring-control-panel/03-monitoring-control-panel-02-SUMMARY.md, .planning/phases/03-monitoring-control-panel/03-monitoring-control-panel-03-SUMMARY.md, .planning/phases/03-monitoring-control-panel/03-monitoring-control-panel-04-SUMMARY.md]
started: 2026-04-06T12:02:05.830877+00:00
updated: 2026-04-06T12:02:05.830877+00:00
---

## Current Test

number: 1
name: Cold Start Smoke Test
expected: |
  Kill any running server/service. Clear ephemeral state (temp DBs, caches, lock files). Start the application from scratch. Server boots without errors, any seed/migration completes, and a primary query (health check, homepage load, or basic API call) returns live data.
awaiting: user response

## Tests

### 1. Cold Start Smoke Test
expected: Kill any running server/service. Clear ephemeral state (temp DBs, caches, lock files). Start the application from scratch. Server boots without errors, any seed/migration completes, and a primary query (health check, homepage load, or basic API call) returns live data.
result: pending

### 2. Monitoring Dashboard Tabs + Cards
expected: Open the Monitoring page. Tabs for Sessions, Tasks, Agents, and Metrics are visible. The top row shows cards labeled Active sessions, Tasks in progress, Tokens consumed, and Failures.
result: pending

### 3. Sessions Window + Empty State
expected: On the Sessions tab, default view shows recent sessions (30m). Toggling Show all reveals historical sessions. If there are no sessions, the empty state shows heading 'No recent sessions' and the body copy about sessions appearing after the next run.
result: pending

### 4. Tasks Metrics + Failure Detail
expected: On the Tasks tab, Cycle time average and Cycle time p95 values are visible along with a Throughput by label list. Selecting a failed task shows a Failure detail panel with Message, Stack trace, and Evidence (expand/collapse works).
result: pending

### 5. Metrics Tab Summary
expected: On the Metrics tab, tokens avg per task, backlog count, tasks completed, and tasks in review are visible.
result: pending

### 6. Agents Tab List
expected: On the Agents tab, a list of agents displays each agent name and status.
result: pending

### 7. Runtime Settings Editor + Confirmations
expected: On Settings page, the Runtime Settings section is present, shows confirmation prompts (Type CONFIRM to proceed, Type DISABLE to proceed), and the primary button reads 'Apply Runtime Settings'. Changing model/thresholds requires CONFIRM; disabling an agent requires DISABLE.
result: pending

## Summary

total: 7
passed: 0
issues: 0
pending: 7
skipped: 0

## Gaps

none yet