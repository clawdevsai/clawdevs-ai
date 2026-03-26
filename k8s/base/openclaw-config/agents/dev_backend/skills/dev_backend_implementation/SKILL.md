---
name: dev_backend_implementation
description: Condensed backend implementation skill for task execution, tests, CI evidence, and cost-performance focus.
---

# Dev Backend Implementation (Condensed)

## When to execute
- Scheduled queue cycle for `back_end` issues.
- Immediate handoff from Architect in shared session.

## Core flow
1. Read TASK + SPEC (+ ADR if relevant).
2. Implement only approved scope.
3. Add/update tests.
4. Run lint/test/build/security checks.
5. Report evidence to Architect.

## Required quality gates
- Security basics (validation/auth/secrets).
- Observable behavior aligned to SPEC.
- Coverage target >= 80% or task target.
- Explicit cost/performance tradeoff when relevant.

## Fallback commands
- Node: `npm ci && npm test && npm run lint && npm run build`
- Python: `pytest` + lint + build/check
- Go: `go test ./... && go vet ./...`
- Rust: `cargo test && cargo clippy`

## Guardrails
- Never bypass tests/security gates.
- Never commit secrets.
- Never use destructive git operations.
