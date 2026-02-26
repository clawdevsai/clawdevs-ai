# 🦙 ollama-local — Gestão e uso de modelos locais

**Objetivo:** Gerenciar e usar modelos Ollama no cluster: listar, baixar, remover, inferir (chat, embeddings, tool use). GPU Lock obrigatório antes de qualquer chamada de inferência.  
**Quando usar:** Inferência local sem custo de API, embeddings para RAG, tool use estruturado.  
**Referência:** `docs/31-ollama-local.md`

---

## Pré-requisitos

```bash
# Ollama deve estar em execução no cluster (pod ollama no namespace ai-agents)
kubectl get pods -n ai-agents -l app=ollama

# Port-forward para acesso local (desenvolvimento)
kubectl port-forward -n ai-agents svc/ollama 11434:11434 &

# Verificar modelos disponíveis
ollama list
```

---

## Passos

### 1. Gerenciar modelos

```bash
# Listar modelos instalados
ollama list

# Baixar modelo (DevOps executa; outros agentes solicitam)
ollama pull deepseek-coder:6.7b    # Developer
ollama pull llama3:8b              # Architect, QA, DBA
ollama pull phi3:mini              # DevOps, UX (CPU)
ollama pull mistral:7b             # CyberSec

# Remover modelo (liberar espaço no PVC)
ollama rm modelo-antigo:versao

# Ver informações do modelo
ollama show llama3:8b
```

### 2. Adquirir GPU Lock antes de chamar Ollama (obrigatório)

```python
# Sempre usar GPU Lock antes de chamar Ollama para inferência
from scripts.gpu_lock import gpu_lock

with gpu_lock(event_key="issue:42"):
    # Sua chamada ao Ollama aqui
    response = ...
```

```bash
# Verificar se lock está ativo
redis-cli get gpu_active_lock
```

### 3. Inferência via API REST

```bash
# Chat completions
curl http://ollama:11434/api/chat -d '{
  "model": "llama3:8b",
  "messages": [{"role": "user", "content": "Revise este código:"}],
  "stream": false
}'

# Generate (prompt único)
curl http://ollama:11434/api/generate -d '{
  "model": "deepseek-coder:6.7b",
  "prompt": "Implemente uma função Python para...",
  "stream": false
}'
```

### 4. Inferência via Python

```python
import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

def chamar_ollama(prompt: str, model: str = "llama3:8b") -> str:
    """Chamar Ollama com GPU Lock. Usar dentro de `with gpu_lock()`."""
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")

# Uso completo com GPU Lock:
from scripts.gpu_lock import gpu_lock

with gpu_lock(event_key="issue:42"):
    resposta = chamar_ollama("Revise este diff:\n...", model="llama3:8b")
```

### 5. Embeddings para RAG

```python
import requests

def gerar_embedding(texto: str, model: str = "llama3:8b") -> list[float]:
    """Gera embedding para armazenamento no LanceDB (memória Elite)."""
    resp = requests.post(
        "http://ollama:11434/api/embeddings",
        json={"model": model, "prompt": texto},
        timeout=30,
    )
    return resp.json().get("embedding", [])
```

### 6. Tool use estruturado

```python
# Ollama suporta tool use (function calling) com modelos compatíveis
payload = {
    "model": "llama3:8b",
    "messages": [{"role": "user", "content": "Qual é o status do PR #42?"}],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_pr_status",
                "description": "Retorna status de um PR do GitHub",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pr_number": {"type": "integer", "description": "Número do PR"}
                    },
                    "required": ["pr_number"]
                }
            }
        }
    ],
    "stream": False,
}
```

---

## Seleção de modelos por agente

| Agente | Modelo | Hardware | Justificativa |
|--------|--------|----------|---------------|
| **Developer** | `deepseek-coder:6.7b` | GPU | Melhor para código |
| **Architect** | `llama3:8b` | GPU | Raciocínio arquitetural |
| **QA** | `llama3:8b` | GPU | Análise de testes |
| **CyberSec** | `mistral:7b` | GPU | Padrões de segurança |
| **DBA** | `llama3:8b` | GPU | SQL e estrutura de dados |
| **DevOps** | `phi3:mini` | CPU | Leveza; sem GPU |
| **UX** | `phi3:mini` | CPU | Leveza; sem GPU |
| **CEO** | Gemini 1.5 Pro | Nuvem | Estratégia complexa |
| **PO** | Gemini 1.5 Flash | Nuvem | Custo menor que Pro |

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `connection refused :11434` | `kubectl get pods -n ai-agents -l app=ollama` + port-forward |
| OOM / crash no pod | Verificar `OLLAMA_MAX_VRAM`; GPU Lock pode estar mal gerenciado |
| `model not found` | `ollama pull <model>` no pod Ollama |
| Timeout na inferência | Aumentar `timeout` na chamada; verificar se GPU Lock está sendo liberado |
| GPU sem acesso | Verificar `nvidia-smi` e toleration no pod |

```bash
# Diagnóstico rápido
kubectl exec -n ai-agents \
  $(kubectl get pods -n ai-agents -l app=ollama -o jsonpath='{.items[0].metadata.name}') \
  -- ollama list

# Verificar GPU no pod
kubectl exec -n ai-agents \
  $(kubectl get pods -n ai-agents -l app=ollama -o jsonpath='{.items[0].metadata.name}') \
  -- nvidia-smi
```
