# Autonomous Health Repair System Design

**Date:** 2026-03-30
**Status:** Approved for Implementation
**Phase:** Phase 1 (Detection Only / MVP)
**Pillar:** Observability & Self-Correction (25% of autonomy gap)

---

## Context

ClawdevsAI is an autonomous development team with 12 specialized agents. Currently, the system monitors health (logs, activity events, metrics) but doesn't **act on failures proactively**. Key gaps:

- Agents can crash/hang → no automatic restart
- Database connection pool can exhaust → service degrades
- Job queue can deadlock → tasks stuck forever
- Human intervention required for any recovery

This design implements **automated detection and remediation** via specialized repair agents, starting with Phase 1 (detection-only) to validate approach safely.

---

## Problem Statement

**Current State:**
- ✅ Health endpoints exist (`/api/health/summary`, `/api/health/tasks/{id}`)
- ✅ Failure detection works (activity_events logged)
- ✅ Escalation system exists (CEO/Arquiteto agents)
- ❌ **No loop actively monitors health**
- ❌ **No proactive recovery actions**
- ❌ **Failures require manual intervention**

**Symptom:** Agent crashes, system waits for human to notice in logs; database connections exhaust, slow degradation without correction; queue deadlocks, tasks hang forever.

**Target:** Agents autonomously detect and repair failures within 5 minutes of occurrence.

---

## Solution Overview

Implement **3 specialized Repair Agents** that run continuously in OpenClaw:

1. **DatabaseHealer** - Monitors PostgreSQL health
2. **AgentReviver** - Monitors agent heartbeats & container status
3. **QueueMechanic** - Monitors Redis queue & job processing

Each agent:
- Runs independently in OpenClaw (like CEO, Dev_Backend, etc)
- Monitors its domain continuously
- Detects issues and logs activity_events
- Escalates findings to appropriate agents (CEO, Arquiteto)
- Updates shared memory with patterns

Backed by a **Health Monitoring Loop** (backend service) that:
- Polls health metrics every 5 minutes
- Invokes the 3 repair agents with fresh data
- Handles failures gracefully

**Phase 1 = Detection Only** (no destructive actions yet). Recovery actions (restart, rebuild pool, retry jobs) deferred to Phase 2.

---

## System Architecture

### 3-Layer Health Ecosystem

```
┌─────────────────────────────────────────────────────────────┐
│                    REPAIR AGENTS (NEW)                       │
│  ┌──────────────────┬───────────────────┬─────────────────┐ │
│  │ DatabaseHealer   │  AgentReviver     │  QueueMechanic  │ │
│  │ - Pool status    │  - Heartbeats     │  - Queue depth  │ │
│  │ - Slow queries   │  - Container logs │  - Dead-letter  │ │
│  │ - Fragmentation  │  - Session activity │ - Job age   │ │
│  └──────────────────┴───────────────────┴─────────────────┘ │
│         ↑                    ↑                     ↑           │
└─────────────────────────────────────────────────────────────┘
         Invoked by:
┌─────────────────────────────────────────────────────────────┐
│          HEALTH MONITORING LOOP (NEW - Backend Service)      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Every 5 minutes:                                       │ │
│  │ 1. Gather metrics (DB, Agents, Queue)                │ │
│  │ 2. Invoke 3 repair agents in parallel               │ │
│  │ 3. Handle failures gracefully                        │ │
│  │ 4. Log loop status                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         Logs findings to:
┌─────────────────────────────────────────────────────────────┐
│         ACTIVITY EVENTS & MEMORY (EXISTING - Enhanced)      │
│  - Detections logged as activity_events                     │
│  - Patterns aggregated by Memory_Curator                    │
│  - Policies inform Phase 2 recovery actions                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. DatabaseHealer Agent

**Purpose:** Detect PostgreSQL health degradation

**Monitoring Signals:**

| Signal | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Connection Pool | < 70% used | 70-90% | > 90% |
| Slow Queries | < 1 per 5min | 1-3 | > 3 |
| Query Latency (p95) | < 100ms | 100-500ms | > 500ms |
| Disk Usage | < 70% | 70-85% | > 85% |
| Replication Lag | < 1s | 1-10s | > 10s |
| Index Fragmentation | < 20% | 20-40% | > 40% |

**Detection Rules (Phase 1):**

```yaml
rules:
  - name: "db_connection_pool_warning"
    condition: "pool_connections > 80% of max"
    severity: "warning"
    action: "log_event"

  - name: "db_connection_pool_critical"
    condition: "pool_connections >= 95%"
    severity: "critical"
    action: "log_event + escalate_to_arquiteto"

  - name: "db_slow_queries_detected"
    condition: "slow_query_count > 3 in last 5min"
    severity: "warning"
    action: "log_event + identify_slow_queries"

  - name: "disk_space_critical"
    condition: "disk_free < 5GB"
    severity: "critical"
    action: "log_event + alert_devops_sre"
