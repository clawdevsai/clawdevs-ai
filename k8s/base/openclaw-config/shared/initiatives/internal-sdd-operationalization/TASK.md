#TASK

## Related artifacts
- BRIEF: `BRIEF.md`
- SPEC: `SPEC.md`
- Clarify: `CLARIFY.md`
- Plan: `PLAN.md`

## Objective
- Publish and operationalize the SDD flow as ClawDevs AI standard.

## Scope
- Includes:
  - official templates
  - operational prompts
  - checklist SDD
  - complete example
- Does not include:
  - gateway architecture change
  - stack change
  - agent runtime rewrite

## Acceptance criteria
1. Given a new agent, when it starts, it then finds the main SDD artifacts.
2. Given a new initiative, when it opens, then there is a clear path to BRIEF -> SPEC -> CLARIFY -> PLAN -> TASK -> VALIDATE.
3. Given the README, when someone opens the repo, then the flow becomes evident in a few seconds.

## Implementation steps
1. Publish shared templates and contracts.
2. Distribute files to agent workspaces.
3. Update README and Makefile.
4. Validate Kustomize rendering.

## Tests
- Unit: N/A
- Integration: `kubectl kustomize k8s`
- Validation: reading prompts and shortcuts

## NFRs
- Performance: zero impact on runtime.
- Cost: no material increase in cost.
- Security: no secrets or credentials.
- Observability: traceable docs in markdown.

## Done when
- The flow is ready for internal use and for projects.