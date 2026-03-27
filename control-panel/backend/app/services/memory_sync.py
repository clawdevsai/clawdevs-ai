"""Memory synchronization service.

Loads OpenClaw MEMORY.md files from the shared data PVC and upserts lightweight
entries into the panel database so the UI can display per-agent memory.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from sqlmodel import select

from app.core.config import get_settings
from app.models import Agent, MemoryEntry

settings = get_settings()


def _extract_title(content: str, fallback: str) -> str:
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            if title:
                return title
    return fallback


async def sync_memory_entries(db_session) -> None:
    """Sync MEMORY.md files from OpenClaw filesystem into memory_entries table."""
    base_path = Path(settings.openclaw_data_path) / "memory"
    if not base_path.exists():
        return

    result = await db_session.exec(select(Agent))
    agents = {a.slug: a for a in result.all()}
    changed = False

    # Per-agent MEMORY.md
    for slug, agent in agents.items():
        memory_file = base_path / slug / "MEMORY.md"
        if not memory_file.exists():
            continue

        try:
            content = memory_file.read_text(encoding="utf-8").strip()
        except OSError:
            continue

        if not content:
            continue

        title = _extract_title(content, f"{slug} memory")
        result_entry = await db_session.exec(
            select(MemoryEntry)
            .where(MemoryEntry.agent_id == agent.id)
            .where(MemoryEntry.entry_type == "active")
            .order_by(MemoryEntry.updated_at.desc())
        )
        existing = result_entry.first()

        if existing:
            if existing.content != content or existing.tags != [title]:
                existing.content = content
                existing.tags = [title]
                existing.source_agents = [slug]
                existing.updated_at = datetime.utcnow()
                changed = True
        else:
            db_session.add(
                MemoryEntry(
                    agent_id=agent.id,
                    entry_type="active",
                    content=content,
                    tags=[title],
                    source_agents=[slug],
                )
            )
            changed = True

    # Shared memory
    shared_file = base_path / "shared" / "SHARED_MEMORY.md"
    if shared_file.exists():
        try:
            content = shared_file.read_text(encoding="utf-8").strip()
        except OSError:
            content = ""

        if content:
            title = _extract_title(content, "Shared memory")
            shared_result = await db_session.exec(
                select(MemoryEntry)
                .where(MemoryEntry.agent_id.is_(None))
                .where(MemoryEntry.entry_type == "global")
                .order_by(MemoryEntry.updated_at.desc())
            )
            shared_existing = shared_result.first()

            if shared_existing:
                if shared_existing.content != content or shared_existing.tags != [title]:
                    shared_existing.content = content
                    shared_existing.tags = [title]
                    shared_existing.source_agents = ["shared"]
                    shared_existing.updated_at = datetime.utcnow()
                    changed = True
            else:
                db_session.add(
                    MemoryEntry(
                        agent_id=None,
                        entry_type="global",
                        content=content,
                        tags=[title],
                        source_agents=["shared"],
                    )
                )
                changed = True

    if changed:
        await db_session.commit()
