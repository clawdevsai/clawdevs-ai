# SOUL — ConfigMap por agente (Fase 1)

O ConfigMap `soul-agents` contém uma versão **compacta** do SOUL de cada agente (exceto CEO, que já tem SOUL completo em [openclaw/workspace-ceo-configmap.yaml](../openclaw/workspace-ceo-configmap.yaml)). Uso: montar em um volume no deployment OpenClaw (ex.: `/workspace/soul/`) para que cada agente possa carregar sua identidade (SOUL) como system prompt ou customInstructions, conforme suporte do OpenClaw.

- **CEO:** SOUL em `openclaw-workspace-ceo` (SOUL.md no workspace do CEO).
- **Demais agentes:** Conteúdo em `soul-agents` (chaves `po.md`, `devops.md`, `architect.md`, `developer.md`, `qa.md`, `cybersec.md`, `ux.md`, `dba.md`).

Documentação completa dos SOUL em [docs/soul/](../../docs/soul/). Referência: [docs/issues/011-soul-identidade-prompts.md](../../docs/issues/011-soul-identidade-prompts.md).
