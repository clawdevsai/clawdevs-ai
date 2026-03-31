<!--
  Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
 -->

# ClawDevs AI — OpenClaw Configuration Index

Complete reference guide to OpenClaw configuration in ClawDevs AI. All configurations follow OpenClaw best practices.

## 📋 Configuration Files

### Core OpenClaw Specifications

**These files define how OpenClaw operates — read these first:**

1. **[CONSTITUTION.md](./shared/CONSTITUTION.md)**
   - Principles and non-negotiables for ClawDevs AI
   - Operating sequence: Constitution → Brief → Spec → Clarify → Plan → Tasks → Implement → Validate
   - Agent autonomy rules, memory & learning, cost optimization

2. **[SDD_CHECKLIST.md](./shared/SDD_CHECKLIST.md)**
   - Readiness gates before moving tasks between stages
   - Use as quality assurance checkl before deployment

3. **[CONTEXT_ENGINE_CONFIG.md](./shared/CONTEXT_ENGINE_CONFIG.md)**
   - How context is selected for each agent run
   - Token limits, recency bias, memory ranking, artifact inclusion
   - Per-agent context overrides

4. **[SESSION_MANAGEMENT_CONFIG.md](./shared/SESSION_MANAGEMENT_CONFIG.md)**
   - Session lifecycle, retention policies, pruning strategies
   - Compaction before deletion, archival after 180+ days
   - Per-agent session policies (CEO vs Dev Backend differences)

5. **[MEMORY_COMPACTION_CONFIG.md](./shared/MEMORY_COMPACTION_CONFIG.md)**
   - Memory lifecycle: Creation → Compression → Summarization → Archival
   - Extraction rules for keeping high-value insights
   - Consolidation of related memories

6. **[STANDING_ORDERS.md](./shared/STANDING_ORDERS.md)**
   - Permanent instructions that guide all agent behavior
   - Security & safety, quality & observability, behavioral standards
   - Per-agent standing orders (CEO, Dev Backend, QA, Memory Curator, etc)

7. **[HOOKS_SPECIFICATION.md](./shared/HOOKS_SPECIFICATION.md)**
   - 13 hook points in the agent execution lifecycle
   - Input/output schemas for each hook
   - Hook ordering, timeout policies, failure handling

8. **[CRON_JOBS_REGISTRY.md](./shared/CRON_JOBS_REGISTRY.md)**
   - All scheduled tasks: Memory curation, session pruning, CI/CD, data management
   - Execution flow, monitoring, failure recovery
   - Per-agent cron schedules from `.env`

---

## 🔌 Plugins & Integrations

### Plugin Documentation

- **[PLUGINS_MANIFEST.md](./plugins/PLUGINS_MANIFEST.md)** — Complete list of active plugins with tools, hooks, and configuration

### Individual Plugin Manifests

All plugins follow standard structure: `plugins/<plugin-id>/manifest.json`

| Plugin | ID | Tools | Hooks | Purpose |
|--------|----|----|-------|---------|
| **GitHub Integration** | `github-integration` | 7 | 3 | Manage repos, issues, PRs, code |
| **Telegram Bot** | `telegram-bot` | 3 | 3 | Send messages & notifications to CEO |
| **Ollama (Local LLM)** | `ollama-llm` | 2 | 2 | Cost-optimized local inference + embeddings |
| **OpenRouter (Remote LLM)** | `openrouter-llm` | 1 | 2 | Remote inference for complex reasoning |
| **SearXNG Search** | `searxng-search` | 2 | 2 | Web search for research & current info |
| **PostgreSQL** | `postgres-db` | 5 | 2 | Sessions, memories, operational data |
| **Redis Cache** | `redis-cache` | 4 | 3 | Fast caching layer for performance |

---

## 🤖 Agent Configurations

Each agent has a unique role. Check agent README for details:

