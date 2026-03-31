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

# Cron Jobs Registry

## Purpose

Define all scheduled/automated tasks that agents execute. Each cron job has a purpose, schedule, timeout, and failure handling policy.

## Global Cron Jobs

### Memory Curation

```yaml
cron_jobs:
  - id: "memory-curator-daily"
    agent: "memory_curator"
    schedule: "0 3 * * *"          # Every day at 03:00 UTC
    timezone: "UTC"
    timeout_seconds: 3600           # 1 hour timeout
    task: "daily_consolidation"
    description: |
      Review all agent memories from past 24h.
      Identify patterns (same issue in 3+ agents).
      Create org-level memory for patterns.
      Update Memory Curator session.
    on_success: "log_metrics"
    on_failure: "retry_once"
    retry_delay_seconds: 300        # 5 min between retries
    alert_on_failure: true
    sla_minutes: 120                # Must complete within 2 hours

  - id: "memory-compaction-weekly"
    agent: "memory_curator"
    schedule: "0 0 * * 1"           # Every Monday at 00:00 UTC
    timeout_seconds: 7200           # 2 hours timeout
    task: "weekly_compaction"
    description: |
      Compact memories > 7 days old.
      Merge similar memories.
      Extract high-value insights.
      Archive low-value entries.
      Report compaction metrics.
    on_success: "log_metrics"
    on_failure: "escalate_to_ceo"
    sla_minutes: 180                # Must complete within 3 hours
```

### Session Management

```yaml
  - id: "session-pruning-daily"
    agent: "devops_sre"
    schedule: "0 2 * * *"           # Every day at 02:00 UTC
    timeout_seconds: 3600
    task: "prune_sessions"
    description: |
      Remove messages older than 90 days.
      Keep last 100 messages per session.
      Compress old messages before deletion.
      Report pruned sessions count.
    on_success: "log_metrics"
    on_failure: "retry_once"
    alert_on_failure: true
    sla_minutes: 120
```

### Deployment & CI/CD

```yaml
  - id: "github-queue-poll-dev-backend"
    agent: "dev_backend"
    schedule: "0 * * * *"           # Every hour at :00
    timeout_seconds: 1800           # 30 min
    task: "poll_github_queue"
    description: |
      Poll GitHub issue queue for dev_backend label.
      Pick next TASK-* or US-* item.
      Start implementation immediately.
    on_success: "update_status"
    on_failure: "escalate_to_po"
    sla_minutes: 120

  - id: "github-queue-poll-dev-frontend"
    agent: "dev_frontend"
    schedule: "15 * * * *"          # Every hour at :15
    timeout_seconds: 1800
    task: "poll_github_queue"
    description: |
      Poll GitHub issue queue for dev_frontend label.
      Pick next TASK-* or US-* item.
      Start implementation immediately.
    on_success: "update_status"
    on_failure: "escalate_to_po"
    sla_minutes: 120

  - id: "github-queue-poll-qa"
    agent: "qa_engineer"
    schedule: "45 * * * *"          # Every hour at :45
    timeout_seconds: 1800
    task: "poll_github_queue"
    description: |
      Poll GitHub issue queue for qa_engineer label.
      Run test suite for marked PRs.
      Report pass/fail results.
    on_success: "update_pr_status"
    on_failure: "escalate_to_devops"
    sla_minutes: 120

  - id: "devops-deployment-check"
    agent: "devops_sre"
    schedule: "*/30 * * * *"        # Every 30 minutes
    timeout_seconds: 600
    task: "check_deployment_status"
    description: |
      Check if any PRs are waiting for deployment.
      Run integration tests if needed.
      Deploy to staging/prod if tests pass.
    on_success: "log_status"
    on_failure: "alert_on_call"
    sla_minutes: 45

  - id: "security-audit-daily"
    agent: "security_engineer"
    schedule: "0 6 * * *"           # Every day at 06:00 UTC
    timeout_seconds: 3600
    task: "daily_security_audit"
    description: |
      Run daily security audit of codebase.
      Check for hardcoded secrets.
      Verify dependencies for vulnerabilities.
      Report findings.
    on_success: "log_report"
    on_failure: "escalate_to_ceo"
    sla_minutes: 120
```

### Data Management

```yaml
  - id: "dba-database-health"
    agent: "dba_data_engineer"
    schedule: "0 * * * *"           # Every hour at :00
    timeout_seconds: 300
    task: "check_database_health"
    description: |
      Check database connections, performance.
      Monitor query performance.
      Check disk space, backups.
      Alert if any issues.
    on_success: "log_metrics"
    on_failure: "page_oncall"
    sla_minutes: 10

  - id: "dba-backup-daily"
    agent: "dba_data_engineer"
    schedule: "0 4 * * *"           # Every day at 04:00 UTC
    timeout_seconds: 1800
    task: "backup_database"
    description: |
      Create daily backup of database.
      Verify backup integrity.
      Store in backup location.
      Report backup status.
    on_success: "log_backup"
    on_failure: "alert_critical"
    sla_minutes: 60
```

