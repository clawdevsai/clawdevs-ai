---
name: memory_curator_promotion
description: Memory curation skill for promoting cross-agent standards and memory health reporting
---

# SKILL.md - Memory_Curator

## Skill: promote_cross_agent_patterns

**Trigger**: Daily Cron at 2am or explicit call by Architect

**Steps**:
1. Read all `/data/openclaw/memory/<id>/MEMORY.md` from active agents
2. Extract `## Active Patterns` section from each file
3. Use LLM to group semantically similar patterns between agents
4. For groups with ≥3 different agents: promote to SHARED_MEMORY.md
5. Update MEMORY.md of source agents (move to Archived)
6. Log result at `/data/openclaw/backlog/status/memory-curator.log`

**Expected input format in MEMORY.md**:
```
- [PATTERN] <descrição> | Descoberto: YYYY-MM-DD | Fonte: <task-id>
```

**Output format in SHARED_MEMORY.md**:
```
- [GLOBAL] <descrição consolidada> | Promovido: YYYY-MM-DD | Origem: <agente1>, <agente2>, <agente3>
```

**Archiving format in agents' MEMORY.md**:
```
- [ARCHIVED] <descrição original> | Arquivado: YYYY-MM-DD | Motivo: Promovido para SHARED_MEMORY
```

## Skill: report_memory_health

**Trigger**: At the end of each promotion cycle

**Output**: Log structured in `/data/openclaw/backlog/status/memory-curator.log` with:
- Timestamp ISO8601
- Agents processed
- Total patterns collected
- Promoted patterns (N new + N updated)
- Archived patterns
- Errors
