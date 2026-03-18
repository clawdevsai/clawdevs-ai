# BOOTSTRAP.md - CEO

Preparação para operação contínua:
1. Carregar configurações do ambiente (`DIRECTORS_NAME`, timezone).
2. Validar que `/data/openclaw/backlog` existe e é gravável.
3. Garantir diretórios de estado/auditoria: `/state`, `/status`, `/audit`.
4. Estabelecer logger para audit trail imutável (JSONL + hash por evento).
5. Carregar política de autonomia e schema de input.
6. Pronto.
