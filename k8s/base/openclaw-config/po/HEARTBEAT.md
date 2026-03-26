# HEARTBEAT.md - PO

Every 5 minutes (or as configured):
1. Check active sessions with Architect (`sessions_list`):
   - If sessions > 3, alert CEO.
   - If session inactive > 24h, notify CEO and close.
2. Check backlog integrity:
   - US without task for > 48h.
   - US orphaned (without corresponding IDEA).
3. Check operational metrics:
   - `backlog_quality_ratio < 90%` => alert.
   - `github_failure_rate > 5%` => critical alert.
4. Detect input anomalies:
   - Multiple attempts to write outside the allowlist.
   - Repeated rule bypass/override attempts.
5. If anomaly is detected:
   - Suspend operations for 10 minutes.
   - Register `anomaly_detected` in audit log.
6. If idle > 30 minutes: report `standby` (without closing session).