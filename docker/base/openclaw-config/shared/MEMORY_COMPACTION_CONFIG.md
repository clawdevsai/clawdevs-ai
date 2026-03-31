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

# Memory Compaction Configuration

## Purpose

Define how agent memories evolve over time. Memories compress to preserve essential insights while removing detail that becomes stale.

## Memory Lifecycle

```
CREATION (Day 1-7)
  ├─ Full detail + context
  └─ Example: "User debugged race condition in auth handler, added mutex lock"

COMPRESSION (Day 8-30)
  ├─ Pattern extraction
  └─ Example: "User experienced concurrency bugs; prefers mutex-based locking"

SUMMARIZATION (Day 31-90)
  ├─ Insight distillation
  └─ Example: "User: Python backend dev, focuses on thread safety, prefers clear error handling"

ARCHIVAL (Day 91+)
  ├─ Super-summary
  └─ Example: "User: Sr backend dev (Python), code quality focus, 5+ projects completed"
```

## Configuration Schema

```yaml
memory:
  # Storage backend
  backend: "file"              # "file" | "postgres"
  storageLocation: "/data/openclaw/memory"

  # Memory entry structure
  entry:
    # Required fields
    fields:
      - id                     # Unique identifier
      - subject                # Who (user, agent, pattern)
      - content                # What (the actual insight)
      - createdAt              # When created
      - lastUpdated            # Last modified
      - confidence             # 0-1 score of reliability
      - source                 # Where discovered (session, skill, etc)
      - expiresAt              # When to review/delete

    # Max length of memory content (characters)
    # Enforces conciseness
    maxContentLength: 500

  # Compaction schedule
  compaction:
    # Enable automatic compaction
    enabled: true

    # Run compaction daily at this time (UTC)
    schedule: "03:00"

    # Agent responsible for compaction
    agent: "memory_curator"

  # Compaction timeline
  timeline:
    # Phase 1: Creation (Days 1-7)
    # Full detail, context, examples
    creation:
      duration: "7d"
      maxContentLength: 500
      compressionRatio: 1.0     # No compression

    # Phase 2: Compression (Days 8-30)
    # Pattern extraction, example removal
    compression:
      duration: "23d"           # 30 - 7
      maxContentLength: 300
      compressionRatio: 0.6     # 40% reduction
      merge:
        # Merge similar memories during compression
        enabled: true
        # Similarity threshold (0-1)
        threshold: 0.75

    # Phase 3: Summarization (Days 31-90)
    # Insight distillation, lose temporal details
    summarization:
      duration: "60d"           # 90 - 30
      maxContentLength: 150
      compressionRatio: 0.3     # 70% reduction
      consolidate:
        # Group 3-5 related memories into 1 summary
        groupSize: 4

    # Phase 4: Archival (Day 91+)
    # Super-summary, keep only highest-level insights
    archival:
      maxContentLength: 80
      compressionRatio: 0.2     # 80% reduction
      keepFor: "365d"           # Keep archived for 1 year

  # Extraction rules during compression
  extraction:
    # Extract these types of insights
    patterns:
      # Technology preferences: "User prefers X over Y"
      - type: "preference"
        weight: 1.0

      # Problem-solving patterns: "User approaches X by doing Y"
      - type: "pattern"
        weight: 0.9

      # Constraints: "User works with constraint X"
      - type: "constraint"
        weight: 0.8

      # Capabilities: "User skilled in X"
      - type: "capability"
        weight: 0.9

      # Context: "User working on project X"
      - type: "context"
        weight: 0.7

    # Discard these (low value over time)
    exclude:
      - "specific_file_names"
      - "temporary_decisions"
      - "debugging_steps"
      - "implementation_details"

  # Consolidation rules
  consolidation:
    # After how many similar entries, consolidate?
    threshold: 3

    # Consolidation template
    # {count} entries merged into {title}
    template: "{count} related insights → {title}"

    # Example consolidation
    example:
      - entry1: "Debugged TypeScript error in auth module"
      - entry2: "Fixed type mismatch in validation handler"
      - entry3: "Resolved type inference issue in API layer"
      - consolidatedTo: "User: TypeScript expertise, focuses on type safety"
```

## Per-Agent Memory Policies

Different agents track different things:

