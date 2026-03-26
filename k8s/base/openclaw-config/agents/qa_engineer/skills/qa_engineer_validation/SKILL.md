---
name: qa_engineer_validation
description: QA validation skill for BDD, e2e testing, quality reporting and coverage analysis
---

# QA_Engineer Skills

---

## Dev-QA Cycle (Core Skill)

This is the main flow of QA_Engineer — executed with each dev agent delegation or by polling.

```
Dev_Agent abre PR → delega QA_Engineer
    ↓
QA lê SPEC (cenários BDD) e TASK
    ↓
QA executa testes (e2e + contrato + BDD validation)
    ↓
PASS → reportar ao Arquiteto → issue fechada
FAIL → reportar ao Dev_Agent com detalhes específicos
    ↓ (dev corrige)
retry 1 → QA re-executa
    ↓
retry 2 → QA re-executa
    ↓
retry 3 → ESCALAR AO ARQUITETO com histórico completo
```

Rule of thumb: **never approve without real evidence of test execution.**

---

## Validate SPEC BDD Scenarios

Workflow:
1. Read `SPEC-XXX-<slug>.md` — extract all BDD scenarios (`Given/When/Then`).
2. Map each scenario to an existing test or create a corresponding test.
3. Run tests.
4. Record result per scenario: ✅ PASS / ❌ FAIL + error message.
5. Report scenario coverage: `X/Y cenários aprovados`.

---

## E2E Web Tests (Playwright / Cypress)

```bash
npx playwright test                        # todos os testes
npx playwright test --reporter=html        # com relatório HTML
npx playwright test --headed               # modo visual (debug)
npx cypress run                            # Cypress headless
npx cypress run --spec "cypress/e2e/**.cy.ts"
```

---

## E2E Mobile Tests (Detox / Maestro)

```bash
npx detox build --configuration ios.sim.release
npx detox test --configuration ios.sim.release
maestro test .maestro/flows/              # Maestro cross-platform
```

---

## Contract Tests (Pact)

```bash
npx pact-js verify                        # verificar contratos
npx pact-js publish                       # publicar contratos ao broker
```

---

## Load Testing (k6)

```bash
k6 run --vus 50 --duration 60s load_test.js
k6 run --out json=results.json load_test.js
```

Standard goals (when SPEC not defined):
- Latency p95 < 300ms
- Latency p99 < 500ms
- Error rate < 1%

---

## Basic Security Scan

```bash
npm audit --audit-level=critical           # dependências Node.js
pip-audit                                  # dependências Python
npx secretlint "**/*"                      # secrets em código
```

---

## PASS Report

```
✅ QA PASS — TASK-XXX | PR #YYY
Cenários BDD: 12/12 aprovados
Cobertura: 84%
E2E: 34 testes, 0 falhas
Latência p95: 187ms (meta: <300ms)
Evidências: playwright-report/index.html
```

---

## FAIL Report

```
❌ QA FAIL — TASK-XXX | PR #YYY | Retry 1/3
Cenários falhando:
  - Cenário 3: "When user submits form with invalid email"
    Error: Expected toast 'Email inválido', received nothing
    Screenshot: test-results/scenario-3-fail.png
  - Cenário 7: "Given user is on checkout, When payment fails"
    Error: Timeout 5000ms — element #error-message not found
Ação necessária: implementar toast de validação e mensagem de erro no checkout
```

---

## Escalation to the Architect (3rd Retry)

```
⚠️ QA ESCALATION — TASK-XXX | 3 retries esgotados
Histórico:
  Retry 1: [data] — FAIL — cenários 3, 7
  Retry 2: [data] — FAIL — cenário 7 (3 persistiu)
  Retry 3: [data] — FAIL — cenário 7
Possible root cause: checkout error logic not implemented according to the SPEC
Ação sugerida: revisar SPEC-XXX cenário 7 com PO ou TASK com Arquiteto
```

---

## Guardrails

- Never approve without real evidence.
- Never deploy production code.
- Never ignore BDD scenarios.
- Always climb on the 3rd retry.
