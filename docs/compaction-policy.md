# Compaction Policy (ETAPA 2)

Este documento define a politica de compaction para memoria dos agentes no Clawdevs AI.

## Quando compactar
- Ao final de cada task concluida (gatilho padrao).
- Quando a memoria do agente ultrapassar o limite de contexto configurado no Context Mode.
- Antes de iniciar uma nova task se a ultima compaction foi ha mais de 24h.

## Quem executa
- Execucao automatica pelo Context Mode no runtime do agente.
- O agente Arquiteto valida quando ha conflito ou risco de perda de contexto.

## Fluxo de compaction (resumo)
1. Memory flush: salva a memoria atual em disco.
2. Resumo incremental: agrega os ultimos eventos relevantes em 1-3 linhas.
3. Persistencia: atualiza `/data/openclaw/memory/<agent>/MEMORY.md`.
4. Registro: grava evidencia no log estruturado de artifacts.

## Memorias antigas
- Devem ser resumidas e compactadas.
- Manter historico em disco por agente (na pasta memory), sem expirar.

## Prova suficiente de compaction
Para considerar OK, devem existir os 3 itens abaixo:
- Log estruturado com evento `compaction_completed` contendo: `agent_id`, `task_id`, `timestamp`, `input_tokens`, `output_tokens`, `summary_hash`.
- Lista de arquivos alterados (ex.: MEMORY.md + diario).
- Hash SHA256 do arquivo `MEMORY.md` apos compaction registrado no log.

## Merge/versionamento em conflito
- Se houver conflito de memoria, o Arquiteto decide a resolucao e registra a justificativa no log.

