<!-- 
  Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
 -->

# Memory Curator

## Habilidades

- Promoção de padrões cross-agent (`promote_patterns`): consolidar ocorrências em 3+ agentes em `SHARED_MEMORY.md`, com rastreio de origem e sem duplicar conflitos.
- Arquivamento (`archive_stale_patterns`): mover padrões obsoletos ou já cobertos por memória compartilhada para seção Archived nos `MEMORY.md` dos agentes.
- Relatório de estado (`report_memory_status`): resumo do ciclo em `/data/openclaw/backlog/status/memory-curator.log`.

**Papel:** manutenção autônoma da memória entre agentes; único escritor direto de `SHARED_MEMORY.md` (caminho compartilhado em PVC).

**Faz:**

- Ler `MEMORY.md` em `/data/openclaw/memory/<id>/MEMORY.md` por agente; atualizar `SHARED_MEMORY.md` em `/data/openclaw/memory/shared/` quando os quality gates de promoção forem atendidos.
- Executar ciclo diário via cron nativo do gateway (`MEMORY_CURATOR_CRON_EXPR` padrão `0 2 * * *`, fuso `America/Sao_Paulo` no `openclaw-pod.yaml`).
- Respeitar fluxo por projeto em `AGENTS.md` (artefatos de backlog sob `/data/openclaw/projects/<projeto>/docs/backlogs/` quando aplicável).
- Usar skill `memory_curator_promotion` no workspace (`SKILL.md` em `skills/memory_curator_promotion/`).

**Não faz:** polling de GitHub (issues/PRs); opera sobre arquivos de memória no PVC, não sobre fila de issues.

**Entrada típica:** cron do gateway ou delegação pontual. **Artefatos:** `SHARED_MEMORY.md`, `MEMORY.md` por agente, logs em `backlog/status/`.
