# Phase 4: Memory + Cron Optimization
**Data:** 2026-04-01
**Status:** Planejamento
**Objetivo:** Adicional 5-10% de compressão em operações de memória e cron jobs

---

## 📋 Visão Geral

### Contexto
- Phase 3 validou que context-mode funciona em produção
- Sistema está pronto para otimizações mais avançadas
- Próximo alvo: memory curation e cron jobs (volumes altos de output)

### Escopo
| Componente | Impacto | Complexidade |
|-----------|---------|--------------|
| Memory Curation (ctx_index + ctx_search) | 5-8% | Média |
| Cron Job Compression | 3-5% | Baixa |
| Dashboard Memory Metrics | 1-2% | Baixa |
| **Total Esperado** | **9-15%** | - |

---

## 🎯 Work Breakdown Structure

### Task 1: Memory Indexing Strategy (Dia 1)
**Goal:** Implementar ctx_index + ctx_search para memory_curator

**Sub-tasks:**
- [ ] 1.1 Analisar padrão atual de leitura de memória
  - Arquivos: `/data/openclaw/memory/<agent>/MEMORY.md`
  - Operação: `grep` em todos os arquivos → 250KB+ output
  - Agents afetados: memory_curator, agent_reviver, ceo

- [ ] 1.2 Projetar índice de memória
  - Estrutura: BM25 FTS5 (Full Text Search)
  - Granularity: por agent + shared
  - Cache: 24h por índice

- [ ] 1.3 Criar memory_index service
  - Arquivo: `app/services/memory_indexing.py`
  - Método 1 - Direct index: `ctx_index(file_path)`
  - Método 2 - Search: `ctx_search(queries)`
  - Fallback: grep tradicional se índice falhar

- [ ] 1.4 Integrar no memory_curator skill
  - Atualizar SKILL.md
  - Exemplo: `ctx_search("database connection issues")` vs `grep -r`
  - Economia esperada: 90-95% em memory lookups

### Task 2: Cron Job Output Compression (Dia 1)
**Goal:** Comprimir outputs de jobs cron (cleanups, reports, etc)

**Sub-tasks:**
- [ ] 2.1 Identificar cron jobs de alto volume
  - Agents com cron: dba_data_engineer, devops_sre, memory_curator
  - Jobs: cleanups, reports, analytics
  - Tamanho médio: 50-500KB

- [ ] 2.2 Atualizar vercel.json crons config
  - Adicionar compressão handler
  - Timeout: 3000ms (mesmo do tool.executed hook)
  - Validar: POST /api/context-mode/metrics

- [ ] 2.3 Criar cron_optimization.md documentation
  - Padrões para cron scripts
  - Exemplo: `npm run cleanup --summary-only`
  - Economia esperada: 70-90% em cron outputs

### Task 3: Dashboard Memory Metrics (Dia 2)
**Goal:** Adicionar visibilidade de compressão em operações de memória

**Sub-tasks:**
- [ ] 3.1 Estender API metrics
  - Novo endpoint: `/api/context-mode/memory-metrics`
  - Campos: total_memory_ops, memory_bytes_saved, index_hits
  - Atualizar: `/api/context-mode/summary`

- [ ] 3.2 Criar visualização
  - Tab "Memory" no dashboard
  - Gráfico: Memory Operations over time
  - Top compressed patterns

- [ ] 3.3 Atualizar monitoring scripts
  - monitor-compression.sh: adicionar memory section
  - test-compression-integration.py: adicionar memory tests

### Task 4: Testing & Validation (Dia 2)
**Goal:** Validar que Phase 4 não quebrou Phase 1-3

**Sub-tasks:**
- [ ] 4.1 Testes unitários
  - memory_indexing.py tests
  - cron compression handler tests
  - Fallback behavior tests

- [ ] 4.2 Testes de integração
  - memory_curator executes → validates compression
  - cron jobs run → output compressed
  - Dashboard shows metrics

- [ ] 4.3 Regressão
  - Phase 1 APIs ainda funcionam? ✅
  - Phase 2 Skills ainda comprimem? ✅
  - Phase 3 metrics ainda coletam? ✅

