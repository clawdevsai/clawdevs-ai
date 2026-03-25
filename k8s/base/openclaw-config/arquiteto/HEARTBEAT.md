# HEARTBEAT.md - Arquiteto

A cada 5 minutos (ou conforme configurado):
1. Sessões ativas (`sessions_list`):
   - Se sessões com PO > 2: alertar PO.
   - Se sessão inativa > 1h: fechar automaticamente.
2. Tarefas pendentes:
   - Tasks sem NFR ou Security/Observabilidade: escalar ao PO.
   - ADR pendente de aprovação > 48h: notificar PO.
3. Research monitor:
   - Se timer > 2h: abortar research, aplicar `Default/Proven`, logar `research_timeout`.
   - Se `web-search` > 30 queries/hora: aplicar throttle.
4. GitHub health:
   - Se falhas > 5% nas últimas 10 operações: alertar PO e usar fallback por arquivo.
5. Pipeline docs/task:
   - Se existir documento novo de CEO/PO/Arquiteto sem commit em `implementation/docs`: alertar PO.
   - Se panel task criada sem commit prévio de docs: marcar não-conforme e escalar PO.
   - Se sessão finalizada sem pasta `session_finished/<session_id>`: marcar não-conforme e corrigir.
6. Anomalias de arquivo:
   - Leitura/escrita fora de `/data/openclaw/backlog`: bloquear, logar, notificar PO.
7. Monitoramento do ciclo Dev-QA:
   - Tasks do panel com label `tests` e status `inbox` > 2h sem mudança: notificar QA_Engineer.
   - Tasks do panel com label `devops` e status `inbox` > 1h sem mudança: notificar DevOps_SRE.
   - QA_Engineer reportou 3 retries em alguma task: escalar ao PO com histórico.
8. Monitoramento de pipelines CI/CD:
   - Falhas repetidas de CI/CD (> 3x no mesmo PR): delegar ao DevOps_SRE.
9. Se ocioso > 20 minutos: reportar `standby` (sem fechar sessão).
