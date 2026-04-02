# Architecture Research

**Domain:** OpenClaw-based autonomous multi-agent dev system
**Researched:** 2026-04-02
**Confidence:** MEDIUM

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Interaction & Control Layer                       │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Control UI  │  │ CLI / Setup │  │ Chat Channels│  │ API Hooks │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘  └─────┬─────┘  │
│         │                │                │                │        │
├─────────┴────────────────┴────────────────┴────────────────┴────────┤
│                     Gateway & Runtime Orchestration                  │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ Router/Policy│  │ Planner/Exec │  │ Agent Manager│  │ Tool Host│ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └────┬─────┘ │
│         │                │                │               │        │
├─────────┴────────────────┴────────────────┴───────────────┴────────┤
│                    State, Memory, and Observability                  │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌───────────────┐  │
│  │ Sessions │  │ Memory Store │  │ Workspace  │  │ Metrics/Logs  │  │
│  └──────────┘  └──────────────┘  └────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Control UI | Human oversight, configuration editing, monitoring | Web UI rendering config schema and activity dashboards | 
| CLI / Setup | Bootstrapping, config validation, quick ops | `openclaw` CLI commands (`setup`, `config`, `doctor`) |
| Chat Channels | User interaction surfaces and routing | Channel adapters (WhatsApp, Discord, WebChat, etc.) |
| Gateway / Runtime | Core message ingest, prompt construction, tool routing | OpenClaw Gateway runtime service |
| Planner/Executor | Plan → execute → review → consolidate loop | Agent-level orchestrator in runtime | 
| Agent Manager | Spawn/route sub-agents, enforce policies | Agent lifecycle manager in runtime |
| Tool Host / Skills | Execute tools, local shell, repo access | Skills/plugins executed by runtime |
| Sessions | Session lifecycle, concurrency limits | Runtime session store |
| Memory Store | Long-term memory, compaction, retrieval | Workspace-linked memory, external store optional |
| Workspace | Durable config, skills, prompts, memory on disk | `~/.openclaw/workspace` repo |
| Metrics/Logs | Tokens, throughput, health, audit trails | Gateway logs, dashboards, external metrics |

## Recommended Project Structure

```
clawdevs-ai/
├── apps/
│   ├── control-ui/          # Next.js UI for monitoring + config
│   └── api/                 # FastAPI backend + orchestration endpoints
├── runtime/
│   ├── gateway/             # OpenClaw runtime configs + wrappers
│   └── agents/              # Agent roles, workflows, prompts
├── memory/
│   ├── store/               # Memory adapters + compaction policies
│   └── schemas/             # Memory record schemas
├── coordination/
│   ├── planner/             # Plan/execution loop
│   └── scheduler/           # Queueing, rate limits, fairness
├── tools/
│   ├── skills/              # Tool definitions + skill registry
│   └── plugins/             # Runtime hooks, safety policies
└── observability/
    ├── metrics/             # Token usage, throughput, latency
    └── audit/               # Run logs, traces, action history
```

### Structure Rationale

- **apps/** keeps UI/API changes isolated from runtime logic.
- **runtime/** mirrors OpenClaw gateway concerns and configs.
- **memory/** separates compaction/storage decisions from agent logic.
- **coordination/** clarifies where planning vs execution responsibility lives.
- **tools/** localizes skill/plugin code and access policies.
- **observability/** makes monitoring first-class for autonomy KPIs.

## Architectural Patterns

### Pattern 1: Gateway-Centric Control Plane

**What:** A single gateway handles message ingress, tool routing, and agent lifecycle. UI/CLI only talk to the gateway API or its config schema.
**When to use:** When you need deterministic behavior and one place to enforce policies.
**Trade-offs:** Simple integration but can become a throughput bottleneck.

### Pattern 2: Workspace-as-System-of-Record

**What:** All durable agent state (skills, prompts, memories, config) lives in the workspace outside the repo.
**When to use:** To preserve customization across upgrades and to keep the runtime stateless.
**Trade-offs:** Requires explicit sync and migration steps.

### Pattern 3: Hook-Based Safety & Monitoring

**What:** Plugin + watcher hooks on lifecycle stages (ingress, prompt assembly, tool execution, sub-agent spawn) enforce policy and collect telemetry.
**When to use:** When you need runtime safety without forking the core runtime.
**Trade-offs:** More moving parts; needs clear performance budgets.

## Data Flow

### Request Flow

```
[User/Channel Event]
    ↓
[Gateway Ingress] → [Router/Policy] → [Planner] → [Executor]
    ↓                                    ↓
[Tool Host/Skills] ← [Tool Calls] ← [Agent Manager]
    ↓
[Workspace + Memory Store] → [Response Assembly] → [Channel/UI]
```

### Key Data Flows

1. **Config changes:** UI/CLI writes config schema → gateway validates/applies → runtime restarts if required.
2. **Session state:** Gateway creates session → pulls memory/workspace context → planner executes → logs/metrics persisted.
3. **Monitoring:** Runtime emits logs/metrics → control UI consumes for dashboards and alerts.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k sessions | Single gateway + local workspace + file-based memory | 
| 1k-100k sessions | External memory store, queueing for tools, async workers |
| 100k+ sessions | Split gateway/agent workers, dedicated metrics pipeline |

## Anti-Patterns

### Anti-Pattern 1: Let agents edit live config

**What people do:** Allow runtime agents to rewrite gateway config directly.
**Why it's wrong:** Causes non-deterministic failures and can break security boundaries.
**Do this instead:** Keep config edits manual or mediated through a human-reviewed control UI.

### Anti-Pattern 2: Memory and monitoring are afterthoughts

**What people do:** Only log after errors, store memory ad-hoc.
**Why it's wrong:** Long-running autonomy degrades with no compaction or KPIs.
**Do this instead:** Define memory schemas, compaction policy, and metrics from day one.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| LLM Provider (Ollama-first) | Model config in OpenClaw config | Must stay low-cost, local-first |
| Search Provider | Web search API config | Often via config section |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Control UI ↔ Gateway | HTTP API / schema-driven config | UI renders schema, applies config |
| CLI ↔ Gateway | CLI commands / config validate | CLI uses config validate/apply |
| Planner ↔ Tool Host | Tool invocation contracts | Enforce policy and logging |
| Gateway ↔ Memory Store | Read/write by session | Must support compaction |
| Gateway ↔ Observability | Log + metric emission | Drives autonomy KPIs |

## Suggested Build Order (Dependencies)

1. **Gateway + Config Schema** (UI/CLI depend on this)
2. **Workspace + Memory Store** (planner/executor depend on this)
3. **Planner/Executor Loop** (tool host depends on policies)
4. **Tool Host + Skills/Plugins** (needs gateway + planner contracts)
5. **Observability Layer** (needs runtime data + session IDs)
6. **Control UI + Monitoring** (depends on metrics + config schema)

## Sources

- https://openclawlab.com/en/docs/gateway/configuration/
- https://openclawdoc.com/docs/getting-started/configuration/
- https://openclawdoc.com/docs/getting-started/installation/
- https://openclaw.im/docs
- https://docs.xiaolongxia.org/start/setup
- https://arxiv.org/abs/2603.24414
- https://arxiv.org/abs/2603.11853

---
*Architecture research for: OpenClaw-based autonomous multi-agent dev system*
*Researched: 2026-04-02*
