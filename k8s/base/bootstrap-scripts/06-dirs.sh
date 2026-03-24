mkdir -p "${OPENCLAW_STATE_DIR}"
mkdir -p ~/.openclaw
mkdir -p "${OPENCLAW_STATE_DIR}/scheduler"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/status"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/idea"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/specs"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/user_story"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/tasks"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/briefs"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/implementation/docs"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/session_finished"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/ux"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/security/scans"
mkdir -p "${OPENCLAW_STATE_DIR}/backlog/database"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-ceo"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-po"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-arquiteto"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-dev_backend"
mkdir -p "${OPENCLAW_STATE_DIR}/agents/ceo/agent" "${OPENCLAW_STATE_DIR}/agents/po/agent" "${OPENCLAW_STATE_DIR}/agents/arquiteto/agent" "${OPENCLAW_STATE_DIR}/agents/dev_backend/agent"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-dev_frontend" "${OPENCLAW_STATE_DIR}/workspace-dev_mobile" "${OPENCLAW_STATE_DIR}/workspace-qa_engineer"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-devops_sre" "${OPENCLAW_STATE_DIR}/workspace-security_engineer"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-ux_designer" "${OPENCLAW_STATE_DIR}/workspace-dba_data_engineer"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-memory_curator"
mkdir -p "${OPENCLAW_STATE_DIR}/agents/dev_frontend/agent" "${OPENCLAW_STATE_DIR}/agents/dev_mobile/agent" "${OPENCLAW_STATE_DIR}/agents/qa_engineer/agent"
mkdir -p "${OPENCLAW_STATE_DIR}/agents/devops_sre/agent" "${OPENCLAW_STATE_DIR}/agents/security_engineer/agent"
mkdir -p "${OPENCLAW_STATE_DIR}/agents/ux_designer/agent" "${OPENCLAW_STATE_DIR}/agents/dba_data_engineer/agent"
mkdir -p "${OPENCLAW_STATE_DIR}/agents/memory_curator/agent"

# Compatibilidade com referencias legadas: /data/openclaw/backlog/TASK-XXX.md
# Mapeia para o arquivo canônico em backlog/tasks/TASK-XXX-*.md quando existir.
for task_file in "${OPENCLAW_STATE_DIR}"/backlog/tasks/TASK-[0-9][0-9][0-9]-*.md; do
  [ -e "${task_file}" ] || continue
  task_num="$(basename "${task_file}" | sed -E 's/^(TASK-[0-9]{3}).*/\1/')"
  ln -sfn "tasks/$(basename "${task_file}")" "${OPENCLAW_STATE_DIR}/backlog/${task_num}.md"
done

# Compatibilidade de workspace por agente apontando para o workspace unico de projeto.
for ws_agent in ceo po arquiteto dev_backend dev_frontend dev_mobile qa_engineer devops_sre security_engineer ux_designer dba_data_engineer memory_curator; do
  ws_dir="${OPENCLAW_STATE_DIR}/workspace-${ws_agent}"
  mkdir -p "${ws_dir}"
  ln -sfn "${OPENCLAW_STATE_DIR}/backlog/implementation/src" "${ws_dir}/src"
  ln -sfn "${OPENCLAW_STATE_DIR}/backlog/implementation/tests" "${ws_dir}/tests"
  for task_file in "${OPENCLAW_STATE_DIR}"/backlog/tasks/TASK-[0-9][0-9][0-9]-*.md; do
    [ -e "${task_file}" ] || continue
    ln -sfn "${task_file}" "${ws_dir}/$(basename "${task_file}")"
  done
done
