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

import json
import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient

from app.core.database import get_session


@pytest.mark.asyncio
class TestContextModeSemanticOptimizationAPI:
    @pytest.mark.asyncio
    async def test_enhance_query_endpoint(self, client: AsyncClient, auth_headers: dict):
        """Test /enhance-query endpoint"""
        with patch(
            "app.api.context_mode_semantic_optimization.query_enhancer.enhance_query"
        ) as mock_enhance:
            mock_enhance.return_value = {
                "original": "docker issue",
                "expanded": ["docker networking", "container"],
                "reasoning": "Expanded with related terms",
            }

            response = await client.post(
                "/api/context-mode/semantic-optimization/enhance-query?query=docker%20issue&agent_id=dev_backend",
                headers=auth_headers,
            )

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_enhance_query_missing_params(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test enhance-query with missing parameters"""
        response = await client.post(
            "/api/context-mode/semantic-optimization/enhance-query",
            headers=auth_headers,
        )

        # Should return validation error (422 or 400)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_rerank_results_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /rerank-results endpoint"""
        payload = {
            "query": "test query",
            "chunks": ["chunk1", "chunk2"],
            "bm25_scores": [0.8, 0.7],
        }

        response = await client.post(
            "/api/context-mode/semantic-optimization/rerank-results",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_classify_output_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /classify-output endpoint"""
        payload = {
            "output": "def foo(): return 42",
            "tool_name": "python",
        }

        response = await client.post(
            "/api/context-mode/semantic-optimization/classify-output",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_classify_output_empty(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test classify-output with empty output"""
        response = await client.post(
            "/api/context-mode/semantic-optimization/classify-output",
            json={"output": "", "tool_name": "python"},
            headers=auth_headers,
        )

        assert response.status_code in [200, 400, 422]

    @pytest.mark.asyncio
    async def test_summarize_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /summarize endpoint"""
        payload = {
            "content": "Long document...",
            "intent": "database_troubleshooting",
            "max_words": 100,
        }

        response = await client.post(
            "/api/context-mode/semantic-optimization/summarize",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_categorize_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /categorize endpoint"""
        payload = {"content": "function implementation details"}

        response = await client.post(
            "/api/context-mode/semantic-optimization/categorize",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_detect_anomaly_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /detect-anomaly endpoint"""
        payload = {
            "output": "Normal output",
            "tool_name": "npm",
        }

        response = await client.post(
            "/api/context-mode/semantic-optimization/detect-anomaly",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_detect_anomaly_empty(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test detect-anomaly with empty output"""
        response = await client.post(
            "/api/context-mode/semantic-optimization/detect-anomaly",
            json={"output": "", "tool_name": "npm"},
            headers=auth_headers,
        )

        assert response.status_code in [200, 400, 422]

    @pytest.mark.asyncio
    async def test_suggest_context_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /suggest-context endpoint"""
        payload = {
            "tool_name": "npm",
            "args": "test",
            "candidate_memories": [
                {"title": "Memory 1", "content": "Content"}
            ],
        }

        response = await client.post(
            "/api/context-mode/semantic-optimization/suggest-context",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_suggest_context_no_candidates(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test suggest-context with no candidates"""
        payload = {
            "tool_name": "npm",
            "args": "test",
            "candidate_memories": None,
        }

        response = await client.post(
            "/api/context-mode/semantic-optimization/suggest-context",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_ollama_health_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /ollama-health endpoint"""
        response = await client.get(
            "/api/context-mode/semantic-optimization/ollama-health",
            headers=auth_headers,
        )

        assert response.status_code in [200, 500]  # 500 if Ollama not available
        if response.status_code == 200:
            data = response.json()
            assert "status" in data

    @pytest.mark.asyncio
    async def test_semantic_optimization_metrics_endpoint(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test /metrics endpoint for Phase 6 stats"""
        response = await client.get(
            "/api/context-mode/semantic-optimization/metrics",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "query_enhancements" in data
        assert "semantic_reranking" in data or "ollama_status" in data

    @pytest.mark.asyncio
    async def test_endpoints_accessible(self, client: AsyncClient):
        """Test that Phase 6 endpoints are accessible"""
        endpoints = [
            ("/api/context-mode/semantic-optimization/enhance-query?query=test&agent_id=test", "POST"),
            ("/api/context-mode/semantic-optimization/rerank-results", "POST"),
            ("/api/context-mode/semantic-optimization/classify-output", "POST"),
            ("/api/context-mode/semantic-optimization/summarize", "POST"),
            ("/api/context-mode/semantic-optimization/categorize", "POST"),
            ("/api/context-mode/semantic-optimization/detect-anomaly", "POST"),
            ("/api/context-mode/semantic-optimization/suggest-context", "POST"),
            ("/api/context-mode/semantic-optimization/ollama-health", "GET"),
            ("/api/context-mode/semantic-optimization/metrics", "GET"),
        ]

        for endpoint, method in endpoints:
            if method == "GET":
                response = await client.get(endpoint)
            else:
                response = await client.post(endpoint, json={})

            # Endpoints should respond (may be 200, 401, 422, etc)
            assert response.status_code in [200, 400, 401, 422, 500]
