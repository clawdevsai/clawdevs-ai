import json
from pathlib import Path

from app.services import agent_activity


def _write_jsonl(path: Path, messages: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "type": "session",
                    "version": 3,
                    "id": "session-1",
                    "timestamp": "2026-03-29T00:00:00.000Z",
                    "cwd": "/tmp",
                }
            )
            + "\n"
        )
        for idx, text in enumerate(messages, start=1):
            f.write(
                json.dumps(
                    {
                        "type": "message",
                        "id": f"m-{idx}",
                        "timestamp": f"2026-03-29T00:00:0{idx}.000Z",
                        "message": {
                            "role": "assistant",
                            "content": [{"type": "text", "text": text}],
                        },
                    }
                )
                + "\n"
            )


def test_get_agent_current_activity_skips_policy_refusal_loop(tmp_path):
    agent_slug = "dev_backend"
    sessions_dir = tmp_path / "agents" / agent_slug / "sessions"
    session_file = sessions_dir / "session-1.jsonl"
    _write_jsonl(
        session_file,
        [
            "Standby normal: sem issue elegivel.",
            "**STANDBY** — 5 recusas, ciclo encerrado. Aguardando correção de política.",
        ],
    )
    sessions_payload = {
        "agent:dev_backend:cron:abc": {
            "sessionId": "session-1",
            "updatedAt": 1774742744616,
            "sessionFile": str(session_file),
        }
    }
    (sessions_dir / "sessions.json").write_text(
        json.dumps(sessions_payload), encoding="utf-8"
    )

    old_path = agent_activity.settings.openclaw_data_path
    agent_activity.settings.openclaw_data_path = str(tmp_path)
    try:
        summary, full, _ = agent_activity.get_agent_current_activity(agent_slug)
    finally:
        agent_activity.settings.openclaw_data_path = old_path

    assert "5 recusas" not in (summary or "")
    assert full == "Standby normal: sem issue elegivel."


def test_get_agent_current_activity_keeps_regular_standby(tmp_path):
    agent_slug = "dev_backend"
    sessions_dir = tmp_path / "agents" / agent_slug / "sessions"
    session_file = sessions_dir / "session-1.jsonl"
    _write_jsonl(
        session_file,
        [
            "**Standby** — Nenhuma issue elegível com label `back_end` encontrada.",
        ],
    )
    sessions_payload = {
        "agent:dev_backend:cron:abc": {
            "sessionId": "session-1",
            "updatedAt": 1774749797957,
            "sessionFile": str(session_file),
        }
    }
    (sessions_dir / "sessions.json").write_text(
        json.dumps(sessions_payload), encoding="utf-8"
    )

    old_path = agent_activity.settings.openclaw_data_path
    agent_activity.settings.openclaw_data_path = str(tmp_path)
    try:
        summary, full, _ = agent_activity.get_agent_current_activity(agent_slug)
    finally:
        agent_activity.settings.openclaw_data_path = old_path

    assert summary is not None
    assert "Nenhuma issue elegível" in summary
    assert full is not None
    assert "Nenhuma issue elegível" in full