- **ceo/** — Orchestrator, delegates work, manages team
- **arquiteto/** — Architecture decisions, system design
- **po/** — Product ownership, specs, requirements
- **dev_backend/** — Backend implementation, APIs
- **dev_frontend/** — Frontend implementation, UI
- **dev_mobile/** — Mobile implementation
- **qa_engineer/** — Quality assurance, testing
- **security_engineer/** — Security audit, risk management
- **devops_sre/** — Deployment, infrastructure, reliability
- **dba_data_engineer/** — Database, data pipelines
- **ux_designer/** — UX/UI design
- **memory_curator/** — Memory consolidation, org patterns

Each agent has:
- `INPUT_SCHEMA.json` — Contracts for what input they accept
- `skills/` directory — Agent-specific commands
- Memory staging directory in `memory/`

---

## 🎯 How to Use This Configuration

### For Agents

Each agent reads relevant configs at startup:

```bash
# Agent loads (in order):
1. CONSTITUTION.md          # Non-negotiables
2. STANDING_ORDERS.md       # Permanent instructions for this agent
3. <agent>/INPUT_SCHEMA.json # What inputs I accept
4. plugins/*/manifest.json  # What tools I have
5. HOOKS_SPECIFICATION.md   # What hooks to listen for
6. CONTEXT_ENGINE_CONFIG.md # How to assemble context
```

### For Developers

When implementing features:

```
1. Check CONSTITUTION.md for principles
2. Use SDD_CHECKLIST.md as quality gate
3. Define in SPEC template (in shared/)
4. Design agent flow respecting STANDING_ORDERS.md
5. Use plugins listed in PLUGINS_MANIFEST.md
6. Configure hooks from HOOKS_SPECIFICATION.md
7. Register cron jobs in CRON_JOBS_REGISTRY.md
```

### For Operations

Monitor and maintain:

```bash
# Check plugin health
openclaw plugin health

# View cron jobs & failures
openclaw cron list
openclaw cron failures --period 24h

# Monitor context usage
openclaw context metrics --period 24h

# Check session growth
openclaw session stats

# Audit hook executions
openclaw hooks audit --period 24h
```

---

## 📊 Summary of Improvements

| Category | Before | After |
|----------|--------|-------|
| **Context Management** | No documentation | Configurable engine with per-agent overrides |
| **Session Lifecycle** | Unbounded growth | Pruning, compaction, archival policies |
| **Memory** | No compaction | Automatic lifecycle with extraction rules |
| **Standing Orders** | Implicit in skills | Explicit, verifiable, auditable |
| **Hooks** | Invisible | 13 documented hooks with schemas |
| **Plugins** | Ad-hoc integrations | 7 official plugins with manifests |
| **Cron Jobs** | Scattered in .env | Registry with monitoring & SLAs |
| **Observability** | Minimal logging | Metrics, alerts, health checks per plugin |

---

## 🔍 Key Metrics to Monitor

```yaml
# Context Health
- Average context window size: 40-80k tokens (target)
- Token usage distribution: Recent msgs 60%, Memory 20%, Artifacts 20%
- Memory rerank accuracy: Top-5 memories relevant > 80%

# Session Health
- Session growth rate: < 5MB/day per active user
- Pruned sessions: Daily at 02:00 UTC
- Archival rate: After 180 days
- Average session size: < 50MB

# Memory Health
- Compaction success rate: > 95%
- Consolidation rate: 3+ similar memories → 1 pattern
- Memory expiry enforcement: 0 missed expirations

# Plugin Health
- GitHub API rate limit: > 100 req/hour remaining
- SearXNG requests: < 30/minute
- OpenRouter cost tracking: $ / token measured
- Cache hit ratio: > 70%

# Standing Orders Compliance
- Auth validation success: 100%
- Secret exposure attempts: 0 (auto-remediated)
- Rate limit violations: 0
- Verification asks (low confidence): < 5% of decisions
```

---

## 🚀 Next Steps

1. **Deploy configs**: All files are ready for `make up`
2. **Enable monitoring**: Start collecting metrics in production
3. **Tune per-agent**: Adjust context, session, memory policies based on agent behavior
4. **Add plugins**: New integrations follow `plugins/<id>/manifest.json` pattern
5. **Update hooks**: Add/modify hooks as new requirements arise
6. **Review quarterly**: Standing Orders, contexts, and policies should be reviewed

---

## 📞 Support

For questions about:
- **OpenClaw concepts** → Read CONSTITUTION.md
- **How agents execute** → Read HOOKS_SPECIFICATION.md
- **Monitoring & alerts** → Check PLUGINS_MANIFEST.md monitoring section
- **New plugins** → Follow pattern in `plugins/` directories
- **Performance tuning** → Check CONTEXT_ENGINE_CONFIG.md and SESSION_MANAGEMENT_CONFIG.md

---

**Last Updated**: 2026-03-31
**OpenClaw Version**: 2026.3.24
**Configuration Version**: 1.0.0

