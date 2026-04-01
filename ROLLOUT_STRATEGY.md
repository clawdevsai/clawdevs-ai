# Week 5: Semantic Optimization Incremental Rollout

## Strategy: One Task Per Week

Ativa uma tarefa por semana, monitora métricas, valida em canary antes de rollout global.

## Week-by-Week Schedule

### Week 1: Query Enhancement
```bash
# Day 1: Canary (dev_backend, memory_curator)
PANEL_SEMANTIC_OPT_CANARY_AGENTS=dev_backend,memory_curator
PANEL_SEMANTIC_OPT_QUERY_ENHANCEMENT=false

# Day 4: Monitor metrics, check errors
GET /api/context-mode/semantic-optimization/metrics

# Day 7: Global rollout
PANEL_SEMANTIC_OPT_QUERY_ENHANCEMENT=true
PANEL_SEMANTIC_OPT_CANARY_AGENTS=
```

### Week 2: Semantic Reranking
```bash
PANEL_SEMANTIC_OPT_SEMANTIC_RERANKING=true
```

### Week 3: Adaptive Compression
```bash
PANEL_SEMANTIC_OPT_ADAPTIVE_COMPRESSION=true
```

### Week 4: Intelligent Summarization
```bash
PANEL_SEMANTIC_OPT_SUMMARIZATION=true
```

### Week 5: Auto-Categorization
```bash
PANEL_SEMANTIC_OPT_CATEGORIZATION=true
```

### Week 6: Anomaly Detection
```bash
PANEL_SEMANTIC_OPT_ANOMALY_DETECTION=true
```

### Week 7: Context Suggestion
```bash
PANEL_SEMANTIC_OPT_CONTEXT_SUGGESTION=true
```

## Validation Checklist

For each task activation:

- [ ] Feature flag enabled in canary agents
- [ ] Monitor `GET /feature-flags/task_name?agent_id=dev_backend` → `enabled: true`
- [ ] Run integration tests: `pytest tests/test_api/test_context_mode_semantic_optimization.py::TestContextModeSemanticOptimizationAPI::test_<task>_endpoint`
- [ ] Check Ollama health: `GET /api/context-mode/semantic-optimization/ollama-health` → `online: true`
- [ ] Verify metrics: `GET /api/context-mode/semantic-optimization/metrics`
- [ ] Check logs for errors (if any agent uses the task)
- [ ] Day 4: Expand to additional agents if stable
- [ ] Day 7: Global rollout (set flag to true, remove from canary)

## Rollback Plan

If task causes errors during canary or rollout:

```bash
# Disable the task immediately
PANEL_SEMANTIC_OPT_<TASK>=false

# Revert to stable canary
PANEL_SEMANTIC_OPT_CANARY_AGENTS=dev_backend,memory_curator

# Investigate logs
make logs | grep -i "enhance-query|rerank|compress|summarize|categorize|anomaly|context"
```

## Success Metrics

- ✅ No HTTP 500 errors from semantic optimization endpoints
- ✅ Ollama stays healthy (latency < 3s)
- ✅ No agent execution delays (agent.task_end - agent.task_start < +500ms baseline)
- ✅ Memory usage stable
- ✅ User acceptance rate > 70% (for context suggestions)

## Deployment

Each week's rollout:

```bash
# Update .env
PANEL_SEMANTIC_OPT_<TASK>=true
PANEL_SEMANTIC_OPT_CANARY_AGENTS=

# Commit
git add .env && git commit -m "rollout: Week N activate <task>"

# Deploy
make deploy
```

After all 7 weeks: All tasks enabled globally ✅
