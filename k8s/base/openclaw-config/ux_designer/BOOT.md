# BOOT.md - UX_Designer

## Sequência de Boot

1. Aguardar gateway OpenClaw estar disponível (health check em loop com backoff).
2. Montar configuração do agente a partir dos ConfigMaps injetados.
3. Carregar `SOUL.md` e `AGENTS.md` do agentDir para ativar constraints e regras.
4. Validar INPUT_SCHEMA.json.
5. Verificar `active_repository.env` em `/data/openclaw/contexts/`.
6. Criar diretórios necessários: `/data/openclaw/backlog/ux/`.
7. Registrar boot: `ux_designer booted successfully`.
