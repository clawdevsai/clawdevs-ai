# BOOTSTRAP.md - Security_Engineer

1. Upload env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Read `README.md` the repository to understand the stack, languages and frameworks used.
3. Validate base structure:
   - `${PROJECT_ROOT}`
   - if non-existent, use fallback `/data/openclaw/backlog/implementation` and mark context as `standby` (without throwing an error)
4. Initialize security working directories:
   - `/data/openclaw/backlog/security/` → security reports and CVEs
   - `/data/openclaw/backlog/security/scans/` → SAST/DAST scan results
   - `/data/openclaw/backlog/security/patches/` → evidence of patches applied
5. Detect dependency manifests in the repository:
   - `package.json` → `npm audit`
   - `requirements.txt` / `pyproject.toml` → `pip-audit`
   - `go.mod` → `osv-scanner`
   - `Cargo.toml` → `cargo audit` / `osv-scanner`
   - `pom.xml` / `build.gradle` → `trivy fs`
   - before reading manifest, validate that the file exists
   - if no manifest exists, do not fail; operate by `technology_stack` or wait for task
6. Configure security tools cache:
   - Update Trivy Database: `trivy image --download-db-only`
   - Update Semgrep rules: `semgrep --update`
   - Check local OSV database
7. Check toolchain in PATH: `semgrep`, `trivy`, `gitleaks`, `trufflehog`, `osv-scanner`, `npm`, `pip-audit`.
8. Configure logger with `task_id`, `scan_type` and `cvss_threshold`.
9. Enable full internet access to consult CVE databases, NVD, OSV, GHSA and Snyk Advisor.
10. Validate `gh` authentication and permissions to create PRs and issues in the active repository.
11. Set up scheduling:
    - fixed interval: 6 hours (cron: `0 */6 * * *`)
    - job source: cron + GitHub issues with label `security` + messages from dev agents
12. Ready.