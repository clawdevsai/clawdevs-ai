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

import httpx
from typing import Any, Optional
from app.core.config import get_settings

settings = get_settings()


class OpenClawClient:
    def __init__(self):
        self.base_url = settings.openclaw_gateway_url.rstrip("/")
        token = (settings.openclaw_gateway_token or "").strip()
        self.headers = {"Authorization": f"Bearer {token}"}

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{self.base_url}/healthz", headers=self.headers)
                return r.status_code == 200
        except Exception:
            return False

    async def get_sessions(self, limit: int = 50) -> list:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(
                    f"{self.base_url}/v1/sessions",
                    headers=self.headers,
                    params={"limit": limit},
                )
                if r.status_code != 200:
                    return []
                payload: Any = r.json()
                if isinstance(payload, list):
                    return payload
                if isinstance(payload, dict):
                    items = payload.get("items", [])
                    return items if isinstance(items, list) else []
                return []
        except Exception:
            return []

    async def get_session(self, session_id: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(
                    f"{self.base_url}/v1/sessions/{session_id}",
                    headers=self.headers,
                )
                if r.status_code != 200:
                    return None
                payload: Any = r.json()
                return payload if isinstance(payload, dict) else None
        except Exception:
            return None

    async def get_approvals(self, status: str = "pending") -> list:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                f"{self.base_url}/v1/approvals",
                headers=self.headers,
                params={"status": status},
            )
            if r.status_code != 200:
                return []
            data: Any = r.json()
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                items = data.get("items", [])
                return items if isinstance(items, list) else []
            return []

    async def decide_approval(
        self, approval_id: str, decision: str, justification: str = ""
    ) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{self.base_url}/v1/approvals/{approval_id}/decide",
                    headers=self.headers,
                    json={"decision": decision, "justification": justification},
                )
                if r.status_code not in (200, 201):
                    return None
                payload: Any = r.json()
                return payload if isinstance(payload, dict) else None
        except Exception:
            return None


openclaw_client = OpenClawClient()