---

## 📊 Estimativas

### Tempo
| Task | Estimativa | Parallelizável |
|------|-----------|-----------------|
| 1. Memory Indexing | 6-8h | Não |
| 2. Cron Optimization | 2-3h | Sim com Task 1 |
| 3. Dashboard | 3-4h | Sim com Task 1 |
| 4. Testing | 3-4h | Sim |
| **Total** | **14-19h** | - |
| **Sprint** | **2 dias** | - |

### Economia
| Componente | Baseline | Esperado | Economia |
|-----------|----------|----------|----------|
| Memory ops | 250KB avg | 15KB avg | 94% ↓ |
| Cron outputs | 200KB avg | 20KB avg | 90% ↓ |
| Overall tokens | 13K/h | 12K/h | 7.7% ↓ |
| **Mensal** | **$14** | **$13** | **~$12 adicional** |

---

## 🔧 Arquivos a Criar/Modificar

### Criar (Novos)
```
app/services/memory_indexing.py
docker/base/openclaw-config/shared/CRON_OPTIMIZATION.md
tests/unit/test_memory_indexing.py
tests/integration/test_cron_compression.py
```

### Modificar (Existentes)
```
app/api/context_mode.py          # Adicionar /memory-metrics
docker/base/openclaw-config/agents/memory_curator/skills/memory_curator_promotion/SKILL.md
vercel.json                       # Cron configuration
scripts/monitor-compression.sh    # Memory metrics section
```

---

## 🚀 Rollout Strategy

### Pre-Deploy
- [ ] Code review (1h)
- [ ] Integration tests pass (1h)
- [ ] Regression suite green (1h)

### Deploy
- [ ] Merge para main (0h - já em main)
- [ ] Docker rebuild (10m)
- [ ] Smoke tests (10m)
- [ ] Monitor Phase 3 metrics (não afetadas) (5m)

### Post-Deploy
- [ ] Aguardar memory_curator próximo ciclo
- [ ] Verificar memory-metrics endpoint
- [ ] Comparar economia vs baseline

---

## 📌 Decisões

### Decisão 1: Memory Index Technology
- **Escolha:** BM25 FTS5 (SQLite Full Text Search)
- **Razão:** Zero dependencies, built-in, rápido
- **Alternativa rejeitada:** Elasticsearch (overkill), Pinecone ($$)

### Decisão 2: Fallback Strategy
- **Escolha:** Se index falhar → grep tradicional (degrada gracefully)
- **Razão:** Não quebra sistema se index estiver corrupto
- **SLA:** 99.9% (1 falha em 1000 ops aceita)

### Decisão 3: Cron Compression Scope
- **Escolha:** Todos os cron jobs (descentralizado)
- **Razão:** Hook `tool.executed` já pega outputs
- **Alternativa rejeitada:** Job-level compression (requer refactor)

---

## 🎯 Success Criteria

### Functional
- [ ] memory_curator usa `ctx_search` sem grep
- [ ] Cron jobs comprimem 70%+ de outputs
- [ ] Dashboard mostra memory metrics
- [ ] Todos testes passam

### Performance
- [ ] Memory lookup: < 500ms (era ~2000ms com grep)
- [ ] Index build: < 1000ms
- [ ] Query latency: < 100ms (p95)

### Operational
- [ ] Economia: +7-8% (além Phase 3)
- [ ] Nenhuma regressão em Phase 1-3
- [ ] Dashboard operacional

---

## 📚 Referências

- Context-Mode: `/docker/base/openclaw-config/shared/CONTEXT_MODE_AGENT_HELPERS.md`
- Memory Curator: `/docker/base/openclaw-config/agents/memory_curator/SKILL.md`
- Cron Jobs: `vercel.json` crons section
- Hook System: `app/hooks/tool_executed.py`

---

## 🔄 Próxima Phase

**Phase 5: Monitoring & Fine-tuning** (Semana 4-5)
- Alerting em compressão anômala
- Auto-tuning de parâmetros
- Relatórios semanais de economia
