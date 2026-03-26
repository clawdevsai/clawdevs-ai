# SDD CHECKLIST

Use this checklist before passing on a change.

##Constitution
- [ ] The change is in line with the constitution of the repository.
- [ ] The objective was written in a short and observable way.

## Brief
- [ ] The problem and the expected value are clear.
- [ ] The scope and non-scope are defined.
- [ ] The main risks have been identified.

## Spec
- [ ] SPEC describes observable behavior.
- [ ] Contracts, invariants and NFRs are explicit.
- [ ] Acceptance criteria are testable.

## Clarify
- [ ] Ambiguities have been resolved.
- [ ] The assumptions were recorded.
- [ ] What was left open was declared.

## Plan
- [ ] There is a technical plan consistent with SPEC.
- [ ] The architectural decisions are justified.
- [ ] The impact on cost, safety and operation was considered.

##Tasks
- [ ] Tasks are small and executable.
- [ ] Traceability to SPEC and BRIEF is maintained.
- [ ] The implementation order reduces risk.

## Implement
- [ ] The minimum demonstrable functional slice exists.
- [ ] Tests cover SPEC scenarios.
- [ ] Logs, metrics and rollback were considered.

## Validate
- [ ] CI or local validation passed.
- [ ] The demo confirmed the expected behavior.
- [ ] The artifact can proceed to the next step without ambiguity.