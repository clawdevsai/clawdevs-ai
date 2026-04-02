# Requirements: ClawDevs AI

**Defined:** 2026-04-02
**Core Value:** Agents coordinate tasks end-to-end without human intervention while keeping cost and hardware usage low.

## v1 Requirements

### Orchestration

- [ ] **ORCH-01**: System runs a deterministic plan → execute → review → consolidate loop for each task
- [ ] **ORCH-02**: Agent handoffs use explicit contracts (inputs/outputs) and are validated
- [ ] **ORCH-03**: Parallelism is gated (default sequential; parallel only when complexity threshold allows)

### Memory

- [ ] **MEM-01**: Each agent has persistent memory storage with a unified access layer
- [ ] **MEM-02**: Memory compaction lifecycle is enforced (create → compress → summarize → archive)
- [ ] **MEM-03**: Memory entries support versioning/merge rules to prevent divergence

### Monitoring

- [ ] **MON-01**: Control panel shows sessions for last 30 minutes + historical session list
- [ ] **MON-02**: Control panel shows metrics: tokens consumed, backlog, tasks in progress, tasks completed
- [ ] **MON-03**: Control panel shows cycle time per task and throughput per team
- [ ] **MON-04**: Control panel exposes failure observability (traces/logs with evidence)

### Workspace & Tooling

- [ ] **WORK-01**: Workspace sandbox with artifact tracking is enforced for all agents
- [ ] **WORK-02**: Tool execution is restricted by allowlist + safety limits
- [ ] **WORK-03**: Runtime supports Ollama-first with controlled fallback (no new external integrations)

### Control Panel Management

- [ ] **CTRL-01**: CTO can manage core runtime settings (agents, sessions, bindings, monitoring) via control panel without recreating existing features

### Evaluation

- [ ] **EVAL-01**: Minimal regression suite for critical coordination scenarios exists and is runnable

## v2 Requirements

### Evaluation

- **EVAL-02**: Autonomy health score derived from monitoring + eval signals

## Out of Scope

| Feature | Reason |
|---------|--------|
| New external integrations | Explicitly excluded in this phase |
| Major UI redesign | Not required for refactor goal |
| Always-on browsing | Increases cost and nondeterminism |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ORCH-01 | Phase 1 | Pending |
| ORCH-02 | Phase 1 | Pending |
| ORCH-03 | Phase 1 | Pending |
| MEM-01 | Phase 2 | Pending |
| MEM-02 | Phase 2 | Pending |
| MEM-03 | Phase 2 | Pending |
| MON-01 | Phase 3 | Pending |
| MON-02 | Phase 3 | Pending |
| MON-03 | Phase 3 | Pending |
| MON-04 | Phase 3 | Pending |
| WORK-01 | Phase 1 | Pending |
| WORK-02 | Phase 3 | Pending |
| WORK-03 | Phase 1 | Pending |
| CTRL-01 | Phase 3 | Pending |
| EVAL-01 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-02*
*Last updated: 2026-04-02 after initial definition*