### Observability & Monitoring

```yaml
  - id: "ceo-daily-briefing"
    agent: "ceo"
    schedule: "0 9 * * 1-5"         # Weekdays at 09:00 UTC
    timeout_seconds: 1800
    task: "daily_briefing"
    description: |
      Poll all sub-agents for status.
      Consolidate blockers and progress.
      Update backlog priorities.
      Notify director of critical issues.
      Delegate urgent work immediately.
    on_success: "send_briefing"
    on_failure: "retry_once"
    alert_on_failure: true
    sla_minutes: 30

  - id: "ceo-weekly-review"
    agent: "ceo"
    schedule: "0 10 * * 1"          # Every Monday at 10:00 UTC
    timeout_seconds: 3600
    task: "weekly_review"
    description: |
      Review week's deliverables.
      Check velocity, quality metrics.
      Update project status.
      Plan next week's priorities.
    on_success: "send_report"
    on_failure: "manual_review"
    sla_minutes: 60
```

## Per-Agent Cron Schedule

Based on `.env` configuration:

```yaml
agent_schedules:
  dev_backend:
    cron_enabled: true
    cron_expr: "0 * * * *"         # Every hour
    description: "Poll GitHub queue, pick tasks, implement"

  dev_frontend:
    cron_enabled: true
    cron_expr: "15 * * * *"        # Every hour at :15
    description: "Poll GitHub queue, pick tasks, implement"

  dev_mobile:
    cron_enabled: true
    cron_expr: "30 * * * *"        # Every hour at :30
    description: "Poll GitHub queue, pick tasks, implement"

  qa_engineer:
    cron_enabled: true
    cron_expr: "45 * * * *"        # Every hour at :45
    description: "Poll GitHub queue, run tests, report results"

  devops_sre:
    cron_enabled: true
    cron_expr: "*/30 * * * *"      # Every 30 minutes
    description: "Check deployment status, run tests, deploy"

  security_engineer:
    cron_enabled: true
    cron_expr: "0 */6 * * *"       # Every 6 hours
    description: "Run security audit, check dependencies"

  ux_designer:
    cron_enabled: true
    cron_expr: "0 */4 * * *"       # Every 4 hours
    description: "Check design feedback, update designs"

  dba_data_engineer:
    cron_enabled: true
    cron_expr: "30 */4 * * *"      # Every 4 hours at :30
    description: "Check database health, backups, performance"

  memory_curator:
    cron_enabled: true
    cron_expr: "0 2 * * *"         # Every day at 02:00 UTC
    description: "Consolidate memories, compact, archive"
```

## Cron Execution Flow

```
┌────────────────┐
│  Cron Trigger  │  (OpenClaw scheduler)
└────────┬───────┘
         │
         ↓
┌────────────────────────┐
│  Start Agent Session   │  (create or resume)
└────────┬───────────────┘
         │
         ↓
┌────────────────────────┐
│  Execute Task          │  (with timeout)
└────────┬───────────────┘
         │
         ├─→ SUCCESS ──→ Log metrics ──→ Update status
         │
         ├─→ TIMEOUT ──→ Kill task ──→ Retry (if policy allows)
         │
         ├─→ FAILURE ──→ Log error ──→ Escalate (if critical)
         │
         └─→ ERROR ───→ Log stacktrace ──→ Alert

         ↓
┌────────────────────────┐
│  Update Session        │  (persist state)
└────────┬───────────────┘
         │
         ↓
┌────────────────────────┐
│  Fire Hook: cron.done  │  (notify observers)
└────────────────────────┘
```

## Monitoring Cron Jobs

```bash
# Show all cron jobs and next run time
openclaw cron list

# Show cron job execution history
openclaw cron history --job github-queue-poll-dev-backend --days 7

# Show cron job execution metrics
openclaw cron metrics --period 24h

# Show failed cron jobs
openclaw cron failures --period 24h

# Manually trigger cron job
openclaw cron trigger --job memory-curator-daily

# View cron logs
openclaw cron logs --job memory-curator-daily --tail 50
```

## Best Practices

1. **Avoid conflicts**: Stagger cron times to prevent thundering herd
2. **Set timeouts**: Every cron job must have explicit timeout
3. **Define SLA**: Know how long each job should take
4. **Monitor failures**: Alert if job fails 2x in a row
5. **Test schedules**: Verify timing before deploying
6. **Log everything**: Full audit trail of executions
7. **Graceful degradation**: If job fails, don't break other jobs

## Troubleshooting

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Cron not running | Agent offline or disabled | Check agent status with `openclaw agent status` |
| Cron timing off | Timezone mismatch | Verify `timezone` setting matches expected |
| Cron timeout | Task takes too long | Increase `timeout_seconds` or optimize task |
| Cron too frequent | Thundering herd | Stagger start times across agents |
| Missing cron metrics | Logging disabled | Enable `log_hooks: true` in config |

