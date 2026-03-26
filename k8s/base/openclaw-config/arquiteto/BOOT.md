# BOOT.md - arquiteto

boot_sequence:
  - load AGENTS.md (primary contract)
  - load INPUT_SCHEMA.json
  - load TOOLS.md
  - read shared memory + agent memory
  - validate active repository context
  - ensure project backlog root exists

ready_when:
  - contracts loaded
  - context validated
  - required paths available
