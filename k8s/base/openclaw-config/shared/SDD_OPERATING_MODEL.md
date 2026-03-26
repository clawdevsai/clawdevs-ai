# SDD OPERATING MODEL

ClawDevs AI applies Spec-Driven Development on two levels:

1. **Internally**: on the platform itself, on the agents, on the bootstrap, on the infrastructure and in the repo automations.
2. **In projects**: in any delivery made to customers, products or internal teams.

## Central rule
- SPEC defines the intended behavior.
- The code is the executable implementation of this SPEC.
- Changes without a clear SPEC should not proceed for implementation.

## Source of truth
- For behavior and contract, the source of truth is the approved SPEC.
- For execution, runtime and automation, the code needs to reflect the SPEC.
- For business and priority, BRIEF and SPEC need to remain aligned.

## How to apply internally
- Every improvement to the ClawDevs AI platform starts with BRIEF or equivalent demand.
- Then, write SPEC with observable behavior and acceptance criteria.
- Then, break into US and TASK for execution.
- If the change affects agents, bootstrap, manifests or automations, the same flow continues to apply.

## How to apply to projects
- Every project feature also follows BRIEF -> SPEC -> US -> TASK.
- SPEC must cover contracts, NFRs, integrations and risks.
- The work must be done in small, demonstrable and reversible slices.
- After the first visible delivery, harden with testing, observability and rollback.

## Expected result
- Less ambiguity.
- Less rework.
- More predictability.
- Better traceability between what was ordered, specified and delivered.