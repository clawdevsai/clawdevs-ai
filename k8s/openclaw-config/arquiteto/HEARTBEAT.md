# HEARTBEAT.md - Arquiteto

A cada 5 minutos (ou conforme configurado):
1. Verificar sessões ativas com PO (`sessions_list`).
2. Verificar se há tasks pendentes de geração (US em `user_story/` sem correspondente em `tasks/`).
3. Reportar status ao sistema (se houver mecanismo de heartbeat).
4. Se ocioso por >30 minutos, considerar standby.

Métricas a monitorar:
- Número de US aguardando decomposição técnica.
- Número de ADRs pendentes de criação.
- Tarefas com estimativa de custo elevada (acima de threshold).