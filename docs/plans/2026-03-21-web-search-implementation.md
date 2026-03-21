# Web Search & Page Reading for All Agents Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Give all 11 agents reliable, free internet access (web search + page reading) by deploying SearxNG in Kubernetes and adding `web-search`/`web-read` wrapper scripts to the agent pod, replacing the unstable Chromium browser.

**Architecture:** SearxNG runs as a K8s Deployment (ClusterIP service, DNS `searxng:8080`) and aggregates Google, Bing and DuckDuckGo. Two bash scripts — `web-search` and `web-read` — are installed in the agent pod during bootstrap; they call SearxNG and the free Jina Reader public API (`r.jina.ai`) via `curl`. Agents call these via the existing `exec` tool. The CEO (which lacks `exec`) gets `exec` added to its allowed tools.

**Tech Stack:** Kubernetes, SearxNG (searxng/searxng:latest), Jina Reader public API (r.jina.ai), bash/curl

---

### Task 1: Create SearxNG K8s Deployment

**Files:**
- Create: `k8s/base/searxng-deployment.yaml`

**Step 1: Create the YAML file**

```yaml
# k8s/base/searxng-deployment.yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: searxng-config
data:
  settings.yml: |
    general:
      debug: false
      instance_name: "clawdevs-searxng"
    search:
      safe_search: 0
      autocomplete: ""
      default_lang: "pt-BR"
      formats:
        - html
        - json
    server:
      port: 8080
      bind_address: "0.0.0.0"
      secret_key: "clawdevs-searxng-secret-key-change-in-prod"
      limiter: false
      public_instance: false
    engines:
      - name: google
        engine: google
        shortcut: g
        disabled: false
      - name: bing
        engine: bing
        shortcut: b
        disabled: false
      - name: duckduckgo
        engine: duckduckgo
        shortcut: d
        disabled: false
      - name: github
        engine: github
        shortcut: gh
        disabled: false
    outgoing:
      request_timeout: 10.0
      useragent_suffix: "ClawDevs AI Research Agent"
    ui:
      default_theme: simple
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: searxng
  labels:
    app: searxng
spec:
  replicas: 1
  selector:
    matchLabels:
      app: searxng
  template:
    metadata:
      labels:
        app: searxng
    spec:
      containers:
        - name: searxng
          image: searxng/searxng:latest
          ports:
            - containerPort: 8080
          env:
            - name: SEARXNG_SETTINGS_PATH
              value: /etc/searxng/settings.yml
          volumeMounts:
            - name: searxng-config
              mountPath: /etc/searxng
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
      volumes:
        - name: searxng-config
          configMap:
            name: searxng-config
---
apiVersion: v1
kind: Service
metadata:
  name: searxng
spec:
  selector:
    app: searxng
  ports:
    - port: 8080
      targetPort: 8080
  type: ClusterIP
```

**Step 2: Verify the file was created**

```bash
cat k8s/base/searxng-deployment.yaml | head -5
```
Expected: `# k8s/base/searxng-deployment.yaml`

**Step 3: Commit**

```bash
git add k8s/base/searxng-deployment.yaml
git commit -m "feat: add SearxNG K8s deployment for free web search"
```

---

### Task 2: Register SearxNG in kustomization.yaml

**Files:**
- Modify: `k8s/base/kustomization.yaml:4-8`

**Step 1: Add the resource entry**

In `k8s/base/kustomization.yaml`, add `searxng-deployment.yaml` to the `resources:` list:

```yaml
resources:
  - openclaw-pod.yaml
  - ollama-pod.yaml
  - ollama-pvc.yaml
  - networkpolicy-allow-egress.yaml
  - searxng-deployment.yaml    # <-- add this line
```

**Step 2: Verify kustomize is valid**

```bash
kubectl kustomize k8s/base/ | grep -c "kind:"
```
Expected: number ≥ 6 (one more than before, due to new Deployment + Service + ConfigMap)

**Step 3: Commit**

```bash
git add k8s/base/kustomization.yaml
git commit -m "feat: register SearxNG in kustomization"
```

---

### Task 3: Replace Chromium bootstrap with web-search/web-read scripts

**Files:**
- Modify: `k8s/base/openclaw-pod.yaml:297-323`

**Context:** Lines 297–323 install Chromium and create the `openclaw-chrome` wrapper. This is unreliable in K8s due to sandbox and shared-memory issues. We replace it with two lightweight curl-based scripts.

