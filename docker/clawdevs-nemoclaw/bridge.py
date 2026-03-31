import json
import os
import subprocess
from typing import Any, Iterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def _openclaw_agent_message(agent_slug: str, message: str, session_id: str) -> str:
    sandbox = os.getenv("NEMOCLAW_SANDBOX_NAME", "clawdevs-ai")
    cmd = [
        "nemoclaw",
        sandbox,
        "connect",
        "--",
        "openclaw",
        "agent",
        "--agent",
        agent_slug,
        "--local",
        "--session-id",
        session_id,
        "-m",
        message,
    ]
    proc = _run(cmd)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip() or "nemoclaw execution failed"
        raise HTTPException(status_code=502, detail=detail)
    return (proc.stdout or "").strip()


def _sse_lines(text: str) -> Iterator[bytes]:
    yield b"data: " + json.dumps({"choices": [{"delta": {"content": ""}}]}).encode() + b"\n\n"
    for chunk in [text[i : i + 256] for i in range(0, len(text), 256)]:
        payload = {"choices": [{"delta": {"content": chunk}}]}
        yield b"data: " + json.dumps(payload).encode("utf-8") + b"\n\n"
    yield b"data: [DONE]\n\n"


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> Any:
    body = await request.json()
    model = str(body.get("model") or "")
    messages = body.get("messages") or []
    stream = bool(body.get("stream"))

    if "/" not in model:
        raise HTTPException(status_code=422, detail="model must be '<prefix>/<agent_slug>'")
    agent_slug = model.split("/", 1)[1].strip()
    if not agent_slug:
        raise HTTPException(status_code=422, detail="agent_slug missing in model")
    if not isinstance(messages, list) or not messages:
        raise HTTPException(status_code=422, detail="messages is required")

    user_text = ""
    for msg in reversed(messages):
        if isinstance(msg, dict) and msg.get("role") == "user":
            user_text = str(msg.get("content") or "").strip()
            break
    if not user_text:
        raise HTTPException(status_code=422, detail="user message is required")

    session_id = os.getenv("NEMOCLAW_SESSION_ID", "panel")
    output_text = _openclaw_agent_message(agent_slug, user_text, session_id=session_id)

    if stream:
        return StreamingResponse(_sse_lines(output_text), media_type="text/event-stream")

    return {
        "choices": [{"message": {"role": "assistant", "content": output_text}}],
        "output_text": output_text,
    }
