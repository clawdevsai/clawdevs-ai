<!--
  Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
 -->

# ClawDevs AI — Plugins Manifest

## Overview

List of all official plugins loaded in ClawDevs AI. Each plugin extends OpenClaw with specialized tools and integrations.

## Active Plugins

### 1. GitHub Integration Plugin

**ID**: `github-integration`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `100` (early)

**Purpose**: Manage GitHub repositories, create issues, manage PRs, check status

**Tools**:
- `create_github_issue` — Create new issue in repository
- `check_pr_status` — Get status of pull request
- `merge_pr` — Merge pull request to target branch
- `list_issues` — List open issues with filters
- `add_pr_comment` — Add comment to PR
- `get_code_file` — Read file from repository
- `search_code` — Search code across repos

**Hooks**:
- `before_model_resolve` — Validate GitHub token availability
- `after_tool_call` — Log all GitHub operations
- `tool.selected` — Rate-limit enforcement

**Configuration**:
```json
{
  "api_token": "${GIT_TOKEN}",
  "organization": "${GIT_ORG}",
  "rate_limit": 5000,
  "retry_attempts": 3,
  "timeout_ms": 30000
}
```

**Used by**: `ceo`, `dev_backend`, `dev_frontend`, `dev_mobile`, `qa_engineer`

**Permissions**:
- `read:repo` ✓
- `write:issues` ✓
- `write:pull_requests` ✓

---

### 2. Telegram Bot Plugin

**ID**: `telegram-bot`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `200` (channel integration)

**Purpose**: Send messages and notifications to Telegram

**Tools**:
- `send_telegram_message` — Send text message to chat
- `send_telegram_notification` — Send formatted notification
- `get_telegram_chat_id` — Get chat ID for user

**Hooks**:
- `response.ready` — Send final response to Telegram
- `error.occurred` — Send error alerts to director
- `cron.done` — Send cron job status updates

**Configuration**:
```json
{
  "bot_token": "${TELEGRAM_BOT_TOKEN_CEO}",
  "chat_id": "${TELEGRAM_CHAT_ID_CEO}",
  "markdown_enabled": true,
  "timeout_ms": 10000
}
```

**Used by**: `ceo`

**Permissions**:
- `send_messages` ✓
- `file_upload` ✓

---

### 3. Ollama LLM Plugin (Local)

**ID**: `ollama-llm`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `300` (inference)

**Purpose**: Local LLM inference via Ollama (cost optimization)

**Tools**:
- `ollama_complete` — Simple text completion
- `ollama_chat` — Multi-turn conversation
- `ollama_embed` — Generate embeddings for semantic search

**Hooks**:
- `before.model` — Route simple tasks to Ollama
- `model.response` — Validate local model output

**Configuration**:
```json
{
  "base_url": "http://ollama:11434",
  "model": "nomic-embed-text",
  "timeout_ms": 60000,
  "fallback_to_remote": true
}
```

**Used by**: all agents (for embeddings; text generation fallback)

**Permissions**:
- `network_access` ✓
- `local_inference` ✓

---

### 4. OpenRouter LLM Plugin (Remote)

**ID**: `openrouter-llm`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `300` (inference)

**Purpose**: Remote LLM inference (GPT-4, Claude) when Ollama insufficient

**Tools**:
- `openrouter_complete` — Use remote model for completion
- `openrouter_chat` — Multi-turn with remote model

**Hooks**:
- `before.model` — Route complex tasks to OpenRouter
- `model.response` — Cost tracking for remote inference

**Configuration**:
```json
{
  "api_key": "${OPENROUTER_API_KEY}",
  "base_url": "${OPENROUTER_BASE_URL}",
  "model": "${OPENROUTER_MODEL}",
  "timeout_ms": 120000,
  "max_tokens": 4096,
  "cost_tracking": true
}
```

**Used by**: `ceo`, `arquiteto`, `security_engineer` (complex reasoning)

**Permissions**:
- `network_access` ✓
- `api_token_usage` ✓

---

### 5. SearXNG Web Search Plugin

**ID**: `searxng-search`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `400` (external data)

**Purpose**: Web search for current information

**Tools**:
- `web_search` — Search the web
- `get_url_content` — Fetch and parse webpage

