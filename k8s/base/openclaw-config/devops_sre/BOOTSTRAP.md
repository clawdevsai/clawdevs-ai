# BOOTSTRAP.md - DevOps_SRE

1. Upload env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Read `README.md` the repository to understand stack and infrastructure.
3. Validate base structure:
   - `${PROJECT_ROOT}`
   - if non-existent, use fallback `/data/openclaw/backlog/implementation` and mark context as `standby` (without throwing an error)
4. Detect infra stack by files:
   - `.github/workflows/` → GitHub Actions
   - `terraform/` or `infra/` → Terraform
   - `helm/` or `charts/` → Helm
   - `k8s/` → Kubernetes manifests
   - `docker-compose.yml` → Docker Compose
   - before reading stack files, validate that the file/directory exists
   - if no stack file exists, do not fail; operate by `technology_stack` or wait for task
5. Detect cloud providers by environment variables or configuration files.
6. Check toolchain in PATH: `kubectl`, `terraform`, `helm`, `docker`, `aws/gcloud/az`.
7. Configure logger with `task_id` and `infra_type`.
8. Enable technical research on the internet for good infrastructure and cloud practices.
9. Validate `gh` authentication and active repository permissions.
10. Set up scheduling:
   - fixed interval: 30 minutes
   - work source: issues GitHub label `devops` + production monitoring
11. Ready.