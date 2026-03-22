APT_STAMP="${OPENCLAW_STATE_DIR}/backlog/status/.apt-installed"
if [ ! -f "${APT_STAMP}" ] || ! command -v gh >/dev/null 2>&1; then
  apt-get update
  apt-get install -y --no-install-recommends ca-certificates curl bash git jq python3
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  apt-get update -qq
  apt-get install -y gh
  apt-get autoremove -y
  apt-get clean
  rm -rf /var/lib/apt/lists/*
  touch "${APT_STAMP}"
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI nao foi instalado corretamente" >&2
  exit 1
fi
gh --version | head -n 1
