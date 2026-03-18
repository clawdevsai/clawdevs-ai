# HEARTBEAT.md - CEO

A cada 5 minutos (ou conforme configurado):
1. Verificar sessoes ativas com PO (`sessions_list`).
2. Ler `DASHBOARD.md` (se existir) em `/data/openclaw/backlog`.
3. Atualizar estado operacional em `/data/openclaw/backlog/status/ceo_health.json`.
4. Validar fila de briefs pendentes e aplicar backpressure quando necessario.
5. Executar deteccao proativa de risco e custo.

## checks proativos
- Tendencia de custo semanal:
  - Se crescimento > 10% semana contra semana: notificar Diretor e sugerir plano de otimizacao.
- SLOs:
  - Se violacao por > 48h: escalar para Diretor com plano de mitigacao.
- Vulnerabilidades:
  - Se houver severidade `critical`: pausar delegacoes nao criticas e abrir memo de incidente.
- Fila:
  - `max_pending_briefs = 10`
  - `max_active_sessions = 3`
  - Se excedido: aplicar `throttle_wait = 30m`.

## recuperacao de sessao
- Se sessao do PO ficar sem resposta por > 30min: enviar ping de status.
- Se sem resposta por > 2h: marcar como degradada e reatribuir/reiniciar sessao.
- Se timeout final (> 6h): escalar para Diretor com resumo do bloqueio.

## metricas a monitorar
- `pending_briefs_count`
- `active_po_sessions`
- `auto_approval_rate`
- `escalation_rate`
- `critical_vulnerabilities_open`
- `cloud_cost_weekly_growth_pct`
