# BRIEF

##Title
- Operationalize SDD as ClawDevs AI standard

## Context
- The platform already has templates, checklists, prompts and SDD contracts.
- This remains to be consolidated as an official and repeatable operational flow for all agents.

## Goal
- Make any internal initiative follow the same SDD contract without relying on additional explanation.

## Scope
- Includes:
  - use of Constitution, BRIEF, SPEC, CLARIFY, PLAN, TASK and VALIDATE
  - use of operational prompts and templates
  - alignment of agents to the shared contract
- Does not include:
  - stack change
  - main runtime change
  - functional rewriting of agents

##Constraints
- Needs to work on local Windows / Docker Desktop / Kubernetes.
- Needs to be documented and replicable.
- Need to keep operating costs low.

## Success metrics
- Every agent can locate the flow in less than 1 minute.
- Every new initiative goes through the SDD checklist before execution.
- The same contract applies to internal platforms and projects.

## Risks
- Risk: becoming unused documentation.
- Mitigation: make prompts and templates the normal path of operation.

## Assumptions
- The team accepts using markdown files as an operational contract.

## Next step
- Produce the operational behavior SPEC.