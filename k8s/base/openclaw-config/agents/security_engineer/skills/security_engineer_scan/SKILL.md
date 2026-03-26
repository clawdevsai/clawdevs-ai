---
name: security_engineer_scan
description: Condensed security scan skill for dependency audit, SAST/DAST, secret detection and autonomous CVE patching.
---

# Security Scan (Condensed)

## Core flow
1. Run dependency audit across manifests.
2. Run SAST and, if URL exists, DAST.
3. Run secret detection.
4. Classify findings by CVSS and act.

## Severity policy
- CVSS >= 9.0 (P0): patch or mitigation immediately and escalate to CEO.
- CVSS 7.0-8.9 (P1): autonomous patch + PR + notify Architect.
- CVSS 4.0-6.9 (P2): security issue + planned remediation.
- CVSS < 4.0 (P3): report and monitor.

## Mandatory evidence
- CVE ID, CVSS, affected package/version, secure version.
- Test status before/after patch.
- Scan artifact paths.

## Minimal commands
- Dependency: `npm audit`, `pip-audit`, `osv-scanner`, `trivy fs`
- SAST: `semgrep` (and language-specific scan as needed)
- DAST: OWASP ZAP baseline when target URL exists
- Secrets: `gitleaks` or `trufflehog`

## Guardrails
- Never commit or print secret values.
- Never ignore CVE without documented risk acceptance.
- Always notify Architect for security patch status.
