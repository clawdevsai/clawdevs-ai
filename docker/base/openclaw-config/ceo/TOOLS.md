<!-- 
  Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
 -->

# TOOLS.md - CEO

allowed_tools:
  - read/write backlog artifacts
  - sessions_list/sessions_spawn/sessions_send
  - exec("gh ...") for read-only GitHub inspection
  - exec("web-search ...") and exec("web-read ...")

rules:
  - validate active repository context before delegation or gh queries
  - enforce SOURCE_VALIDATION.md for external-information decisions (>=3 independent sources, >=1 official source, explicit date, confidence)
  - keep one session per initiative (avoid duplicated threads)
  - use sessions_send for agent channels (not message)
  - when delegating to another agent (e.g. PO at agent:po:main), always pass timeoutSeconds: 1800 on sessions_send so the gateway waits long enough for the peer run plus agent-to-agent reply-back; the default wait window is often too short and returns status timeout even while the target agent is still running (use sessions_history to inspect if needed)
  - optional: timeoutSeconds: 0 for fire-and-forget handoff; then tell the Director to open the PO chat or check sessions_history for the outcome
  - persist decision evidence contract: claim, sources, confidence, invalidators
  - if tool fails, register once and continue with fallback
  - internet access is available through exec("web-search ...") and exec("web-read ..."); do not claim lack of internet access without attempting these tools first
  - if exec policy denies a web command, report the exact denial and request explicit approval/reconfiguration instead of assuming permanent internet restriction

restrictions:
  - no commit/push/merge/pr/issue creation
  - no secret exposure
  - no actions outside authorized paths/context

github_permissions:
  type: read-only
  org: "__GIT_ORG__"
  allowed: 
    - "gh repo list __GIT_ORG__ --limit 1000"
    - "gh issue list"
    - "gh pr list"
    - "gh workflow list"
    - "gh run view"
    - "gh label list"
  denied: 
    - "gh issue create/edit/close"
    - "gh pr create/merge"
    - "gh workflow run"
    - "gh repo create/delete/update"
    - "any write op"

inter_agent_sessions:
  key_format: "agent:<id>:main"
  use_sessions_send_for_agents: true
  sessions_send_delegation:
    po_session_key: "agent:po:main"
    recommended_timeout_seconds: 1800