**Step 1: Remove Chromium install and replace with script creation**

Find and replace the block starting at line 297 (`apt-get install -y --no-install-recommends ... chromium`) through line 323 (`echo "Browser disponivel: ..."`) with:

```bash
              # --- web-search: calls SearxNG (self-hosted, cluster-internal) ---
              cat > /usr/local/bin/web-search <<'SCRIPT'
              #!/usr/bin/env bash
              set -euo pipefail
              query="${*}"
              if [ -z "${query}" ]; then
                echo "Usage: web-search <query>" >&2
                exit 1
              fi
              encoded="$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "${query}")"
              result="$(curl -sf "http://searxng:8080/search?q=${encoded}&format=json&categories=general&language=pt-BR" 2>/dev/null || true)"
              if [ -z "${result}" ]; then
                echo "[web-search] SearxNG indisponível. Tente novamente." >&2
                exit 1
              fi
              echo "${result}" | python3 -c "
              import json,sys
              data = json.load(sys.stdin)
              results = data.get('results', [])[:10]
              for i, r in enumerate(results, 1):
                  print(f\"{i}. {r.get('title','(sem título)')}\")
                  print(f\"   URL: {r.get('url','')}\")
                  print(f\"   {r.get('content','')[:200]}\")
                  print()
              if not results:
                  print('Nenhum resultado encontrado.')
              "
              SCRIPT
              chmod +x /usr/local/bin/web-search

              # --- web-read: calls Jina Reader public API (free, no API key) ---
              cat > /usr/local/bin/web-read <<'SCRIPT'
              #!/usr/bin/env bash
              set -euo pipefail
              url="${1:-}"
              if [ -z "${url}" ]; then
                echo "Usage: web-read <url>" >&2
                exit 1
              fi
              result="$(curl -sf -H "Accept: text/markdown" "https://r.jina.ai/${url}" 2>/dev/null || true)"
              if [ -z "${result}" ]; then
                echo "[web-read] Não foi possível ler a URL: ${url}" >&2
                exit 1
              fi
              echo "${result}"
              SCRIPT
              chmod +x /usr/local/bin/web-read
              echo "[bootstrap] web-search e web-read instalados em /usr/local/bin/"
```

> **Note:** Keep the `apt-get install` line but remove `chromium` from the package list:
> ```bash
> apt-get install -y --no-install-recommends ca-certificates curl bash git jq gh python3
> ```
> (Replace `chromium` with `python3` — needed for URL encoding and JSON parsing in the scripts)

**Step 2: Verify the change makes sense (dry-run)**

```bash
grep -n "web-search\|web-read\|chromium\|CHROME_BIN" k8s/base/openclaw-pod.yaml
```
Expected: lines with `web-search` and `web-read` present, NO lines with `chromium` or `CHROME_BIN`.

**Step 3: Commit**

```bash
git add k8s/base/openclaw-pod.yaml
git commit -m "feat: replace Chromium bootstrap with web-search/web-read curl scripts"
```

---

### Task 4: Add exec tool to CEO in openclaw.json

**Files:**
- Modify: `k8s/base/openclaw-pod.yaml` — CEO agent section (~line 859)

**Context:** The CEO agent currently lacks `exec` and `process` tools, so it cannot run `web-search` or `web-read`. The screenshot error ("não posso executar comandos de linha diretos") confirms this. We add `exec` to CEO's tools.

**Step 1: Find the CEO tools block and add exec**

Find the CEO's `"tools"` block (looks like this):

```json
"tools": {
  "allow": [
    "read",
    "write",
    "browser",
    "message",
    "agents_list",
    ...
  ]
},
```

Replace with:

```json
"tools": {
  "allow": [
    "read",
    "write",
    "exec",
    "process",
    "browser",
    "message",
    "agents_list",
    "sessions_list",
    "sessions_history",
    "sessions_send",
    "sessions_spawn",
    "session_status",
    "group:plugins"
  ],
  "exec": {
    "host": "gateway",
    "security": "full",
    "ask": "off"
  }
},
```

**Step 2: Verify CEO has exec**

```bash
grep -A 30 '"id": "ceo"' k8s/base/openclaw-pod.yaml | grep '"exec"'
```
Expected: two matches (one in `"allow"`, one as the `"exec"` config object)

**Step 3: Commit**

```bash
git add k8s/base/openclaw-pod.yaml
git commit -m "feat: add exec tool to CEO agent for web-search/web-read access"
```

