# BOOT.md - Dev_Mobile

## Boot Sequence

1. Load `IDENTITY.md`.
2. Load `AGENTS.md`.
3. Read `README.md` the repository to understand the application, stack and target platforms.
4. Load `SOUL.md`.
5. Load `INPUT_SCHEMA.json`.
6. Read `/data/openclaw/memory/shared/SHARED_MEMORY.md` — apply global team standards as base context.
7. Read `/data/openclaw/memory/dev_mobile/MEMORY.md` — retrieve your own relevant mobile learning.
8. Validate `/data/openclaw/` and implementation workspace.
9. Detect mobile framework by task's `technology_stack` or by files (`app.json`, `expo.json`, `pubspec.yaml`).
10. Identify target platform: iOS, Android or both.
11. Load standard commands per framework (Expo/EAS or Flutter).
12. Validate tools in PATH: `node`, `npm`, `npx`, `expo`, `eas-cli` (or `flutter`, `dart`).
13. Check tools: `read`, `write`, `exec`, `git`, `sessions_send`.
14. Check presence of UX artifacts in `/data/openclaw/backlog/ux/` for screen-scoped tasks.
15. When completing the session: register up to 3 learnings in `/data/openclaw/memory/dev_mobile/MEMORY.md`.
16. Ready to receive task from the Architect.

##healthcheck
- `/data/openclaw/` accessible? ✅
- INPUT_SCHEMA.json loaded? ✅
- Mobile framework detected? ✅
- Target platform identified? ✅
- SHARED_MEMORY.md and MEMORY.md (dev_mobile) read? ✅
- `ACTIVE_GITHUB_REPOSITORY` defined? ✅