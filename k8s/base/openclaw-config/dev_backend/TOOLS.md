# TOOLS.md - Dev_Backend

tools:
  - read/write
  - exec for lint/test/build/security checks
  - exec("gh ...") for PR/workflow/check operations
  - panel API (list/update/create tasks)
  - sessions_list/sessions_send
  - web-search/web-read

rules:
  - process back_end tasks only
  - validate active repository context before git/gh
  - mark task in_progress on pickup and done on completion
  - always run tests before reporting completion
  - use sessions_send for agent channels (not message)

github_permissions:
  type: read+write_limited
  allowed: ["gh pr", "gh label", "gh workflow", "gh run view"]
  denied: ["gh issue create/edit/close"]

restrictions:
  - no secrets in commits/logs
  - no destructive commands or force push
