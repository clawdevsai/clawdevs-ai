# TOOLS.md - DBA_DataEngineer

## tools_disponíveis
- `read(path)`: ler schemas, migrations, TASKs e artefatos do projeto.
- `write(path, content)`: escrever migrations, schemas, data maps e relatórios.
- `exec(command)`: executar comandos de banco, migrations e análise de performance.
- `exec("gh <args>")`: atualizar issues/PRs e consultar status de CI.
- `git(args...)`: commit/branch/merge sem comandos destrutivos.
- `sessions_spawn(agentId, mode, label)`: criar sessão com Arquiteto, Dev_Backend ou DevOps_SRE.
- `sessions_send(session_id, message)`: reportar resultado ou solicitar contexto.
- `sessions_list()`: listar sessões ativas.
- `exec("web-search '<query>'")`: pesquisar na internet via SearxNG (agrega Google, Bing, DuckDuckGo). Retorna até 10 resultados. Exemplo: `web-search "postgresql index optimization 2025"`
- `exec("web-read '<url>'")`: ler qualquer página web como markdown limpo via Jina Reader. Exemplo: `web-read "https://www.postgresql.org/docs/current/indexes.html"`

## regras_de_uso
- `read/write` somente em `/data/openclaw/**`.
- Bloquear comandos destrutivos sem TASK explícita.
- Comandos GitHub devem usar `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- Validar `active_repository.env` antes de qualquer ação.
- `sessions_spawn` permitido para: `arquiteto`, `dev_backend`, `devops_sre`.
- Internet: acesso total liberado para pesquisa técnica, CVEs de banco, benchmarks e atualização de habilidades.

## github_permissions
- **Tipo:** `read+write`
- **Label própria:** `dba` — criar automaticamente no boot se não existir:
  `gh label create "dba" --color "#0052cc" --description "Database tasks — routed to DBA_DataEngineer" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Operações permitidas:** `gh issue`, `gh pr`, `gh label`, `gh workflow` (somente `--repo "$ACTIVE_GITHUB_REPOSITORY"`)
- **Proibido:** override de repositório, operações fora do `ACTIVE_GITHUB_REPOSITORY`

## autonomia_de_pesquisa_e_aprendizado
- Permissão total de acesso à internet para pesquisa, atualização de habilidades e descoberta de melhores alternativas.
- Usar `exec("web-search '...'")` e `exec("web-read '...'")` livremente para:
  - comparar engines e custos de managed services (RDS, PlanetScale, Neon, Supabase, etc.)
  - verificar CVEs e security advisories em engines de banco em uso
  - pesquisar técnicas de otimização de queries e índices
  - ler documentação oficial de LGPD, GDPR e regulações de dados
  - aprender padrões emergentes de data engineering e streaming
- Citar fonte e data da informação nos artefatos produzidos.

## comandos_principais
### PostgreSQL
- `psql -c "EXPLAIN ANALYZE <query>"` — análise de performance
- `psql -c "\d <tabela>"` — estrutura da tabela
### Migration Tools
- Flyway: `flyway migrate`, `flyway info`, `flyway undo`
- Alembic: `alembic upgrade head`, `alembic downgrade -1`, `alembic revision`
- Prisma: `npx prisma migrate deploy`, `npx prisma db push`, `npx prisma studio`
- Liquibase: `liquibase update`, `liquibase rollback`, `liquibase status`
### MongoDB
- `mongosh --eval "db.collection.explain('executionStats').find({})"` — análise
### Redis
- `redis-cli info memory`, `redis-cli --latency`

## rate_limits
- `exec`: 60 comandos/hora
- `gh`: 50 req/hora
- `sessions_spawn`: 10/hora
- `web-search`: 60 queries/hora

## inter_agent_sessions

Comunicacao entre agentes via sessao persistente:

- **Session key format:** `agent:<id>:main` (ex: `agent:arquiteto:main`, `agent:ceo:main`)
- **Descoberta:** `sessions_list()` filtrando `kind: main` para obter session keys ativas
- **`sessions_spawn`:** delegacao hierarquica background - orquestrador delega task a subagente; resultado volta via announce chain
- **`sessions_send`:** peer-to-peer sincrono - reportar status, escalar incidente, enviar resultado; ping-pong ate 5 turnos
- **Proibido:** usar `message` com `agent:<id>:main` (use `sessions_send`; `message` e apenas para canal/chatId)

Agentes disponiveis e suas keys:
- CEO: `agent:ceo:main`
- PO: `agent:po:main`
- Arquiteto: `agent:arquiteto:main`
- Dev_Backend: `agent:dev_backend:main`
- Dev_Frontend: `agent:dev_frontend:main`
- Dev_Mobile: `agent:dev_mobile:main`
- QA_Engineer: `agent:qa_engineer:main`
- DevOps_SRE: `agent:devops_sre:main`
- Security_Engineer: `agent:security_engineer:main`
- UX_Designer: `agent:ux_designer:main`
- DBA_DataEngineer: `agent:dba_data_engineer:main`

