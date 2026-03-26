# TOOLS.md - Architect

tools:
  - read/write
  - exec for git/gh/curl operational flow
  - sessions_list/sessions_spawn/sessions_send
  - web-search/web-read

rules:
  - validate active repository context before any gh/git action
  - use panel API for task lifecycle (create/update/list)
  - mandatory order: docs -> commit -> panel_task -> validation -> session_finished
  - use sessions_send for agent channels (not message)

routing_by_label:
  back_end: dev_backend
  front_end: dev_frontend
  mobile: dev_mobile
  tests: qa_engineer
  devops: devops_sre
  dba: dba_data_engineer
  security: security_engineer

github_permissions:
  type: read+write_limited
  allowed: ["gh pr", "gh label", "gh workflow", "gh run view"]
  denied: ["gh issue create/edit/close"]

panel_api_contract:
  required_fields: ["title", "label", "github_repo", "description"]
