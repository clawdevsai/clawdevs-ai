# BOOTSTRAP.md - QA_Engineer

1. Carregar env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Ler `README.md` do repositório para entender stack e comandos de teste.
3. Validar estrutura base:
   - `${PROJECT_ROOT}`
   - se inexistente, usar fallback `/data/openclaw/backlog/implementation` e marcar contexto como `standby` (sem lançar erro)
4. Detectar tipo de app:
   - `next.config.js` / `vite.config.ts` → web (Playwright/Cypress)
   - `app.json` / `expo.json` → mobile (Detox/Maestro)
   - `package.json` + `express` / `fastapi` → API (k6 + Pact)
   - antes de ler arquivos de build, validar se o arquivo existe
   - se nenhum arquivo de build existir, não falhar; operar por `technology_stack` ou aguardar task
5. Verificar toolchain no PATH por tipo.
6. Configurar logger com `task_id` e `test_type`.
7. Configurar retry_counter storage (em memória ou `/data/openclaw/backlog/qa/retries/`).
8. Validar autenticação `gh` para atualização de issues/PRs.
9. Configurar agendamento:
   - intervalo fixo: 60 minutos (offset: :45 de cada hora)
   - origem de trabalho: issues GitHub label `tests`
10. Pronto.
