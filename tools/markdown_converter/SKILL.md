# 📝 markdown-converter (markitdown)

**Objetivo:** Converter PDF, Word, PowerPoint, Excel, HTML, imagens, áudio, YouTube e EPUB para Markdown legível por LLM e RAG.  
**Quando usar:** Pré-processamento de documentação externa, geração de microADRs, pipeline de RAG, resumos executivos.  
**Referência:** `docs/27-ferramenta-markdown-converter.md`

---

## Instalação

```bash
# Via pip (global)
pip install markitdown[all]

# Via uvx (sem instalar, executa direto — recomendado para pods efêmeros)
uvx markitdown <arquivo>

# Verificar instalação
uvx markitdown --version
```

---

## Passos

### 1. Converter documento para Markdown

```bash
# PDF
uvx markitdown relatorio.pdf > relatorio.md

# Word / PowerPoint / Excel
uvx markitdown especificacao.docx > especificacao.md
uvx markitdown apresentacao.pptx > apresentacao.md
uvx markitdown planilha.xlsx > planilha.md

# URL pública
uvx markitdown https://example.com/doc > doc-externo.md

# YouTube (transcrição automática de legendas)
uvx markitdown https://youtube.com/watch?v=xxxx > transcricao-video.md

# Imagem (OCR)
uvx markitdown diagrama.png > diagrama.md

# EPUB / ZIP
uvx markitdown livro.epub > livro.md
uvx markitdown pacote.zip > conteudo.md
```

### 2. Integrar com pipeline RAG

```bash
# Converter + salvar no working buffer (pipeline RAG)
uvx markitdown doc.pdf | head -500 > /app/memory/warm/summaries/doc-$(date +%Y%m%d).md
```

### 3. Architect: gerar microADR ao aprovar PR

```bash
# Após revisão de PR, Architect gera microADR estruturado:
cat pr-diff.md | uvx markitdown -  # Normalizar formato se necessário

# Ou diretamente via Python:
python -c "
from memory.hot.elite_memory import WarmStore
from pathlib import Path

store = WarmStore()
store.create_adr(
    adr_id='ADR-042',
    title='Usar JWT com refresh token rotativo',
    decision='Implementar JWT com rotação automática de refresh token a cada 7 dias.',
    rationale='Taxa de 0 incidentes em produção com refresh rotativo em últimos 3 projetos analisados.',
    consequences='Sessões encerram em 7d; clientes mobile precisam de UX de re-login.',
    agent='Architect',
)
"
```

> **Invariante:** microADRs gerados pelo Architect via markitdown são armazenados com `_never_summarize=True` e nunca passam pelo pipeline de truncamento.

---

## Formatos suportados

| Formato | Extensão / Fonte |
|---------|-----------------|
| PDF | `.pdf` |
| Word | `.docx`, `.doc` |
| PowerPoint | `.pptx`, `.ppt` |
| Excel | `.xlsx`, `.xls` |
| HTML / Web | `.html`, `.htm`, URLs |
| Imagens (OCR) | `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp` |
| Áudio | `.mp3`, `.wav`, `.m4a`, `.ogg` |
| Vídeo | `.mp4`, `.webm` |
| YouTube | URLs do YouTube |
| EPUB | `.epub` |
| ZIP | `.zip` (extrai e converte conteúdo textual) |

---

## Integração por agente

| Agente | Caso de uso principal |
|--------|----------------------|
| **CEO** | Resumo de relatórios de mercado, PDFs estratégicos, vídeos de conferência |
| **PO** | Converter especificações externas (Word/PDF) para Issues estruturadas |
| **Architect** | Gerar microADR após aprovação de PR; normalizar RFCs e documentação técnica |
| **Developer** | Converter documentação de bibliotecas para consulta local sem API |
| **QA** | Converter relatórios de teste (Excel/PDF) para análise |

---

## Boas práticas

- Usar `uvx markitdown` (sem instalação) nos pods efêmeros para manter imagem enxuta
- Salvar markdown convertido no `memory/warm/summaries/` com TTL no Redis
- **Architect** deve gerar microADR para toda decisão técnica relevante aprovada em PR
- Não passar conteúdo sensível (contratos, dados pessoais) por APIs externas de OCR
- Registrar gotchas de conversão em `memory/warm/TOOLS.md`
