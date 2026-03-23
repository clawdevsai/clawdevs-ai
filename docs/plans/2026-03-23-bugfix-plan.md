# ClawDevs AI — Bug Fix Plan

> **For Claude:** Use `superpowers:subagent-driven-development` to execute this plan.

**Goal:** Fix all confirmed bugs found during codebase and documentation analysis on 2026-03-23.

**Scope:** Bootstrap scripts and Kubernetes manifests only. No application code.

---

## Bug Summary

### BUG-1 (CRITICAL): SDD templates missing from 7 agent workspaces
**File:** `k8s/base/bootstrap-scripts/07-agent-workspaces.sh`
**Impact:** `dev_frontend`, `dev_mobile`, `qa_engineer`, `devops_sre`, `security_engineer`, `ux_designer`, `dba_data_engineer` are missing 13 SDD template files each that `dev_backend` has. Agents can't follow the SDD workflow without these templates.
**Root cause:** `dev_backend` block (lines 105–138) copies the full SDD template set; subsequent agent blocks were truncated and only copy `CONSTITUTION.md` and `project-README.md`.

Missing files per agent:
- `shared-BRIEF_TEMPLATE.md`
- `shared-CLARIFY_TEMPLATE.md`
- `shared-SDD_CHECKLIST.md`
- `shared-SDD_FULL_CYCLE_EXAMPLE.md`
- `shared-SDD_OPERATIONAL_PROMPTS.md`
- `shared-SPEC_TEMPLATE.md`
- `shared-PLAN_TEMPLATE.md`
- `shared-TASK_TEMPLATE.md`
- `shared-VALIDATE_TEMPLATE.md`
- `shared-VIBE_CODING_PLAYBOOK.md`
- `shared-SDD_OPERATING_MODEL.md`
- `shared-SPECKIT_ADAPTATION.md`
- `initiatives/internal-sdd-operationalization/` (7 files)

### BUG-2 (HIGH): `claw-repo-switch` crashes without useful error on non-existent repo
**File:** `k8s/base/bootstrap-scripts/04-repo-tools.sh`, line 92
**Impact:** `claw-repo-switch <nonexistent-repo>` fails silently due to `set -euo pipefail` with no error message to the user.
**Root cause:** `gh api "repos/${target_ref}" --silent >/dev/null 2>&1` is not wrapped in an `if` statement. Under `set -euo pipefail`, a non-zero exit code aborts the script.
**Fix:** Wrap in `if ... ; then ... else echo "ERROR: repo not found"; exit 1; fi`

