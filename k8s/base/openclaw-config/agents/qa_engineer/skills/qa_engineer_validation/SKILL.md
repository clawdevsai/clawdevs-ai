---
name: qa_engineer_validation
description: Condensed QA validation skill for BDD, e2e validation, and evidence-based PASS/FAIL reporting.
---

# QA Validation (Condensed)

## Core cycle
1. Read SPEC + TASK.
2. Map BDD scenarios to tests.
3. Run tests and collect evidence.
4. Report PASS/FAIL.
5. On 3rd retry failure, escalate to Architect.

## PASS criteria
- All required scenarios executed.
- No critical failures.
- Evidence attached (logs/report/screenshots/traces).

## FAIL criteria
- List exact failing scenarios and error messages.
- Include reproduction/evidence path.
- Provide next action for dev agent.

## Default tools
- Web e2e: Playwright/Cypress
- Mobile e2e: Detox/Maestro
- Contract: Pact
- Load: k6
- Security baseline: dependency + secret checks

## Guardrails
- Never approve without evidence.
- Never skip BDD scenario validation.
- Never modify production code.
