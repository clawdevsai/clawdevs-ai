# Design: Web Search & Page Reading for All Agents (Free)

**Date:** 2026-03-21
**Status:** Approved

## Problem

Agents fail to browse the internet because Chromium running inside a Kubernetes container is unstable (shared memory issues, sandboxing restrictions, env var persistence failures). Agents receive "browser temporarily unavailable" errors and fall back to stale data.

## Goal

Give all 11 agents reliable, free internet access for:
- **Web search** — find links and snippets for any query (Google, Bing, DuckDuckGo)
- **Page reading** — fetch and read any URL as clean markdown

## Solution: Jina Reader + SearxNG

### Architecture

```
Agent (OpenClaw)
    │
    ├── web_search("query") ──► SearxNG pod (K8s ClusterIP :8080)
    │                            aggregates Google + Bing + DDG
    │                            returns JSON with links/snippets
    │
    └── web_read("https://...") ──► r.jina.ai/{url} (free public API)
                                     returns clean markdown
```

### Components

#### 1. SearxNG — New K8s Deployment
- **Image:** `searxng/searxng:latest` (open-source, free, self-hosted)
- **Service:** ClusterIP, port `8080`, DNS name: `searxng`
- **Config:** `settings.yml` enabling Google, Bing, DuckDuckGo, GitHub engines
- **Auth:** none (internal cluster network)
- **New file:** `k8s/base/searxng-deployment.yaml`
- **Kustomization:** add resource entry to `k8s/base/kustomization.yaml`

#### 2. Jina Reader — No Deployment Needed
- **Public API:** `https://r.jina.ai/{target_url}`
- **Example:** `curl https://r.jina.ai/https://docs.python.org/3/` → markdown
- **Cost:** free for moderate use, no API key required
- **Self-hosted fallback:** `jinaai/reader` Docker image if rate limits become an issue

#### 3. Wrapper Scripts in Agent Pod
Two new scripts added during bootstrap in `openclaw-pod.yaml`:

- **`/usr/local/bin/web-search`**
  Calls `http://searxng:8080/search?q=<query>&format=json&categories=general`
  Returns formatted list of results (title, URL, snippet)

- **`/usr/local/bin/web-read`**
  Calls `https://r.jina.ai/<url>` via curl
  Returns clean markdown content of the page

Both scripts replace the Chromium installation that was causing failures.

#### 4. OpenClaw Tool Registration
Two new `exec`-based tools in `openclaw.json` (embedded in `openclaw-pod.yaml`):
- `web_search` — enabled for all 11 agents
- `web_read` — enabled for all 11 agents

The existing unstable `browser` tool remains in config but agents are instructed to prefer `web_search`/`web_read`.

#### 5. Agent TOOLS.md Updates
All 11 agents' `TOOLS.md` updated to document:
- `web_search "<query>"` — search the web
- `web_read "<url>"` — read a page as markdown
- When to use each tool

## Files Changed

```
# New files
k8s/base/searxng-deployment.yaml          — SearxNG K8s Deployment + Service + ConfigMap

# Modified files
k8s/base/kustomization.yaml               — add searxng-deployment.yaml resource
k8s/base/openclaw-pod.yaml                — add wrapper scripts in bootstrap; add web_search/web_read tools in openclaw.json; remove Chromium bootstrap
k8s/base/openclaw-config/ceo/TOOLS.md
k8s/base/openclaw-config/po/TOOLS.md
k8s/base/openclaw-config/arquiteto/TOOLS.md
k8s/base/openclaw-config/dev_backend/TOOLS.md
k8s/base/openclaw-config/dev_frontend/TOOLS.md
k8s/base/openclaw-config/dev_mobile/TOOLS.md
k8s/base/openclaw-config/qa_engineer/TOOLS.md
k8s/base/openclaw-config/security_engineer/TOOLS.md
k8s/base/openclaw-config/ux_designer/TOOLS.md
k8s/base/openclaw-config/devops_sre/TOOLS.md
k8s/base/openclaw-config/dba_data_engineer/TOOLS.md
```

## Cost

| Component | Cost |
|---|---|
| SearxNG | $0 — self-hosted open-source |
| Jina Reader (public API) | $0 — free for moderate use |
| Jina Reader (self-hosted) | $0 — if rate limits are hit |
| **Total** | **$0** |

## Verification

1. `kubectl exec -it clawdevs-ai-0 -- web-search "python asyncio tutorial"` → returns results
2. `kubectl exec -it clawdevs-ai-0 -- web-read "https://docs.python.org/3/"` → returns markdown
3. Ask an agent to search for something → agent uses `web_search` tool successfully
4. `kubectl get pods -n default | grep searxng` → SearxNG pod running
5. `curl http://searxng:8080/healthz` from inside the cluster → 200 OK
