# BOOT.md - CEO

Ao iniciar:
1. Carregar `IDENTITY.md`.
2. Carregar `AGENTS.md` (regras, validacoes e fluxos de decisao).
3. Carregar `SOUL.md` (postura executiva e guardrails).
4. Carregar `AUTONOMY_POLICY.md` e resolver `autonomy_level` ativo.
5. Carregar schema de input em `INPUT_SCHEMA.json`.
6. Validar acesso de leitura/escrita em `/data/openclaw/backlog`.
7. Validar presenca de diretorios operacionais:
   - `/data/openclaw/backlog/briefs`
   - `/data/openclaw/backlog/decisions`
   - `/data/openclaw/backlog/status`
   - `/data/openclaw/backlog/state`
   - `/data/openclaw/backlog/audit`
8. Inicializar estado persistente:
   - `/data/openclaw/backlog/state/ceo_state.json`
   - `/data/openclaw/backlog/state/director_sessions.json`
9. Verificar ferramentas disponiveis (read, write, sessions_spawn, sessions_send, sessions_list, internet_search).
10. Pronto para receber input.

## healthcheck
- Diretório `/data/openclaw/backlog` existe e e gravavel? ✅
- Schema `INPUT_SCHEMA.json` carregado? ✅
- Politica de autonomia carregada? ✅
- Estado persistente carregado? ✅
- Ferramentas obrigatorias disponiveis? ✅
- Timeouts de sessao e fila definidos? ✅

Se qualquer healthcheck falhar: bloquear delegacoes, registrar em `/data/openclaw/backlog/audit/ceo-audit.jsonl` e aguardar configuracao.
