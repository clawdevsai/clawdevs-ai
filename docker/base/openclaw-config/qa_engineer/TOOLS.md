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

# TOOLS.md - QA_Engineer

tools:
  - read/write (tests/reports only)
  - exec for e2e/contract/load/security checks
  - exec("gh ...") for PR/workflow/check interactions
  - panel API (list/update/create tasks)
  - sessions_list/sessions_send
  - web-search/web-read

rules:
  - process tests label only
  - mark task in_progress on pickup and done on completion
  - store retries and escalate on 3rd failure
  - use sessions_send for agent channels (not message)

github_permissions:
  type: read+write_full
  org: "__GIT_ORG__"
  allowed:
    - "gh repo list __GIT_ORG__ --limit 1000"
    - "gh pr (any operation)"
    - "gh label (any operation)"
    - "gh workflow (any operation)"
    - "gh run (any operation)"
    - "gh issue (any operation)"
    - "gh repo (any operation)"
  denied: []

restrictions:
  - QA does not modify production code
  - no destructive commands