```

**Outputs:**
- activity_events with type `repair_db_*`
- Memory: patterns like "pool exhaustion after 10+ concurrent Dev tasks"
- Escalations to Arquiteto (critical) or CEO (warning)

**Implementation Files:**
- Agent dir: `docker/base/openclaw-config/agents/database_healer/` (NEW)
- Skills: `database_healer/skills/monitor_connections.md`, `monitor_queries.md`, etc
- Integration: Health loop queries PostgreSQL directly via SQLAlchemy

---

### 2. AgentReviver Agent

**Purpose:** Detect agent crashes, hangs, container failures

**Monitoring Signals:**

| Signal | Healthy | Stale | Dead |
|--------|---------|-------|------|
| Heartbeat Age | < 5 min | 5-30 min | > 30 min |
| Status | online/working | idle | offline |
| Container Health | healthy | starting | unhealthy |
| Last Activity | < 10 min | 10-30 min | > 1 hour |
| Cron Execution | success | none | failed 3x |

**Detection Rules (Phase 1):**

```yaml
rules:
  - name: "agent_heartbeat_timeout"
    condition: "last_heartbeat_at > 30 minutes"
    severity: "critical"
    affected_agents: "any"
    action: "log_event + escalate_to_ceo"

  - name: "agent_offline"
    condition: "agent.status == offline > 5 minutes"
    severity: "critical"
    action: "log_event + check_container_health"

  - name: "agent_container_unhealthy"
    condition: "container.health_status == unhealthy"
    severity: "critical"
    action: "log_event + escalate_to_devops"

  - name: "agent_cron_repeated_failures"
    condition: "cron_failures >= 3 consecutive"
    severity: "warning"
    action: "log_event + suggest_manual_debug"
```

**Outputs:**
- activity_events with type `repair_agent_*`
- Memory: patterns like "Dev_Backend crashes when task queue > 50"
- Escalations to CEO (critical) or DevOps (container issues)

**Implementation Files:**
- Agent dir: `docker/base/openclaw-config/agents/agent_reviver/` (NEW)
- Skills: `agent_reviver/skills/heartbeat_monitor.md`, `container_health.md`
- Integration: Uses agent_sync.py + session artifacts

---

### 3. QueueMechanic Agent

**Purpose:** Detect queue deadlocks, stuck jobs, high failure rates

**Monitoring Signals:**

| Signal | Healthy | Degraded | Critical |
|--------|---------|----------|----------|
| Queue Depth | < 50 jobs | 50-200 | > 200 |
| Processing Rate | > 10 jobs/min | 5-10 | < 5 |
| Job Age (max) | < 5 min | 5-30 min | > 30 min |
| Failure Rate | < 5% | 5-20% | > 20% |
| Dead-Letter Queue | < 5 jobs | 5-20 | > 20 |
| Redis Memory | < 500MB | 500-800MB | > 800MB |

**Detection Rules (Phase 1):**

```yaml
rules:
  - name: "queue_processing_stuck"
    condition: "queued_jobs > 100 AND processing_rate < 5/min"
    severity: "critical"
    likely_cause: "deadlock or hung worker"
    action: "log_event + analyze_job_dependency + escalate_to_ceo"

  - name: "job_aging_without_progress"
    condition: "oldest_job_age > 1 hour AND not in progress"
    severity: "critical"
    action: "log_event + identify_blocker + escalate_to_qa"

  - name: "persistent_job_failures"
    condition: "dead_letter_queue > 10 in last hour"
    severity: "warning"
    action: "log_event + failure_pattern_analysis"

  - name: "redis_memory_pressure"
    condition: "redis_memory > 750MB"
    severity: "warning"
    action: "log_event + suggest_cleanup"
