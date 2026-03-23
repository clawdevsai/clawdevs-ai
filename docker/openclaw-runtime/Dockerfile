FROM node:22-bookworm-slim

ARG OPENCLAW_VERSION=2026.3.22
ARG DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends ca-certificates curl bash git jq python3; \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg; \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      > /etc/apt/sources.list.d/github-cli.list; \
    apt-get update -qq; \
    apt-get install -y --no-install-recommends gh; \
    npm install -g npm@11.12.0; \
    if [ -n "${OPENCLAW_VERSION}" ]; then OPENCLAW_NPM_SPEC="openclaw@${OPENCLAW_VERSION}"; else OPENCLAW_NPM_SPEC="openclaw@latest"; fi; \
    npm install -g --omit=dev "${OPENCLAW_NPM_SPEC}"; \
    npm cache clean --force; \
    openclaw --version | head -n 1; \
    gh --version | head -n 1; \
    apt-get autoremove -y --purge; \
    apt-get clean; \
    rm -rf /root/.npm /tmp/* /var/tmp/*; \
    rm -rf /var/lib/apt/lists/*

ENV OPENCLAW_NO_ONBOARD=1 \
    OPENCLAW_NO_PROMPT=1 \
    OPENCLAW_STATE_DIR=/data/openclaw \
    GH_CONFIG_DIR=/data/openclaw/.config/gh

WORKDIR /data/openclaw
