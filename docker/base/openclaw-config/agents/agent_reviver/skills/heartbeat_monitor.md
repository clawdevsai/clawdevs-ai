# Skill: heartbeat_monitor

## Purpose
Monitor agent heartbeat freshness, detect offline or stalled agents, verify container health status, and identify cron job failures. This skill applies detection rules to agent metrics and generates activity events, memory patterns, and escalations to the CEO for critical health issues.

## Input Parameters

### Required Inputs
- `agent_id`: Unique identifier for the monitored agent (string)
- `agent_name`: Human-readable agent name (string)
- `heartbeat_age_minutes`: Time elapsed since last activity in minutes (number)
- `status`: Current agent status (string: "online", "offline", "idle", "stalled")
- `runtime_status`: Agent runtime state (string: "active", "paused", "error", "starting")

### Optional Inputs
- `container_health`: Container health status object
  - `container_id`: Docker container ID (string)
  - `container_status`: Container state (string: "running", "stopped", "error", "exited")
  - `health_status`: Health check result (string: "healthy", "unhealthy", "unknown")
  - `restart_count`: Number of recent restarts (integer)
  - `last_restart_timestamp`: ISO timestamp of last restart (string)

- `cron_metrics`: Scheduled task failure tracking
  - `total_cron_jobs`: Total number of scheduled tasks (integer)
  - `failed_jobs`: Array of failed job information
    - `job_id`: Job identifier (string)
    - `failure_count`: Consecutive failures (integer)
    - `last_failure_timestamp`: ISO timestamp (string)
    - `error_message`: Failure description (string)

- `context`: Analysis context from agent memory
  - `previous_alerts`: Recent alerts for deduplication (array)
  - `baseline_freshness_minutes`: Historical baseline for heartbeat age (number)
  - `escalation_history`: Recent escalations to avoid spam (array)
  - `agent_type`: Agent functional category (string)

## Output Structure

```json
{
  "analysis_timestamp": "ISO 8601 timestamp",
  "agent_id": "agent identifier",
  "agent_name": "agent name",
  "summary": {
    "health_status": "healthy|warning|critical",
    "issues_detected": 0,
    "escalations_required": 0,
    "alert_summary": "Brief health status description"
  },
  "activity_events": [
    {
      "event_id": "unique identifier",
      "timestamp": "ISO 8601",
      "agent_id": "agent identifier",
      "category": "heartbeat|status|container|cron",
      "severity": "info|warning|critical",
      "title": "Event title",
      "description": "Detailed description",
      "metric_name": "Specific metric (e.g., heartbeat_age_minutes)",
      "metric_value": "Current value",
      "threshold_value": "Threshold that triggered rule",
      "rule_name": "Matching detection rule ID"
    }
  ],
  "memory_updates": [
    {
      "memory_key": "Key path in agent memory",
      "value": "Value to store",
      "timestamp": "ISO 8601",
      "ttl_seconds": "Cache duration (300 for 5 min, null for permanent)"
    }
  ],
  "escalations": [
    {
      "escalation_id": "Unique identifier",
      "timestamp": "ISO 8601",
      "severity": "critical|high",
      "target": "ceo",
      "title": "Escalation title",
      "description": "Issue description with context",
      "affected_agent": "agent name",
      "affected_component": "heartbeat|status|container|cron",
      "current_value": "Current metric value",
      "threshold_value": "Threshold value",
      "recommended_actions": [
        "Action 1",
        "Action 2"
      ]
    }
  ]
}
```

## Detection Rules

