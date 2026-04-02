---
status: human_needed
phase: 02-memory-orchestration-loop
started: 2026-04-02
updated: 2026-04-02
---

# Phase 2: Memory + Orchestration Loop — Verification

## Summary

Static verification passed for ORCH-01..03 and MEM-01..03 based on code and tests. Runtime checks are still required.

## Verified (Evidence)

- Deterministic loop with contract validation implemented in `control-panel/backend/app/tasks/task_orchestration.py` and `control-panel/backend/app/services/task_contracts.py`.
- Parallelism gate with adaptive thresholds implemented in `control-panel/backend/app/services/parallelism_gate.py` and enforced in `control-panel/backend/app/services/task_workflow.py`.
- Unified memory lifecycle with compaction and merge rules implemented in `control-panel/backend/app/services/memory_lifecycle.py` and integrated into `control-panel/backend/app/tasks/periodic_sync.py`.
- Unit tests added: `control-panel/backend/tests/test_task_contracts.py`, `control-panel/backend/tests/test_task_orchestration_loop.py`, `control-panel/backend/tests/test_parallelism_gate.py`, `control-panel/backend/tests/test_memory_lifecycle.py`.

## Human Verification Required

1. **Live orchestration loop**
   - Run a real task through plan→execute→self-review→peer-review→consolidate.
   - Expected: states advance in order with ActivityEvent logs and task ends completed.

2. **Invalid contract handling**
   - Force invalid JSON output from an agent step.
   - Expected: `task.replan_requested` logged and attempts increment until capped.

3. **Memory compaction runtime**
   - Trigger periodic sync/compaction.
   - Expected: archive written, summary stored, `events.jsonl` updated.

## Requirements Covered
- ORCH-01
- ORCH-02
- ORCH-03
- MEM-01
- MEM-02
- MEM-03

## Notes
- Once human checks pass, phase is fully verified.
