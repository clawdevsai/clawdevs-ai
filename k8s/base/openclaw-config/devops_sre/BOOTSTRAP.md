# BOOTSTRAP.md - DevOps_SRE

1. Carregar env:
   - `GITHUB_ORG`
   - `ACTIVE_GITHUB_REPOSITORY`
   - `OPENCLAW_ENV`
   - `PROJECT_ROOT` (default `/data/openclaw/backlog/implementation`)
2. Ler `README.md` do repositório para entender stack e infra.
3. Validar estrutura base:
   - `${PROJECT_ROOT}`
   - se inexistente, usar fallback `/data/openclaw/backlog/implementation` e marcar contexto como `standby` (sem lançar erro)
4. Detectar stack de infra por arquivos:
   - `.github/workflows/` → GitHub Actions
   - `terraform/` ou `infra/` → Terraform
   - `helm/` ou `charts/` → Helm
   - `k8s/` → Kubernetes manifests
   - `docker-compose.yml` → Docker Compose
   - antes de ler arquivos de stack, validar se o arquivo/diretório existe
   - se nenhum arquivo de stack existir, não falhar; operar por `technology_stack` ou aguardar task
5. Detectar cloud provider por variáveis de ambiente ou arquivos de configuração.
6. Verificar toolchain no PATH: `kubectl`, `terraform`, `helm`, `docker`, `aws/gcloud/az`.
7. Configurar logger com `task_id` e `infra_type`.
8. Habilitar pesquisa técnica na internet para boas práticas de infra e cloud.
9. Validar autenticação `gh` e permissões do repositório ativo.
10. Configurar agendamento:
   - intervalo fixo: 30 minutos
   - origem de trabalho: issues GitHub label `devops` + monitoramento de produção
11. Pronto.
