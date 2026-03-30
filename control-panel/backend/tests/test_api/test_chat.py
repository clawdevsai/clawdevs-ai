# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime, UTC
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import chat as chat_api
from app.models import Agent, ChatPanelTranscript, MemoryEntry, Session


async def _create_agent(db_session: AsyncSession, slug: str = "po") -> Agent:
    agent = Agent(
        slug=slug,
        display_name=slug.upper(),
        role="Product Owner",
        status="online",
        last_heartbeat_at=datetime.now(UTC).replace(tzinfo=None),
    )
    db_session.add(agent)
    await db_session.commit()
    await db_session.refresh(agent)
    return agent


class TestChatApi:
    def test_stream_legacy_agent_slug_resolves_main_session(self):
        body = chat_api.ChatRequest(agent_slug="po", message="legacy")
        resolved_agent, resolved_session = chat_api._resolve_agent_and_session_key(body)

        assert resolved_agent == "po"
        assert resolved_session == "agent:po:main"

    @pytest.mark.asyncio
    async def test_stream_uses_session_key(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession
    ):
        await _create_agent(db_session, "po")
        captured: dict[str, str] = {}

        async def fake_events():
            yield {"event": "done"}

        def fake_stream_chat(*, agent_slug: str, message: str, session_key: str):
            captured["agent_slug"] = agent_slug
            captured["message"] = message
            captured["session_key"] = session_key
            return fake_events()

        original_stream_chat = chat_api.openclaw_client.stream_chat
        try:
            chat_api.openclaw_client.stream_chat = fake_stream_chat
            response = await client.post(
                "/chat/stream",
                headers=auth_headers,
                json={"session_key": "agent:po:main", "message": "hello"},
            )
        finally:
            chat_api.openclaw_client.stream_chat = original_stream_chat

        assert response.status_code == 200
        assert captured == {
            "agent_slug": "po",
            "message": "hello",
            "session_key": "agent:po:main",
        }
        assert "data: [DONE]" in response.text

    @pytest.mark.asyncio
    async def test_stream_rejects_invalid_session_key(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.post(
            "/chat/stream",
            headers=auth_headers,
            json={"session_key": "main", "message": "hello"},
        )

        assert response.status_code == 422
        assert "session_key" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_stream_rejects_agent_slug_mismatch(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.post(
            "/chat/stream",
            headers=auth_headers,
            json={
                "agent_slug": "ceo",
                "session_key": "agent:po:main",
                "message": "hello",
            },
        )

        assert response.status_code == 400
        assert "agent_slug does not match" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_history_reads_specific_session_from_file_index(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        tmp_path,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        monkeypatch.setattr(chat_api.settings, "openclaw_data_path", str(tmp_path))

        sessions_dir = tmp_path / "agents" / "po" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / "sessions.json").write_text(
            '{"agent:po:main":{"sessionId":"sess-file-1"}}',
            encoding="utf-8",
        )

        get_session_mock = AsyncMock(
            return_value={
                "messages": [{"role": "assistant", "content": "from-index"}]
            }
        )
        monkeypatch.setattr(chat_api.openclaw_client, "get_session", get_session_mock)

        response = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["agent_slug"] == "po"
        assert payload["messages"][0]["content"] == "from-index"
        get_session_mock.assert_awaited_once_with("sess-file-1")

    @pytest.mark.asyncio
    async def test_history_uses_gateway_sessions_fallback(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        tmp_path,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        monkeypatch.setattr(chat_api.settings, "openclaw_data_path", str(tmp_path))

        monkeypatch.setattr(
            chat_api.openclaw_client,
            "get_sessions",
            AsyncMock(
                return_value=[
                    {"key": "agent:po:cron:sync", "sessionId": "sess-fallback-1"}
                ]
            ),
        )
        monkeypatch.setattr(
            chat_api.openclaw_client,
            "get_session",
            AsyncMock(
                return_value={
                    "messages": [{"role": "assistant", "content": "from-fallback"}]
                }
            ),
        )

        response = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:cron:sync"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["messages"][0]["content"] == "from-fallback"

    @pytest.mark.asyncio
    async def test_history_session_not_found_returns_empty(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        tmp_path,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        monkeypatch.setattr(chat_api.settings, "openclaw_data_path", str(tmp_path))
        monkeypatch.setattr(chat_api.openclaw_client, "get_sessions", AsyncMock(return_value=[]))

        response = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["agent_slug"] == "po"
        assert payload["messages"] == []

    @pytest.mark.asyncio
    async def test_history_resolves_session_from_db_when_file_and_gateway_miss(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        tmp_path,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        monkeypatch.setattr(chat_api.settings, "openclaw_data_path", str(tmp_path))

        db_session.add(
            Session(
                openclaw_session_id="sess-from-db",
                openclaw_session_key="agent:po:main",
                agent_slug="po",
            )
        )
        await db_session.commit()

        monkeypatch.setattr(chat_api.openclaw_client, "get_sessions", AsyncMock(return_value=[]))
        get_session_mock = AsyncMock(
            return_value={
                "messages": [{"role": "assistant", "content": "from-gateway-after-db"}]
            }
        )
        monkeypatch.setattr(chat_api.openclaw_client, "get_session", get_session_mock)

        response = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["messages"][0]["content"] == "from-gateway-after-db"
        get_session_mock.assert_awaited_once_with("sess-from-db")

    @pytest.mark.asyncio
    async def test_history_uses_jsonl_when_gateway_empty(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        tmp_path,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        monkeypatch.setattr(chat_api.settings, "openclaw_data_path", str(tmp_path))

        db_session.add(
            Session(
                openclaw_session_id="sess-jsonl",
                openclaw_session_key="agent:po:main",
                agent_slug="po",
            )
        )
        await db_session.commit()

        monkeypatch.setattr(chat_api.openclaw_client, "get_sessions", AsyncMock(return_value=[]))
        monkeypatch.setattr(chat_api.openclaw_client, "get_session", AsyncMock(return_value={}))

        sessions_dir = tmp_path / "agents" / "po" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        jsonl_line = (
            '{"type":"message","message":{"role":"assistant","content":"from-jsonl"}}\n'
        )
        (sessions_dir / "sess-jsonl.jsonl").write_text(jsonl_line, encoding="utf-8")

        response = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert len(payload["messages"]) == 1
        assert payload["messages"][0]["content"] == "from-jsonl"

    @pytest.mark.asyncio
    async def test_history_prefers_panel_transcript_over_openclaw(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        transcript = ChatPanelTranscript(
            agent_slug="po",
            session_key="agent:po:main",
            messages=[
                {"role": "user", "content": "from-panel"},
                {"role": "assistant", "content": "panel-reply"},
            ],
        )
        db_session.add(transcript)
        await db_session.commit()

        get_session_mock = AsyncMock(
            return_value={
                "messages": [{"role": "assistant", "content": "from-gateway"}]
            }
        )
        monkeypatch.setattr(chat_api.openclaw_client, "get_session", get_session_mock)

        response = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert len(payload["messages"]) == 2
        assert payload["messages"][0]["content"] == "from-panel"
        assert payload["messages"][1]["content"] == "panel-reply"
        get_session_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_transcript_turn_appends_and_shows_in_history(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession
    ):
        await _create_agent(db_session, "po")
        post = await client.post(
            "/chat/transcript/turn",
            headers=auth_headers,
            json={
                "agent_slug": "po",
                "session_key": "agent:po:main",
                "turn_id": "turn-panel-1",
                "user_message": "hello",
                "assistant_message": "hi there",
            },
        )
        assert post.status_code == 200
        assert post.json()["status"] == "appended"

        hist = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )
        assert hist.status_code == 200
        msgs = hist.json()["messages"]
        assert len(msgs) == 2
        assert msgs[0]["content"] == "hello"
        assert msgs[1]["content"] == "hi there"

    @pytest.mark.asyncio
    async def test_transcript_turn_duplicate_turn_id_no_extra_messages(
        self, client: AsyncClient, auth_headers: dict, db_session: AsyncSession
    ):
        await _create_agent(db_session, "po")
        body = {
            "agent_slug": "po",
            "session_key": "agent:po:main",
            "turn_id": "turn-dedupe",
            "user_message": "once",
            "assistant_message": "ok",
        }
        first = await client.post(
            "/chat/transcript/turn", headers=auth_headers, json=body
        )
        second = await client.post(
            "/chat/transcript/turn", headers=auth_headers, json=body
        )
        assert first.status_code == 200
        assert second.status_code == 200
        assert first.json()["status"] == "appended"
        assert second.json()["status"] == "duplicate"

        hist = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )
        assert len(hist.json()["messages"]) == 2

    @pytest.mark.asyncio
    async def test_transcript_turn_seeds_from_openclaw_when_row_empty(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        tmp_path,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")
        monkeypatch.setattr(chat_api.settings, "openclaw_data_path", str(tmp_path))
        sessions_dir = tmp_path / "agents" / "po" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / "sessions.json").write_text(
            '{"agent:po:main":{"sessionId":"sess-seed-1"}}',
            encoding="utf-8",
        )
        monkeypatch.setattr(
            chat_api.openclaw_client,
            "get_session",
            AsyncMock(
                return_value={
                    "messages": [{"role": "assistant", "content": "prior-openclaw"}]
                }
            ),
        )

        post = await client.post(
            "/chat/transcript/turn",
            headers=auth_headers,
            json={
                "agent_slug": "po",
                "session_key": "agent:po:main",
                "turn_id": "turn-after-seed",
                "user_message": "next",
                "assistant_message": "reply",
            },
        )
        assert post.status_code == 200

        hist = await client.get(
            "/chat/history/po",
            headers=auth_headers,
            params={"session_key": "agent:po:main"},
        )
        msgs = hist.json()["messages"]
        assert len(msgs) == 3
        assert msgs[0]["content"] == "prior-openclaw"
        assert msgs[1]["content"] == "next"
        assert msgs[2]["content"] == "reply"

    def test_trim_messages_to_word_budget_drops_from_start(self):
        msgs = [
            chat_api.Message(role="user", content="one two"),
            chat_api.Message(role="assistant", content="three four"),
            chat_api.Message(role="user", content="five"),
            chat_api.Message(role="assistant", content="six"),
        ]
        out = chat_api._trim_messages_to_word_budget(msgs, max_words=3)
        assert chat_api._total_words_in_messages(out) <= 3
        assert out[-1].role == "assistant"
        assert out[-1].content == "six"


class TestChatRagTurnApi:
    @pytest.mark.asyncio
    async def test_rag_turn_persists_memory_entry(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")

        async def fake_embedding(self, text: str):
            return [0.1] * 1536

        monkeypatch.setattr(
            chat_api.EmbeddingService,
            "generate_embedding",
            fake_embedding,
        )

        response = await client.post(
            "/chat/rag/turn",
            headers=auth_headers,
            json={
                "agent_slug": "po",
                "session_key": "agent:po:main",
                "turn_id": "turn-001",
                "user_message": "Como implementar cache?",
                "assistant_message": "Use Redis com TTL e invalidação por evento.",
            },
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "created"

        entries = (
            await db_session.exec(
                select(MemoryEntry).where(
                    MemoryEntry.source_file_path == "chat-rag/po/a85f2dfbef41e49b/turn-001"
                )
            )
        ).all()
        assert len(entries) == 1
        assert entries[0].agent_slug == "po"
        assert entries[0].entry_type == "active"
        assert entries[0].embedding is not None

    @pytest.mark.asyncio
    async def test_rag_turn_is_idempotent_by_turn_id(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db_session: AsyncSession,
        monkeypatch,
    ):
        await _create_agent(db_session, "po")

        async def fake_embedding(self, text: str):
            return [0.1] * 1536

        monkeypatch.setattr(
            chat_api.EmbeddingService,
            "generate_embedding",
            fake_embedding,
        )

        request_payload = {
            "agent_slug": "po",
            "session_key": "agent:po:main",
            "turn_id": "turn-002",
            "user_message": "Preciso de logs estruturados.",
            "assistant_message": "Use logs JSON com correlação por request_id.",
        }

        first_response = await client.post(
            "/chat/rag/turn",
            headers=auth_headers,
            json=request_payload,
        )
        second_response = await client.post(
            "/chat/rag/turn",
            headers=auth_headers,
            json=request_payload,
        )

        assert first_response.status_code == 200
        assert second_response.status_code == 200
        assert first_response.json()["status"] == "created"
        assert second_response.json()["status"] == "exists"
        assert first_response.json()["memory_id"] == second_response.json()["memory_id"]

        entries = (
            await db_session.exec(
                select(MemoryEntry).where(
                    MemoryEntry.source_file_path == "chat-rag/po/a85f2dfbef41e49b/turn-002"
                )
            )
        ).all()
        assert len(entries) == 1

    @pytest.mark.asyncio
    async def test_rag_turn_rejects_agent_session_mismatch(
        self,
        client: AsyncClient,
        auth_headers: dict,
    ):
        response = await client.post(
            "/chat/rag/turn",
            headers=auth_headers,
            json={
                "agent_slug": "ceo",
                "session_key": "agent:po:main",
                "turn_id": "turn-003",
                "user_message": "x",
                "assistant_message": "y",
            },
        )

        assert response.status_code == 400
        assert "agent_slug does not match" in response.json()["detail"]