### BUG-3 (MEDIUM): `repair_main_session` skips seeding on fresh pod
**File:** `k8s/base/bootstrap-scripts/09-openclaw-config.sh`, lines 559–561
**Impact:** On first deployment, `sessions.json` does not exist → function returns 0 → no seed session messages created for any agent. Control UI shows empty sessions.
**Root cause:** Early return when `sessions.json` is absent.
**Fix:** When `sessions.json` is absent, create it with the new seed session entry directly (don't return early).

### BUG-4 (MEDIUM): `OPENCLAW_VERSION` in `.env.example` is dead config
**File:** `k8s/base/openclaw-pod.yaml`, line 82 + `k8s/.env.example`
**Impact:** Users following `.env.example` comments to pin `OPENCLAW_VERSION` get no effect. The pod always uses the hardcoded value `"2026.3.13"`.
**Root cause:** Pod manifest sets `OPENCLAW_VERSION` as a literal `value:` instead of referencing the secret.
**Fix:** Change pod manifest to read `OPENCLAW_VERSION` from the `openclaw-auth` secret (optional), with the hardcoded value moved to `.env.example` as the default. **Note:** Keep the current hardcoded `2026.3.13` as the default value in `.env.example`.

### BUG-5 (LOW): Race condition on `/tmp/openclaw-cron.json`
**File:** `k8s/base/bootstrap-scripts/10-background-services.sh`
**Impact:** Multiple background subshells simultaneously write to `/tmp/openclaw-cron.json`. One may read a partially-written file. Retry logic (24×5s) mitigates this in practice.
**Fix:** Use per-subshell temp files (e.g., `/tmp/openclaw-cron-${agent_name}.json`) instead of a shared file.

### BUG-6 (LOW): Readiness probe missing `initialDelaySeconds`
**File:** `k8s/base/openclaw-pod.yaml`, lines 184–189
**Impact:** Pod shows as `NotReady` for the full bootstrap duration (5–10 min). Cosmetic issue only (no liveness probe to cause restarts).
**Fix:** Add `initialDelaySeconds: 300` (5 minutes) to give bootstrap time to complete.

---

## Implementation Tasks

### Task 1: Fix SDD templates missing from agent workspaces (BUG-1)

**File:** `k8s/base/bootstrap-scripts/07-agent-workspaces.sh`

After each agent's `cp shared-CONSTITUTION.md` + `cp project-README.md` lines, add the same SDD template block that `dev_backend` has.

Agents to fix: `dev_frontend`, `dev_mobile`, `qa_engineer`, `devops_sre`, `security_engineer`, `ux_designer`, `dba_data_engineer`.

For each agent `<AGENT>`, add after `cp /bootstrap/agent-config/project-README.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/README.md"`:

```sh
cp /bootstrap/agent-config/shared-BRIEF_TEMPLATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/BRIEF_TEMPLATE.md"
cp /bootstrap/agent-config/shared-CLARIFY_TEMPLATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/CLARIFY_TEMPLATE.md"
cp /bootstrap/agent-config/shared-SDD_CHECKLIST.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/SDD_CHECKLIST.md"
cp /bootstrap/agent-config/shared-SDD_FULL_CYCLE_EXAMPLE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/SDD_FULL_CYCLE_EXAMPLE.md"
cp /bootstrap/agent-config/shared-SDD_OPERATIONAL_PROMPTS.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/SDD_OPERATIONAL_PROMPTS.md"
mkdir -p "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization"
cp /bootstrap/agent-config/shared-sdd-initiative-README.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/README.md"
cp /bootstrap/agent-config/shared-sdd-initiative-BRIEF.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/BRIEF.md"
cp /bootstrap/agent-config/shared-sdd-initiative-SPEC.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/SPEC.md"
cp /bootstrap/agent-config/shared-sdd-initiative-CLARIFY.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/CLARIFY.md"
cp /bootstrap/agent-config/shared-sdd-initiative-PLAN.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/PLAN.md"
cp /bootstrap/agent-config/shared-sdd-initiative-TASK.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/TASK.md"
cp /bootstrap/agent-config/shared-sdd-initiative-VALIDATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/initiatives/internal-sdd-operationalization/VALIDATE.md"
cp /bootstrap/agent-config/shared-SPEC_TEMPLATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/SPEC_TEMPLATE.md"
cp /bootstrap/agent-config/shared-PLAN_TEMPLATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/PLAN_TEMPLATE.md"
cp /bootstrap/agent-config/shared-TASK_TEMPLATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/TASK_TEMPLATE.md"
cp /bootstrap/agent-config/shared-VALIDATE_TEMPLATE.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/VALIDATE_TEMPLATE.md"
cp /bootstrap/agent-config/shared-VIBE_CODING_PLAYBOOK.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/VIBE_CODING_PLAYBOOK.md"
cp /bootstrap/agent-config/shared-SDD_OPERATING_MODEL.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/SDD_OPERATING_MODEL.md"
cp /bootstrap/agent-config/shared-SPECKIT_ADAPTATION.md "${OPENCLAW_STATE_DIR}/workspace-<AGENT>/SPECKIT_ADAPTATION.md"
```

### Task 2: Fix `claw-repo-switch` crash (BUG-2)

**File:** `k8s/base/bootstrap-scripts/04-repo-tools.sh`

Replace line 92:
```sh
gh api "repos/${target_ref}" --silent >/dev/null 2>&1
```
With:
```sh
if ! gh api "repos/${target_ref}" --silent >/dev/null 2>&1; then
  echo "ERROR: repositorio '${target_ref}' nao encontrado ou sem acesso." >&2
  exit 1
fi
```

### Task 3: Fix `repair_main_session` to seed on fresh pod (BUG-3)

**File:** `k8s/base/bootstrap-scripts/09-openclaw-config.sh`

Replace lines 559–561:
```sh
if [ ! -f "${sess_dir}/sessions.json" ]; then
    return 0
fi
```
With:
```sh
if [ ! -f "${sess_dir}/sessions.json" ]; then
    ts="$(date -u +%Y%m%dT%H%M%SZ)"
    new_id="$(cat /proc/sys/kernel/random/uuid)"
    now_ms="$(($(date -u +%s)*1000))"
    cat > "${sess_dir}/${new_id}.jsonl" <<EOF
{"type":"session","version":3,"id":"${new_id}","timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)","cwd":"${workspace_dir}"}
{"type":"message","id":"seed-${agent_id}-main","parentId":null,"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)","message":{"role":"assistant","content":[{"type":"text","text":"${seed_text}"}],"stopReason":"stop","provider":"system","model":"seed"}}
EOF
    cat > "${sess_dir}/sessions.json" <<EOF
{
  "agent:${agent_id}:main": {
    "sessionId": "${new_id}",
    "updatedAt": ${now_ms},
    "chatType": "direct",
    "deliveryContext": {"channel":"webchat"},
    "lastChannel": "webchat",
    "origin": {"provider":"webchat","surface":"webchat","chatType":"direct"},
    "sessionFile": "${sess_dir}/${new_id}.jsonl",
    "abortedLastRun": false,
    "compactionCount": 0
  }
}
EOF
    return 0
fi
```

### Task 4: Fix `OPENCLAW_VERSION` dead config (BUG-4)

**File:** `k8s/base/openclaw-pod.yaml`

Replace:
```yaml
- name: OPENCLAW_VERSION
  value: "2026.3.13"
```
With:
```yaml
- name: OPENCLAW_VERSION
  valueFrom:
    secretKeyRef:
      name: openclaw-auth
      key: OPENCLAW_VERSION
      optional: true
```

**File:** `k8s/.env.example`

Change:
```
OPENCLAW_VERSION=
```
To:
```
OPENCLAW_VERSION=2026.3.13
```

### Task 5: Fix race condition on cron temp files (BUG-5)

**File:** `k8s/base/bootstrap-scripts/10-background-services.sh`

In each cron creation subshell block, change all occurrences of `/tmp/openclaw-cron.json` to use a unique temp file per agent (e.g., `/tmp/openclaw-cron-${CRON_NAME}.json`).

Also fix the watchdog block: change `/tmp/openclaw-cron-watchdog.json` (already unique) to keep its current name (it's already separate).

### Task 6: Add `initialDelaySeconds` to readiness probe (BUG-6)

**File:** `k8s/base/openclaw-pod.yaml`

Add `initialDelaySeconds: 300` to the readiness probe:
```yaml
readinessProbe:
  httpGet:
    path: /healthz
    port: gateway
  initialDelaySeconds: 300
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

---

## Execution Order

Tasks 1, 2, 3 are independent. Tasks 4, 5, 6 are independent.
All 6 tasks can be executed in sequence without conflicts.

Suggested order: Task 1 (highest impact) → Task 2 → Task 3 → Task 4 → Task 5 → Task 6.
