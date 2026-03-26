# PROMPT CHANGELOG

History of relevant changes to operational prompts and SDD templates.

## 2026-03-25

### Added
- Operational gates and minimum output for auditing at `SDD_OPERATIONAL_PROMPTS.md`.
- Blocos few-shot (`entrada -> output`) for role in `SDD_OPERATIONAL_PROMPTS.md`.
- Operational reverse prompting section in `SDD_OPERATIONAL_PROMPTS.md`.
- Gate and traceability fields in `VALIDATE_TEMPLATE.md`.

### Changed
- Agent rules (`ceo`, `po`, `arquiteto`, `dev_backend`) for hard gate SDD and mandatory evidence before `DONE`.

## Registration convention
- Always record: date, type (`Added|Changed|Removed`), file and expected impact.
- In changes that alter behavior, include a short before/after example in the PR.