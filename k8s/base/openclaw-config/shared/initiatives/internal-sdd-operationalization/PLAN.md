# PLAN

## Goal
- Make the SDD stream the ClawDevs AI default operating path.

## Inputs
- BRIEF
- SPEC
- CLARIFY
- Constitution
- Checklist SDD

##Architecture
- `k8s/base/openclaw-config/shared/` keeps the contracts.
- `k8s/base/openclaw-pod.yaml` distributes the artifacts to the workspaces.
- `k8s/base/kustomization.yaml` exposes the files in configMap.
- `README.md` points to the official entry of the stream.
- `Makefile` offers shortcuts to templates and operational prompts.

## Alternatives considered
- Option: leave the flow only in the documentation.
- Tradeoff: Less work now, greater risk of inconsistent use.
- Rejected because: does not create operational habit.

## Phases
1. Consolidate templates, checklists and prompts.
2. Expose everything to agents via bootstrap.
3. Create a complete example to guide new initiatives.

## Risks
- Risk: duplication of artifacts and confusion of the source of truth.
- Mitigation: keep the package shared and the main documentation lean.

## Validation
- kustomize rendering.
- README check.
- Verification of Makefile shortcuts.

## Rollback
- Remove shortcuts and new references without affecting the agents' runtime.