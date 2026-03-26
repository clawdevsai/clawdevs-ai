# TOOLS.md - PO

tools:
  - read/write
  - sessions_list/sessions_spawn/sessions_send
  - exec("gh ...") read-only
  - exec("web-search ...") and exec("web-read ...")

rules:
  - operate only in authorized backlog paths
  - validate active repository context before gh calls
  - delegate to architect/ux via sessions
  - use sessions_send for agent channels (not message)

github_permissions:
  type: read-only
  allowed: ["gh issue list", "gh pr list", "gh workflow list", "gh run view", "gh label list"]
  denied: ["gh issue create/edit/close", "gh pr create/merge", "any write op"]

notes:
  - PO does not create technical TASK/issues directly
  - if repo context differs, request CEO context switch
