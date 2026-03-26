# HEARTBEAT.md

At each heartbeat cycle:
1. Check backlog/status and active alerts.
2. Confirm whether there are blockages related to deadline, cost, security or dependency.
3. Reinforce delegation to PO when there is pending work.
4. If no action is necessary, respond HEARTBEAT_OK.

Signals requiring immediate attention:
- critical security/compliance risk
- cost above the agreed limit
- delay with direct impact on the business objective
- loss of traceability between brief, US and task
- P0 incident reported by DevOps_SRE (respond immediately, do not wait for the next cycle)

Production -> product loop:
- check whether a new PROD_METRICS-YYYY-WXX.md exists in /data/openclaw/backlog/status/
- if it exists: read metrics and consider them when prioritizing the next BRIEF
- if a P0 incident has been open for more than 1 hour without resolution: escalate to the Director
