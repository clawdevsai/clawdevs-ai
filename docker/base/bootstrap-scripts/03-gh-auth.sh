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

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) ausente no bootstrap" >&2
  exit 1
fi
gh --version | head -n 1

# Autenticar GitHub CLI de forma nao interativa para os agentes
if [ -n "${GH_TOKEN:-}" ]; then
  printf '%s' "${GH_TOKEN}" | gh auth login --hostname github.com --with-token >/tmp/gh-auth.log 2>&1 || true
  gh auth setup-git >/tmp/gh-auth-setup-git.log 2>&1 || true
  gh auth status >/tmp/gh-auth-status.log 2>&1 || true
else
  echo "GH_TOKEN ausente: GitHub CLI iniciara sem autenticacao persistida" >/tmp/gh-auth-status.log
fi
# Contexto inicial: primeiro repositorio listavel da org (sem repo fixo em env). Demais repos: gh e claw-repo-discover / claw-repo-switch.
initial_repo=""
if [ -n "${GH_TOKEN:-}" ] || [ -n "${GIT_TOKEN:-}" ]; then
  initial_repo="$(gh repo list "${GIT_ORG}" --limit 1 --json nameWithOwner --jq '.[0].nameWithOwner' 2>/dev/null || true)"
  case "${initial_repo}" in ''|'null') initial_repo="" ;; esac
  if [ -n "${initial_repo}" ] && gh api "repos/${initial_repo}" --silent >/dev/null 2>&1; then
    write_repository_context "${initial_repo}" "${ACTIVE_REPOSITORY_BRANCH}"
  else
    echo "[bootstrap] nenhum repositorio inicial para '${GIT_ORG}' (lista vazia ou sem acesso); use claw-repo-switch org/repo"
    echo "[bootstrap] repositorios listados por gh para '${GIT_ORG}' (ate 200; vazio = token/org ou permissao):"
    if ! gh repo list "${GIT_ORG}" --limit 200 --json nameWithOwner --jq '.[].nameWithOwner' 2>/tmp/gh-repo-list-bootstrap.log; then
      echo "[bootstrap] falha ao listar; ver /tmp/gh-repo-list-bootstrap.log"
      sed -n '1,20p' /tmp/gh-repo-list-bootstrap.log 2>/dev/null || true
    fi
  fi
else
  echo "[bootstrap] sem token GitHub: pulando contexto de repositorio; use claw-repo-switch apos autenticar"
fi
