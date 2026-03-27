# RAG (Retrieval-Augmented Generation) Setup Guide

Semantic memory search using local embeddings via Ollama.

---

## System Requirements

### 1. Ollama (Local Embedding Generation)

**What:** Open-source LLM framework for running models locally
**Why:** Generates free vector embeddings without API costs
**Installation:** https://ollama.ai

```bash
# macOS / Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download

# Start Ollama
ollama serve

# In another terminal, pull the embedding model
ollama pull mistral  # or your preferred model
```

**Verify:**
```bash
curl http://localhost:11434/api/tags
# Should show available models including mistral
```

### 2. PostgreSQL Extensions

**pgvector** enables vector similarity search in PostgreSQL.

```sql
-- Connect to your database
psql -U postgres -d clawdevs_ai

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify
\dx vector
```

**If pgvector not installed:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-15-pgvector

# macOS
brew install pgvector

# Or build from source
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install
```

### 3. Python Dependencies

Add to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
httpx = "^0.24.0"        # For Ollama API calls
requests = "^2.31.0"     # For health checks
pgvector = "^0.2.0"      # For PostgreSQL vector type
```

**Install:**
```bash
cd control-panel/backend
poetry add httpx requests pgvector
poetry install
```

---

## How RAG Works

### 1. Memory Encoding (Done Once)

When a memory is created or updated:
```
Memory Text → Ollama Embedding Model → Vector (1536-dim) → PostgreSQL
```

**Example:**
```python
memory.body = "To handle database migrations, use Alembic..."
embedding = embedding_service.generate_embedding(memory.body)
# embedding = [0.123, -0.456, 0.789, ...]
memory.embedding = json.dumps(embedding)
```

### 2. Query Search (Runtime)

When an agent needs context:
```
Agent Query → Ollama Embedding → Vector Search → Top-K Similar Memories
```

**Example:**
```python
query = "How do we handle database schema changes?"
query_vec = embedding_service.generate_embedding(query)
# Cosine similarity search returns 5 most similar memories
```

### 3. Context Injection

Agents receive retrieved context:
```
Agent Task → RAG Search → Similar Solutions → Inject into Prompt
```

---

## API Endpoints

### Search for Similar Solutions

```bash
GET /api/memory/rag/search?query=database+migration&top_k=5
```

Response:
```json
{
  "query": "database migration",
  "results_count": 5,
  "results": [
    {
      "id": "uuid",
      "title": "Alembic Migration Pattern",
      "body": "To handle migrations...",
      "similarity_score": 0.92,
      "created_at": "2026-03-20T10:00:00"
    },
    ...
  ]
}
```

### Get Agent Context

```bash
GET /api/memory/rag/agent/dev_backend/context?task_description=implement+user+authentication&max_items=5
```

Response:
```json
{
  "agent_slug": "dev_backend",
  "query": "implement user authentication",
  "similar_solutions": [
    "[JWT Implementation Pattern (0.89)] To implement JWT...",
    "[OAuth2 Flow (0.85)] For OAuth2 integration..."
  ],
  "tagged_patterns": ["Authentication Security Checklist"],
  "recommendation": "Use retrieved context as reference..."
}
```

### Health Check

```bash
GET /api/memory/rag/health
```

Response:
```json
{
  "status": "healthy",
  "ollama_available": true,
  "embedding_model": "mistral",
  "message": "RAG system operational"
}
```

---

## Configuration

### Ollama

Environment variables (optional):

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_EMBEDDING_MODEL=mistral
export OLLAMA_TIMEOUT=60
```

Defaults in code:
```python
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_EMBEDDING_MODEL = "mistral"
OLLAMA_TIMEOUT = 60.0
```

### Similarity Threshold

Minimum similarity score to include results (default: 0.5):

```python
# In rag_retriever.py
self.min_similarity_threshold = 0.5  # Adjust as needed
```

**Lower threshold:** More results, some less relevant
**Higher threshold:** Fewer results, higher quality

---

## Performance Tuning

### Embedding Generation

- **First embedding:** ~500ms (model load + inference)
- **Subsequent embeddings:** ~100-200ms each
- **Batch processing:** Use `batch_embed_chunks()` for efficiency

### Similarity Search

- **PostgreSQL ARRAY search:** ~50-100ms for 1000 entries
- **Indexing:** Create index for faster searches

```sql
-- Speed up similarity searches
CREATE INDEX idx_memory_embedding ON memory_entries
  USING IVFFlat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### Optimize for Scale

