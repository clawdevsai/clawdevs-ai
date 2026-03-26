# TOOLS.md - Dev_Mobile

## tools_disponíveis
- `read(path)`: ler arquivos da task/projeto e artefatos UX.
- `write(path, content)`: escrever screens/componentes/testes/docs.
- `exec(command)`: executar build/test/lint mobile.
- `exec("gh <args>")`: atualizar issues/PRs e consultar workflows.
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=mobile&page_size=20'")`: Poll de fila de tasks no control panel.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Atualizar status da task.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Criar nova task (sub-tasks, bugs encontrados, etc.).
- `git(args...)`: commit/branch/merge sem comandos destrutivos.
- `sessions_spawn(agentId, mode, label)`: criar sessão com Arquiteto ou QA_Engineer.
- `sessions_send(session_id, message)`: enviar update ou delegar ao QA_Engineer.
- `sessions_list()`: listar sessões ativas.
- `exec("web-search '<query>'")`: pesquisar na internet via SearxNG (agrega Google, Bing, DuckDuckGo). Retorna até 10 resultados. Exemplo: `web-search "react native performance optimization 2025"`
- `exec("web-read '<url>'")`: ler qualquer página web como markdown limpo via Jina Reader. Exemplo: `web-read "https://reactnative.dev/docs/performance"`

## regras_de_uso
- `read/write` somente em `/data/openclaw/**`.
- Bloquear comandos destrutivos (`rm -rf`, `git push -f`, etc.).
- Comandos GitHub devem usar `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- Validar `active_repository.env` antes de qualquer ação gh/git.
- Poll de fila control panel 1x por hora:
  - exemplo: `curl -s -H "Authorization: Bearer $PANEL_TOKEN" "$PANEL_API_URL/tasks?status=inbox&label=mobile&page_size=20"`
- Ao pegar uma task: `PATCH /tasks/<id>` com `{"status":"in_progress"}` imediatamente.
- Ao concluir: `PATCH /tasks/<id>` com `{"status":"done"}`.
- Processar somente label `mobile`. TASK_GITHUB_REPO = campo `github_repo` da task.
- `sessions_spawn` permitido para: `arquiteto`, `qa_engineer`.

## github_permissions
- **Tipo:** `read+write`
- **Label própria:** `mobile` — criar automaticamente no boot se não existir:
  `gh label create "mobile" --color "#e4e669" --description "Mobile tasks — routed to Dev_Mobile" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Operações permitidas:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (somente `--repo "$TASK_GITHUB_REPO"`)
- **Proibido:** `gh issue create`, `gh issue edit`, `gh issue close` — usar control panel API
- **Repo ativo:** usar `$TASK_GITHUB_REPO` (campo `github_repo` da task) em vez de `$ACTIVE_GITHUB_REPOSITORY`

## comandos_adicionais_mobile
- `expo`: `npx expo start`, `npx expo lint`, `eas build`, `eas submit`
- `flutter`: `flutter test`, `flutter build apk`, `flutter build ios`
- `detox`: `npx detox test` (e2e React Native)
- `maestro`: `maestro test` (e2e cross-platform)

## autonomia_de_pesquisa_e_aprendizado
- Permissão total de acesso à internet para pesquisa, atualização de habilidades e descoberta de melhores alternativas mobile.
- Usar `exec("web-search '...'")` e `exec("web-read '...'")` livremente para:
  - descobrir SDKs, bibliotecas e ferramentas de build mais eficientes para o problema
  - verificar CVEs e vulnerabilidades em dependências nativas e JS mobile
  - comparar benchmarks de startup time, bundle size e performance entre alternativas
  - ler documentação oficial de iOS, Android, Expo, Flutter e React Native
  - aprender padrões emergentes de performance mobile e app store compliance
- Citar fonte e data da informação nos artefatos produzidos.

## rate_limits
- `exec`: 120 comandos/hora
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