```yaml
rules:
  - name: "agent_heartbeat_timeout"
    condition: "heartbeat_age_minutes > 30"
    severity: "critical"
    category: "heartbeat"
    description: "Agent heartbeat not received for more than 30 minutes"
    action: "log_event + escalate_to_ceo"
    escalation_target: "ceo"
    recommended_actions:
      - "Investigate agent availability and connectivity"
      - "Check agent logs for errors or crashes"
      - "Verify network connectivity to agent"
      - "Consider manual restart if needed"

  - name: "agent_offline_extended"
    condition: "status == 'offline' AND status_duration_minutes > 5"
    severity: "critical"
    category: "status"
    description: "Agent has been offline for more than 5 minutes"
    action: "log_event + escalate_to_ceo"
    escalation_target: "ceo"
    recommended_actions:
      - "Check agent process status"
      - "Verify container is running"
      - "Review agent error logs"
      - "Determine if manual intervention needed"

  - name: "container_unhealthy"
    condition: "container_health.health_status == 'unhealthy' OR container_status == 'error'"
    severity: "critical"
    category: "container"
    description: "Docker container health check failed or container in error state"
    action: "log_event + escalate_to_ceo"
    escalation_target: "ceo"
    recommended_actions:
      - "Review container logs for errors"
      - "Check container resource utilization"
      - "Verify container configuration"
      - "Consider container restart"

  - name: "cron_repeated_failures"
    condition: "failure_count >= 3"
    severity: "warning"
    category: "cron"
    description: "Cron job has failed 3 or more consecutive times"
    action: "log_event + escalate_to_ceo"
    escalation_target: "ceo"
    recommended_actions:
      - "Review cron job error messages"
      - "Check job scheduling configuration"
      - "Verify external dependencies (APIs, databases)"
      - "Consider disabling job until fixed"

  - name: "heartbeat_aging"
    condition: "heartbeat_age_minutes > 15 AND heartbeat_age_minutes <= 30"
    severity: "warning"
    category: "heartbeat"
    description: "Agent heartbeat aging but not yet critical"
    action: "log_event + update_memory"
    escalation_target: null
    recommended_actions:
      - "Monitor next heartbeat update"
      - "Check agent activity logs"

  - name: "agent_stalled"
    condition: "status == 'offline' AND heartbeat_age_minutes > 10"
    severity: "warning"
    category: "status"
    description: "Agent appears stalled with old heartbeat"
    action: "log_event + update_memory"
    escalation_target: null
    recommended_actions:
      - "Monitor for heartbeat recovery"
      - "Check agent network connectivity"

  - name: "runtime_error_state"
    condition: "runtime_status == 'error'"
    severity: "critical"
    category: "status"
    description: "Agent runtime in error state"
    action: "log_event + escalate_to_ceo"
    escalation_target: "ceo"
    recommended_actions:
      - "Check agent initialization logs"
      - "Verify agent configuration is valid"
      - "Review environment variables"
      - "Consider agent restart"

  - name: "container_restart_pattern"
    condition: "restart_count > 3 AND restart_count < 10"
    severity: "warning"
    category: "container"
    description: "Container showing restart pattern indicating instability"
    action: "log_event + update_memory"
    escalation_target: null
    recommended_actions:
      - "Review container logs for failure patterns"
      - "Check for resource constraints"

  - name: "container_restart_critical"
    condition: "restart_count >= 10"
    severity: "critical"
    category: "container"
    description: "Container restarting excessively (10+ restarts)"
    action: "log_event + escalate_to_ceo"
    escalation_target: "ceo"
    recommended_actions:
      - "Investigate root cause of repeated failures"
      - "Review container configuration"
      - "Check system resource availability"

  - name: "agent_healthy"
    condition: "heartbeat_age_minutes <= 5 AND status == 'online' AND runtime_status == 'active'"
    severity: "info"
    category: "heartbeat"
    description: "Agent healthy with fresh heartbeat and active status"
    action: "log_event + update_memory"
    escalation_target: null
    recommended_actions: []

  - name: "agent_idle"
    condition: "status == 'idle' AND heartbeat_age_minutes > 30"
    severity: "warning"
    category: "status"
    description: "Agent idle with no activity for extended period"
    action: "log_event + update_memory"
    escalation_target: null
    recommended_actions:
      - "Monitor for activity resumption"
      - "Verify agent hasn't become stuck"

  - name: "single_cron_failure"
    condition: "failure_count == 1"
    severity: "info"
    category: "cron"
    description: "Cron job experienced a single failure"
    action: "log_event + update_memory"
    escalation_target: null
    recommended_actions:
      - "Monitor next execution"
      - "Review error details"
```

## Examples

### Example 1: Heartbeat Timeout (Critical)

**Input:**
```json
{
  "agent_id": "dev_backend_001",
  "agent_name": "dev_backend",
  "heartbeat_age_minutes": 35,
  "status": "offline",
  "runtime_status": "error",
  "context": {
    "baseline_freshness_minutes": 2,
    "escalation_history": []
  }
}
```