As memory grows:
1. **Batch indexing:** Regenerate embeddings in chunks (100-500 at a time)
2. **Pruning:** Archive old memories (>90 days unused)
3. **Filtering:** Use `agent_slug` and `entry_type` to narrow search space

---

## Troubleshooting

### "Cannot connect to Ollama"

```
Error: Cannot connect to Ollama at http://localhost:11434
```

**Fix:**
```bash
# 1. Is Ollama running?
ps aux | grep ollama

# 2. Start it
ollama serve

# 3. Pull embedding model
ollama pull mistral

# 4. Test
curl http://localhost:11434/api/tags
```

### "Model not available"

```
Error: Ollama healthy but mistral not available
```

**Fix:**
```bash
# Pull the model
ollama pull mistral

# List available models
ollama ls
```

### "pgvector extension not found"

```sql
CREATE EXTENSION vector;
-- ERROR: could not open extension control file
```

**Fix:**
```bash
# Install pgvector
# macOS
brew install pgvector

# Ubuntu
sudo apt-get install postgresql-15-pgvector

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Slow embedding generation

If embedding takes >5 seconds:
- Check Ollama is healthy: `GET /api/memory/rag/health`
- Increase `OLLAMA_TIMEOUT` if needed
- Consider switching to smaller model: `ollama pull orca-mini`

---

## Model Options

Available free models via Ollama:

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| mistral | 7B | Medium | High |
| llama2 | 7B | Medium | High |
| orca-mini | 3B | Fast | Good |
| neural-chat | 7B | Medium | High |

**Recommendation:** Mistral is good balance of speed/quality

**To switch:**
```bash
ollama pull orca-mini
# Update env or code: OLLAMA_EMBEDDING_MODEL=orca-mini
```

---

## Cost Analysis

### Free (Ollama)

- Embedding generation: **FREE** (runs locally)
- Vector storage: **FREE** (PostgreSQL)
- API calls: **FREE** (localhost)

**Total cost:** $0/month + compute

### Comparison: Paid (OpenAI API)

- Embeddings: $0.02 / 1M tokens
- 1,000 memories x 500 tokens = $0.01/regeneration
- Ongoing searches: Small cost per query

---

## Integration with Agent Workflows

### During Task Execution

```python
# In agent code
from app.services.rag_retriever import RAGRetriever

retriever = RAGRetriever(session)
context = await retriever.get_rag_context(
    agent_slug="dev_backend",
    task_description="implement user authentication",
)

# Inject into LLM prompt
prompt = f"""
You are {agent_slug}. Here's relevant context from past solutions:

{context['similar_solutions']}

Now, {task_description}
"""
```

### Memory Sync with Embeddings

```python
# In memory_sync.py (enhanced)
from app.services.embedding_service import EmbeddingService

embedding_service = EmbeddingService()
for memory in memories_to_sync:
    if not memory.embedding:
        embedding = await embedding_service.generate_embedding(memory.body)
        if embedding:
            memory.embedding = json.dumps(embedding)
            memory.embedding_generated_at = datetime.utcnow()
```

---

## Next Steps

1. ✅ Install Ollama and pull mistral model
2. ✅ Enable pgvector in PostgreSQL
3. ✅ Add Python dependencies
4. ✅ Deploy code changes
5. ✅ Call `/api/memory/rag/health` to verify
6. ✅ Regenerate embeddings: `POST /api/memory/rag/regenerate-embeddings`
7. ✅ Test search: `GET /api/memory/rag/search?query=authentication`

---

## References

- [Ollama GitHub](https://github.com/ollama/ollama)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Vector Similarity Search](https://www.pinecone.io/learn/vector-similarity/)
- [RAG Pattern](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
