# 🔍 skill-discovery — Descoberta e instalação de skills (Zero Trust)

**Objetivo:** Encontrar skills do ecossistema que ampliem capacidades do enxame; propor ao Diretor; instalar somente após checklist de segurança completo.  
**Quando usar:** Quando for solicitado "como fazer X" e X pode ser coberto por skill existente, ou quando o Diretor pede extensão de capacidades.  
**Referência:** `docs/19-descoberta-instalacao-skills.md`

---

## ⚠️ Regras inegociáveis

| Regra | Detalhe |
|-------|---------|
| **Nunca instalar sem aprovação** | Buscar e listar é permitido; instalar exige Diretor + checklist |
| **Zero binários** | Skills apenas em texto claro (Python, Bash, JS legível); binários → rejeitar |
| **Hash SHA-256 obrigatório** | `skillstracelock.json` deve bater 100%; roteador rejeita automaticamente sem consultar LLM |
| **Egress whitelist** | Domínios não declarados na whitelist global são bloqueados; skill não pode abrir firewall sozinha |

---

## Passos

### 1. Entender a necessidade

Identificar:
1. **Domínio** — React, testes, DevOps, documentação, design...
2. **Tarefa concreta** — escrever testes, criar changelog, revisar PRs...
3. **Frequência** — é recorrente o suficiente para justificar instalar uma skill?

### 2. Buscar skills

```bash
# Busca interativa
npx skills find [query]

# Exemplos:
npx skills find react performance
npx skills find pr review
npx skills find changelog
npx skills find e2e testing playwright
npx skills find kubernetes deploy
```

**Catálogo completo:** https://skills.sh/

### 3. Apresentar ao Diretor

Formato de proposta ao Diretor:

```
Encontrei uma skill que pode ajudar: "<nome>" faz <o que faz>.

Comando de instalação sugerido:
  npx skills add <owner/repo@skill>

Mais informações: https://skills.sh/<owner/repo>/<skill>

Checklist de segurança preliminar:
✅ Origem: <author/org> (confiável / desconhecido)
✅ Tipo: texto claro (Python/Bash) / binário (REJEITAR)
⏳ Hash skillstracelock.json: a verificar
⏳ Comandos no SKILL.md: a revisar
```

### 4. Checklist de segurança (CyberSec verifica; DevOps instala)

```bash
# 1. Verificar SKILL.md em busca de comandos suspeitos
npx skills add <skill> --dry-run   # Simulação sem instalar

# 2. Checar skillstracelock.json (hash SHA-256)
cat node_modules/.../skillstracelock.json
# Hash deve corresponder ao manifesto na origem

# 3. Confirmar: zero binários
find node_modules/.../skills/ -type f | grep -vE '\.(py|sh|js|ts|md|json|yaml|txt)$'
# Nenhum resultado = OK. Qualquer binário = REJEITAR

# 4. Revisar domínios de egress declarados no manifesto
# Confirmar que estão na whitelist global (config/agents/agents-config.yaml → egress.static_whitelist)
```

### 5. Instalar (somente DevOps, após aprovação do Diretor)

```bash
# Instalação após aprovação e checklist completo
npx skills add <owner/repo@skill> -g -y
```

### 6. Registro pós-instalação

```bash
# Registrar skill instalada no arquivo de controle
echo "<skill> — instalada em $(date +%Y-%m-%d) — aprovada por Diretor" >> skills/INSTALLED.md
```

---

## Score de confiança → ação

| Situação | Ação |
|----------|------|
| Manifesto validado (hash ok) + zero binários | Sandbox de execução (quarentena); sem bloquear sprint |
| Publicador confiável (Vercel, Google, Microsoft) | Instalação facilitada; ainda passa pelo checklist |
| Hash não bate | Roteador rejeita automaticamente; não notificar LLM |
| Binários encontrados | Architect rejeita; registrar em `memory/cold/learnings/` |
| Dúvida sobre origem | Aprovação explícita do Diretor obrigatória |

---

## Categorias de busca por caso de uso

| Necessidade | Termos de busca |
|-------------|----------------|
| Frontend React/Next.js | `react`, `nextjs`, `typescript`, `tailwind` |
| Testes | `testing`, `jest`, `playwright`, `e2e` |
| DevOps/IaC | `deploy`, `docker`, `kubernetes`, `ci-cd` |
| Documentação | `docs`, `readme`, `changelog`, `api-docs` |
| Code Review | `review`, `lint`, `refactor`, `best-practices` |
| Design | `ui`, `ux`, `design-system`, `acessibilidade` |
| Busca web | `brave-search`, `web search`, `exa`, `search api` |
| Dados/alertas | `prediction markets`, `watchlist`, `alerts`, `paper trading` |

---

## Quando não houver skill

1. Informar ao Diretor que nenhuma skill relevante foi encontrada
2. Oferecer resolver com capacidades atuais do agente
3. Se for recorrente → registrar em `.learnings/FEATURE_REQUESTS.md` para virar skill própria
4. Ver processo de criação de skills: `skills/skill-creation/SKILL.md`

---

## Quem pode fazer o quê

| Agente | Buscar | Propor ao Diretor | Instalar |
|--------|--------|------------------|---------|
| CEO, PO, QA, UX, CyberSec | ✅ | ✅ | ❌ |
| Architect | ✅ | ✅ (com parecer técnico) | ❌ |
| Developer | ✅ | ✅ | ❌ (depende de Architect/CyberSec) |
| **DevOps** | ✅ | ✅ | ✅ (após aprovação do Diretor) |
