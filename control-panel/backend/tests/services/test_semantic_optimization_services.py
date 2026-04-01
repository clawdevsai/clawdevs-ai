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
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.ollama_client import OllamaClient
from app.services.query_enhancer import QueryEnhancer
from app.services.semantic_ranker import SemanticRanker
from app.services.adaptive_compressor import AdaptiveCompressor
from app.services.summarizer import IntelligentSummarizer
from app.services.categorizer import MemoryCategorizer
from app.services.anomaly_detector import AnomalyDetector
from app.services.context_suggester import ContextSuggester


@pytest.mark.asyncio
class TestOllamaClient:
    @pytest.fixture
    def client(self):
        return OllamaClient(base_url="http://localhost:11434")

    @pytest.mark.asyncio
    async def test_health_check_success(self, client):
        """Test successful health check"""
        with patch("app.services.ollama_client.aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={"status": "ok"})
            mock_get.return_value.__aenter__.return_value = mock_response

            result = await client.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_generate_success(self, client):
        """Test successful text generation"""
        with patch("app.services.ollama_client.aiohttp.ClientSession.post") as mock_post:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(
                return_value={"response": "test response"}
            )
            mock_post.return_value.__aenter__.return_value = mock_response

            result = await client.generate("test prompt")
            assert result == "test response"

    @pytest.mark.asyncio
    async def test_generate_timeout(self, client):
        """Test timeout handling in generate"""
        with patch("app.services.ollama_client.aiohttp.ClientSession.post") as mock_post:
            import asyncio

            mock_post.side_effect = asyncio.TimeoutError()
            result = await client.generate("test prompt", timeout=0.1)
            assert result is None

    @pytest.mark.asyncio
    async def test_generate_error(self, client):
        """Test error handling in generate"""
        with patch("app.services.ollama_client.aiohttp.ClientSession.post") as mock_post:
            mock_post.side_effect = Exception("Connection error")
            result = await client.generate("test prompt")
            assert result is None


@pytest.mark.asyncio
class TestQueryEnhancer:
    @pytest.fixture
    def enhancer(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return QueryEnhancer(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_enhance_query_success(self, enhancer):
        """Test successful query enhancement"""
        mock_response = json.dumps(
            {
                "original": "docker issue",
                "expanded": [
                    "docker networking",
                    "container issues",
                    "docker compose",
                ],
                "reasoning": "Expanded with related terms",
            }
        )
        enhancer.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await enhancer.enhance_query("docker issue", "dev_backend")
        assert result["original"] == "docker issue"
        assert len(result["expanded"]) == 3

    @pytest.mark.asyncio
    async def test_enhance_query_empty_response(self, enhancer):
        """Test handling of empty Ollama response"""
        enhancer.ollama_client.generate = AsyncMock(return_value=None)

        result = await enhancer.enhance_query("test", "agent")
        assert result["original"] == "test"
        assert result["expanded"] == []


@pytest.mark.asyncio
class TestSemanticRanker:
    @pytest.fixture
    def ranker(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return SemanticRanker(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_rerank_success(self, ranker):
        """Test successful semantic reranking"""
        mock_response = json.dumps({"ratings": [9, 7, 5]})
        ranker.ollama_client.generate = AsyncMock(return_value=mock_response)

        chunks = ["chunk1", "chunk2", "chunk3"]
        bm25_scores = [0.8, 0.7, 0.6]
        result = await ranker.rerank("query", chunks, bm25_scores, top_k=2)

        assert len(result) == 2
        assert result[0][1] > result[1][1]  # Score should be higher for first chunk

    @pytest.mark.asyncio
    async def test_rerank_empty_chunks(self, ranker):
        """Test reranking with empty chunks"""
        result = await ranker.rerank("query", [], [])
        assert result == []


@pytest.mark.asyncio
class TestAdaptiveCompressor:
    @pytest.fixture
    def compressor(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return AdaptiveCompressor(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_classify_code(self, compressor):
        """Test classification of code output"""
        mock_response = json.dumps(
            {"type": "code", "confidence": 0.95}
        )
        compressor.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await compressor.compress_adaptive(
            "def foo(): return 42", "python"
        )
        assert "compressed" in result
        assert result["strategy"] == "code"

    @pytest.mark.asyncio
    async def test_classify_logs(self, compressor):
        """Test classification of log output"""
        mock_response = json.dumps(
            {"type": "logs", "confidence": 0.9}
        )
        compressor.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await compressor.compress_adaptive("INFO: Starting server", "npm")
        assert result["strategy"] == "logs"


@pytest.mark.asyncio
class TestIntelligentSummarizer:
    @pytest.fixture
    def summarizer(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return IntelligentSummarizer(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_summarize_success(self, summarizer):
        """Test successful summarization"""
        mock_response = json.dumps(
            {
                "summary": "Docker networking issue resolved",
                "key_points": ["Network isolation", "DNS resolution"],
            }
        )
        summarizer.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await summarizer.summarize("Long technical document about docker with more than 50 characters...")
        assert "summary" in result
        assert isinstance(result["key_points"], list)

    @pytest.mark.asyncio
    async def test_summarize_empty_content(self, summarizer):
        """Test summarization with empty content"""
        result = await summarizer.summarize("")
        assert result["summary"] == ""


@pytest.mark.asyncio
class TestMemoryCategorizer:
    @pytest.fixture
    def categorizer(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return MemoryCategorizer(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_categorize_code(self, categorizer):
        """Test categorization of code memory"""
        mock_response = json.dumps(
            {"primary": "code", "secondary": "implementation", "confidence": 0.92}
        )
        categorizer.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await categorizer.categorize("function implementation details")
        assert result["primary"] == "code"

    @pytest.mark.asyncio
    async def test_categorize_security(self, categorizer):
        """Test categorization of security memory"""
        mock_response = json.dumps(
            {"primary": "security", "secondary": "authentication", "confidence": 0.88}
        )
        categorizer.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await categorizer.categorize("JWT token validation")
        assert result["primary"] == "security"


@pytest.mark.asyncio
class TestAnomalyDetector:
    @pytest.fixture
    def detector(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return AnomalyDetector(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_detect_normal_output(self, detector):
        """Test detection of normal output"""
        mock_response = json.dumps(
            {"type": None, "score": 0.2, "severity": "low"}
        )
        detector.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await detector.detect("Normal output", "npm")
        assert result["anomaly_score"] < 0.7

    @pytest.mark.asyncio
    async def test_detect_error_output(self, detector):
        """Test detection of error anomaly"""
        mock_response = json.dumps(
            {"type": "error_stack", "score": 0.95, "severity": "high"}
        )
        detector.ollama_client.generate = AsyncMock(return_value=mock_response)

        result = await detector.detect("Error: Stack trace...", "npm")
        assert result["should_skip_compression"] is True

    @pytest.mark.asyncio
    async def test_detect_empty_output(self, detector):
        """Test detection with empty output"""
        result = await detector.detect("", "npm")
        assert result["anomaly_score"] == 0.0


@pytest.mark.asyncio
class TestContextSuggester:
    @pytest.fixture
    def suggester(self):
        mock_ollama = AsyncMock(spec=OllamaClient)
        return ContextSuggester(ollama_client=mock_ollama)

    @pytest.mark.asyncio
    async def test_suggest_empty_candidates(self, suggester):
        """Test suggestion with empty candidates"""
        result = await suggester.suggest_context("npm", "test", [])
        assert result["suggestions"] == []
        assert result["reason"] == "no_candidates"

    @pytest.mark.asyncio
    async def test_suggest_few_candidates(self, suggester):
        """Test suggestion with fewer candidates than top_k"""
        candidates = [
            {"title": "Memory 1", "content": "Content 1"},
            {"title": "Memory 2", "content": "Content 2"},
        ]
        result = await suggester.suggest_context("npm", "test", candidates, top_k=5)
        assert result["reason"] == "all_candidates"
        assert len(result["suggestions"]) == 2

    @pytest.mark.asyncio
    async def test_suggest_ranked(self, suggester):
        """Test ranking of multiple candidates"""
        mock_response = json.dumps({"rankings": [1, 3, 2]})
        suggester.ollama_client.generate = AsyncMock(return_value=mock_response)

        candidates = [
            {"title": "Memory 1", "content": "Content 1"},
            {"title": "Memory 2", "content": "Content 2"},
            {"title": "Memory 3", "content": "Content 3"},
        ]
        result = await suggester.suggest_context("npm", "test", candidates, top_k=2)
        assert result["reason"] == "semantic_ranking"
        assert len(result["suggestions"]) == 2
