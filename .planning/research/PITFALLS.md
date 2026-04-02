# Pitfalls Research

**Domain:** OpenClaw-based autonomous multi-agent dev system coordination/communication refactor
**Researched:** 2026-04-02
**Confidence:** MEDIUM

## Critical Pitfalls

### Pitfall 1: Unspecified Handoff Contracts (Implicit Interfaces)

**What goes wrong:**
Agents complete subtasks but produce outputs that don’t match downstream expectations (structure, scope, naming, or assumptions), causing silent integration failures.

**Why it happens:**
Teams assume “natural language is enough,” skipping explicit schemas, ownership, and acceptance criteria for plan -> execute -> review -> consolidate steps.

**How to avoid:**
Define explicit handoff contracts per step: input schema, output schema, success criteria, and ownership. Enforce via validators + diff checks before handoff.

**Warning signs:**
Reruns that “fix” formatting, repeated reviewer corrections to structure, or reviewers rejecting work for missing context rather than correctness.

**Phase to address:**
Coordination Refactor (plan/execute/review/consolidate contract definition)

---

### Pitfall 2: Shared Memory Without Consistency Controls

**What goes wrong:**
Agents write conflicting or stale state to a shared memory/blackboard, leading to contradictory decisions and regressions.

**Why it happens:**
Shared memory is treated as a dump; no versioning, locking, or provenance. Concurrent writes or late writes override correct state.

**How to avoid:**
Use structured memory entries with version IDs, source agent, and timestamps. Require explicit merge rules and conflict resolution (last-write-wins is not enough).

**Warning signs:**
Plans flip-flop, agents cite different “current” tasks, or consolidation removes work that was correct earlier.

**Phase to address:**
Memory Persistence + Compaction Policies

---

### Pitfall 3: Coordination Overhead Exceeds Task Value

**What goes wrong:**
More agents increase token use and latency without better outcomes; the system is slower and costlier than a single strong agent.

**Why it happens:**
Over-communication, broadcast messaging, or redundant agents are added without clear ROI or gating.

**How to avoid:**
Start with minimal agent count, use filtered channels, and gate coordination by task complexity. Measure “coordination cost per accepted change.”

**Warning signs:**
Token burn spikes with no quality gains, high message volume per task, or review cycles that never converge.

**Phase to address:**
Cost/Performance Controls + Monitoring

---

### Pitfall 4: Silent Success (False Positives)

**What goes wrong:**
Agents report “done” with outputs that look valid but are incomplete or wrong, passing format checks but failing intent.

**Why it happens:**
Validation focuses on structure, not semantic correctness or integration. Reviewers are under-specified.

**How to avoid:**
Add semantic checks: test execution, diff-based assertions, and reviewer prompts that require evidence (tests run, files changed list).

**Warning signs:**
High “completion” rates but downstream fixes are frequent; PRs reopened for missing edge cases.

**Phase to address:**
Review + Consolidation Quality Gates

---

### Pitfall 5: Orchestrator as Single Point of Failure

**What goes wrong:**
Central coordinator becomes a bottleneck, and any bug or stall halts the system.

**Why it happens:**
All routing, memory writes, and retries funnel through one orchestrator without fallbacks.

**How to avoid:**
Separate routing, memory, and execution services; add watchdogs and simple failover (restart with state replay).

**Warning signs:**
Backlog stalls when coordinator is busy, or queue builds up even though workers are idle.

**Phase to address:**
Runtime Configuration Alignment + Orchestration Hardening

---

### Pitfall 6: Retry/Repair Loops That Amplify Noise

**What goes wrong:**
Failed tasks retry endlessly or oscillate between plan/execute/review without converging.

**Why it happens:**
Retries are agent-driven with no tool-layer backoff, no escalation rules, and no “stop” condition.

**How to avoid:**
Centralize retry policy at the tool/runtime layer with exponential backoff, caps, and escalation to human or alternative agent.

**Warning signs:**
Repeated identical failures, long sessions with no net progress, or identical diffs reintroduced.

**Phase to address:**
Runtime Configuration Alignment (retry policy + escalation)

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Broadcast all messages to all agents | Fast visibility | Message flood, token blow-up | Never (use filtered routing) |
| Unstructured memory blobs | Easy to implement | Impossible to reconcile state | MVP only, with rapid replacement plan |
| Single model for all roles | Simpler ops | Same blind spots everywhere | Small experiments only |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Shared memory store | No versioning / provenance | Versioned writes + merge rules |
| Task queue | No idempotency | Deterministic task IDs + replay-safe handlers |
| Tooling layer | Agent-owned retries | Centralized retry/backoff at tool layer |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Over-communication | Token spend grows linearly with agent count | Filtered channels + minimal agents | 3+ agents on simple tasks |
| Heavy shared context | Slow response, memory bloat | Aggressive compaction + scoped context | Long sessions > 1 hour |
| Always-on reviewers | Latency spikes, throughput drops | Event-driven review | Backlog > 20 tasks |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Prompt injection into shared memory | Corrupts downstream agent actions | Content sanitization + allowlisted sources |
| Over-privileged tool access | Unintended file changes | Least-privilege tool scopes per agent |
| Secrets in shared logs | Credential leakage | Redaction at ingestion + scoped secrets |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Opaque agent decisions | Low trust, no adoption | Traceable rationale + artifacts per step |
| “All green” dashboard with silent failures | False confidence | Surface validation failures clearly |
| No cost visibility | Surprise bills | Token/compute budget per session |

## "Looks Done But Isn't" Checklist

- [ ] **Coordination loop:** Often missing explicit handoff contracts — verify schema + acceptance criteria per step
- [ ] **Shared memory:** Often missing conflict resolution — verify versioning + merge rules
- [ ] **Review gate:** Often missing semantic verification — verify tests run + evidence recorded
- [ ] **Monitoring:** Often missing cost metrics — verify token and throughput dashboards

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Handoff contract mismatch | MEDIUM | Pause pipeline, define schema, re-run consolidation |
| Shared memory inconsistency | HIGH | Snapshot rollback, rehydrate from last known good state |
| Coordination overhead | LOW | Reduce agents, add routing filters |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Unspecified Handoff Contracts | Coordination Refactor | Contract tests + reviewer acceptance rate |
| Shared Memory Without Consistency | Memory Persistence + Compaction | Conflict rate near zero; deterministic replay |
| Coordination Overhead | Monitoring + Cost Controls | Cost per task <= baseline target |
| Silent Success | Review + Consolidation Quality Gates | Semantic checks pass; regression rate drops |
| Orchestrator SPOF | Runtime Config Alignment | Orchestrator restart without lost state |
| Retry/Repair Loops | Runtime Config Alignment | Retry caps respected; no infinite loops |

## Sources

- https://cognitioncommons.org/research/multi-agent-coordination
- https://getathenic.com/blog/multi-agent-systems-coordination-patterns
- https://woliveiras.com/posts/building-multi-agent-systems-architectures-coordination-protocols-orchestration/
- https://mbrenndoerfer.com/writing/multi-agent-systems-coordination-communication-protocols
- https://arxiv.org/abs/2603.24284
- https://arxiv.org/abs/2511.17656
- https://arxiv.org/abs/1202.2773

---
*Pitfalls research for: OpenClaw-based autonomous multi-agent dev system*\n*Researched: 2026-04-02*
