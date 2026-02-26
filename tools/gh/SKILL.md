# 🐙 gh — GitHub CLI para agentes ClawDevs

**Objetivo:** Gerenciar Issues, PRs, CI/CD e consultas avançadas ao GitHub API sem expor tokens.  
**Quando usar:** Criar/listar Issues, abrir/revisar PRs, verificar status de CI, consultas via `gh api`.  
**Referência:** `docs/20-ferramenta-github-gh.md`

---

## Pré-requisitos

```bash
# Verificar instalação
gh --version

# Autenticar (token via env, nunca exposto em chat/logs)
gh auth login              # Interativo (uso manual)
gh auth status             # Verificar autenticação

# Variável de ambiente (para uso em pods K8s):
# Definir via Secret K8s → env GH_TOKEN no pod
export GH_TOKEN="ghp_..."   # Nunca commitar
```

> **Zero Trust:** Token `GH_TOKEN` somente via Secret K8s (`clawdevs-secrets`). Nunca em variáveis inline, logs ou chat.

---

## Matriz de uso por agente

| Agente | Comandos autorizados |
|--------|---------------------|
| **PO** | `gh issue list/create/edit`, `gh project` |
| **Developer** | `gh pr create/list/view`, `gh issue view` |
| **Architect** | `gh pr review`, `gh pr merge`, `gh pr checks` |
| **DevOps/SRE** | todos + `gh repo`, `gh run list/view/rerun` |
| **QA** | `gh pr checks`, `gh run list/view`, `gh run download` |
| **CyberSec** | `gh pr view`, `gh api` (auditoria) |

---

## Passos por caso de uso

### Issues (PO)

```bash
# Listar issues abertas
gh issue list --state open --label "backlog"

# Criar issue
gh issue create \
  --title "feat: implementar autenticação JWT" \
  --body "## Descrição\n...\n## Critérios de aceite\n- [ ] ..." \
  --label "backlog,feat" \
  --assignee "@developer-agent"

# Editar issue
gh issue edit 42 --add-label "in-progress" --remove-label "backlog"

# Fechar issue
gh issue close 42 --comment "Implementado no PR #43"
```

### PRs (Developer/Architect)

```bash
# Criar PR
gh pr create \
  --title "feat: JWT auth (#42)" \
  --body "Closes #42\n\n## Alterações\n..." \
  --base main \
  --head feat/jwt-auth \
  --draft

# Listar PRs
gh pr list --state open

# Ver status dos checks de CI
gh pr checks 43

# Adicionar review (Architect)
gh pr review 43 --approve --body "LGTM. microADR gerado."
gh pr review 43 --request-changes --body "Ajustar: ..."

# Merge (somente Architect)
gh pr merge 43 --squash --delete-branch
```

### CI/CD (DevOps/QA)

```bash
# Listar runs do workflow
gh run list --workflow=ci.yaml --limit 10

# Ver detalhes do run
gh run view 12345678

# Ver logs de falha
gh run view 12345678 --log-failed

# Re-executar run falho
gh run rerun 12345678

# Baixar artefatos
gh run download 12345678 --name test-report
```

### Consultas avançadas via API (CyberSec/DevOps)

```bash
# Listar PRs abertos com labels
gh api repos/:owner/:repo/pulls \
  --jq '[.[] | {number, title, labels: [.labels[].name]}]'

# Auditoria: commits de um usuário nos últimos 7 dias
gh api repos/:owner/:repo/commits \
  --jq '[.[] | select(.commit.author.date > "2026-02-18") | {sha:.sha[:7], msg:.commit.message, author:.commit.author.name}]'

# Verificar secret scanning (CyberSec)
gh api repos/:owner/:repo/secret-scanning/alerts --jq '.[].secret_type'
```

### GitHub Projects (PO/Kanban)

```bash
# Listar projetos
gh project list --owner <org>

# Adicionar item ao projeto
gh project item-add <project-number> --owner <org> --url <issue-url>

# Ver itens do projeto
gh project item-list <project-number> --owner <org>
```

---

## Segurança

- **Nunca** expor `GH_TOKEN` em respostas de chat, logs de pod, ou código commitado
- Credenciais somente via Secret K8s (`clawdevs-secrets.github-token`)
- Usando `--repo owner/repo` quando o agente opera fora do diretório do repositório
- CyberSec audita tentativas de `gh api` com escopo fora do esperado
- DevOps é o único agente que pode executar `gh repo` (criação/deleção de repos)

---

## Boas práticas

- PRs **sempre** com referência à Issue: `Closes #<numero>` no corpo
- Body de Issues: seção "Descrição" + "Critérios de aceite" (checklist)
- Mensagens de commit seguem Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`
- Usar `--draft` ao criar PR — só remover o draft quando pronto para revisão
- Registrar falhas recorrentes em `memory/warm/TOOLS.md` (gotchas do `gh`)
