# Project Research Summary

**Project:** clawdevs-ai
**Domain:** OpenClaw-based autonomous multi-agent software development platform (Ollama-first)
**Researched:** 2026-04-02
**Confidence:** MEDIUM

## Executive Summary

This project is an OpenClaw-based autonomous multi-agent development platform optimized for local-first, low-cost inference (Ollama-first). The research converges on a gateway-centric orchestration model with explicit planning/execution loops, durable workspace-as-system-of-record, and first-class memory plus observability. Experts build these systems by anchoring configuration and runtime control in a single gateway, then layering planners, tool hosts, and memory with strict contracts and auditability.

Recommended approach: start with the core runtime (gateway + config schema), workspace + memory store, and deterministic orchestration loop, then add tool-hosted skills and observability before shipping a control UI. The MVP should prioritize deterministic orchestration, unified memory with compaction, monitoring/session history, and workspace sandboxing. Key risks are coordination contract drift, inconsistent shared memory, and silent false positives; mitigate with explicit handoff schemas, versioned memory entries, and semantic validation gates.

## Key Findings

### Recommended Stack

The stack centers on OpenClaw Gateway v2026.4.1 with Node.js 24.x, Ollama v0.19.0, and PostgreSQL 18.3 + pgvector 0.8.2 for durable state + vector retrieval. Qdrant is an optional scale-up vector store if pgvector cannot meet latency/recall needs. OpenClaw config and workspace must remain outside the repo; secrets should use SecretRef with file-backed stores.

**Core technologies:**
- OpenClaw Gateway v2026.4.1: orchestration runtime — latest stable aligned with gateway behavior.
- Node.js 24.x: runtime — recommended by OpenClaw; 22.14+ supported fallback.
- Ollama v0.19.0: local LLM serving — stable local API for low-cost inference.
- PostgreSQL 18.3 + pgvector 0.8.2: durable state + vector search — keep storage consolidated.

### Expected Features

MVP must include deterministic multi-agent orchestration, unified memory with compaction policies, monitoring + session history, and a workspace sandbox with artifact tracking. Differentiators include cost-aware long-horizon autonomy, deterministic coordination/replay, and advanced observability. Evaluation tracking and autonomy health scoring should follow once the core loop is stable. Avoid always-on browsing, unbounded memory growth, and “integrate everything” marketplaces.

**Must have (table stakes):**
- Deterministic multi-agent orchestration — baseline loop stability.
- Unified memory + compaction — required for long-running autonomy.
- Monitoring dashboards + session history — visibility and trust.
- Workspace sandbox + artifact tracking — reliable code changes.

**Should have (competitive):**
- Cost caps + budget-aware autonomy — aligns to low-cost constraint.
- Deterministic coordination/replay — boosts trust and reliability.
- Memory lifecycle policies + observability — reduces drift and bloat.

**Defer (v2+):**
- Advanced observability (loop detection, bottleneck analysis).
- Deterministic replay at scale.

### Architecture Approach

The reference architecture is a gateway-centric control plane with planner/executor, agent manager, tool host, and a state layer for sessions, memory, workspace, and metrics. The workspace lives outside the repo as the system of record. Safety and monitoring should be enforced via lifecycle hooks.

**Major components:**
1. Gateway/Runtime — ingress, routing, agent lifecycle, tool policy.
2. Planner/Executor + Agent Manager — plan→execute→review loop and agent spawning.
3. Memory + Workspace — durable state, compaction, and artifact storage.
4. Observability — metrics, logs, audit trails for autonomy KPIs.
5. Control UI/CLI — schema-driven config + monitoring.

### Critical Pitfalls

1. **Unspecified handoff contracts** — define explicit input/output schemas and enforce validators before handoff.
2. **Shared memory without consistency controls** — use versioned entries, provenance, and merge rules.
3. **Coordination overhead > value** — start with minimal agents, gate parallelism by task complexity.
4. **Silent success (false positives)** — require semantic checks, tests, and evidence in reviews.
5. **Orchestrator SPOF + retry loops** — separate concerns, add watchdogs, centralized retry/backoff caps.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Runtime Foundation
**Rationale:** Gateway + config schema are prerequisite for all other layers.  
**Delivers:** OpenClaw gateway config, workspace location, basic session lifecycle.  
**Addresses:** Deterministic orchestration baseline, workspace sandboxing.  
**Avoids:** Orchestrator SPOF (by isolating routing vs execution early).

### Phase 2: Memory + Orchestration Loop
**Rationale:** Planner/executor depends on memory + workspace primitives.  
**Delivers:** Plan→execute→review loop, memory store, compaction policies, handoff contracts.  
**Addresses:** Unified memory, deterministic orchestration.  
**Avoids:** Handoff mismatch, shared memory inconsistency.

### Phase 3: Tool Host + Skills + Monitoring
**Rationale:** Tool execution and observability need stable runtime contracts.  
**Delivers:** Tool host, skill registry, structured logs/metrics, session history.  
**Addresses:** Monitoring dashboards, auditability, cost visibility.  
**Avoids:** Silent success, coordination overhead without metrics.

### Phase 4: Control UI + Evaluation Tracking
**Rationale:** UI consumes config schema + metrics; evals need reproducible runs.  
**Delivers:** Control UI, dashboards, evaluation harness + regression trends.  
**Addresses:** Evaluation tracking, autonomy health score (derivable).  
**Avoids:** False confidence from “all green” dashboards.

### Phase Ordering Rationale

- Gateway/config → workspace/memory → planner/executor → tools/observability → UI/evals is the dependency chain in ARCHITECTURE.md.
- Memory and monitoring are first-class to avoid long-run degradation and hidden failures.
- Phases explicitly target pitfalls: handoff contracts, memory consistency, and semantic validation.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** Memory compaction + conflict resolution policies (design choices vary).
- **Phase 3:** Tool safety policies + retry/backoff strategies.

Phases with standard patterns (skip research-phase):
- **Phase 1:** Gateway configuration + workspace layout (well-documented in OpenClaw docs).
- **Phase 4:** UI dashboards + eval harness patterns (established in agent tooling space).

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM | Mostly official docs/releases; some version lines inferred. |
| Features | MEDIUM | Ecosystem expectations + research papers; some community evidence. |
| Architecture | MEDIUM | Standard patterns with some non-official sources. |
| Pitfalls | MEDIUM | Research + practitioner sources; needs validation in this codebase. |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Project-specific requirements**: PROJECT.md missing; confirm exact product scope and non-goals.
- **Scale targets**: no explicit concurrency/throughput goals; needed to decide pgvector vs Qdrant and runtime sharding.
- **Security model**: access control and sandboxing policies need explicit definition before tool host work.

## Sources

### Primary (HIGH confidence)
- OpenClaw docs/releases — gateway setup, config, and Node version guidance.
- Ollama docs/releases — local LLM API and versioning.
- PostgreSQL roadmap and pgvector docs — version compatibility.

### Secondary (MEDIUM confidence)
- Agent observability and evaluation papers (AgentSight/AgentCompass).
- CrewAI/AutoGPT memory behavior references.
- Multi-agent coordination pattern articles.

---
*Research completed: 2026-04-02*  
*Ready for roadmap: yes*
