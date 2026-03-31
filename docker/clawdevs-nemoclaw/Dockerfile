FROM public.ecr.aws/docker/library/node:22-bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
      ca-certificates bash git curl jq python3 python3-venv python3-pip \
      docker.io tzdata; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone; \
    python3 -m venv /opt/nemoclaw-bridge-venv; \
    /opt/nemoclaw-bridge-venv/bin/pip install --no-cache-dir fastapi==0.115.12 uvicorn==0.34.0; \
    npm install -g npm@10.9.0; \
    apt-get autoremove -y --purge; \
    apt-get clean; \
    rm -rf /root/.npm /tmp/* /var/tmp/* /var/lib/apt/lists/*

ENV HOME=/data/nemoclaw \
    NEMOCLAW_NON_INTERACTIVE=1

WORKDIR /data/nemoclaw

COPY docker/clawdevs-nemoclaw/bridge.py /opt/nemoclaw-bridge/bridge.py
COPY docker/clawdevs-nemoclaw/entrypoint.sh /usr/local/bin/nemoclaw-entrypoint.sh
RUN chmod +x /usr/local/bin/nemoclaw-entrypoint.sh

EXPOSE 18789

ENTRYPOINT ["/usr/local/bin/nemoclaw-entrypoint.sh"]
