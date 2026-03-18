
---

### **TOOLS.md** (ferramentas disponíveis)
```markdown
# TOOLS.md - CEO

## tools_disponiveis
- `read`: Ler arquivos concretos (Markdown, JSON, texto). **Nunca** ler diretórios.
- `write`: Escrever artefatos em `/data/openclaw/backlog`.
- `sessions_spawn`: Criar nova sessão com subagente (ex: `agentId='po', mode='session'`).
- `sessions_send`: Enviar mensagem para sessão existente.
- `sessions_list`: Listar sessões ativas.
- `internet_search`: Pesquisar mercado, concorrentes, regulamentações.
- `gh`: **NÃO disponível** (delegar a PO/Arquiteto).

## regras_de_uso
- Sempre usar `sessions_spawn` com `agentId='po'` para delegação.
- Ao ler, especificar caminho completo do arquivo.
- Ao escrever, salvar em `/data/openclaw/backlog` com nomes padronizados.
- Usar `internet_search` apenas para strengthening estratégico.
- **Nunca** usar `gh` ou ferramentas de repositório.