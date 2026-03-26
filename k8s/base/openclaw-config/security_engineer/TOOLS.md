# TOOLS.md - Security_Engineer

## available_tools
- `read(path)`: read dependency manifests, source code, configs, scan reports and git history.
- `write(path, content)`: write security reports, evidence of CVEs and patch artifacts.
- `exec(command)`: run security tools (npm audit, pip-audit, trivy, semgrep, gitleaks, osv-scanner, trufflehog, syft, grype).
- `exec("gh <args>")`: create patch PRs, security issues, consult Dependabot alerts and manage `security` labels.
- `exec("curl -s -H 'Authorization: Bearer $PANEL_TOKEN' '$PANEL_API_URL/tasks?status=inbox&label=security&page_size=20'")`: Task queue poll in the control panel.
- `exec("curl -s -X PATCH -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks/<id>")`: Update task status.
- `exec("curl -s -X POST -H 'Authorization: Bearer $PANEL_TOKEN' -H 'Content-Type: application/json' -d '<json>' $PANEL_API_URL/tasks")`: Create new task (sub-tasks, bugs found, etc.).
- `git(args...)`: create security branches, commit patches, check commit history to detect secrets.
- `sessions_spawn(agentId, mode, label)`: create session with Architect (P1/P2) or CEO (P0).
- `sessions_send(session_id, message)`: Report critical vulnerabilities, patch status and escalations.
- `sessions_list()`: list active sessions.
- `exec("web-search '<query>'")`: search the internet via SearxNG (aggregates Google, Bing, DuckDuckGo). Returns up to 10 results. Example: `web-search "CVE-2024-1234 patch nodejs"`
- `exec("web-read '<url>'")`: read any web page as clean markdown via Jina Reader. Example: `web-read "https://nvd.nist.gov/vuln/detail/CVE-2024-1234"`

## usage_rules
- `read/write` only in `/data/openclaw/**` and project workspace.
- Block paths with `../` or outside the allowlist (path traversal prevention).
- GitHub commands must use `exec('gh ... --repo "$ACTIVE_GITHUB_REPOSITORY"')`.
- Validate `active_repository.env` before taking any action.
- `sessions_spawn` allowed for: `arquiteto`, `ceo` (P0 only).
- Control panel queue poll 1x per hour:
  - example: `curl -s -H "Authorization: Bearer $PANEL_TOKEN" "$PANEL_API_URL/tasks?status=inbox&label=security&page_size=20"`
- When picking up a task: `PATCH /tasks/<id>` with `{"status":"in_progress"}` immediately.
- At the end: `PATCH /tasks/<id>` with `{"status":"done"}`.
- Process label `security` only. TASK_GITHUB_REPO = field `github_repo` of the task.
- Never log the value of detected secrets or credentials.
- Never commit secrets, credentials or tokens under any circumstances.
- `exec` with scanner commands: always redirect output to `/data/openclaw/backlog/security/scans/`.

## github_permissions
- **Type:** `read+write`
- **Own label:** `security` — automatically created at boot if it does not exist:
  `gh label create "security" --color "#ee0701" --description "Security tasks — routed to Security_Engineer" --repo "$ACTIVE_GITHUB_REPOSITORY" 2>/dev/null || true`
- **Allowed operations:** `gh pr`, `gh label`, `gh workflow`, `gh run view` (`--repo "$TASK_GITHUB_REPO"` only)
- **Prohibited:** `gh issue create`, `gh issue edit`, `gh issue close` — use control panel API
- **Active repo:** use `$TASK_GITHUB_REPO` (task field `github_repo`) instead of `$ACTIVE_GITHUB_REPOSITORY`

## main_commands

### Dependency Audit
```bash
# Node.js
npm audit --json
npm audit fix --json

# Python
pip-audit --json
pip-audit --fix

# Multi-linguagem (Go, Rust, Python, etc.)
osv-scanner --json --recursive .

# Cobertura ampla
trivy fs --json --exit-code 0 .
trivy image --json <imagem>
```

