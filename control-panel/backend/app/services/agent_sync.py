import re
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()

AGENT_SLUGS = [
    "ceo", "po", "arquiteto", "dev_backend", "dev_frontend",
    "dev_mobile", "qa_engineer", "devops_sre", "security_engineer",
    "ux_designer", "dba_data_engineer", "memory_curator"
]

CRON_MAP = {
    "dev_backend": "0 * * * *",
    "dev_frontend": "15 * * * *",
    "dev_mobile": "30 * * * *",
    "qa_engineer": "45 * * * *",
    "devops_sre": "*/30 * * * *",
    "security_engineer": "0 */6 * * *",
    "ux_designer": "0 */4 * * *",
    "dba_data_engineer": "30 */4 * * *",
    "memory_curator": "0 2 * * *",
}


def parse_identity(slug: str) -> dict:
    base = Path(settings.openclaw_data_path) / "agents" / slug
    identity_file = base / "IDENTITY.md"
    if not identity_file.exists():
        return {"display_name": slug, "role": slug}
    content = identity_file.read_text()
    name_match = re.search(r"Nome[:\s]+(.+)", content)
    role_match = re.search(r"Papel[:\s]+(.+)", content)
    return {
        "display_name": name_match.group(1).strip() if name_match else slug,
        "role": role_match.group(1).strip() if role_match else slug,
    }


async def sync_agents(session) -> None:
    from app.models import Agent
    from sqlmodel import select

    for slug in AGENT_SLUGS:
        result = await session.exec(select(Agent).where(Agent.slug == slug))
        agent = result.first()
        identity = parse_identity(slug)
        if not agent:
            agent = Agent(
                slug=slug,
                display_name=identity["display_name"],
                role=identity["role"],
                avatar_url=f"/static/avatars/{slug}.png",
                cron_expression=CRON_MAP.get(slug),
            )
            session.add(agent)
        else:
            agent.display_name = identity["display_name"]
            agent.role = identity["role"]
    await session.commit()
