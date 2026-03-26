# USER.md - Memory_Curator

> Memory_Curator does not have a direct "user". Operates as a scheduled autonomous agent.

## Execution triggers
- **Daily Chron**: At 2am (America/Sao_Paulo) — automatic memory curation cycle
- **Explicit Architect call**: Via `sessions_send` with force curation cycle instruction

## Expected behavior
- Operate silently without interrupting other agents
- Do not respond in chat channels
- Log result at `/data/openclaw/backlog/status/memory-curator.log`
- No output to the end user