**Output (Critical Escalation):**
```json
{
  "analysis_timestamp": "2026-03-30T15:45:00Z",
  "agent_id": "dev_backend_001",
  "agent_name": "dev_backend",
  "summary": {
    "health_status": "critical",
    "issues_detected": 2,
    "escalations_required": 2,
    "alert_summary": "Agent offline with heartbeat timeout (35 min) and runtime error"
  },
  "activity_events": [
    {
      "event_id": "evt_20260330_154500_001",
      "timestamp": "2026-03-30T15:45:00Z",
      "agent_id": "dev_backend_001",
      "category": "heartbeat",
      "severity": "critical",
      "title": "Agent Heartbeat Timeout",
      "description": "Agent dev_backend has not sent heartbeat for 35 minutes, exceeding 30-minute critical threshold",
      "metric_name": "heartbeat_age_minutes",
      "metric_value": 35,
      "threshold_value": 30,
      "rule_name": "agent_heartbeat_timeout"
    },
    {
      "event_id": "evt_20260330_154500_002",
      "timestamp": "2026-03-30T15:45:00Z",
      "agent_id": "dev_backend_001",
      "category": "status",
      "severity": "critical",
      "title": "Agent Runtime Error",
      "description": "Agent runtime_status is 'error', indicating a fatal initialization or execution failure",
      "metric_name": "runtime_status",
      "metric_value": "error",
      "threshold_value": "not error",
      "rule_name": "runtime_error_state"
    }
  ],
  "memory_updates": [
    {
      "memory_key": "agents:dev_backend_001:last_critical_alert",
      "value": "2026-03-30T15:45:00Z",
      "timestamp": "2026-03-30T15:45:00Z",
      "ttl_seconds": null
    },
    {
      "memory_key": "agents:dev_backend_001:heartbeat_age_trend",
      "value": [2, 5, 12, 25, 35],
      "timestamp": "2026-03-30T15:45:00Z",
      "ttl_seconds": 3600
    }
  ],
  "escalations": [
    {
      "escalation_id": "esc_20260330_154500_001",
      "timestamp": "2026-03-30T15:45:00Z",
      "severity": "critical",
      "target": "ceo",
      "title": "CRITICAL: Agent dev_backend Heartbeat Timeout",
      "description": "Agent dev_backend (dev_backend_001) has not sent a heartbeat for 35 minutes and is in offline status with runtime error. Immediate investigation required to determine if agent process is crashed or unresponsive.",
      "affected_agent": "dev_backend",
      "affected_component": "heartbeat",
      "current_value": "35 minutes",
      "threshold_value": "30 minutes",
      "recommended_actions": [
        "Immediately check agent process status on host machine",
        "Review agent logs for crash messages or fatal errors",
        "Verify network connectivity between agent and control plane",
        "Check if container is still running (if containerized)",
        "Consider manual restart if logs show recoverable error"
      ]
    }
  ]
}
```

### Example 2: Cron Repeated Failures (Warning)

**Input:**
```json
{
  "agent_id": "qa_engineer_001",
  "agent_name": "qa_engineer",
  "heartbeat_age_minutes": 3,
  "status": "online",
  "runtime_status": "active",
  "cron_metrics": {
    "total_cron_jobs": 5,
    "failed_jobs": [
      {
        "job_id": "daily_regression_tests",
        "failure_count": 3,
        "last_failure_timestamp": "2026-03-30T14:30:00Z",
        "error_message": "Database connection timeout during test setup"
      }
    ]
  }
}
```

