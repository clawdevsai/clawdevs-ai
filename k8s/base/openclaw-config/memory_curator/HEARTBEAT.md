# HEARTBEAT.md - Memory_Curator

Daily at 2am (cron: `0 2 * * *`, TZ: America/Sao_Paulo):

1. **Initialize** — Set `MEMORY_BASE=/data/openclaw/memory`; check that the directory exists
2. **Collect patterns** — For each agent in `ceo po arquiteto dev_backend dev_frontend dev_mobile qa_engineer security_engineer devops_sre ux_designer dba_data_engineer`:
   - Read `${MEMORY_BASE}/<id>/MEMORY.md`
   - Extract all lines from `## Active Patterns` (lines starting with `- [PATTERN]`)
   - Store list of patterns with origin (agent_id)
3. **Identify cross patterns** — Group semantically similar patterns between agents:
   - Use LLM to compare descriptions and identify equivalences
   - Patterns with 3+ distinct origins → promotion candidates
4. **Promote to SHARED_MEMORY.md** — For each candidate pattern:
   - Check if it already exists in `${MEMORY_BASE}/shared/SHARED_MEMORY.md`
   - If it doesn't exist: add `- [GLOBAL] <descrição consolidada> | Promovido: <data> | Origem: <agentes>`
   - If it already exists: update field `Origem` with new agents if necessary
5. **Archive to source agents** — For each promoted pattern:
   - In each source agent MEMORY.md: move line from `## Active Patterns` → `## Archived`
   - Add suffix `| Arquivado: <data> | Motivo: Promovido para SHARED_MEMORY`
6. **Generate report** — Write to `/data/openclaw/backlog/status/memory-curator.log`:
   - Cycle timestamp
   - Agents processed (N)
   - Patterns collected (total)
   - Standards promoted in the cycle (N new)
   - Patterns filed with agents (N)
   - Errors found (0 expected)