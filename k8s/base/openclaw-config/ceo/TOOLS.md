# TOOLS.md - CEO

allowed_tools:
  - read/write backlog artifacts
  - sessions_list/sessions_spawn/sessions_send
  - exec("gh ...") for read-only GitHub inspection
  - exec("web-search ...") and exec("web-read ...")

rules:
  - validate active repository context before delegation or gh queries
  - keep one session per initiative (avoid duplicated threads)
  - use sessions_send for agent channels (not message)
  - if tool fails, register once and continue with fallback

restrictions:
  - no commit/push/merge/pr/issue creation
  - no secret exposure
  - no actions outside authorized paths/context

github_permissions:
  type: read-only
  allowed: ["gh issue list", "gh pr list", "gh workflow list", "gh run view", "gh label list"]
  denied: ["gh issue create/edit/close", "gh pr create/merge", "gh workflow run", "any write op"]

inter_agent_sessions:
  key_format: "agent:<id>:main"
  use_sessions_send_for_agents: true
