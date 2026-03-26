# SPEC TEMPLATE

Use this model to describe external behavior before coding.
The objective is to reduce ambiguity, align humans and agents and maintain traceability between BRIEF, SPEC, US and TASK.

## 1. Context
- Problem we are solving
- Who is affected
- Because it matters now

## 2. Objective
- Expected result in one sentence
- Business or operational value

## 3. No goals
- What is explicitly out of scope

## 4. Functional scope
- Main streams
- Relevant alternative flows
- Expected error cases

## 5. Behavior
Describe in domain language and, when useful, in Given/When/Then format.

### Stream 1
- Given:
- When:
- Then:

### Stream 2
- Given:
- When:
- Then:

## 6. Contracts
- Entrances and exits
- Validation rules
- Preconditions and postconditions
- Invariants
- Integrations and limits between systems
- Status or sequence, if applicable

## 7. Non-functional requirements
- Performance
- Cost
- Security
- Observability
- Compliance
- Availability and resilience

## 8. Data
- Data created, read, updated and removed
- Classification of sensitive data
- Retention and audit

## 9. Tests and acceptance criteria
- Validation scenarios
- Objective acceptance criteria
- Signs of failure

## 10. Rollout
- Delivery plan
- Migration, if any
- Rollback, if necessary

## 11. Risks and decisions
- Known risks
- Decisions made
- Assumptions adopted

## 12. Traceability
- BRIEF:
- SPEC:
- US:
- TASK:
- Issues:

## Usage rule
- Keep the spec complete but concise.
- Prefer observable behavior over vague descriptions.
- Redo the spec before refactoring the implementation when the behavior changes.