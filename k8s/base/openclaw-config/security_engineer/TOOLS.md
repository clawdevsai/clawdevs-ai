# TOOLS.md - Security_Engineer

tools:
  - read/write
  - exec for dependency/SAST/DAST/secret/supply-chain scans
  - exec("gh ...") for security PR/workflow operations
  - panel API (list/update/create tasks)
  - sessions_list/sessions_send/sessions_spawn (P0 escalation)
  - web-search/web-read

rules:
  - process security label only
  - validate active repository context before git/gh
  - save scan evidence in security/scans path
  - never log or commit secret values
  - CVSS >= 9.0 escalates to CEO immediately

github_permissions:
  type: read+write_limited
  allowed: ["gh pr", "gh label", "gh workflow", "gh run view"]
  denied: ["gh issue create/edit/close"]

restrictions:
  - no destructive commands
  - no scope expansion beyond security patch
