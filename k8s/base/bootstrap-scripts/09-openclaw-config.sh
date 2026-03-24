# Verificar se o config ja existe e tem o token correto - evitar sobrescrita
# desnecessaria que causa "missing-meta-before-write" e faz o gateway encerrar.
_existing_token="$(jq -r '.gateway.auth.token // empty' "${OPENCLAW_STATE_DIR}/openclaw.json" 2>/dev/null || true)"
_existing_bind="$(jq -r '.gateway.bind // empty' "${OPENCLAW_STATE_DIR}/openclaw.json" 2>/dev/null || true)"
_existing_host_fallback="$(jq -r '.gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback // empty' "${OPENCLAW_STATE_DIR}/openclaw.json" 2>/dev/null || true)"
if [ -f "${OPENCLAW_STATE_DIR}/openclaw.json" ] && [ -n "${_existing_token}" ] && [ "${_existing_token}" = "${OPENCLAW_GATEWAY_TOKEN}" ] && [ "${_existing_bind}" = "lan" ] && [ "${_existing_host_fallback}" = "true" ]; then
  echo "[bootstrap] openclaw.json ja configurado com token correto e bind valido (${_existing_bind}), pulando escrita"
  mkdir -p ~/.openclaw
  cp "${OPENCLAW_STATE_DIR}/openclaw.json" ~/.openclaw/openclaw.json
