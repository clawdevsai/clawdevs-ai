# TOOLS.md - QA_Engineer

tools:
  - read/write (tests/reports only)
  - exec for e2e/contract/load/security checks
  - exec("gh ...") for PR/workflow/check interactions
  - panel API (list/update/create tasks)
  - sessions_list/sessions_send
  - web-search/web-read

rules:
  - process tests label only
  - mark task in_progress on pickup and done on completion
  - store retries and escalate on 3rd failure
  - use sessions_send for agent channels (not message)

github_permissions:
  type: read+write_limited
  allowed: ["gh pr", "gh label", "gh workflow", "gh run view"]
  denied: ["gh issue create/edit/close"]

restrictions:
  - QA does not modify production code
  - no destructive commands
