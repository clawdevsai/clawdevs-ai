# HEARTBEAT.md - security_engineer

heartbeat:
  interval: "as configured by orchestrator"
  actions:
    - check pending assigned work
    - verify context integrity
    - emit concise status snapshot