**Output (Warning Escalation):**
```json
{
  "analysis_timestamp": "2026-03-30T15:00:00Z",
  "agent_id": "qa_engineer_001",
  "agent_name": "qa_engineer",
  "summary": {
    "health_status": "warning",
    "issues_detected": 1,
    "escalations_required": 1,
    "alert_summary": "Agent healthy but cron job failing repeatedly"
  },
  "activity_events": [
    {
      "event_id": "evt_20260330_150000_001",
      "timestamp": "2026-03-30T15:00:00Z",
      "agent_id": "qa_engineer_001",
      "category": "cron",
      "severity": "warning",
      "title": "Cron Job Repeated Failures",
      "description": "Job 'daily_regression_tests' has failed 3 consecutive times. Last failure at 2026-03-30T14:30:00Z with error: Database connection timeout during test setup",
      "metric_name": "cron_failure_count",
      "metric_value": 3,
      "threshold_value": 3,
      "rule_name": "cron_repeated_failures"
    }
  ],
  "memory_updates": [
    {
      "memory_key": "agents:qa_engineer_001:cron:daily_regression_tests:failure_streak",
      "value": 3,
      "timestamp": "2026-03-30T15:00:00Z",
      "ttl_seconds": 86400
    },
    {
      "memory_key": "agents:qa_engineer_001:cron:daily_regression_tests:last_failures",
      "value": ["2026-03-30T12:00:00Z", "2026-03-30T13:00:00Z", "2026-03-30T14:30:00Z"],
      "timestamp": "2026-03-30T15:00:00Z",
      "ttl_seconds": 604800
    }
  ],
  "escalations": [
    {
      "escalation_id": "esc_20260330_150000_001",
      "timestamp": "2026-03-30T15:00:00Z",
      "severity": "critical",
      "target": "ceo",
      "title": "CRITICAL: Cron Job daily_regression_tests Failing (3 consecutive)",
      "description": "The 'daily_regression_tests' cron job has failed 3 consecutive times (last at 2026-03-30T14:30:00Z). Error indicates database connection timeout during test setup. This job is critical for QA validation and needs immediate attention.",
      "affected_agent": "qa_engineer",
      "affected_component": "cron",
      "current_value": "3 consecutive failures",
      "threshold_value": ">=3 failures",
      "recommended_actions": [
        "Verify database connectivity from agent host",
        "Check database service status and available connections",
        "Review test setup configuration for hardcoded timeouts",
        "Temporarily disable job if blocking other operations",
        "Increase connection pool or timeout thresholds if appropriate"
      ]
    }
  ]
}
```

### Example 3: Healthy Agent (Info)

**Input:**
```json
{
  "agent_id": "arquiteto_001",
  "agent_name": "arquiteto",
  "heartbeat_age_minutes": 2,
  "status": "online",
  "runtime_status": "active",
  "container_health": {
    "container_id": "abc123def456",
    "container_status": "running",
    "health_status": "healthy",
    "restart_count": 0
  }
}
```

**Output (Healthy Status):**
```json
{
  "analysis_timestamp": "2026-03-30T15:15:00Z",
  "agent_id": "arquiteto_001",
  "agent_name": "arquiteto",
  "summary": {
    "health_status": "healthy",
    "issues_detected": 0,
    "escalations_required": 0,
    "alert_summary": "Agent healthy with fresh heartbeat"
  },
  "activity_events": [
    {
      "event_id": "evt_20260330_151500_001",
      "timestamp": "2026-03-30T15:15:00Z",
      "agent_id": "arquiteto_001",
      "category": "heartbeat",
      "severity": "info",
      "title": "Agent Health Check Passed",
      "description": "Agent arquiteto is healthy with fresh heartbeat (2 minutes old), active runtime status, and container running normally",
      "metric_name": "heartbeat_age_minutes",
      "metric_value": 2,
      "threshold_value": 5,
      "rule_name": "agent_healthy"
    }
  ],
  "memory_updates": [
    {
      "memory_key": "agents:arquiteto_001:last_healthy_check",
      "value": "2026-03-30T15:15:00Z",
      "timestamp": "2026-03-30T15:15:00Z",
      "ttl_seconds": 300
    }
  ],
  "escalations": []
}
```

## Memory Storage Patterns

The skill maintains these memory patterns for trend analysis:

```
agents:<agent_id>:heartbeat_age_trend
  - Rolling array of last 10 heartbeat age readings
  - Used to detect trending degradation
  - TTL: 24 hours

agents:<agent_id>:status_history
  - Recent status transitions with timestamps
  - Pattern: {timestamp, from_status, to_status}
  - TTL: 7 days

agents:<agent_id>:cron:<job_id>:failure_streak
  - Current consecutive failure count
  - Reset on success
  - TTL: 24 hours

agents:<agent_id>:last_critical_alert
  - Timestamp of most recent critical alert
  - Used for deduplication
  - TTL: permanent

agents:<agent_id>:container_restart_history
  - Array of restart events with timestamps
  - Used to detect restart patterns
  - TTL: 30 days
```

## Integration Notes

- Executes on recurring schedule (recommended: every 5 minutes)
- Deduplicates alerts using memory escalation history
- Maintains trend data for anomaly detection
- Escalations reach CEO for immediate action on critical issues
- All metrics must include proper timestamps for SLA calculations
