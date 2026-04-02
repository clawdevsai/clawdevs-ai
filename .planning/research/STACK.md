# Stack Research

**Domain:** OpenClaw-based autonomous multi-agent orchestration (Ollama-first)
**Researched:** 2026-04-02
**Confidence:** MEDIUM

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| OpenClaw Gateway | v2026.4.1 | Orchestration runtime (gateway, agent lifecycle, tool policies) | Latest stable release; aligns with current OpenClaw runtime and gateway behavior. Confidence: HIGH. | 
| Node.js | 24.x (22.14+ supported) | Runtime for OpenClaw Gateway and tooling | Official OpenClaw setup recommends Node 24, with Node 22.14+ still supported. Confidence: HIGH. |
| Ollama | v0.19.0 | Local LLM serving for low-cost inference | Current release; provides local API with stable localhost base URL. Confidence: HIGH. |
| PostgreSQL | 18.3 | Durable state store (tasks, memory, audit, metadata) | Current supported release line; keeps state + vector storage in one service. Confidence: MEDIUM. |
| pgvector | 0.8.2 | Vector search inside Postgres | Latest pgvector release; integrates with Postgres 13+ and avoids a separate vector DB for low-cost ops. Confidence: HIGH. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Qdrant | 1.17.1 | Dedicated vector DB | Use only if Postgres+pgvector cannot meet recall/latency or scale targets. Confidence: HIGH. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| pnpm | Package manager for OpenClaw Gateway | Required by OpenClaw setup instructions. |
| Docker | Local containerization | Optional per OpenClaw setup; use for containerized dev/e2e. |

## Installation

```bash
# Core (installed via OpenClaw and system installers, not npm)
# - OpenClaw (gateway/runtime)
# - Node.js 24.x
# - Ollama v0.19.0
# - PostgreSQL 18.3 + pgvector 0.8.2
```

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Storing OpenClaw config/workspace inside the repo | OpenClaw docs explicitly place config + workspace outside the repo to keep updates safe and avoid overwrites | Keep config in `~/.openclaw/openclaw.json` and workspace in `~/.openclaw/workspace` |
| Hardcoding secrets in `openclaw.json` | OpenClaw supports SecretRef + file-backed secrets for safer credential handling | Use `~/.openclaw/secrets.json` + SecretRef in config |

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| PostgreSQL 18.3 + pgvector 0.8.2 | Qdrant 1.17.1 | Use Qdrant for high-scale vector search or when isolating vector workloads is required |
| Node.js 24.x | Node.js 22.14+ LTS | Use 22.14+ only if your environment cannot yet upgrade to Node 24 |

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| pgvector 0.8.2 | PostgreSQL 13+ (recommended with 18.3) | pgvector supports Postgres 13+; match the pgvector build to your Postgres major version |
| OpenClaw Gateway v2026.4.1 | Node.js 24.x (22.14+ supported) | OpenClaw setup recommends Node 24; 22.14+ still supported |

## Sources

- https://github.com/openclaw/openclaw/releases — OpenClaw latest release version
- https://docs.openclaw.ai/start/setup — Node version + config/workspace location
- https://docs.openclaw.ai/gateway/configuration-reference — SecretRef + secrets.json pattern
- https://github.com/ollama/ollama/releases — Ollama latest release version
- https://docs.ollama.com/api/introduction — Ollama API base URL
- https://www.postgresql.org/developer/roadmap/ — PostgreSQL 18.3 current release line
- https://github.com/pgvector/pgvector — pgvector 0.8.2 and Postgres compatibility
- https://github.com/qdrant/qdrant/releases — Qdrant latest release version
