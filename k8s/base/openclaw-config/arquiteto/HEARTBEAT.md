# HEARTBEAT.md - Architect

Every 5 minutes (or as configured):
1. Active sessions (`sessions_list`):
   - If sessions with PO > 2: alert PO.
   - If session inactive > 1h: close automatically.
2. Pending tasks:
   - Tasks without NFR or Security/Observability: escalate to PO.
   - ADR pending approval > 48h: notify PO.
3. Research monitor:
   - If timer > 2h: abort research, apply `Default/Proven`, log in `research_timeout`.
   - If `web-search` > 30 queries/hour: apply throttle.
4. GitHub health:
   - If failures > 5% in last 10 operations: alert PO and use per-file fallback.
5. Docs/task pipeline:
   - If there is a new CEO/PO/Architect document without commit in `implementation/docs`: alert PO.
   - If panel task created without prior commit of docs: mark non-conforming and escalate PO.
   - If session ended without folder `session_finished/<session_id>`: mark non-compliant and correct.
6. File anomalies:
   - Reading/writing outside `/data/openclaw/backlog`: block, log in, notify PO.
7. Dev-QA cycle monitoring:
   - Tasks from the panel with label `tests` and status `inbox` > 2h without change: notify QA_Engineer.
   - Tasks from the panel with label `devops` and status `inbox` > 1h without change: notify DevOps_SRE.
   - QA_Engineer reported 3 retries in some task: escalate to PO with history.
8. CI/CD pipeline monitoring:
   - Repeated CI/CD failures (> 3x in the same PR): delegate to DevOps_SRE.
9. If idle > 20 minutes: report `standby` (without closing session).