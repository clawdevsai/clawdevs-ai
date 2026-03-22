mkdir -p "${OPENCLAW_STATE_DIR}/git-hooks"
cat > "${OPENCLAW_STATE_DIR}/git-hooks/pre-commit" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
case "${branch}" in
  main|master)
    echo "Commit bloqueado: branch '${branch}' protegida. Crie uma branch de trabalho e abra PR."
    exit 1
    ;;
esac
exit 0
EOF
cat > "${OPENCLAW_STATE_DIR}/git-hooks/pre-push" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
while read -r local_ref local_sha remote_ref remote_sha; do
  remote_branch="${remote_ref#refs/heads/}"
  case "${remote_branch}" in
    main|master)
      echo "Push bloqueado: envio direto para '${remote_branch}' e proibido. Use Pull Request."
      exit 1
      ;;
  esac
done
exit 0
EOF
chmod +x "${OPENCLAW_STATE_DIR}/git-hooks/pre-commit" "${OPENCLAW_STATE_DIR}/git-hooks/pre-push"
git config --global core.hooksPath "${OPENCLAW_STATE_DIR}/git-hooks"