```

**Outputs:**
- activity_events with type `repair_queue_*`
- Memory: patterns like "Task X + Agent Y combo = deadlock"
- Escalations to CEO (critical) or QA (failure pattern)

**Implementation Files:**
- Agent dir: `docker/base/openclaw-config/agents/queue_mechanic/` (NEW)
- Skills: `queue_mechanic/skills/queue_monitor.md`, `deadlock_detector.md`
- Integration: Uses Redis client + RQ job inspection

---

### 4. Health Monitoring Loop (Backend Service)

**Purpose:** Periodically invoke repair agents with fresh health data

**File:** `control-panel/backend/app/services/health_monitor.py` (NEW)

**Responsibilities:**

```python
class HealthMonitorLoop:
    """Periodic health check orchestrator"""

    async def run_loop(self):
        """Main loop - runs every 5 minutes"""
        while self.enabled:
            try:
                # 1. Gather metrics from infrastructure
                db_metrics = await self.gather_db_metrics()
                agent_metrics = await self.gather_agent_metrics()
                queue_metrics = await self.gather_queue_metrics()

                # 2. Invoke repair agents in parallel
                tasks = [
                    self.invoke_agent("database_healer", db_metrics),
                    self.invoke_agent("agent_reviver", agent_metrics),
                    self.invoke_agent("queue_mechanic", queue_metrics),
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # 3. Log loop execution
                await self.log_loop_execution(results)

            except Exception as e:
                logger.error(f"Health monitor error: {e}")

            # 4. Sleep until next interval
            await asyncio.sleep(self.interval_seconds)
```

**Metric Gathering:**

| Metric Type | Source | Query |
|-----------|--------|-------|
| DB Metrics | PostgreSQL | Connection pool, slow query log, table stats |
| Agent Metrics | Agent table + session files | Heartbeat age, status, container health |
| Queue Metrics | Redis + RQ | Job counts, processing rate, dead-letter queue |

**Agent Invocation:**

```python
async def invoke_agent(self, agent_slug: str, metrics: dict):
    """Invoke repair agent with metrics payload"""

    session = await self.openclaw_client.create_session(agent_slug)
    payload = {
        "role": "repair",
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Send to agent, wait for response
    response = await self.openclaw_client.send_message(
        session_id=session.id,
        message=json.dumps(payload)
    )

    return {
        "agent": agent_slug,
        "session_id": session.id,
        "success": response.status == "success",
        "findings": response.findings,
    }
```

**Configuration (.env):**

```bash
# Health Monitor Settings
HEALTH_MONITOR_ENABLED=true
HEALTH_MONITOR_INTERVAL_SECONDS=300        # 5 minutes
HEALTH_MONITOR_STARTUP_DELAY_SECONDS=30    # Wait before first run

# Individual Repair Agent Toggles
DATABASE_HEALER_ENABLED=true
AGENT_REVIVER_ENABLED=true
QUEUE_MECHANIC_ENABLED=true

# Thresholds (used by repair agents)
DB_CONNECTION_POOL_WARNING_THRESHOLD=80
DB_CONNECTION_POOL_CRITICAL_THRESHOLD=95
AGENT_HEARTBEAT_TIMEOUT_MINUTES=30
QUEUE_PROCESSING_TIMEOUT_MINUTES=60
```

**Startup Integration:**

```python
# In app/main.py
@app.on_event("startup")
async def startup_health_monitor():
    """Start health monitor loop on app startup"""
    if config.HEALTH_MONITOR_ENABLED:
        health_monitor = HealthMonitorLoop(
            interval=config.HEALTH_MONITOR_INTERVAL_SECONDS
        )
        asyncio.create_task(health_monitor.run_loop())
        logger.info("Health monitor loop started")
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Health Monitor Loop Trigger (every 5 min)                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Gather Metrics                                            │
│    - PostgreSQL connection pool, query logs                  │
│    - Agent heartbeat timestamps, session activity           │
│    - Redis queue depth, job counts, processing rate        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Invoke 3 Repair Agents (Parallel)                        │
│    DatabaseHealer (DB metrics) →                           │
│    AgentReviver (Agent metrics) →                          │
│    QueueMechanic (Queue metrics) →                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Each Agent Analyzes Metrics Against Detection Rules      │
│    DatabaseHealer: pool > 90%? → CRITICAL                   │
│    AgentReviver: heartbeat > 30min? → CRITICAL             │
│    QueueMechanic: jobs > 100 AND rate < 5/min? → CRITICAL │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Log Findings to Activity Events                           │
│    INSERT activity_events (                                  │
│      event_type='repair_db_pool_critical',                 │
│      severity='critical',                                   │
│      agent_id='database_healer',                            │
│      payload={metrics, threshold, action}                  │
│    )                                                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Memory & Pattern Recognition (Phase 1.5)                 │
│    Memory_Curator reads activity_events                     │
│    Extracts patterns: "DB pool > 90% when 10+ tasks"        │
│    Updates SHARED_MEMORY.md                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Phase 2: Recovery Policies (Future)                      │
│    Policy Engine reads patterns & SHARED_MEMORY             │
│    Decides action: restart agent? rebuild pool? retry job? │
│    Executes action autonomously (< 5min response)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### Database Schema Changes

**Extend existing `activity_events` table (no new tables in Phase 1):**

```sql
-- Existing table, used for all activity
activity_events (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50),          -- 'repair_db_*', 'repair_agent_*', etc
    severity VARCHAR(20),              -- 'info', 'warning', 'critical'
    agent_id UUID REFERENCES agents,   -- Which repair agent detected
    payload JSONB,                      -- Metrics + rules + findings
    created_at TIMESTAMP,
    ...existing fields...
);
```

**New health metrics table (optional, for trend analysis Phase 2):**

```sql
health_metrics (
    id UUID PRIMARY KEY,
    metric_type VARCHAR(50),        -- 'db_pool', 'agent_heartbeat', 'queue_depth'
    agent_id UUID REFERENCES agents, -- Which agent the metric is about
    value FLOAT,
    unit VARCHAR(20),
    timestamp TIMESTAMP,
    INDEX (agent_id, timestamp)
);
```

### API Endpoints (NEW)

```
GET /api/health/monitor/status
  → Returns: enabled, last_run, next_run, health_of_monitor_itself

POST /api/health/monitor/trigger
  → Manually trigger health monitor (for testing)
  → Returns: invocation results

GET /api/health/metrics/latest
  → Returns: latest health snapshot (db, agents, queue)

GET /api/health/repairs/history?limit=50
  → Returns: history of repair agent invocations
  → Filters: agent_type, severity, date_range

GET /api/health/repairs/{repair_id}/details
  → Returns: detailed findings from specific repair run
```

### Environment Variables (NEW)

```bash
# .env additions
HEALTH_MONITOR_ENABLED=true
HEALTH_MONITOR_INTERVAL_SECONDS=300
DATABASE_HEALER_ENABLED=true
AGENT_REVIVER_ENABLED=true
QUEUE_MECHANIC_ENABLED=true

# Thresholds (read by repair agents)
DB_CONNECTION_POOL_WARNING_PCT=80
DB_CONNECTION_POOL_CRITICAL_PCT=95
AGENT_HEARTBEAT_TIMEOUT_MINUTES=30
QUEUE_CRITICAL_DEPTH=100
QUEUE_CRITICAL_PROCESSING_RATE_MIN=5
```

---

## Phase 1 Constraints (Detection-Only)

**What Phase 1 Does:**
- ✅ Detect PostgreSQL health issues
- ✅ Detect agent hangs/crashes
- ✅ Detect queue deadlocks
- ✅ Log all findings to activity_events
- ✅ Update memory with patterns
- ✅ Escalate to CEO/Arquiteto (informational)

**What Phase 1 Does NOT Do:**
- ❌ Auto-restart containers
- ❌ Rebuild connection pools
- ❌ Retry jobs
- ❌ Kill hanging tasks
- ❌ Take any destructive action

**Why:** To validate detection accuracy before adding recovery. Phase 2 adds recovery policies once we're confident in detection.

---

## Testing & Validation (Phase 1)

### Unit Tests

```python
# tests/services/test_health_monitor.py
class TestHealthMonitor:
    async def test_monitor_loop_runs_on_interval(self):
        # Verify loop runs every 5 min

    async def test_gather_db_metrics(self):
        # Query PostgreSQL, verify metrics structure

    async def test_invoke_repair_agent(self):
        # Mock OpenClaw client, verify agent invocation

    async def test_graceful_failure(self):
        # If agent invoke fails, loop continues

# tests/agents/test_database_healer.py
class TestDatabaseHealer:
    async def test_detect_pool_exhaustion(self):
        # Mock high connection count, verify detection

    async def test_detect_slow_queries(self):
        # Query log with slow queries, verify detection

    async def test_output_activity_event(self):
        # Verify findings logged correctly

# tests/agents/test_agent_reviver.py
class TestAgentReviver:
    async def test_detect_heartbeat_timeout(self):
        # Agent with stale heartbeat, verify critical event

    async def test_detect_offline_status(self):
        # Agent status offline, verify detection

# tests/agents/test_queue_mechanic.py
class TestQueueMechanic:
    async def test_detect_stuck_queue(self):
        # High queue depth, low processing, verify detection

    async def test_detect_job_aging(self):
        # Job stuck > 1h, verify critical event
```

### Integration Tests

```python
# tests/integration/test_health_repair_e2e.py
class TestHealthRepairE2E:
    async def test_full_flow_db_issue(self):
        """
        1. Reduce PostgreSQL max_connections
        2. Create connections until warning threshold
        3. Verify monitor detects and invokes DatabaseHealer
        4. Verify activity_event logged
        5. Verify Memory_Curator finds pattern
        """

    async def test_full_flow_agent_timeout(self):
        """
        1. Stop an agent's heartbeat
        2. Wait > 30 min
        3. Verify AgentReviver detects
        4. Verify CEO notified via escalation
        """

    async def test_full_flow_queue_deadlock(self):
        """
        1. Create dependent jobs that deadlock
        2. Verify QueueMechanic detects stuck queue
        3. Verify activity_event with deadlock pattern
        """
```

### Manual Validation Checklist

- [ ] Monitor loop starts on app startup
- [ ] Loop runs every 5 min (check logs for timestamps)
- [ ] Manually trigger via `POST /api/health/monitor/trigger`
- [ ] Verify each repair agent receives metrics
- [ ] Verify activity_events created (check DB)
- [ ] Verify escalations to CEO/Arquiteto work
- [ ] Disable/re-enable via `.env`, verify behavior
- [ ] Run 24h stress test, monitor loop should not crash

---

## Success Criteria (Phase 1)

✅ **MVP is successful when:**
1. Health monitor loop runs continuously without crashing
2. All 3 repair agents detect their target issues (100% recall)
3. All detections logged to activity_events within 5 min of occurrence
4. Memory_Curator extracts patterns from detections
5. No false positives (high precision)
6. Escalations to CEO/Arquiteto work reliably
7. System can run 24/7 with 100% uptime of monitor itself

**Go/No-Go for Phase 2:**
- If success criteria met → implement recovery policies (Phase 2)
- If failures found → iterate on detection rules, don't move to Phase 2

---

## Future (Phase 2+)

### Phase 2: Add Recovery Actions

Once Phase 1 validated, Phase 2 adds autonomous recovery:

```
Repair agents + Policy Engine:
├─ DatabaseHealer: Rebuild pool → rotate connections
├─ AgentReviver: Auto-restart container → reset session
└─ QueueMechanic: Retry stuck jobs → escalate if permanent failure
```

### Phase 3: Learning & Adaptation

- Repair agents learn patterns from Memory_Curator
- Policies evolve (e.g., "restart earlier if pattern X detected")
- Resource optimization (e.g., pre-scale pool during high-demand hours)

---

## Files to Create/Modify

### NEW FILES

| Path | Purpose |
|------|---------|
| `control-panel/backend/app/services/health_monitor.py` | Health monitoring loop service |
| `docker/base/openclaw-config/agents/database_healer/` | DatabaseHealer agent (IDENTITY, skills) |
| `docker/base/openclaw-config/agents/agent_reviver/` | AgentReviver agent (IDENTITY, skills) |
| `docker/base/openclaw-config/agents/queue_mechanic/` | QueueMechanic agent (IDENTITY, skills) |
| `control-panel/backend/app/api/health_repairs.py` | API endpoints for repair history |
| `docs/plans/2026-03-30-autonomous-health-repair-design.md` | THIS FILE |

### MODIFIED FILES

| Path | Changes |
|------|---------|
| `control-panel/backend/app/main.py` | Add startup hook for health monitor |
| `control-panel/backend/app/core/config.py` | Add health monitor config variables |
| `.env.example` | Add HEALTH_MONITOR_* variables |
| `docker-compose.yml` | No changes (repair agents run in OpenClaw) |

---

## References

- **Current Health System:** `control-panel/backend/app/api/health.py`
- **Agent Model:** `control-panel/backend/app/models/agent.py`
- **Activity Events:** `control-panel/backend/app/models/activity_event.py`
- **Agent Sync:** `control-panel/backend/app/services/agent_sync.py`
- **OpenClaw Client:** `control-panel/backend/app/services/openclaw_client.py`
- **Task Workflow:** `control-panel/backend/app/services/task_workflow.py`

