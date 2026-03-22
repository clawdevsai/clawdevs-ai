# O que a aplicação ClawDevs AI faz

## Visão geral

O repositório **clawdevs-ai** define um stack em Kubernetes que sobe:

1. **Ollama** — API de modelos em `http://ollama:11434`, com modelos cloud configurados no bootstrap do pod Ollama.
2. **OpenClaw** — gateway multi-agente num container Debian: instala o CLI via `install.sh`, gera `openclaw.json` e executa `openclaw gateway` na porta **18789** (probe e Service). Estado persistente em PVC `openclaw-data` montado em `/data/openclaw`.
3. **SearXNG** — busca interna no cluster; o bootstrap do OpenClaw expõe o comando `web-search` que chama `http://searxng:8080`.
4. **Ferramentas no container OpenClaw** — `gh` autenticado com `GITHUB_TOKEN`, `web-search` (SearXNG), `web-read` (Jina Reader em `https://r.jina.ai/...`), scripts `claw-repo-discover`, `claw-repo-ensure`, `claw-repo-switch` em `/data/openclaw/bin` e em `/usr/local/bin`.

O **StatefulSet** `clawdevs-ai` (container `openclaw`) é o núcleo: um time de agentes (CEO, PO, Arquiteto, Dev_Backend, Dev_Frontend, Dev_Mobile, QA_Engineer, DevOps_SRE, Security_Engineer, UX_Designer, DBA_Data_Engineer) com workspaces sob `/data/openclaw/workspace-*`, regras em `AGENTS.md` copiadas do ConfigMap `openclaw-agent-config`, e modelo padrão apontando para provedores Ollama no `openclaw.json`.

## Comportamento principal

- **Spec-Driven Development (SDD)** — templates e constitution em `k8s/base/openclaw-config/shared/`; artefatos esperados em `/data/openclaw/backlog/` (briefs, specs, tasks, user_story, implementation, status, etc.).
- **Delegação entre agentes** — `openclaw.json` habilita `agentToAgent` entre os IDs listados; CEO costuma orquestrar; executor técnico (ex.: Dev_Backend) trabalha a partir de TASK/issue conforme `AGENTS.md`.
- **Telegram** — binding padrão: agente **ceo** no canal Telegram (bot `TELEGRAM_BOT_TOKEN_CEO`, allowlist `TELEGRAM_CHAT_ID_CEO`). Mensagens de grupo fora da política podem ser negadas pelas regras de `session.sendPolicy`.
- **GitHub** — contexto ativo em `/data/openclaw/contexts/active_repository.env` (`ACTIVE_GITHUB_REPOSITORY`, branch, org). Fallback de repo no bootstrap se `GITHUB_DEFAULT_REPOSITORY` não existir na org.
- **Crons nativos (gateway)** — variáveis `*_CRON_ENABLED`, `*_CRON_EXPR`, fuso `America/Sao_Paulo` no manifest disparam ciclos que invocam agentes (ex.: filas por label no GitHub). Valores efetivos estão no `openclaw-pod.yaml` (ex.: dev_backend `0 * * * *`, dev_frontend `15 * * * *`, etc.).
- **Roteador de erros** — com `AGENT_ERROR_ROUTER_ENABLED=true`, um loop observa sessões dos agentes e envia alerta ao CEO via `openclaw agent --agent ceo --message ...`.
- **Git hooks globais** — bloqueiam commit/push direto em `main`/`master` (caminho configurado para hooks em `/data/openclaw/git-hooks`).

## O que você pode fazer (exemplos)

### Operar o cluster

```bash
make preflight
make clawdevs-up
```

GPU só no Ollama quando aplicar overlay: `make openclaw-apply-gpu` ou fluxo `gpu-migrate-apply` (ver `docs/README.md`).

### Acessar o gateway na máquina local

```bash
kubectl --context=clawdevs-ai port-forward service/clawdevs-ai 18789:18789
```

Autenticação HTTP do gateway usa o token `OPENCLAW_GATEWAY_TOKEN` do `k8s/.env` (Bearer nas APIs do OpenClaw, conforme documentação do produto).

NodePort do Service (quando útil no Minikube): **31879** → 18789.

### Abrir dashboard OpenClaw dentro do pod

```bash
make openclaw-dashboard
```

(executa `openclaw dashboard --no-open` no pod.)

### Entrar no container e usar ferramentas de bootstrap

```bash
kubectl --context=clawdevs-ai exec -it statefulset/clawdevs-ai -c openclaw -- bash
```

```bash
claw-repo-discover
claw-repo-discover billing
claw-repo-switch minha-org/meu-repo develop
claw-repo-ensure minha-org/novo-repo --create
```

```bash
web-search licença MIT diferença Apache
web-read https://docs.github.com/en/rest
```

### Conversar com o CEO pelo Telegram

1. Preencher `TELEGRAM_BOT_TOKEN_CEO` e `TELEGRAM_CHAT_ID_CEO` no `k8s/.env`.
2. Aplicar o stack; o bot só aceita DMs/grupos allowlisted com esse chat id.
3. Enviar mensagem ao bot — o agente default do binding é o **ceo** (orquestração, BRIEF/SPEC, delegação ao PO/Arquiteto conforme regras).

### Integrar fila GitHub → Dev_Backend (exemplo)

1. Garantir contexto: `claw-repo-switch org/repo` ou `GITHUB_DEFAULT_REPOSITORY` correto.
2. Criar issue no repositório ativo com label **`back_end`** (e sem conflito com outras trilhas, conforme `AGENTS.md` do dev_backend).
3. No horário do cron do agente (ver env no `openclaw-pod.yaml`), o ciclo pode acionar o agente para pegar a issue; delegação imediata também pode vir do Arquiteto na mesma sessão.

### Logs e diagnóstico

```bash
make openclaw-logs
```

Bootstrap: `/data/openclaw/backlog/status/openclaw-bootstrap.log` (e `openclaw-gateway-last.log` em cópia após saída do gateway). Com `DEBUG_LOG_ENABLED=true` no secret, mais verbosidade e espelhamento de sessões no log.

### Persistência

- Dados OpenClaw: PVC `openclaw-data`.
- Modelos Ollama: PVC `ollama-data`.

## Agentes

Resumo por agente: [agentes/README.md](./agentes/README.md). Contrato completo: `k8s/base/openclaw-config/<id>/AGENTS.md`.