### SAST
```bash
# Multi-linguagem com regras OWASP
semgrep --config=p/security-audit --config=p/owasp-top-ten --json .

# Python
bandit -r . -f json

# JavaScript/TypeScript (ESLint security)
npx eslint --plugin security --format json .
```

### DAST
```bash
# OWASP ZAP baseline scan
docker run --rm owasp/zap2docker-stable zap-baseline.py -t "$TARGET_URL" -J report.json

# OWASP ZAP full scan
docker run --rm owasp/zap2docker-stable zap-full-scan.py -t "$TARGET_URL" -J report.json
```

### Secret Detection
```bash
# Histórico completo
trufflehog git file://. --json

# Commits recentes
gitleaks detect --source . --log-opts HEAD~10..HEAD --report-format json

# Pre-commit (verificar staged)
gitleaks protect --staged
```

### Supply Chain / SBOM
```bash
# Generate SBOM
syft . -o cyclonedx-json
syft . -o spdx-json

# Check vulnerabilidades no SBOM
grype sbom:sbom.json --output json

# Check imagem de container
grype <imagem>:<tag>
```

### GitHub Security
```bash
# List Dependabot alerts
gh api repos/$ACTIVE_GITHUB_REPOSITORY/dependabot/alerts --jq '.[] | select(.state=="open")'

# Create security issue
gh issue create --repo "$ACTIVE_GITHUB_REPOSITORY" \
  --label security --title "CVE-YYYY-XXXXX: ..." --body "..."

# Create PR de patch
gh pr create --repo "$ACTIVE_GITHUB_REPOSITORY" \
  --label security --title "security: fix CVE-YYYY-XXXXX" --body "..."
```

## full_internet_access

Full internet access permission for security research, querying CVE databases and discovering patches.Use `exec("web-search '...'")` and `exec("web-read '...'")` freely to:
- consult NVD (https://nvd.nist.gov/vuln/search), OSV (https://osv.dev), GHSA and Snyk Advisor
- check for patch available for specific CVE in any language
- search for safer alternative libraries when no patch is available
- read supply chain advisories (PyPI malware reports, npm security advisories, etc.)
- see OWASP Top 10, CWE (Common Weakness Enumeration), NIST 800-53
- learn emerging attack techniques and exploitation vectors to improve scan coverage
- check maintainer reputation and package security incident history
- compare security tools (Snyk vs Trivy vs Grype vs OWASP Dependency-Check)

Cite source, CVE ID and date of information in all reports and PRs produced.

## rate_limits
- `exec`: 120 commands/hour
- `gh`: 50 req/hour
- `sessions_spawn`: 10/hour
- `web-search`: 60 queries/hour
- `trivy` / `semgrep`: no limit (local tools); update DB at most 1x/hour

## inter_agent_sessions

Communication between agents via persistent session:

- **Session key format:** `agent:<id>:main` (ex: `agent:arquiteto:main`, `agent:ceo:main`)
- **Discovery:** `sessions_list()` filtering `kind: main` for active session keys
- **`sessions_spawn`:** hierarchical delegation background - orchestrator delegates task to subagent; result comes back via announce chain
- **`sessions_send`:** synchronous peer-to-peer - report status, escalate incident, send result; ping-pong up to 5 turns
- **Forbidden:** use `message` with `agent:<id>:main` (use `sessions_send`; `message` and only for channel/chatId)

Available agents and their keys:
- CEO: `agent:ceo:main`
- PO: `agent:po:main`
- Architect: `agent:arquiteto:main`
- Dev_Backend: `agent:dev_backend:main`
- Dev_Frontend: `agent:dev_frontend:main`
- Dev_Mobile: `agent:dev_mobile:main`
- QA_Engineer: `agent:qa_engineer:main`
- DevOps_SRE: `agent:devops_sre:main`
- Security_Engineer: `agent:security_engineer:main`
- UX_Designer: `agent:ux_designer:main`
- DBA_DataEngineer: `agent:dba_data_engineer:main`