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

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://panel:password@clawdevs-panel-db:5432/clawdevs_panel"

    # Redis
    redis_url: str = "redis://:password@clawdevs-panel-redis:6379/0"

    # Auth
    secret_key: str = "change-me-32-chars-minimum-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Admin bootstrap
    admin_username: str = "admin"
    admin_password: str = "change-me"

    # OpenClaw gateway
    openclaw_gateway_url: str = "http://clawdevs-ai:18789"
    openclaw_gateway_token: str = ""

    # GitHub
    github_token: str = ""
    github_org: str = ""
    github_default_repository: str = ""

    # OpenClaw data path (PVC mounted read-only)
    openclaw_data_path: str = "/data/openclaw"

    # Kubernetes
    k8s_namespace: str = "default"

    # Security
    debug: bool = False
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://clawdevs-panel-frontend:3000",
    ]

    model_config = {"env_prefix": "PANEL_", "env_file": ".env", "extra": "allow"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
