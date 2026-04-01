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

import pytest
from unittest.mock import patch
from httpx import AsyncClient

from app.services.semantic_optimization_flags import SemanticOptimizationFlags


@pytest.mark.asyncio
class TestSemanticOptimizationRollout:
    """Test rollout strategy and feature flag validation."""

    def test_all_tasks_disabled_by_default(self):
        """Verify all tasks are disabled by default."""
        flags = SemanticOptimizationFlags()
        status = flags.get_all_status()

        for task, info in status.items():
            assert info["enabled"] is False, f"{task} should be disabled by default"

    def test_canary_agents_empty_by_default(self):
        """Verify canary agents list is empty by default."""
        flags = SemanticOptimizationFlags()
        assert flags.get_canary_agents() == []

    def test_is_enabled_with_disabled_flag(self):
        """Task disabled globally should return False even with canary agent."""
        flags = SemanticOptimizationFlags()
        assert flags.is_enabled("query_enhancement", "dev_backend") is False

    def test_feature_flag_task_names(self):
        """Verify all 7 tasks are registered."""
        expected_tasks = [
            "query_enhancement",
            "semantic_reranking",
            "adaptive_compression",
            "summarization",
            "categorization",
            "anomaly_detection",
            "context_suggestion",
        ]
        flags = SemanticOptimizationFlags()
        actual_tasks = list(flags.TASK_FLAGS.keys())

        assert sorted(actual_tasks) == sorted(expected_tasks)

    @pytest.mark.asyncio
    async def test_disabled_endpoint_returns_503(self, client: AsyncClient, auth_headers: dict):
        """Disabled task endpoint should return 503 Service Unavailable."""
        # Feature flag is disabled by default
        response = await client.post(
            "/context-mode/semantic-optimization/enhance-query?query=test&agent_id=dev_backend",
            headers=auth_headers,
        )

        assert response.status_code == 503
        assert "not enabled" in response.text.lower()

    @pytest.mark.asyncio
    async def test_get_feature_flags_endpoint(self, client: AsyncClient, auth_headers: dict):
        """GET /feature-flags should list all tasks and canary agents."""
        response = await client.get(
            "/context-mode/semantic-optimization/feature-flags",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "flags" in data
        assert "canary_agents" in data
        assert len(data["flags"]) == 7
        assert data["canary_agents"] == []

    @pytest.mark.asyncio
    async def test_check_task_enabled_endpoint(self, client: AsyncClient, auth_headers: dict):
        """GET /feature-flags/{task_name} should check if task is enabled."""
        response = await client.get(
            "/context-mode/semantic-optimization/feature-flags/query_enhancement",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["task"] == "query_enhancement"
        assert data["enabled"] is False
        assert data["canary"] is False

    @pytest.mark.asyncio
    async def test_check_task_with_agent_id(self, client: AsyncClient, auth_headers: dict):
        """Check task enabled for specific agent."""
        response = await client.get(
            "/context-mode/semantic-optimization/feature-flags/query_enhancement?agent_id=dev_backend",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["agent_id"] == "dev_backend"

    def test_rollout_week1_canary_setup(self):
        """Simulate Week 1 canary deployment setup."""
        # Patch settings to simulate .env config
        with patch("app.services.semantic_optimization_flags.get_settings") as mock_settings:
            mock_settings.return_value.SEMANTIC_OPT_QUERY_ENHANCEMENT = False
            mock_settings.return_value.SEMANTIC_OPT_CANARY_AGENTS = "dev_backend,memory_curator"

            flags = SemanticOptimizationFlags()

            # Global flag is false
            assert flags.is_enabled("query_enhancement") is False

            # But canary agents have access
            assert flags.is_enabled("query_enhancement", "dev_backend") is True
            assert flags.is_enabled("query_enhancement", "memory_curator") is True

            # Other agents don't
            assert flags.is_enabled("query_enhancement", "ux_designer") is False

    def test_rollout_week1_global_enable(self):
        """Simulate Week 1 global rollout after canary validation."""
        with patch("app.services.semantic_optimization_flags.get_settings") as mock_settings:
            mock_settings.return_value.SEMANTIC_OPT_QUERY_ENHANCEMENT = True
            mock_settings.return_value.SEMANTIC_OPT_CANARY_AGENTS = ""

            flags = SemanticOptimizationFlags()

            # All agents have access
            assert flags.is_enabled("query_enhancement") is True
            assert flags.is_enabled("query_enhancement", "dev_backend") is True
            assert flags.is_enabled("query_enhancement", "ux_designer") is True

    def test_rollout_disable_on_error(self):
        """Simulate disabling a task if errors occur during rollout."""
        with patch("app.services.semantic_optimization_flags.get_settings") as mock_settings:
            # Task was enabled but now disabled due to errors
            mock_settings.return_value.SEMANTIC_OPT_QUERY_ENHANCEMENT = False
            mock_settings.return_value.SEMANTIC_OPT_CANARY_AGENTS = "dev_backend,memory_curator"

            flags = SemanticOptimizationFlags()

            # Revert to canary for investigation
            assert flags.is_enabled("query_enhancement", "dev_backend") is True
            assert flags.is_enabled("query_enhancement", "ux_designer") is False
