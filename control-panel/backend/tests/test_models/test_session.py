"""
Unit tests for Session model - 100% mocked, no external access.
"""

import pytest
from datetime import datetime
from uuid import UUID, uuid4


class TestSessionModel:
    """Test Session model creation and validation - UNIT TESTS ONLY."""

    def test_session_creation(self):
        """Test basic session creation."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="sess-12345",
            channel_type="telegram",
        )
        
        assert session.openclaw_session_id == "sess-12345"
        assert session.channel_type == "telegram"
        assert session.status == "active"
        assert session.message_count == 0
        assert session.token_count == 0
        assert session.id is not None
        assert isinstance(session.id, UUID)

    def test_session_with_all_fields(self):
        """Test session with all fields populated."""
        from app.models.session import Session
        
        now = datetime.utcnow()
        
        session = Session(
            openclaw_session_id="complete-sess",
            agent_slug="test-agent",
            channel_type="cli",
            channel_peer="123456789",
            status="active",
            message_count=150,
            token_count=2500,
            started_at=now,
            last_active_at=now,
        )
        
        assert session.agent_slug == "test-agent"
        assert session.channel_peer == "123456789"
        assert session.status == "active"
        assert session.message_count == 150
        assert session.token_count == 2500

    def test_session_status_values(self):
        """Test valid status values for session."""
        from app.models.session import Session
        
        valid_statuses = ["active", "ended", "error"]
        
        for status in valid_statuses:
            session = Session(
                openclaw_session_id=f"sess-{status}",
                channel_type="cli",
                status=status,
            )
            assert session.status == status

    def test_session_without_agent(self):
        """Test session without agent_slug."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="agent-to-agent-sess",
            channel_type="agent-to-agent",
        )
        
        assert session.agent_slug is None

    def test_session_with_ended_status(self):
        """Test session with ended status."""
        from app.models.session import Session
        from datetime import timedelta
        
        now = datetime.utcnow()
        
        session = Session(
            openclaw_session_id="ended-sess",
            channel_type="cli",
            status="ended",
            started_at=now - timedelta(hours=2),
            ended_at=now - timedelta(hours=1),
            message_count=100,
            token_count=1500,
        )
        
        assert session.status == "ended"
        assert session.ended_at is not None

    def test_session_timestamps(self):
        """Test automatic timestamp creation."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="timestamp-sess",
            channel_type="telegram",
        )
        
        assert session.created_at is not None
        assert isinstance(session.created_at, datetime)

    def test_session_update(self):
        """Test updating session attributes."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="update-sess",
            channel_type="telegram",
            status="active",
            message_count=10,
        )
        
        session.message_count = 15
        session.status = "ended"
        
        assert session.message_count == 15
        assert session.status == "ended"


class TestSessionEdgeCases:
    """Test edge cases for Session model."""

    def test_session_id_is_uuid(self):
        """Test that session ID is UUID."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="uuid-sess",
            channel_type="cli",
        )
        
        assert isinstance(session.id, UUID)
        assert len(str(session.id)) == 36

    def test_session_empty_channel(self):
        """Test session with empty channel type."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="empty-channel-sess",
            channel_type="",
        )
        
        assert session.channel_type == ""

    def test_session_none_channel_peer(self):
        """Test session with None channel peer."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="none-peer-sess",
            channel_type="cli",
            channel_peer=None,
        )
        
        assert session.channel_peer is None


class TestSessionStatistics:
    """Test session statistics tracking - UNIT TESTS ONLY."""

    def test_session_message_count(self):
        """Test message count increment."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="count-sess",
            channel_type="cli",
            message_count=10,
        )
        
        session.message_count += 5
        
        assert session.message_count == 15

    def test_session_token_count(self):
        """Test token count tracking."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="token-sess",
            channel_type="telegram",
            token_count=1000,
        )
        
        session.token_count += 500
        
        assert session.token_count == 1500


class TestSessionEdgeCases2:
    """Additional edge cases for Session model."""

    def test_session_max_values(self):
        """Test session with maximum values."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="max-sess",
            channel_type="cli",
            message_count=999999,
            token_count=9999999,
        )
        
        assert session.message_count == 999999
        assert session.token_count == 9999999

    def test_session_min_values(self):
        """Test session with minimum values."""
        from app.models.session import Session
        
        session = Session(
            openclaw_session_id="min-sess",
            channel_type="cli",
            message_count=0,
            token_count=0,
        )
        
        assert session.message_count == 0
        assert session.token_count == 0
