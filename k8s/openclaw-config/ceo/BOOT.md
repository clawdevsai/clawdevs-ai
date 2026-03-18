
---

### **3. BOOT.md - CEO** (Adicionado healthcheck de custo/segurança)

```markdown
# BOOT.md - CEO

Ao iniciar:
1. Carregar `IDENTITY.md`.
2. Carregar `AGENTS.md` (regras e capabilities).
3. Carregar `SOUL.md` (postura e princípios de custo/segurança/performance).
4. Validar acesso a `/data/openclaw/backlog`.
5. Verificar ferramentas disponíveis (read, write, sessions_spawn, internet_search).
6. Carregar configurações de custo/segurança (ex: `CLOUD_BUDGET_MONTHLY`, `SECURITY_CLASSIFICATION_GUIDELINES`).
7. Pronto para receber input do Diretor.

## healthcheck
- Diretório `/data/openclaw/backlog` existe e é gravável? ✅
- Ferramentas disponíveis? ✅
- Variáveis de ambiente (ex: `DIRECTORS_NAME`, `CLOUD_BUDGET_MONTHLY`) definidas? ✅
- Políticas de segurança carregadas? ✅
- Metadata da organização (classificação de dados) disponível? ✅

Se qualquer healthcheck falhar: logar erro e aguardar configuração.