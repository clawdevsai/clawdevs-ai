# 🏗 skill-creation — Criação de skills próprias

**Objetivo:** Criar uma skill quando não existe nenhuma no ecossistema e a necessidade é recorrente.  
**Quando usar:** Quando `npx skills find <query>` não retornar resultado relevante e a tarefa aparecer repetidamente em `.learnings/FEATURE_REQUESTS.md`.  
**Quem cria:** Developer (implementa), Architect (revisa anatomia e segurança), DevOps (publica).  
**Referência:** `docs/29-criacao-de-skills.md`

---

## Princípios

- **Concisão:** Skill faz uma coisa bem feita. Sem escopo inflado.
- **Grau de liberdade:** Passos claros mas com margem para o agente adaptar ao contexto.
- **Zero binários:** Sempre texto claro (Python, Bash, JS legível). Sem pré-compilados.
- **Documentação primeiro:** SKILL.md escrito antes da implementação.
- **Testável:** Cada passo deve ter saída verificável.

---

## Anatomia de uma skill

```
skills/<nome-da-skill>/
├── SKILL.md          ← Instruções principais (obrigatório)
│   ├── Objetivo / Quando usar
│   ├── Pré-requisitos
│   ├── Passos (numbered, claros)
│   ├── Exemplos
│   └── Boas práticas / Troubleshooting
├── scripts/          ← Scripts auxiliares (opcional)
│   └── executar.py / executar.sh
├── references/       ← Documentação de referência (opcional)
│   └── api-docs.md
└── assets/           ← Arquivos de suporte (opcional)
    └── template.yaml
```

---

## Processo em 6 passos

### 1. Descobrir a necessidade

```bash
# Verificar FEATURE_REQUESTS
cat .learnings/FEATURE_REQUESTS.md | grep "<necessidade>"

# A necessidade aparece 3+ vezes? → justifica criar skill
```

### 2. Confirmar que não existe alternativa

```bash
npx skills find <query>
npx skills find <query-alternativo>
# Nenhum resultado relevante? → prosseguir
```

### 3. Desenhar o SKILL.md (antes de implementar)

```bash
# Usar o template:
npx skills init <nome-da-skill>
# Ou criar manualmente em skills/<nome>/SKILL.md
```

Template mínimo do SKILL.md:

```markdown
# <emoji> <nome> — <descrição curta>

**Objetivo:** ...
**Quando usar:** ...
**Referência:** docs/<arquivo>.md

## Pré-requisitos
...

## Passos
### 1. ...
### 2. ...

## Exemplos
...

## Boas práticas
...
```

### 4. Implementar scripts (se necessário)

```bash
# Criar script Python (preferido)
cat > skills/<nome>/scripts/executar.py << 'EOF'
#!/usr/bin/env python3
"""Descrição da skill."""
import sys
# ...
EOF

chmod +x skills/<nome>/scripts/executar.py
```

**Checklist do Developer antes de submeter:**
- [ ] Sem binários — apenas texto claro
- [ ] Sem egress não autorizado (sem curl para domínios fora da whitelist)
- [ ] Sem eval(), exec() ou subprocess com shell=True sem justificativa
- [ ] `skillstracelock.json` gerado com hash SHA-256
- [ ] Funciona em modo offline (se possível)

### 5. Gerar manifesto SHA-256 (obrigatório)

```bash
# Gerar skillstracelock.json com hash de todos os arquivos da skill
python3 - << 'EOF'
import hashlib, json
from pathlib import Path

skill_dir = Path("skills/<nome-da-skill>")
hashes = {}
for f in sorted(skill_dir.rglob("*")):
    if f.is_file() and f.name != "skillstracelock.json":
        content = f.read_bytes()
        hashes[str(f.relative_to(skill_dir))] = hashlib.sha256(content).hexdigest()

lock = {"version": "1", "files": hashes}
(skill_dir / "skillstracelock.json").write_text(json.dumps(lock, indent=2))
print("skillstracelock.json gerado.")
EOF
```

### 6. Documentar e publicar (ou uso interno)

**Para uso interno (não publicar):**
```bash
# Registrar em INSTALLED.md
echo "<nome-skill> — criada em $(date +%Y-%m-%d) — uso interno" >> skills/INSTALLED.md

# Commit
git add skills/<nome-da-skill>/
git commit -m "feat: skill <nome> para <caso de uso>"
```

**Para publicar no ecossistema (após revisão do Architect + CyberSec):**
```bash
npx skills publish skills/<nome-da-skill>/
```

---

## Padrões de fluxo e saída

| Padrão | Convenção |
|--------|-----------|
| Formato de saída | Markdown (quando texto) ou JSON estruturado |
| Código de retorno | 0 = sucesso, 1 = erro esperado, 2 = erro fatal |
| Logs | stderr para diagnóstico; stdout apenas para saída principal |
| Interatividade | Evitar prompts; usar argumentos CLI ou env vars |

---

## Guardrails (Architect revisa antes de merge)

- Zero binários — rejeitar qualquer artefato compilado
- Sem `sudo` sem justificativa documentada
- Sem `curl | bash` ou equivalente
- Egress apenas para domínios na whitelist global
- SKILL.md tem seção "Quando usar" E "Quando não usar"
- Scripts têm shebang correto e são executáveis

---

## Integração com learnings

Registrar a criação da skill em memória:

```python
from memory.hot.elite_memory import ColdStore
store = ColdStore()
store.capture_learning(
    agent="Developer",
    learning="Skill <nome> criada para resolver <necessidade>. Localização: skills/<nome>/",
    category="tools",
)
```
