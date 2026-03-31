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

# Context Engine Configuration

## Purpose

Define how the OpenClaw context engine selects and assembles context for each agent run. Context must remain below token limits while preserving the most relevant information.

## Architecture

```
┌──────────────────────────────────────────┐
│  SESSION (persistent on disk)            │
│  - Full message history (unbounded)      │
│  - Memory entries (user, agent state)    │
│  - Workspace files and artifacts         │
└────────────┬─────────────────────────────┘
             │ Context Engine (smart selection)
             ↓
    ┌────────────────────────┐
    │  CONTEXT WINDOW        │
    │  (for this run)        │
    │  Max ~100k tokens      │
    ├────────────────────────┤
    │ + System Prompt        │
    │ + Recent Messages      │
    │ + Top K Memories       │
    │ + Essential Artifacts  │
    └────────────┬───────────┘
                 │
                 ↓
        ┌────────────────────┐
        │  LLM INFERENCE     │
        └────────────────────┘
```

## Configuration Schema

```yaml
context:
  # Hard limit on context window size (tokens)
  # Prevents OOM and excessive cost
  maxTokens: 100000

  # Maximum number of recent messages to always include
  # Provides continuity of conversation
  # Typical values: 15-30
  recencyWindow: 20

  # Token budget for recency bias
  # Reserve tokens for recent messages before considering old ones
  recencyTokenBudget: 10000

  # Number of memories to include (ranked by relevance)
  # Memories are scored by relevance to current query
  memoryTopK: 5

  # Token budget for memories
  # Memories are concise but valuable
  memoryTokenBudget: 5000

  # Prioritize memory entries over old messages
  # Memory = distilled insights; old messages = raw history
  prioritizeMemory: true

  # Minimum relevance score to include an old message (0-1)
  # If relevanceScore < this, message is excluded
  relevanceThreshold: 0.6

  # Strategy for selecting from old messages
  # "relevance": rank by relevance to query
  # "timescale": geometric distribution (recent weighted higher)
  selectionStrategy: "relevance"

  # Scoring model for relevance (if available)
  # Leave empty to use basic keyword matching
  relevanceScorerModel: "nomic-embed-text"

  # Include which artifact types
  artifacts:
    workspaceFiles: true          # .md, .yaml, etc from workspace
    recentErrorLogs: true         # Last 10 errors
    contextualMetadata: true      # Workspace state, env vars
    sessionMetadata: true         # Session info, timestamps

  # Token budget for artifacts
  artifactTokenBudget: 8000

monitoring:
  # Log context assembly for debugging
  logContextAssembly: false

  # Alert if context window exceeds % of max
  alertThresholdPercent: 90

  # Track context statistics per agent
  trackMetrics: true

  # Dump full context to file on every run (debug)
  dumpContextOnRun: false
```

## Per-Agent Overrides

Specialized agents may need different context strategies:

```yaml
# CEO (orchestrator) — needs broad context
agents:
  ceo:
    context:
      maxTokens: 120000
      recencyWindow: 30          # More recent history needed
      memoryTopK: 10             # More strategic memory
      prioritizeMemory: true

  # Dev Backend — focused on code
  dev_backend:
    context:
      maxTokens: 100000
      recencyWindow: 15          # Less chat history
      memoryTopK: 3              # Code patterns only
      artifacts:
        workspaceFiles: true     # Include code snippets
        recentErrorLogs: true
        contextualMetadata: true

  # QA Engineer — needs test context
  qa_engineer:
    context:
      maxTokens: 95000
      recencyWindow: 20
      memoryTopK: 4
      artifacts:
        workspaceFiles: true     # Include test files
        recentErrorLogs: true
        sessionMetadata: true

  # Memory Curator — sees everything
  memory_curator:
    context:
      maxTokens: 150000          # Larger window for compaction analysis
      recencyWindow: 50
      memoryTopK: 20             # All memories to consolidate
```

## Runtime Commands

Monitor context via Gateway CLI:

```bash
# Show current context for session
openclaw context status --session user:12345

# Show context assembly strategy
openclaw context strategy --agent dev_backend

# Force context dump (debug)
openclaw context dump --session user:12345 --output /tmp/ctx.json

# Show metrics
openclaw context metrics --period 24h --agent ceo
```

## Best Practices

1. **Keep recent messages**: Always include last N messages (20 is typical)
2. **Use memory for patterns**: Store insights in memory, not full chat history
3. **Compress aggressively**: After 30 days, summarize to single entry
4. **Monitor token usage**: Alert at 90% of max; act at 95%
5. **Test relevance scoring**: Wrong scores waste tokens on irrelevant data
6. **Per-agent tuning**: CEO needs more context than Dev Backend
7. **Measure impact**: Track if context changes improve latency/cost

## Examples

### Example 1: High-Context Agent (CEO)

```yaml
# CEO needs full picture for orchestration
context:
  maxTokens: 120000
  recencyWindow: 30           # Keep 30 recent msgs
  recencyTokenBudget: 15000
  memoryTopK: 10              # 10 most relevant memories
  memoryTokenBudget: 8000
  prioritizeMemory: true
  selectionStrategy: "relevance"
  artifacts:
    workspaceFiles: true
    recentErrorLogs: true
    contextualMetadata: true
    sessionMetadata: true
  artifactTokenBudget: 20000
```

### Example 2: Low-Context Agent (Dev Backend)

```yaml
# Dev Backend focused on code, not history
context:
  maxTokens: 85000            # Smaller window
  recencyWindow: 10           # Recent msgs only
  recencyTokenBudget: 8000
  memoryTopK: 2               # Minimal memories
  memoryTokenBudget: 3000
  prioritizeMemory: false
  selectionStrategy: "relevance"
  artifacts:
    workspaceFiles: true      # Include code
    recentErrorLogs: true
    contextualMetadata: false # Less metadata
    sessionMetadata: false
  artifactTokenBudget: 12000
```

## Troubleshooting

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Context exceeds max | Too many recent msgs or memories | Lower `recencyWindow` or `memoryTopK` |
| Missing context | Relevance threshold too high | Lower `relevanceThreshold` |
| Slow inference | Token count too high | Reduce `maxTokens` or compress more |
| Agent loses continuity | `recencyWindow` too small | Increase from 20 to 30 |
| Stale insights in context | Memory not being refreshed | Check Memory Curator compaction |