**Hooks**:
- `after.tool_call` — Sanitize search results (remove PII)
- `tool.selected` — Rate-limit enforcement (max 30 req/min)

**Configuration**:
```json
{
  "base_url": "http://searxng-proxy:18080",
  "timeout_ms": 30000,
  "max_results": 10,
  "rate_limit_per_minute": 30
}
```

**Used by**: `ceo`, `po`, `memory_curator` (research)

**Permissions**:
- `network_access` ✓
- `external_api_calls` ✓

---

### 6. PostgreSQL Data Plugin

**ID**: `postgres-db`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `500` (persistence)

**Purpose**: Persistent storage of sessions, memories, artifacts

**Tools**:
- `query_database` — Execute SELECT query
- `save_record` — Insert/update record
- `transaction_begin` — Start transaction
- `transaction_commit` — Commit changes

**Hooks**:
- `session.saved` — Persist session to database
- `error.occurred` — Log errors with context

**Configuration**:
```json
{
  "host": "postgres",
  "port": 5432,
  "database": "openclaw",
  "user": "${PANEL_DB_USER}",
  "password": "${PANEL_DB_PASSWORD}",
  "ssl": false,
  "pool_size": 20,
  "query_timeout_ms": 10000
}
```

**Used by**: internal (session/memory persistence)

**Permissions**:
- `database_read` ✓
- `database_write` ✓

---

### 7. Redis Cache Plugin

**ID**: `redis-cache`
**Version**: `1.0.0`
**Status**: `active`
**Load Order**: `600` (performance)

**Purpose**: Fast caching of frequently accessed data

**Tools**:
- `cache_get` — Retrieve from cache
- `cache_set` — Store in cache
- `cache_delete` — Remove from cache

**Hooks**:
- `context.loaded` — Check cache for memories
- `tool.executed` — Cache tool results
- `session.saved` — Cache session metadata

**Configuration**:
```json
{
  "host": "redis",
  "port": 6379,
  "password": "${PANEL_REDIS_PASSWORD}",
  "db": 0,
  "default_ttl_seconds": 3600
}
```

**Used by**: internal (caching layer)

**Permissions**:
- `cache_read` ✓
- `cache_write` ✓

---

## Plugin Execution Order

```
Startup:
  1. postgres-db (persistence)
  2. redis-cache (cache)
  3. ollama-llm (local inference)
  4. openrouter-llm (remote inference)
  5. github-integration (external APIs)
  6. searxng-search (web access)
  7. telegram-bot (notifications)

Agent Run:
  1. before.model → openrouter-llm (route decision)
  2. before.tool_call → github-integration (auth check)
  3. tool.executed → redis-cache (cache result)
  4. response.ready → telegram-bot (notify director)
  5. session.saved → postgres-db (persist)
```

## Plugin Dependencies

```
postgres-db
  └─ (none)

redis-cache
  └─ (none)

ollama-llm
  └─ (none)

openrouter-llm
  └─ (none)

github-integration
  ├─ postgres-db (log operations)
  └─ redis-cache (cache API responses)

searxng-search
  ├─ postgres-db (log queries)
  └─ redis-cache (cache results)

telegram-bot
  └─ (none)
```

## Plugin Health Check

```bash
# Check all plugins
openclaw plugin health

# Output:
# github-integration    ✓ healthy (auth ok, ratelimit 4950/5000)
# telegram-bot         ✓ healthy (connected)
# ollama-llm          ✓ healthy (model loaded)
# openrouter-llm      ✓ healthy (api responding)
# searxng-search      ✓ healthy (search working)
# postgres-db         ✓ healthy (2 connections)
# redis-cache         ✓ healthy (cache hit ratio 85%)
```

## Adding New Plugins

To add a new plugin:

1. Create plugin directory: `docker/base/openclaw-config/plugins/<plugin-id>/`
2. Create `manifest.json` with tools, hooks, config
3. Create `SKILL.md` with description
4. Implement tools in `src/` directory
5. Add entry to this document
6. Test locally: `openclaw plugin test <plugin-id>`
7. Load in agent config: `"plugins": ["plugin-id"]`

## Updating Plugins

When updating a plugin:

1. Update version in manifest.json
2. Document breaking changes
3. Run test suite
4. Update SKILL.md if interface changes
5. Reload OpenClaw: `openclaw plugin reload <plugin-id>`

