# Phase 1: Runtime Foundation & Sandbox - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver an Ollama-first runtime foundation with enforced workspace sandboxing and tool safety, enabling agents to operate deterministically within approved boundaries.

</domain>

<decisions>
## Implementation Decisions

### Workspace Sandbox + Artifact Tracking
- **D-01:** Workspaces live at `/data/openclaw/workspace-<agent>` for all agents.
- **D-02:** Sandbox allows read/write inside agent workspace and shared `projects/` directory.
- **D-03:** Artifact tracking must include executed commands, tests run, diffs, and logs.
- **D-04:** Proof of artifact tracking requires structured logs + file list + hash.

### Tool Policy (Allowlist + Limits)
- **D-05:** All agents have full tool permissions; blocking is human‑mediated when needed.
- **D-06:** Block exposure of sensitive data by default.
- **D-07:** Enforce process limits and output size limits; use Context Mode to cap output.
- **D-08:** No per‑agent allowlist differences; security guardrails enforced via `SOUL.md` and `AGENTS.md`.

### Ollama-First + Fallback
- **D-09:** Fallback is automatic.
- **D-10:** Allowed fallback models: `qwen3-next:80b-cloud`, `gpt-oss:120b-cloud`, `nemotron-3-super:cloud`, `qwen3-coder:480b-cloud`, `gemma3:27b-cloud`, `qwen3-vl:235b-cloud`, `qwen3.5:397b-cloud`, `minimax-m2.7:cloud`, `qwen3-coder-next:cloud`.
- **D-11:** External token usage is allowed with no explicit limit.
- **D-12:** OpenRouter is allowed as an additional fallback option.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Runtime & OpenClaw Config
- `docker/base/openclaw-config/INDEX.md` — master index of OpenClaw configuration structure
- `docker/base/bootstrap-scripts/09-openclaw-config.sh` — current gateway config generation and policy defaults
- `docker/base/bootstrap-scripts/07-agent-workspaces.sh` — workspace and memory layout logic
- `docker/base/bootstrap-scripts/06-dirs.sh` — runtime directories and workspace symlinks

### Internal Docs (partially outdated)
- `docs/` — internal documentation to consider during refactor

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- OpenClaw config generation already lives in `docker/base/bootstrap-scripts/09-openclaw-config.sh`.
- Workspace setup and memory wiring exists in `docker/base/bootstrap-scripts/07-agent-workspaces.sh`.

### Established Patterns
- Runtime state and workspaces are centralized under `/data/openclaw` paths.
- Bootstrap scripts enforce environment-driven configuration via `.env`.

### Integration Points
- Gateway config is written to `${OPENCLAW_STATE_DIR}/openclaw.json` and mirrored to `~/.openclaw/openclaw.json`.
- Control panel backend reads gateway URL/token from `control-panel/backend/app/core/config.py`.

</code_context>

<specifics>
## Specific Ideas

- Prefer reusing existing control-panel and OpenClaw config flows rather than re‑implementing.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-runtime-foundation-sandbox*
*Context gathered: 2026-04-02*
