---
phase: 1
name: Runtime Foundation & Sandbox
status: planned
owner: gsd-planner (manual)
wave: 1
depends_on: []
files_modified:
  - docker/base/bootstrap-scripts/07-agent-workspaces.sh
  - docker/base/bootstrap-scripts/09-openclaw-config.sh
  - docker/base/openclaw-config/*/SOUL.md
  - docker/base/openclaw-config/*/AGENTS.md
  - docker/base/openclaw-config/shared/CONTEXT_MODE_HOOKS_CONFIG.yaml
requirements_addressed:
  - WORK-01
  - WORK-02
  - WORK-03
must_haves:
  - Agents operate inside `/data/openclaw/workspace-<agent>` with artifact tracking
  - Tool execution limited by explicit safety policy and output caps
  - Ollama-first runtime with automatic fallback to approved models
---

# Phase 1 Plan: Runtime Foundation & Sandbox

## Objective
Implement the runtime foundations for sandboxed workspaces, artifact tracking, tool safety, and Ollama-first automatic fallback as defined in 01-CONTEXT.md.

## Plan

### Task 01 — Enforce workspace sandbox + artifact tracking contract
<task>
  <id>01</id>
  <title>Standardize workspace sandbox paths and artifact tracking outputs</title>
  <read_first>
    docker/base/bootstrap-scripts/07-agent-workspaces.sh
    docker/base/openclaw-config/INDEX.md
    .planning/phases/01-runtime-foundation-sandbox/01-CONTEXT.md
  </read_first>
  <action>
    Update docker/base/bootstrap-scripts/07-agent-workspaces.sh to:
    1) Assert workspaces are created at /data/openclaw/workspace-<agent> for every agent in AGENTS.
    2) Ensure shared projects path is accessible inside each workspace via symlink or bind target named "projects" pointing to /data/openclaw/projects.
    3) Create artifact tracking directory per workspace at /data/openclaw/workspace-<agent>/artifacts.
    4) Write a structured artifact log schema file at /data/openclaw/workspace-<agent>/artifacts/artifacts.schema.json with fields: command, args, cwd, started_at, finished_at, exit_code, stdout_hash, stderr_hash, files_changed (list), diffs_hash, tests_run (list).
    5) Create a bootstrap artifact log seed at /data/openclaw/workspace-<agent>/artifacts/artifacts.log.jsonl with a header entry indicating schema version "v1".
  </action>
  <acceptance_criteria>
    - 07-agent-workspaces.sh contains creation of /data/openclaw/workspace-<agent>/artifacts for each agent
    - 07-agent-workspaces.sh creates a "projects" link inside each workspace pointing to /data/openclaw/projects
    - 07-agent-workspaces.sh writes artifacts.schema.json with the exact fields: command, args, cwd, started_at, finished_at, exit_code, stdout_hash, stderr_hash, files_changed, diffs_hash, tests_run
    - 07-agent-workspaces.sh seeds artifacts.log.jsonl with schema_version "v1"
  </acceptance_criteria>
</task>

### Task 02 — Tool policy safety + output caps (Context Mode)
<task>
  <id>02</id>
  <title>Apply tool safety policy and output limits via Context Mode + guardrails</title>
  <read_first>
    docker/base/bootstrap-scripts/09-openclaw-config.sh
    docker/base/openclaw-config/shared/CONTEXT_MODE_HOOKS_CONFIG.yaml
    docker/base/openclaw-config/*/SOUL.md
    docker/base/openclaw-config/*/AGENTS.md
    .planning/phases/01-runtime-foundation-sandbox/01-CONTEXT.md
  </read_first>
  <action>
    1) Update docker/base/bootstrap-scripts/09-openclaw-config.sh exec approvals defaults to enforce output-size limits using Context Mode hooks. Add or update ENV keys (if missing) to set a maximum output size and ensure session tools visibility remains "all".
    2) Update docker/base/openclaw-config/shared/CONTEXT_MODE_HOOKS_CONFIG.yaml to include explicit max_output_bytes and max_process_time_seconds values (choose concrete defaults and document them in the file header).
    3) Add guardrail text to every docker/base/openclaw-config/*/SOUL.md and docker/base/openclaw-config/*/AGENTS.md that explicitly forbids exposing sensitive data and requires redaction before output.
  </action>
  <acceptance_criteria>
    - 09-openclaw-config.sh contains concrete output cap values passed to Context Mode configuration
    - CONTEXT_MODE_HOOKS_CONFIG.yaml defines max_output_bytes and max_process_time_seconds with numeric values
    - Every SOUL.md and AGENTS.md under docker/base/openclaw-config/* contains a "Sensitive Data" section with a prohibition on secrets exposure
  </acceptance_criteria>
</task>

### Task 03 — Ollama-first with automatic fallback to approved models
<task>
  <id>03</id>
  <title>Lock Ollama-first runtime and automatic fallback model list</title>
  <read_first>
    docker/base/bootstrap-scripts/09-openclaw-config.sh
    .planning/phases/01-runtime-foundation-sandbox/01-CONTEXT.md
  </read_first>
  <action>
    Update docker/base/bootstrap-scripts/09-openclaw-config.sh to ensure:
    1) Ollama is the default provider when no explicit provider is set.
    2) Automatic fallback is enabled and uses the exact allowed model list:
       - qwen3-next:80b-cloud
       - gpt-oss:120b-cloud
       - nemotron-3-super:cloud
       - qwen3-coder:480b-cloud
       - gemma3:27b-cloud
       - qwen3-vl:235b-cloud
       - qwen3.5:397b-cloud
       - minimax-m2.7:cloud
       - qwen3-coder-next:cloud
    3) OpenRouter remains an allowed fallback provider when OPENROUTER_API_KEY is present.
  </action>
  <acceptance_criteria>
    - 09-openclaw-config.sh contains the full allowed model list exactly as specified
    - 09-openclaw-config.sh keeps provider selection default to ollama when PROVEDOR_LLM is empty or invalid
    - 09-openclaw-config.sh retains OpenRouter fallback behavior guarded by OPENROUTER_API_KEY
  </acceptance_criteria>
</task>

## Verification
- Run a bootstrap dry-run or config render script to confirm openclaw.json contains the allowed model list and tool policy values.
- Inspect a generated workspace directory to confirm artifacts/ paths and projects link exist.
- Grep SOUL.md/AGENTS.md for the new Sensitive Data guardrail.

## Notes
- All changes must reuse existing control-panel and OpenClaw flows without re-implementing the stack.
