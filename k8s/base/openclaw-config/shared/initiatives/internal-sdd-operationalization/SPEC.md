# SPEC

## Behavior
- When starting an initiative, the CEO consolidates demand in BRIEF and initial SPEC.
- If there is ambiguity, the flow produces CLARIFY before PLAN.
- PO refines the SPEC into FEATURE and USER STORY.
- The Architect converts the SPEC into PLAN, TASK and validation criteria.
- Dev_Backend implements only the specified behavior.

##Contracts
- BRIEF defines context, value, scope and constraints.
- SPEC defines observable behavior, contracts, NFRs and acceptance criteria.
- CLARIFY records ambiguity, decisions and assumptions.
- PLAN defines architecture, phases, risks and validation.
- TASK defines small, traceable execution.
- VALIDATE confirms readiness and evidence.

## Acceptance criteria
1. Given a new demand, when the CEO starts the operation, then there is an initial BRIEF and SPEC.
2. Given an ambiguity, when the flow encounters a gap, then CLARIFY happens before PLAN.
3. Given a ready TASK, when the Dev_Backend executes, then delivery follows traceability to the SPEC.

## NFRs
- Low friction for human use and agents.
- Complete traceability between artifacts.
- Repeatability in new initiatives.

## Invariants
- Do not implement without sufficient SPEC.
- Do not close a stage without a checklist.
- Do not leave an outdated plan when the SPEC changes.