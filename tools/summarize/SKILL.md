# 📄 summarize

**Objetivo:** Resumir URLs, PDFs, imagens, áudio, YouTube e texto longo para processamento por LLM ou RAG.  
**Quando usar:** Redução de contexto no pipeline de truncamento, resumos executivos do CEO/PO, pré-processamento de documentos externos.  
**Referência:** `docs/12-ferramenta-summarize.md`

---

## ⚠️ Restrição crítica — itens que NUNCA passam pelo summarize

| Item | Motivo |
|------|--------|
| **microADRs** | São preservados integralmente na memória Elite (never_summarize=true); ver `memory/warm/` |
| **Invariantes de negócio** (tag `<!-- INVARIANTE -->`) | Nunca truncados; protegidos por regex no pipeline |
| **Critérios de aceite** (tag `<!-- CRITERIOS_ACEITE -->`) | Separados do payload antes do truncamento |
| **Chaves e segredos** | Nunca passam por APIs externas |

---

## Instalação

```bash
# markitdown (conversão de formatos → Markdown para LLM/RAG)
pip install markitdown[all]
# ou via uvx (sem instalar globalmente):
uvx markitdown <arquivo>

# Para resumo via Ollama local (sem custo de API):
# Usar o pipeline de truncamento já implementado em:
# orchestrator/gateway/gateway.py → ContextTruncator
```

---

## Passos

### 1. Identificar o tipo de fonte

| Fonte | Ferramenta |
|-------|------------|
| URL pública | `markitdown <url>` ou `uvx markitdown <url>` |
| PDF, Word, PowerPoint, Excel | `uvx markitdown <arquivo.pdf>` |
| Imagem (OCR) | `uvx markitdown <imagem.png>` |
| Áudio (transcrever) | `python scripts/m4a_to_md.py <arquivo.m4a>` |
| YouTube | `uvx markitdown <url-youtube>` |
| EPUB, ZIP | `uvx markitdown <arquivo.epub>` |

### 2. Converter para Markdown

```bash
uvx markitdown documento.pdf > documento.md
uvx markitdown https://example.com/artigo > artigo.md
uvx markitdown video.mp4 > transcricao.md
```

### 3. Resumir com Ollama local (sem custo)

```bash
# Usando Ollama local (GPU Lock necessário para agentes técnicos):
cat documento.md | head -200 | ollama run phi3:mini "Resuma em PT-BR, máx 300 palavras:"

# Ou via pipeline de truncamento automático:
# gateway.py → ContextTruncator.truncate() já faz isso automaticamente
```

### 4. Verificar invariantes antes de resumir

```python
# Antes de resumir qualquer texto, verificar se contém tags protegidas:
from orchestrator.gateway.gateway import ContextTruncator
truncator = ContextTruncator()
clean_payload, criteria = truncator.protect_acceptance_criteria(texto)
truncated, was_truncated = truncator.truncate(clean_payload)
```

---

## Formatos suportados (markitdown)

| Formato | Extensões |
|---------|-----------|
| Documentos | `.pdf`, `.docx`, `.doc`, `.pptx`, `.ppt`, `.xlsx`, `.xls` |
| Web | `.html`, URLs públicas |
| Imagens (OCR) | `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp` |
| Áudio | `.mp3`, `.wav`, `.m4a`, `.ogg` |
| Vídeo | `.mp4`, `.webm` (extrai áudio) |
| Outros | `.epub`, `.zip` (extrai e converte conteúdo), YouTube URLs |

---

## Integração com o pipeline de truncamento

O pipeline de truncamento (`orchestrator/gateway/gateway.py`) usa `ContextTruncator` automaticamente:

1. **Pre-flight:** Para eventos com > 3 interações acumuladas, resume antes de enviar à nuvem
2. **Proteção de invariantes:** Critérios de aceite e microADRs são separados antes do truncamento
3. **Estimativa de tokens:** 1 token ≈ 4 caracteres (aproximação conservadora)
4. **TTL working buffer:** Contexto com TTL de 24h no Redis (expiração automática)

```python
# Exemplo de uso direto:
from orchestrator.gateway.gateway import ContextTruncator
t = ContextTruncator(max_tokens=4000)
resumido, foi_truncado = t.truncate(texto_longo)
```

---

## Uso por agente

| Agente | Caso de uso |
|--------|-------------|
| **CEO** | Resumo executivo de relatórios, artigos, pesquisas de mercado |
| **PO** | Resumo de especificações externas, documentos de requisitos |
| **Developer** | Converter documentação técnica para consulta por LLM |
| **Architect** | Resumo de RFCs, documentação de bibliotecas |
| **QA** | Resumo de relatórios de teste longos |

---

## Boas práticas

- Prefira resumo **local** (Ollama Phi-3 Mini em CPU) para reduzir custo de API
- **Nunca** passe microADRs, invariantes ou segredos pelo resumo
- Para documentos > 100 páginas: dividir em seções e resumir por partes
- Salvar o Markdown gerado no working buffer Redis (TTL 24h) para reutilização