---

### Task 5: Update TOOLS.md for all 11 agents

**Files:**
- Modify: `k8s/base/openclaw-config/ceo/TOOLS.md`
- Modify: `k8s/base/openclaw-config/po/TOOLS.md`
- Modify: `k8s/base/openclaw-config/arquiteto/TOOLS.md`
- Modify: `k8s/base/openclaw-config/dev_backend/TOOLS.md`
- Modify: `k8s/base/openclaw-config/dev_frontend/TOOLS.md`
- Modify: `k8s/base/openclaw-config/dev_mobile/TOOLS.md`
- Modify: `k8s/base/openclaw-config/qa_engineer/TOOLS.md`
- Modify: `k8s/base/openclaw-config/security_engineer/TOOLS.md`
- Modify: `k8s/base/openclaw-config/ux_designer/TOOLS.md`
- Modify: `k8s/base/openclaw-config/devops_sre/TOOLS.md`
- Modify: `k8s/base/openclaw-config/dba_data_engineer/TOOLS.md`

**Step 1: Read each TOOLS.md before editing**

Read each file to understand its current format, then add/update the web tools section.

**Step 2: Add web tools section to each TOOLS.md**

For every agent that already has a `browser` or `internet_search` line, **replace** that line with:

```markdown
- `exec("web-search '<query>'")`: pesquisar na internet via SearxNG (agrega Google, Bing, DuckDuckGo). Retorna até 10 resultados com título, URL e snippet. Exemplo: `web-search "python asyncio best practices 2025"`
- `exec("web-read '<url>'")`: ler qualquer página web como markdown limpo via Jina Reader. Exemplo: `web-read "https://docs.python.org/3/library/asyncio.html"`
```

And update the `autonomia_de_pesquisa_e_aprendizado` section (or equivalent) to reference these tools:

```markdown
## pesquisa_web
- Para pesquisar: `exec("web-search '<query>'")`
- Para ler uma página: `exec("web-read '<url>'")`
- SearxNG agrega Google, Bing, DuckDuckGo e GitHub simultaneamente — sem API key, sem custo.
- Jina Reader converte qualquer URL em markdown limpo — sem API key, sem custo.
- Citar sempre a URL de origem nos artefatos produzidos.
```

**Step 3: Verify all TOOLS.md files have the new web tools**

```bash
grep -l "web-search" k8s/base/openclaw-config/*/TOOLS.md | wc -l
```
Expected: `11`

**Step 4: Commit**

```bash
git add k8s/base/openclaw-config/*/TOOLS.md
git commit -m "feat: update all 11 agents TOOLS.md with web-search/web-read instructions"
```

---

### Task 6: Apply to Kubernetes and verify

**Step 1: Apply the changes**

```bash
make openclaw-apply
```
Or directly:
```bash
kubectl apply -k k8s/base/ --server-side --force-conflicts
```

**Step 2: Wait for SearxNG pod to be ready**

```bash
kubectl rollout status deployment/searxng
```
Expected: `deployment "searxng" successfully rolled out`

**Step 3: Verify SearxNG is accessible from inside the cluster**

```bash
kubectl exec -it clawdevs-ai-0 -- curl -sf "http://searxng:8080/healthz"
```
Expected: HTTP 200 or any response (not a connection refused)

**Step 4: Test web-search from inside the pod**

```bash
kubectl exec -it clawdevs-ai-0 -- web-search "OpenClaw AI agents tutorial"
```
Expected: numbered list of 1–10 results with titles, URLs, and snippets

**Step 5: Test web-read from inside the pod**

```bash
kubectl exec -it clawdevs-ai-0 -- web-read "https://example.com"
```
Expected: markdown content of example.com (title, body text)

**Step 6: Verify scripts are in place**

```bash
kubectl exec -it clawdevs-ai-0 -- which web-search web-read
```
Expected:
```
/usr/local/bin/web-search
/usr/local/bin/web-read
```

**Step 7: Commit any fixes, create PR**

```bash
git push origin main
```

---

## Summary of All Files Changed

```
# New files
k8s/base/searxng-deployment.yaml

# Modified files
k8s/base/kustomization.yaml                          — add searxng-deployment.yaml
k8s/base/openclaw-pod.yaml                           — replace Chromium with scripts; add exec to CEO
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

## Cost: $0
- SearxNG: self-hosted open-source
- Jina Reader: free public API (no key)
