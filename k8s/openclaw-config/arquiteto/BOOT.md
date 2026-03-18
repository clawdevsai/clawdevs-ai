# BOOT.md - Arquiteto

Ao iniciar:
1. Carregar `IDENTITY.md`.
2. Carregar `AGENTS.md` (regras e capabilities).
3. Carregar `SOUL.md` (postura).
4. Validar acesso a `/data/openclaw/backlog` (e subpastas: `idea`, `user_story`, `tasks`, `architecture`, `briefs`).
5. Verificar ferramentas disponíveis (read, write, sessions_spawn, internet_search, gh).
6. Validar variáveis de ambiente (GITHUB_REPOSITORY, GITHUB_TOKEN se disponível).
7. Pronto para receber input do PO.

## healthcheck
- Diretório `/data/openclaw/backlog` existe e é gravável? ✅
- Ferramentas disponíveis? ✅
- `GITHUB_REPOSITORY` definido? ✅ (opcional, mas necessário para GitHub integration)