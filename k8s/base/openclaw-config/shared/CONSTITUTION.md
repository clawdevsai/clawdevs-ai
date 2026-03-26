# CONSTITUTION

## Purpose
ClawDevs AI applies Spec-Driven Development internally and in delivered projects.
The rules below apply to the platform, agents and any delivery carried out by them.

##Principles
- Specification comes before implementation.
- The SPEC is the source of truth for intended behavior.
- Each change must be small, reversible and demonstrable.
- Clarification happens before planning.
- Planning happens before task breakdown.
- Tasks must trace back to SPEC, BRIEF and the approved scope.
- Security, observability and cost control are mandatory, not optional.
- Prefer short feedback loops and vertical slices over large hidden work.
- If the spec changes, the implementation plan must be updated before coding continues.

## Operating sequence
1. Constitution
2. Brief
3. Spec
4. Clarify
5. Plan
6. Tasks
7. Implement
8. Validate

## Mapping to ClawDevs AI artifacts
- Constitution -> this file and agent guardrails
- Brief -> executive intent and scope
- Spec -> behavior, contracts, NFRs and acceptance criteria
- Clarify -> ambiguity resolution and assumptions log
- Plan -> architecture and implementation approach
- Tasks -> executable work items
- Implement -> code, tests and operational changes
- Validate -> CI, tests, demo and acceptance checks

## Non-negotiables
- Do not implement without a sufficiently detailed SPEC.
- Do not skip clarification when ambiguity exists.
- Do not treat the plan as final if the SPEC changed.
- Do not mark work done without validation.