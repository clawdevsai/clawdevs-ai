# --- web-search: pesquisa via SearxNG (self-hosted, cluster-internal) ---
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
  echo "[web-search] SearxNG indisponivel. Tente novamente." >&2
  exit 1
fi
echo "${result}" | python3 -c "
import json,sys
data = json.load(sys.stdin)
results = data.get('results', [])[:10]
for i, r in enumerate(results, 1):
    print(f'{i}. {r.get(\"title\",\"(sem titulo)\")}')
    print(f'   URL: {r.get(\"url\",\"\")}')
    print(f'   {r.get(\"content\",\"\")[:200]}')
    print()
if not results:
    print('Nenhum resultado encontrado.')
"
SCRIPT
chmod +x /usr/local/bin/web-search
# --- web-read: leitura de paginas via Jina Reader (API publica gratuita) ---
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
  echo "[web-read] Nao foi possivel ler a URL: ${url}" >&2
  exit 1
fi
echo "${result}"
SCRIPT
chmod +x /usr/local/bin/web-read
echo "[bootstrap] web-search e web-read instalados em /usr/local/bin/"
