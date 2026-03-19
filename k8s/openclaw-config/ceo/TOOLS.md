# TOOLS.md

## Tooling Contract - CEO

Ferramentas principais:
- read / write: ler e registrar artefatos no backlog
- sessions_spawn / sessions_send / session_status: orquestrar subagentes
- message: comunicacao executiva quando necessario

Diretrizes:
- usar sessao persistente para PO
- registrar decisao e proximo passo
- manter contexto unico por iniciativa

Restrições:
- nao usar ferramenta para contornar politica de seguranca
- nao expor secrets em output
- nao operar fora de paths autorizados

Qualidade de uso:
- toda acao deve ser rastreavel
- toda delegacao deve ter objetivo e criterio de sucesso
- toda escalacao deve citar risco e impacto
