"""Semantic Optimization API endpoints for Ollama-enhanced optimization."""
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import get_settings
from app.core.database import get_session
from app.services.query_enhancer import QueryEnhancer
from app.services.semantic_ranker import SemanticRanker
from app.services.adaptive_compressor import AdaptiveCompressor
from app.services.summarizer import IntelligentSummarizer
from app.services.categorizer import MemoryCategorizer
from app.services.anomaly_detector import AnomalyDetector
from app.services.context_suggester import ContextSuggester
from app.services.ollama_client import OllamaClient
from app.services.semantic_optimization_flags import flags
from app.services.context_metrics import context_tracker

# NOTE: No leading /api — Next.js proxies /api/* → backend /* (path after /api/).
router = APIRouter(prefix="/context-mode/semantic-optimization", tags=["semantic-optimization"])

# Service instances (singleton-like)
query_enhancer = QueryEnhancer()
semantic_ranker = SemanticRanker()
adaptive_compressor = AdaptiveCompressor()
summarizer = IntelligentSummarizer()
categorizer = MemoryCategorizer()
anomaly_detector = AnomalyDetector()
context_suggester = ContextSuggester()
ollama_client = OllamaClient()


def _semantic_ui_metrics_from_tracker(summary: Dict[str, Any]) -> Dict[str, Any]:
    """Map context_tracker summary to dashboard card shape expected by the frontend."""
    per_task = summary.get("per_task") or {}

    def ex(task_key: str) -> int:
        block = per_task.get(task_key)
        if isinstance(block, dict):
            return int(block.get("executions", 0) or 0)
        return 0

    def ratio_pct(task_key: str) -> str:
        block = per_task.get(task_key)
        if not isinstance(block, dict):
            return "0%"
        b = float(block.get("baseline_tokens", 0) or 0)
        opt = float(block.get("optimized_tokens", 0) or 0)
        if b <= 0:
            return "0%"
        saved = max(0.0, (b - opt) / b * 100.0)
        return f"{saved:.1f}%"

    return {
        "query_enhancements": {
            "total_queries": ex("query_enhancement"),
            "avg_expansion_terms": float(ex("query_enhancement")),
            "semantic_coverage_improvement": ratio_pct("query_enhancement"),
        },
        "semantic_reranking": {
            "total_reranks": ex("semantic_reranking"),
            "avg_rerank_improvement": ratio_pct("semantic_reranking"),
            "latency_p95": "—",
        },
        "intelligent_summarization": {
            "chunks_summarized": ex("auto_compression_pipeline") + ex("summarization"),
            "avg_reduction": (
                ratio_pct("auto_compression_pipeline")
                if ex("auto_compression_pipeline")
                else ratio_pct("summarization")
            ),
            "information_preservation": "—",
        },
        "auto_categorization": {
            "chunks_categorized": ex("categorization"),
            "top_category": "—",
            "categorization_confidence_avg": "—",
        },
        "anomaly_detection": {
            "anomalies_detected": ex("anomaly_detection"),
            "critical_anomalies": 0,
            "compression_skips": 0,
        },
        "context_suggestions": {
            "suggestions_offered": ex("context_suggestion"),
            "acceptance_rate": ratio_pct("context_suggestion"),
            "avg_relevance_score": "—",
        },
    }


@router.post("/enhance-query")
async def enhance_query(query: str, agent_id: str):
    """Expand query with semantic variations."""
    if not query or len(query) < 2:
        raise HTTPException(status_code=400, detail="Query too short")

    if not flags.is_enabled("query_enhancement", agent_id):
        raise HTTPException(
            status_code=503,
            detail="Query enhancement feature is not enabled",
        )

    agent_context = agent_id  # Could fetch from DB
    result = await query_enhancer.enhance_query(query, agent_context)
    return result


@router.post("/rerank-results")
async def rerank_results(query: str, chunks: list[str], bm25_scores: list[float] = None):
    """Rerank chunks by semantic relevance."""
    if not chunks or not query:
        raise HTTPException(status_code=400, detail="Missing query or chunks")

    if not bm25_scores:
        bm25_scores = [0.5] * len(chunks)

    result = await semantic_ranker.rerank(query, chunks, bm25_scores, top_k=5)
    return {"reranked": [{"chunk": c[:200], "score": s} for c, s in result]}


@router.post("/classify-output")
async def classify_output(output: str, tool_name: str = ""):
    """Classify output type and select compression strategy."""
    if not output:
        raise HTTPException(status_code=400, detail="Output required")

    result = await adaptive_compressor.compress_adaptive(output, tool_name)
    return result


@router.post("/summarize")
async def summarize(content: str, intent: str = None, max_words: int = 100):
    """Summarize content intelligently."""
    if not content:
        raise HTTPException(status_code=400, detail="Content required")

    result = await summarizer.summarize(content, intent, max_words)
    return result


@router.post("/categorize")
async def categorize(content: str):
    """Auto-categorize memory chunk."""
    if not content:
        raise HTTPException(status_code=400, detail="Content required")

    result = await categorizer.categorize(content)
    return result


@router.post("/detect-anomaly")
async def detect_anomaly(output: str, tool_name: str = ""):
    """Detect anomalies in tool output."""
    if not output:
        raise HTTPException(status_code=400, detail="Output required")

    result = await anomaly_detector.detect(output, tool_name)
    return result


@router.post("/suggest-context")
async def suggest_context(tool_name: str, args: str, candidate_memories: list[dict] = None):
    """Suggest relevant memories for agent action."""
    if not tool_name:
        raise HTTPException(status_code=400, detail="Tool name required")

    if not candidate_memories:
        candidate_memories = []

    result = await context_suggester.suggest_context(tool_name, args, candidate_memories)
    return result


@router.get("/ollama-health")
async def ollama_health():
    """Check Ollama server health."""
    settings = get_settings()
    online = await ollama_client.health_check()
    return {
        "status": "active" if online else "unavailable",
        "model": ollama_client.model,
        "online": online,
        "base_url": settings.ollama_base_url,
    }


@router.get("/metrics")
async def semantic_optimization_metrics(session: AsyncSession = Depends(get_session)):
    """Get semantic optimization context metrics (compression tracking)."""
    summary = context_tracker.get_summary()
    ollama_ok = await ollama_client.health_check()
    ui = _semantic_ui_metrics_from_tracker(summary)

    return {
        "context_compression": summary,
        "ollama_status": "active" if ollama_ok else "unavailable",
        "model": ollama_client.model,
        **ui,
    }


@router.get("/feature-flags")
async def get_feature_flags():
    """Get all semantic optimization feature flags status."""
    return {
        "flags": flags.get_all_status(),
        "canary_agents": flags.get_canary_agents(),
    }


@router.get("/feature-flags/{task_name}")
async def check_task_enabled(task_name: str, agent_id: str = None):
    """Check if a specific task is enabled for an agent."""
    is_enabled = flags.is_enabled(task_name, agent_id)
    return {
        "task": task_name,
        "agent_id": agent_id,
        "enabled": is_enabled,
        "canary": agent_id in flags.canary_agents if agent_id else False,
    }
