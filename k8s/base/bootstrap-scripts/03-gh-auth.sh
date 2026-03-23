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
if ! gh api "repos/${GITHUB_DEFAULT_REPOSITORY}" --silent >/dev/null 2>&1; then
  discovered_repo="$(gh repo list "${GITHUB_ORG}" --limit 1 --json nameWithOwner --jq '.[0].nameWithOwner' 2>/dev/null || true)"
  if [ -n "${discovered_repo}" ]; then
    GITHUB_DEFAULT_REPOSITORY="${discovered_repo}"
  fi
fi
if ! gh api "repos/${GITHUB_DEFAULT_REPOSITORY}" --silent >/dev/null 2>&1; then
  GITHUB_DEFAULT_REPOSITORY="${GITHUB_ORG}/user-api"
fi
write_repository_context "${GITHUB_DEFAULT_REPOSITORY}" "${ACTIVE_REPOSITORY_BRANCH}"
