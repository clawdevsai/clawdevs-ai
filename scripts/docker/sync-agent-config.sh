#!/bin/bash
# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
#
# Gera tmp/agent-config-flat/ com os arquivos de configuracao dos agentes
# com os nomes "flat" exatamente como o Kustomize configMapGenerator produziria.
#
# Uso: bash scripts/docker/sync-agent-config.sh
# Executado automaticamente por 'make up' antes do docker compose up.

set -euo pipefail

KUST="container/base/kustomization.yaml"
SRC_BASE="container/base"
DST="tmp/agent-config-flat"

if [ ! -f "$KUST" ]; then
  echo "[sync-agent-config] ERRO: $KUST nao encontrado. Execute a partir da raiz do projeto."
  exit 1
fi

mkdir -p "$DST"

in_agent_config=false
in_files=false
count=0

while IFS= read -r line; do
  # Detecta inicio do configMapGenerator openclaw-agent-config
  if [[ "$line" == *"name: openclaw-agent-config"* ]]; then
    in_agent_config=true
    in_files=false
    continue
  fi

  # Para ao encontrar o proximo configMapGenerator (openclaw-bootstrap-scripts)
  if $in_agent_config && [[ "$line" == *"name: openclaw-bootstrap-scripts"* ]]; then
    break
  fi

  # Detecta secao 'files:' dentro do configMap correto
  if $in_agent_config && [[ "$line" =~ ^[[:space:]]*files: ]]; then
    in_files=true
    continue
  fi

  # Para secao files ao encontrar outra chave no mesmo nivel
  if $in_files && [[ "$line" =~ ^[[:space:]]{2}[a-zA-Z] ]] && ! [[ "$line" =~ ^[[:space:]]*- ]]; then
    in_files=false
  fi

  # Extrai mapeamentos: - key=path (com ou sem comentario no final)
  if $in_files && [[ "$line" =~ ^[[:space:]]*-[[:space:]]([^=]+)=([^[:space:]#]+) ]]; then
    key="${BASH_REMATCH[1]}"
    src_rel="${BASH_REMATCH[2]}"
    src_full="${SRC_BASE}/${src_rel}"

    if [ -f "$src_full" ]; then
      cp "$src_full" "${DST}/${key}"
      count=$((count + 1))
    else
      echo "[sync-agent-config] AVISO: arquivo fonte nao encontrado: $src_full"
    fi
  fi
done < "$KUST"

echo "[sync-agent-config] $count arquivos sincronizados em $DST"