else
echo "[bootstrap] escrevendo openclaw.json (primeira execucao ou token mudou)"
cat > "${OPENCLAW_STATE_DIR}/openclaw.json" <<'EOF'
{
  "gateway": {
    "mode": "local",
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "dangerouslyAllowHostHeaderOriginFallback": true
    },
    "auth": {
      "token": "__TOKEN__"
    }
  },
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://ollama:11434",
        "models": [
          {
            "id": "qwen3-next:80b-cloud",
            "name": "qwen3-next:80b-cloud"
          },
          {
            "id": "gpt-oss:120b-cloud",
            "name": "gpt-oss:120b-cloud"
          },
          {
            "id": "nemotron-3-super:cloud",
            "name": "nemotron-3-super:cloud"
          },
          {
            "id": "qwen3-coder:480b-cloud",
            "name": "qwen3-coder:480b-cloud"
          },
          {
            "id": "gemma3:27b-cloud",
            "name": "gemma3:27b-cloud"
          },
          {
            "id": "qwen3-vl:235b-cloud",
            "name": "qwen3-vl:235b-cloud"
          },
          {
            "id": "qwen3.5:397b-cloud",
            "name": "qwen3.5:397b-cloud"
          },
          {
            "id": "minimax-m2.7:cloud",
            "name": "minimax-m2.7:cloud"
          }
        ]
      }
    }
  },
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true,
      "allow": ["ceo", "po", "arquiteto", "dev_backend", "dev_frontend", "dev_mobile", "qa_engineer", "devops_sre", "security_engineer", "ux_designer", "dba_data_engineer"]
    }
  },
  "session": {
    "dmScope": "per-channel-peer",
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "30d",
      "maxEntries": 1000,
      "rotateBytes": "20mb",
      "maxDiskBytes": "3gb",
      "highWaterBytes": "2.4gb"
    },
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "unknown", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  },
  "skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 250
    }
  },
  "agents": {
    "defaults": {
      "model": "ollama/nemotron-3-super:cloud",
      "bootstrapMaxChars": 25000,
      "thinkingDefault": "low",
      "typingMode": "instant",
      "typingIntervalSeconds": 4,
      "sandbox": {
        "mode": "off",
        "sessionToolsVisibility": "spawned"
      },
      "subagents": {
        "runTimeoutSeconds": 1800,
        "maxConcurrent": 6,
        "maxSpawnDepth": 3,
        "maxChildrenPerAgent": 8,
        "archiveAfterMinutes": 120
      },
      "heartbeat": {
        "includeReasoning": true
      }
    },
    "list": [
      {
        "id": "ceo",
        "default": true,
        "name": "CEO",
        "model": "ollama/qwen3-vl:235b-cloud",
        "workspace": "/data/openclaw/workspace-ceo",
        "agentDir": "/data/openclaw/agents/ceo/agent",
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
        "subagents": {
          "allowAgents": ["po", "arquiteto", "dev_backend", "dev_frontend", "dev_mobile", "qa_engineer", "devops_sre", "security_engineer", "ux_designer", "dba_data_engineer"]
        }
      },
      {
        "id": "po",
        "name": "PO",
        "model": "ollama/nemotron-3-super:cloud",
        "workspace": "/data/openclaw/workspace-po",
        "agentDir": "/data/openclaw/agents/po/agent",
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
        "subagents": {
          "allowAgents": ["arquiteto", "ux_designer", "dev_backend", "dev_frontend", "dev_mobile", "qa_engineer", "devops_sre", "security_engineer", "dba_data_engineer"]
        }
      },
      {
        "id": "arquiteto",
        "name": "Arquiteto",
        "model": "ollama/qwen3.5:397b-cloud",
        "workspace": "/data/openclaw/workspace-arquiteto",
        "agentDir": "/data/openclaw/agents/arquiteto/agent",
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
        "subagents": {
          "allowAgents": ["dev_backend", "dev_frontend", "dev_mobile", "qa_engineer", "devops_sre", "security_engineer", "dba_data_engineer"]
        }
      },
      {
        "id": "dev_backend",
        "name": "Dev_Backend",
        "model": "ollama/qwen3-coder:480b-cloud",
        "workspace": "/data/openclaw/workspace-dev_backend",
        "agentDir": "/data/openclaw/agents/dev_backend/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": ["qa_engineer", "security_engineer"]
        }
      },
      {
        "id": "dev_frontend",
        "name": "Dev_Frontend",
        "model": "ollama/qwen3-coder:480b-cloud",
        "workspace": "/data/openclaw/workspace-dev_frontend",
        "agentDir": "/data/openclaw/agents/dev_frontend/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": ["qa_engineer", "security_engineer"]
        }
      },
      {
        "id": "dev_mobile",
        "name": "Dev_Mobile",
        "model": "ollama/qwen3-coder:480b-cloud",
        "workspace": "/data/openclaw/workspace-dev_mobile",
        "agentDir": "/data/openclaw/agents/dev_mobile/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": ["qa_engineer", "security_engineer"]
        }
      },
      {
        "id": "qa_engineer",
        "name": "QA_Engineer",
        "model": "ollama/nemotron-3-super:cloud",
        "workspace": "/data/openclaw/workspace-qa_engineer",
        "agentDir": "/data/openclaw/agents/qa_engineer/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": []
        }
      },
      {
        "id": "devops_sre",
        "name": "DevOps_SRE",
        "model": "ollama/nemotron-3-super:cloud",
        "workspace": "/data/openclaw/workspace-devops_sre",
        "agentDir": "/data/openclaw/agents/devops_sre/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": []
        }
      },
      {
        "id": "security_engineer",
        "name": "Security_Engineer",
        "model": "ollama/qwen3.5:397b-cloud",
        "workspace": "/data/openclaw/workspace-security_engineer",
        "agentDir": "/data/openclaw/agents/security_engineer/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": ["dev_backend", "dev_frontend", "dev_mobile"]
        }
      },
      {
        "id": "ux_designer",
        "name": "UX_Designer",
        "model": "ollama/nemotron-3-super:cloud",
        "workspace": "/data/openclaw/workspace-ux_designer",
        "agentDir": "/data/openclaw/agents/ux_designer/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": []
        }
      },
      {
        "id": "dba_data_engineer",
        "name": "DBA_DataEngineer",
        "model": "ollama/qwen3.5:397b-cloud",
        "workspace": "/data/openclaw/workspace-dba_data_engineer",
        "agentDir": "/data/openclaw/agents/dba_data_engineer/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "process",
            "browser",
            "message",
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
        "subagents": {
          "allowAgents": ["dev_backend", "devops_sre"]
        }
      },
      {
        "id": "memory_curator",
        "name": "Memory_Curator",
        "model": "ollama/qwen3-coder:480b-cloud",
        "workspace": "/data/openclaw/workspace-memory_curator",
        "agentDir": "/data/openclaw/agents/memory_curator/agent",
        "tools": {
          "allow": [
            "read",
            "write",
            "exec",
            "message",
            "sessions_list",
            "sessions_history",
            "group:plugins"
          ],
          "exec": {
            "host": "gateway",
            "security": "full",
            "ask": "off"
          }
        },
        "subagents": {
          "allowAgents": []
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "ceo",
      "match": {
        "channel": "telegram",
        "accountId": "default"
      }
    }
  ],
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "hash"
  },
  "channels": {
    "telegram": {
      "dmPolicy": "allowlist",
      "allowFrom": ["__TELEGRAM_CHAT_ID__"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["__TELEGRAM_CHAT_ID__"],
      "streaming": "partial",
      "accounts": {
        "default": {
          "botToken": "__TELEGRAM_BOT_TOKEN_CEO__",
          "dmPolicy": "allowlist",
          "allowFrom": ["__TELEGRAM_CHAT_ID__"],
          "groupPolicy": "allowlist",
          "groupAllowFrom": ["__TELEGRAM_CHAT_ID__"],
          "streaming": "partial"
        }
      }
    }
  }
}
EOF
sed -i "s/__TOKEN__/${OPENCLAW_GATEWAY_TOKEN}/g" "${OPENCLAW_STATE_DIR}/openclaw.json"
sed -i "s/__TELEGRAM_BOT_TOKEN_CEO__/${TELEGRAM_BOT_TOKEN_CEO}/g" "${OPENCLAW_STATE_DIR}/openclaw.json"
sed -i "s/__TELEGRAM_CHAT_ID__/${TELEGRAM_CHAT_ID}/g" "${OPENCLAW_STATE_DIR}/openclaw.json"
mkdir -p ~/.openclaw
cp "${OPENCLAW_STATE_DIR}/openclaw.json" ~/.openclaw/openclaw.json
fi
# Exec approvals: ask=off para todos os agentes — sem socket (evita erro "approval not enabled on Telegram").
# Todos os agentes aprovam automaticamente exec sem precisar de UI de aprovacao.
EXEC_APPROVALS_FILE=~/.openclaw/exec-approvals.json
cat > "${EXEC_APPROVALS_FILE}" << 'EOFAPPROVALS'
{
  "version": 1,
  "defaults": {
    "ask": "off",
    "autoAllowSkills": true
  },
  "agents": {
    "ceo":              { "ask": "off", "autoAllowSkills": true },
    "po":               { "ask": "off", "autoAllowSkills": true },
    "arquiteto":        { "ask": "off", "autoAllowSkills": true },
    "dev_backend":      { "ask": "off", "autoAllowSkills": true },
    "dev_frontend":     { "ask": "off", "autoAllowSkills": true },
    "dev_mobile":       { "ask": "off", "autoAllowSkills": true },
    "qa_engineer":      { "ask": "off", "autoAllowSkills": true },
    "security_engineer":{ "ask": "off", "autoAllowSkills": true },
    "ux_designer":      { "ask": "off", "autoAllowSkills": true },
    "devops_sre":       { "ask": "off", "autoAllowSkills": true },
    "dba_data_engineer":  { "ask": "off", "autoAllowSkills": true },
    "memory_curator":    { "ask": "off", "autoAllowSkills": true }
  }
}
EOFAPPROVALS
# Repair agent main sessions when the persisted transcript is missing, invalid,
# or contains no assistant text messages that the chat UI can render.
repair_main_session() {
  agent_id="$1"
  workspace_dir="$2"
  seed_text="$3"
  sess_dir="${OPENCLAW_STATE_DIR}/agents/${agent_id}/sessions"
  sess_key="agent:${agent_id}:main"
  mkdir -p "${sess_dir}"
  if [ ! -f "${sess_dir}/sessions.json" ]; then
    ts="$(date -u +%Y%m%dT%H%M%SZ)"
    new_id="$(cat /proc/sys/kernel/random/uuid)"
    now_ms="$(($(date -u +%s)*1000))"
    cat > "${sess_dir}/${new_id}.jsonl" <<SEEDEOF
{"type":"session","version":3,"id":"${new_id}","timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)","cwd":"${workspace_dir}"}
{"type":"message","id":"seed-${agent_id}-main","parentId":null,"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)","message":{"role":"assistant","content":[{"type":"text","text":"${seed_text}"}],"stopReason":"stop","provider":"system","model":"seed"}}
SEEDEOF
    printf '{"agent:%s:main":{"sessionId":"%s","updatedAt":%s,"chatType":"direct","deliveryContext":{"channel":"webchat"},"lastChannel":"webchat","origin":{"provider":"webchat","surface":"webchat","chatType":"direct"},"sessionFile":"%s","abortedLastRun":false,"compactionCount":0}}\n' \
      "${agent_id}" "${new_id}" "${now_ms}" "${sess_dir}/${new_id}.jsonl" \
      > "${sess_dir}/sessions.json"
    return 0
  fi
  main_file="$(jq -r --arg key "${sess_key}" '.[$key].sessionFile // empty' "${sess_dir}/sessions.json" 2>/dev/null || true)"
  main_ok=0
  if [ -n "${main_file}" ] && [ -f "${main_file}" ]; then
    if jq -c . "${main_file}" >/dev/null 2>&1; then
      if jq -e 'select(.type=="message" and .message.role=="assistant") | .message.content[]? | select(.type=="text" and ((.text // "") | length > 0))' "${main_file}" >/dev/null 2>&1; then
        main_ok=1
      fi
    fi
  fi
  if [ "${main_ok}" -eq 1 ]; then
    return 0
  fi
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  new_id="$(cat /proc/sys/kernel/random/uuid)"
  now_ms="$(($(date -u +%s)*1000))"
  cp "${sess_dir}/sessions.json" "${sess_dir}/sessions.json.bak.${ts}"
  if [ -n "${main_file}" ] && [ -f "${main_file}" ]; then
    cp "${main_file}" "${main_file}.bak.${ts}"
  fi
  cat > "${sess_dir}/${new_id}.jsonl" <<EOF
{"type":"session","version":3,"id":"${new_id}","timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)","cwd":"${workspace_dir}"}
{"type":"message","id":"seed-${agent_id}-main","parentId":null,"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)","message":{"role":"assistant","content":[{"type":"text","text":"${seed_text}"}],"stopReason":"stop","provider":"system","model":"seed"}}
EOF
  jq --arg key "${sess_key}" \
     --arg newId "${new_id}" \
     --arg newFile "${sess_dir}/${new_id}.jsonl" \
     --argjson now "${now_ms}" \
     '.[$key].sessionId = $newId |
      .[$key].updatedAt = $now |
      .[$key].chatType = "direct" |
      .[$key].deliveryContext = {"channel":"webchat"} |
      .[$key].lastChannel = "webchat" |
      .[$key].origin = {"provider":"webchat","surface":"webchat","chatType":"direct"} |
      .[$key].sessionFile = $newFile |
      .[$key].abortedLastRun = false |
      .[$key].compactionCount = 0' \
     "${sess_dir}/sessions.json" > "${sess_dir}/sessions.json.tmp"
  mv "${sess_dir}/sessions.json.tmp" "${sess_dir}/sessions.json"
}
repair_main_session "ceo" "/data/openclaw/workspace-ceo" "CEO pronto. Delegacao imediata na mesma sessao — sem fila com prazos em horas entre agentes. Pode acionar por aqui."
repair_main_session "po" "/data/openclaw/workspace-po" "PO pronto. Pode me acionar para planejamento, backlog, prioridades e coordenacao com Arquiteto."
repair_main_session "arquiteto" "/data/openclaw/workspace-arquiteto" "Arquiteto pronto. Pode me acionar para desenho tecnico, tasks e trade-offs de arquitetura."
repair_main_session "dev_backend" "/data/openclaw/workspace-dev_backend" "Dev_Backend pronto. Pode me acionar para implementacao de tasks, testes e atualizacao de status."
repair_main_session "dev_frontend" "/data/openclaw/workspace-dev_frontend" "Dev_Frontend pronto. Pode me acionar para implementacao de tasks frontend, testes e atualizacao de status."
repair_main_session "dev_mobile" "/data/openclaw/workspace-dev_mobile" "Dev_Mobile pronto. Pode me acionar para implementacao de tasks mobile, testes e atualizacao de status."
repair_main_session "qa_engineer" "/data/openclaw/workspace-qa_engineer" "QA_Engineer pronto. Pode me acionar para validacao, testes BDD e relatorios de qualidade."
repair_main_session "devops_sre" "/data/openclaw/workspace-devops_sre" "DevOps_SRE pronto. Pode me acionar para pipelines, infra, SLOs e escalacao de incidentes."
repair_main_session "security_engineer" "/data/openclaw/workspace-security_engineer" "Security_Engineer pronto. Pode me acionar para scans de seguranca, CVEs e escalacao de vulnerabilidades."
repair_main_session "ux_designer" "/data/openclaw/workspace-ux_designer" "UX_Designer pronto. Pode me acionar para wireframes, fluxos de usuario e design tokens."
repair_main_session "dba_data_engineer" "/data/openclaw/workspace-dba_data_engineer" "DBA_DataEngineer pronto. Pode me acionar para schemas, migrations, queries e compliance LGPD."
repair_main_session "memory_curator" "/data/openclaw/workspace-memory_curator" "Memory_Curator pronto. Executo curadoria diaria de padroes cross-agent e promocao para SHARED_MEMORY."