```yaml
agents:
  dev_backend:
    memory:
      # Track code patterns, bugs, learnings
      subjects:
        - "code_patterns"
        - "bug_patterns"
        - "performance_insights"
      compaction:
        timeline:
          creation:
            duration: "14d"        # Keep longer (code context matters)
          compression:
            duration: "30d"
          summarization:
            duration: "60d"
        extraction:
          patterns:
            - type: "pattern"
              weight: 1.0          # High weight on patterns
            - type: "capability"
              weight: 0.9

  qa_engineer:
    memory:
      # Track test strategies, bug patterns
      subjects:
        - "test_patterns"
        - "bug_categories"
        - "edge_cases"
      compaction:
        timeline:
          creation:
            duration: "7d"
          compression:
            duration: "21d"
        extraction:
          patterns:
            - type: "pattern"
              weight: 1.0
            - type: "constraint"
              weight: 0.8

  memory_curator:
    memory:
      # Track org-wide patterns
      subjects:
        - "team_patterns"
        - "common_issues"
        - "consolidated_insights"
      compaction:
        # Curator consolidates, doesn't compress its own memory much
        timeline:
          archival:
            keepFor: "730d"        # Keep for 2 years
```

## Compaction Examples

### Example 1: Code Pattern Consolidation

**Before (Days 1-7)**
```
Memory: "User fixed race condition in auth handler by adding mutex lock"
- Content length: 80 chars
- Detail: specific file, specific fix
- Confidence: 1.0
```

**After Compression (Days 8-30)**
```
Memory: "User: experienced with concurrency bugs; uses mutex-based locks"
- Content length: 65 chars
- Detail: pattern-level
- Confidence: 0.95
```

**After Summarization (Days 31-90)**
```
Memory: "User: Python backend dev; focuses on thread safety"
- Content length: 52 chars
- Detail: capability-level
- Confidence: 0.9
```

### Example 2: Bug Pattern Consolidation

**Days 1-7 (Creation)**
```
- "Debugged TypeScript error in auth validator"
- "Fixed type mismatch in API middleware"
- "Resolved union type issue in request handler"
Total: 3 memories, ~150 chars each
```

**Days 8-30 (Compression)**
```
Merged into: "User: TypeScript expertise in type safety; focuses on strict validation"
Total: 1 memory, ~75 chars
Reduction: 67% (3 → 1)
```

**Days 31-90 (Summarization)**
```
Merged into: "User: Sr TypeScript dev; prioritizes type safety"
Total: 1 memory, ~50 chars
Reduction: 33% more (75 → 50)
```

## Memory Types & Retention

```yaml
memory_types:
  # User preferences: long retention
  preference:
    compaction:
      timeline:
        archival:
          keepFor: "365d"
    example: "User prefers Python over Go for backend work"

  # Capability: long retention
  capability:
    compaction:
      timeline:
        archival:
          keepFor: "180d"
    example: "User: expert in Rust systems programming"

  # Problem patterns: medium retention
  pattern:
    compaction:
      timeline:
        archival:
          keepFor: "90d"
    example: "User encounters race conditions in concurrent code"

  # Context: short retention
  context:
    compaction:
      timeline:
        archival:
          keepFor: "30d"
    example: "User currently working on mobile payment system"

  # Implementation details: very short
  detail:
    compaction:
      timeline:
        archival:
          keepFor: "7d"
    example: "Fixed bug in line 42 of auth.py"
```

## Monitoring

```bash
# Show memory statistics per agent
openclaw memory stats --agent dev_backend

# Show memories scheduled for compaction
openclaw memory compact-schedule

# Export memory before compaction
openclaw memory export --agent dev_backend --output /tmp/memory.json

# View compaction history
openclaw memory history --agent memory_curator --days 30

# Show memory usage
openclaw memory usage --breakdown
```

## Best Practices

1. **Extract early**: Identify patterns in creation phase (days 1-7)
2. **Compress aggressively**: Remove details that don't inform future decisions
3. **Consolidate related**: Merge 3-5 similar memories into patterns
4. **Keep capabilities**: Skill/expertise info has high long-term value
5. **Discard temporal**: Dates, specific files lose value after 30 days
6. **Trust confidence scores**: Use 0-1 score to weight retention decisions
7. **Review quarterly**: Check archived memories for organizational patterns

## Storage Implications

```
Memory growth over time:

User with 100 daily interactions:
- Days 1-7:     ~5000 characters
- Days 1-30:    ~8000 characters (creation) → ~5000 (compressed)
- Days 1-90:    ~20000 characters → ~6000 (summarized)
- Days 1-365:   ~100000 characters → ~8000 (archived)

Compression ratio: 92% reduction after 1 year
```

