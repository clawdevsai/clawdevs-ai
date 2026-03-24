# BOOTSTRAP.md - Dev_Mobile

1. Carregar env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Ler `README.md` do repositório para entender app, stack e plataformas alvo.
3. Validar estrutura base:
   - `${PROJECT_ROOT}`
   - se inexistente, usar fallback `/data/openclaw/backlog/implementation` e marcar contexto como `standby` (sem lançar erro)
4. Detectar framework por arquivos:
   - `app.json` / `expo.json` → React Native + Expo
   - `pubspec.yaml` → Flutter
   - `package.json` + `react-native` → React Native bare
   - antes de ler arquivos de build, validar se o arquivo existe
   - se nenhum arquivo de build existir, não falhar; operar por `technology_stack` ou aguardar task
5. Identificar plataforma: verificar `app.json.expo.platforms` ou ADR da task.
6. Definir comandos padrão por framework.
7. Verificar toolchain no PATH:
   - Expo: `node`, `npm`, `npx`, `expo`, `eas`
   - Flutter: `flutter`, `dart`
8. Configurar logger com `task_id`, `framework` e `platform`.
9. Verificar artefatos UX em `/data/openclaw/backlog/ux/`.
10. Habilitar pesquisa técnica na internet para boas práticas mobile.
11. Validar autenticação `gh` e permissões do repositório ativo.
12. Configurar agendamento:
    - intervalo fixo: 60 minutos (offset: :30 de cada hora)
    - origem de trabalho: issues GitHub label `mobile`
13. Pronto.
