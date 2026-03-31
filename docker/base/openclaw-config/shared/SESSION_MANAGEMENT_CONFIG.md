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

# Session Management Configuration

## Purpose

Define lifecycle, retention, and cleanup policies for agent sessions. Sessions can grow indefinitely without management; this document prevents bloat while preserving important history.

## Session Lifecycle

```
CREATE         →  ACTIVE         →  IDLE           →  PRUNE         →  ARCHIVE
New session       Processing        No activity       Remove old      Long-term
                  messages          for N days        messages        reference
```

## Configuration Schema

```yaml
session:
  # Session storage backend
  # "file" = local filesystem (/data/openclaw/sessions)
  # "postgres" = PostgreSQL (if available)
  backend: "file"

  # Session ID format
  # "user:<user-id>" or "hook:<webhook-id>"
  # Pattern: alphanumeric + colon, no spaces
  idPattern: "^(user|hook):[a-zA-Z0-9_-]+$"

  # Session timeout (no activity)
  # If no messages for this duration, session moves to IDLE
  inactivityTimeout: "7d"

  # Metadata retention
  # Store: agent state, user preferences, workspace info
  metadata:
    enabled: true
    retentionDays: 90

  # Message retention policy
  retention:
    # Keep full messages for recent period
    keepFullMessages:
      duration: "30d"
      # After 30 days, summarize old messages

    # Total messages to keep per session
    # Prevents unbounded growth
    maxMessages: 5000

    # Full history backup location
    # Compress and archive older messages here
    backupLocation: "/data/openclaw/session-backups"

  # Pruning strategy
  pruning:
    # Enable automatic pruning
    enabled: true

    # Run pruning daily at this time (UTC)
    schedule: "02:00"

    # Delete messages older than this
    deleteOlderThan: "90d"

    # Keep last N messages regardless of age
    keepLastMessages: 100

    # Compress old messages instead of delete
    # Creates summary before removal
    compressInstead: true

    # Token-based cleanup
    # If session exceeds this many tokens, prune from oldest
    maxSessionTokens: 500000

  # Compaction strategy
  compaction:
    # Run compaction before each pruning cycle
    enabled: true

    # Compress messages older than this
    compactOlderThan: "30d"

    # Create weekly digests
    weeklyDigests:
      enabled: true
      dayOfWeek: "Monday"      # ISO 8601: Monday=1
      keepLastN: 12            # Keep last 12 weeks

    # Compression algorithm
    algorithm: "summary"        # "summary" | "extract" | "semantic"

  # Session locking
  # Prevent concurrent writes
  locking:
    enabled: true
    lockTimeout: "30s"
    maxRetries: 3

  # Archival
  # Move old sessions to cold storage
  archival:
    enabled: true
    archiveAfter: "180d"       # Move to archive after 6 months
    archiveLocation: "/data/openclaw/session-archive"
    compressFormat: "gzip"
```

## Per-Agent Session Policies

Different agents may have different session patterns:

```yaml
agents:
  # CEO (long-running, orchestration)
  ceo:
    session:
      inactivityTimeout: "30d"     # Keep alive longer
      retention:
        keepFullMessages:
          duration: "60d"          # Longer history
        maxMessages: 10000
      pruning:
        enabled: true
        deleteOlderThan: "180d"    # Prune less aggressively
        keepLastMessages: 500
      archival:
        archiveAfter: "365d"       # Archive after 1 year

  # Dev Backend (high-volume, task-focused)
  dev_backend:
    session:
      inactivityTimeout: "14d"
      retention:
        keepFullMessages:
          duration: "14d"          # Shorter history
        maxMessages: 2000
      pruning:
        enabled: true
        deleteOlderThan: "30d"     # Prune more aggressively
        keepLastMessages: 50
      archival:
        archiveAfter: "90d"

  # Memory Curator (consolidation)
  memory_curator:
    session:
      inactivityTimeout: "7d"
      retention:
        keepFullMessages:
          duration: "90d"          # Longer for analysis
        maxMessages: 50000
      pruning:
        compressInstead: true      # Always compress, never delete
        deleteOlderThan: "180d"
      archival:
        enabled: false             # Never archive
```

## Compaction Strategies

### Strategy 1: Weekly Digest

```
Week 1: Daily detailed entries
Week 2: Daily detailed entries
...
Week 5: Summary of weeks 1-4 + week 5 detailed
...
Month 2: Summary of month 1 + month 2 summary
```

### Strategy 2: Exponential Decay

```
Day 1-7:    Keep all details
Day 8-30:   Keep 1 entry per 3 days
Day 31-90:  Keep 1 entry per week
Day 91+:    Keep 1 entry per month
```

### Strategy 3: Semantic Clustering

```
1. Extract semantic meaning from each message
2. Group similar messages into clusters
3. Keep 1 representative per cluster
4. Discard duplicative content
5. Reduce storage by 60-80%
```

## Monitoring

```bash
# Show session statistics
openclaw session stats --agent ceo

# Show sessions scheduled for pruning
openclaw session prune-schedule

# Show session size
openclaw session size --session user:12345

# Export session before archival
openclaw session export --session user:12345 --output /tmp/session.json

# Restore from archive
openclaw session restore --session user:12345 --from-archive
```

## Best Practices

1. **Prune regularly**: Run pruning daily (off-peak hours)
2. **Compress before delete**: Preserve knowledge in compressed form
3. **Keep recent messages**: Always keep last 100 messages uncompressed
4. **Archive strategically**: Move old sessions to cold storage after 6 months
5. **Monitor growth**: Alert if session token count > 400k
6. **Test restoration**: Verify archived sessions can be restored
7. **Backup before prune**: Ensure backups exist before deletion

## Failure Recovery

If session corruption is detected:

```bash
# Restore from backup
openclaw session restore --session user:12345 --from-backup

# Roll back to specific date
openclaw session rollback --session user:12345 --to-date 2026-03-25

# Verify session integrity
openclaw session verify --session user:12345
```

## Storage Implications

```
Typical session growth:
- Day 1-30:    ~5-10 MB (raw)
- Day 1-90:    ~15-30 MB (raw)
- Day 1-180:   ~40-80 MB (raw)

After compaction:
- Day 1-90:    ~3-5 MB (compressed)
- Day 1-180:   ~8-15 MB (compressed)

Archival (gzip):
- 1 year of data: ~2-5 MB per user
- 10k users: ~20-50 GB total
```

## Examples

### Example 1: Aggressive Pruning (Dev Agents)

```yaml
session:
  inactivityTimeout: "7d"
  pruning:
    enabled: true
    deleteOlderThan: "14d"       # Prune fast
    keepLastMessages: 30
    compressInstead: false       # Delete, don't compress
  archival:
    archiveAfter: "60d"          # Archive fast
```

### Example 2: Conservative Pruning (CEO)

```yaml
session:
  inactivityTimeout: "30d"
  pruning:
    enabled: true
    deleteOlderThan: "180d"      # Prune slow
    keepLastMessages: 500
    compressInstead: true        # Always compress
    weeklyDigests:
      enabled: true
  archival:
    archiveAfter: "365d"         # Archive very slow
```

