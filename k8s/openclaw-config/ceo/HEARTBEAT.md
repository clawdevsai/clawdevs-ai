# HEARTBEAT.md - CEO

A cada 5 minutos (ou conforme configurado):
1. Verificar sessões ativas com PO (`sessions_list`).
2. Verificar pedidos pendentes do Diretor.
3. Reportar status ao sistema (se houver mecanismo de heartbeat).
4. Se ocioso por >30 minutos, considerar standby.

Métricas a monitorar:
- Tempo desde último input do usuário.
- Número de sessões ativas.
- Número de artefatos gerados.