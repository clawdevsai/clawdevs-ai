# VIBE CODING PLAYBOOK

ClawDevs AI should optimize for speed with observable quality.
The goal is to deliver a small, demonstrable and reversible slice quickly, then harden it with testing, contracts and observability.

## Principles
- Prioritize a short flow: idea -> spec -> vertical slice -> demo -> refinement.
- Always keep the user seeing real progress with each cycle.
- Prefer small, reversible changes with a clear scope.
- Avoid overengineering, but do not compromise on testing, security and traceability.
- Everything that goes into production needs to have acceptance, rollback and validation criteria.

## Recommended loop
1. Define the visible result in a sentence.
2. Write the minimum SPEC with observable behavior.
3. Deliver a functional vertical slice.
4. Validate with demo and human feedback.
5. Add tests, logs, metrics and hardening.
6. Repeat until the flow closes.

## What characterizes a good iteration
- Shows business or operation value quickly.
- Can be tested in minutes, not days.
- There is a clear path to entry, exit and error.
- Does not block further evolution.
- Leaves traceability to the next person or agent.

## Rules to avoid bad vibecoding
- Do not replace specifications with improvisation.
- Do not accumulate invisible refactoring without demonstrable delivery.
- Do not leave an implicit integration contract.
- Do not add abstractions without real need.
- Do not promote to "ready" without minimal testing and checking NFRs.

## Expected artifacts
- BRIEF
- SPEC
- US
- TASK
- demo notes
- tests
- observability

## Minimum quality per iteration
- Demonstrable behavior.
- Objective acceptance criteria.
- Testing evidence.
- Known risk and mitigation.
- Rollback or reversal path.