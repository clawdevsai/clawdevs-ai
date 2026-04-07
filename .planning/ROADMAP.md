# Roadmap: ClawDevs AI

## Overview

This roadmap delivers reliable local operation of the ClawDevs AI control plane from infrastructure hardening through frontend critical-path stability. Phases are derived from v1 requirement groups and ordered by dependency: safe startup/security first, then control-plane contract stability, then observability, memory continuity, and final frontend reliability expansion.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions after planning

- [ ] **Phase 1: Foundation Hardening** - Secure and deterministic local bootstrap/shutdown baseline.
- [ ] **Phase 2: Control Plane Contract Stability** - Stable agent/session/task operations over REST and WS contracts.
- [ ] **Phase 3: Observability and Degraded Operations** - Operator-visible SLO health and degraded mode signaling.
- [ ] **Phase 4: Memory and RAG Continuity** - Session continuity across restarts with safe semantic-search fallback.
- [ ] **Phase 5: Frontend Critical Path Reliability** - Reliable critical routes and auth/session behavior in the panel.

## Phase Details

### Phase 1: Foundation Hardening
**Goal**: Operators can boot and stop the local stack safely with secure configuration defaults.
**Depends on**: Nothing (first phase)
**Requirements**: LIFE-01, LIFE-02, LIFE-03, SECU-01, SECU-02, SECU-03
**Success Criteria** (what must be TRUE):
  1. Operator can start the full stack with one command and receive deterministic service status.
  2. Dependent services stay blocked when a base-service health check fails.
  3. Operator can perform clean shutdown while preserving critical state volumes.
  4. Non-local execution is rejected when insecure/default secrets are active.
  5. Sensitive actions only execute with valid authentication and emit an audit trail tied to a user.
**Plans**: TBD

### Phase 2: Control Plane Contract Stability
**Goal**: Operators can manage agents, sessions, and tasks with consistent state over versioned API and WS contracts.
**Depends on**: Phase 1
**Requirements**: CTRL-01, CTRL-02, CTRL-03, CONT-01, CONT-02, CONT-03
**Success Criteria** (what must be TRUE):
  1. Operator can list, inspect, and synchronize agents with consistent state.
  2. Operator can track session and task status updates through the control-plane APIs.
  3. Operator can re-run or reconcile failed flows without corrupting persisted state.
  4. Critical REST and WS flows stay compatible with the active versioned contract, including first-frame WS auth.
  5. Breaking contract changes are blocked by automated validation before merge.
**Plans**: TBD

### Phase 3: Observability and Degraded Operations
**Goal**: Operators can monitor critical flow health and detect degraded dependency states early.
**Depends on**: Phase 2
**Requirements**: MONI-01, MONI-02, MONI-03
**Success Criteria** (what must be TRUE):
  1. Operator can view availability and latency indicators for critical product flows.
  2. System clearly signals degraded mode when DB, Redis, OpenClaw, or Ollama dependencies fail.
  3. Context and optimization metrics are visible in near real time on monitoring screens.
  4. Operator can identify which critical flows are impacted during dependency degradation.
**Plans**: TBD
**UI hint**: yes

### Phase 4: Memory and RAG Continuity
**Goal**: Operators can continue work across restarts with reliable memory behavior and safe semantic-search fallback.
**Depends on**: Phase 3
**Requirements**: MEMR-01, MEMR-02
**Success Criteria** (what must be TRUE):
  1. Session and memory context remain available after restart within the defined retention policy.
  2. Operator can detect semantic-search unavailability and continue using a safe fallback path.
  3. Fallback behavior preserves core task flow without blocking operation or corrupting persisted context.
**Plans**: TBD

### Phase 5: Frontend Critical Path Reliability
**Goal**: Operators can use critical frontend routes reliably with consistent auth and preserved working context.
**Depends on**: Phase 4
**Requirements**: FRON-01, FRON-02, FRON-03
**Success Criteria** (what must be TRUE):
  1. Smoke E2E checks pass for `/login`, `/chat`, `/sessions`, `/monitoring`, and `/settings`.
  2. Invalid frontend auth tokens are cleared and the user is redirected to login consistently.
  3. Essential operator context is preserved across refresh and navigation on critical routes.
  4. Critical route behavior remains stable across releases without regression in the validated smoke suite.
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation Hardening | 0/TBD | Not started | - |
| 2. Control Plane Contract Stability | 0/TBD | Not started | - |
| 3. Observability and Degraded Operations | 0/TBD | Not started | - |
| 4. Memory and RAG Continuity | 0/TBD | Not started | - |
| 5. Frontend Critical Path Reliability | 0/TBD | Not started | - |
