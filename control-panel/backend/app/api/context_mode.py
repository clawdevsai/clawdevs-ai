"""
Context Mode API Endpoints
==========================

Endpoints for monitoring context-mode compression metrics
and viewing compression statistics.

Accessible at: /context-mode/
"""

from datetime import datetime, UTC
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from app.core.database import get_session
from app.hooks.tool_executed import get_compression_metrics
from app.models import Agent
from app.services.memory_indexing import get_memory_indexing_service

logger = logging.getLogger("openclaw.api.context_mode")

router = APIRouter(prefix="/context-mode", tags=["context-mode"])


async def build_monitoring_payload(session: AsyncSession) -> Dict[str, Any]:
    """Aggregate compression stats + memory index + agent registry for the monitoring UI."""
    raw = get_compression_metrics() or {}
    memory_service = get_memory_indexing_service()
    memory_metrics = memory_service.get_metrics()
    indexed_rows = memory_service.list_indexed_agents_detail()

    count_stmt = select(func.count(Agent.id))
    total_agents_res = await session.exec(count_stmt)
    total_agents = int(total_agents_res.one())

    name_stmt = select(Agent.slug, Agent.display_name)
    name_pairs = (await session.exec(name_stmt)).all()
    slug_to_display = {slug: name for slug, name in name_pairs}

    indexed_agents = memory_metrics.get("total_indexed_agents", len(indexed_rows))
    if memory_metrics.get("status") != "success":
        indexed_agents = len(indexed_rows)

    agents_out = []
    for row in indexed_rows:
        aid = row["agent_id"]
        mem_b = int(row["memory_size_bytes"] or 0)
        agents_out.append(
            {
                "agent_id": aid,
                "display_name": slug_to_display.get(aid),
                "compression_ratio": 0.0,
                "tokens_saved": int(mem_b / 4 * 0.95) if mem_b else 0,
                "indexed_at": row["last_indexed"],
                "memory_size_bytes": mem_b,
                "status": "indexed",
            }
        )

    last_updated = datetime.now(UTC).replace(tzinfo=None).isoformat()

    if not raw:
        msg = "No compression metrics yet (no large tool outputs detected)"
        if agents_out or total_agents > 0:
            return {
                "status": "success",
                "message": msg,
                "compression_rate": 0.0,
                "tokens_saved_estimate": 0,
                "total_executions": 0,
                "total_compressions": 0,
                "total_agents": total_agents,
                "indexed_agents": indexed_agents,
                "average_compression_ratio": 0.0,
                "monthly_savings_estimate": 0.0,
                "last_updated": last_updated,
                "agents": agents_out,
            }
        return {
            "status": "no_data",
            "message": msg,
            "compression_rate": 0.0,
            "tokens_saved_estimate": 0,
            "total_executions": 0,
            "total_compressions": 0,
            "total_agents": total_agents,
            "indexed_agents": indexed_agents,
            "average_compression_ratio": 0.0,
            "monthly_savings_estimate": 0.0,
            "last_updated": last_updated,
            "agents": agents_out,
        }

    te = int(raw.get("total_executions", 0) or 0)
    tc = int(raw.get("total_compressions", 0) or 0)
    compression_rate = (tc / te) if te > 0 else 0.0
    tse = int(raw.get("tokens_saved_estimate", 0) or 0)
    monthly = float(tse * 30 * 0.0015)

    acr_raw = raw.get("average_compression_ratio", "0")
    acr_float = 0.0
    if isinstance(acr_raw, str) and "%" in acr_raw:
        try:
            acr_float = float(acr_raw.replace("%", "").strip()) / 100.0
        except ValueError:
            acr_float = 0.0
    elif isinstance(acr_raw, (int, float)):
        acr_float = float(acr_raw)

    return {
        "status": "success",
        "compression_rate": compression_rate,
        "tokens_saved_estimate": tse,
        "total_executions": te,
        "total_compressions": tc,
        "total_original_bytes": raw.get("total_original_bytes", 0),
        "total_compressed_bytes": raw.get("total_compressed_bytes", 0),
        "total_agents": total_agents,
        "indexed_agents": indexed_agents,
        "average_compression_ratio": acr_float,
        "monthly_savings_estimate": monthly,
        "last_updated": last_updated,
        "agents": agents_out,
    }


@router.get("/metrics")
async def get_metrics(session: AsyncSession = Depends(get_session)) -> Dict[str, Any]:
    """Unified monitoring metrics: compression stats, agent registry, memory index."""
    try:
        payload = await build_monitoring_payload(session)
        logger.info("Fetched context-mode metrics", extra={"status": payload.get("status")})
        return payload
    except Exception as e:
        logger.error("Error fetching compression metrics: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/summary")
async def get_summary(session: AsyncSession = Depends(get_session)) -> Dict[str, Any]:
    """
    Get context-mode compression summary for dashboard card.
    """
    try:
        data = await build_monitoring_payload(session)
        if data.get("status") == "no_data":
            return {
                "status": "initializing",
                "message": "Context-mode compression waiting for large tool outputs",
            }

        tokens_saved = int(data.get("tokens_saved_estimate", 0) or 0)
        monthly_savings = float(data.get("monthly_savings_estimate", 0) or 0)
        acr = float(data.get("average_compression_ratio", 0) or 0)
        compression_efficiency = f"{(1.0 - acr) * 100:.1f}%" if acr > 0 else "N/A"

        return {
            "status": "active",
            "tokens_saved_per_hour": int(tokens_saved / 24) if tokens_saved else 0,
            "estimated_monthly_cost_reduction": f"${monthly_savings:.2f}",
            "compression_efficiency": compression_efficiency,
            "total_compressions": data.get("total_compressions", 0),
            "next_hour_estimate": int(tokens_saved / 24) if tokens_saved else 0,
        }

    except Exception as e:
        logger.error("Error generating compression summary: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/status")
async def get_status(session: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    """Get context-mode compression status."""
    try:
        data = await build_monitoring_payload(session)
        if data.get("status") == "no_data":
            return {
                "status": "initializing",
                "message": "Context-mode compression active, waiting for large outputs to compress",
                "config_status": "active",
                "hook_status": "tool.executed hook registered",
            }

        return {
            "status": "active",
            "message": f"Context-mode compression active ({data.get('total_compressions', 0)} compressions so far)",
            "config_status": "active",
            "hook_status": "tool.executed hook registered",
            "metrics_available": True,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error checking context-mode status: {str(e)}",
        }
