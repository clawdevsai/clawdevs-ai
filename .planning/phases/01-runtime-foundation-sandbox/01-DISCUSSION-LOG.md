# Phase 1: Runtime Foundation & Sandbox - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 1-Runtime Foundation & Sandbox
**Areas discussed:** Workspace sandbox, Tool policy, Ollama-first fallback

---

## Workspace Sandbox + Artifact Tracking

| Option | Description | Selected |
|--------|-------------|----------|
| /data/openclaw/workspace-<agent> | Workspace path for all agents | ✓ |
| Artifacts: commands/tests/diffs/logs | Required artifact tracking set | ✓ |
| Sandbox read/write projects/ | Allow shared project dir | ✓ |
| Proof: structured log + file list + hash | Required proof | ✓ |

**User's choice:** Use `/data/openclaw/workspace-<agent>`, track commands/tests/diffs/logs, allow shared `projects/`, proof via structured log + file list + hash.

---

## Tool Policy (Allowlist + Limits)

| Option | Description | Selected |
|--------|-------------|----------|
| Full permissions for all agents | No per‑agent allowlist restrictions | ✓ |
| Block sensitive data exposure | Default safety block | ✓ |
| Enforce process + output limits | Use Context Mode for output size | ✓ |
| Security guardrails in SOUL.md/AGENTS.md | Hard rules in agent docs | ✓ |

**User's choice:** Full permissions for all agents; block sensitive data exposure; enforce process + output limits with Context Mode; guardrails in `SOUL.md` and `AGENTS.md`.

---

## Ollama-First + Fallback

| Option | Description | Selected |
|--------|-------------|----------|
| Automatic fallback | No human confirmation | ✓ |
| Allowed models | List provided | ✓ |
| External tokens allowed | No explicit limit | ✓ |
| OpenRouter allowed | Additional fallback | ✓ |

**User's choice:** Automatic fallback. Allowed models: qwen3-next:80b-cloud, gpt-oss:120b-cloud, nemotron-3-super:cloud, qwen3-coder:480b-cloud, gemma3:27b-cloud, qwen3-vl:235b-cloud, qwen3.5:397b-cloud, minimax-m2.7:cloud, qwen3-coder-next:cloud. External tokens allowed with no explicit limit. OpenRouter allowed.

---

## the agent's Discretion

None

## Deferred Ideas

None
