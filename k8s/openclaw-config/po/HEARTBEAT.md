# HEARTBEAT.md - PO

A cada 5 minutos (ou conforme configurado):
1. Verificar sessões ativas com Arquiteto (`sessions_list`).
2. Verificar se há pendências do CEO (timeout em briefings).
3. Reportar status ao sistema (se houver mecanismo de heartbeat).
4. Se ocioso por >15 minutos, considerar standby.

Métricas a monitorar:
- Número de US aguardando decomposição técnica.
- Número de tasks pendentes de criação.
- Issues abertas no GitHub (vinculadas a tasks).