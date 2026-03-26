# SPECKIT ADAPTATION

This repository does not use the official Spec Kit as a required dependency.
Instead, it takes the same mental model and adapts it to ClawDevs AI artifacts.

## Correspondence between Spec Kit and ClawDevs AI
- `constitution` -> `CONSTITUTION.md`
- `specify` -> `SPEC_TEMPLATE.md` and `backlog/specs/`
- `clarify` -> record of ambiguities, assumptions and SPEC revisions
- `plan` -> `ADR`, `TASK` and the Architect's technical plan
- `tasks` -> `TASK-XXX-<slug>.md`
- `analyze` -> validation of NFRs, risks, security and cost
- `implement` -> Dev_Backend executing the task

## Operational objective
- Maintain the spec-driven flow for both the ClawDevs AI platform and project deliveries.
- Preserve end-to-end traceability.
- Avoid "loose" code without a clear contract.

## How to use
- The CEO consolidates the demand in Brief + SPEC.
- PO refines the SPEC and creates User Stories.
- The Architect converts SPEC/US into a technical plan and tasks.
- Dev_Backend strictly implements what is specified.