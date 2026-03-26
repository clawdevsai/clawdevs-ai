# BOOTSTRAP.md - Dev_Mobile

1. Upload env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Read `README.md` the repository to understand the target app, stack and platforms.
3. Validate base structure:
   - `${PROJECT_ROOT}`
   - if non-existent, use fallback `/data/openclaw/backlog/implementation` and mark context as `standby` (without throwing an error)
4. Detect framework by files:
   - `app.json` / `expo.json` → React Native + Expo
   - `pubspec.yaml` → Flutter
   - `package.json` + `react-native` → React Native bare
   - before reading build files, validate that the file exists
   - if no build file exists, do not fail; operate by `technology_stack` or wait for task
5. Identify platform: check `app.json.expo.platforms` or ADR of the task.
6. Define default commands per framework.
7. Check toolchain in PATH:
   - Expo: `node`, `npm`, `npx`, `expo`, `eas`
   - Flutter: `flutter`, `dart`
8. Configure logger with `task_id`, `framework` and `platform`.
9. Check out UX artifacts at `/data/openclaw/backlog/ux/`.
10. Enable technical research on the internet for good mobile practices.
11. Validate `gh` authentication and active repository permissions.
12. Set up scheduling:
    - fixed interval: 60 minutes (offset: :30 of each hour)
    - work source: issues GitHub label `mobile`
13. Ready.