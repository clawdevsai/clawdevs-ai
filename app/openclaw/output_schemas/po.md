Expected output schema for PO.

Return a concise JSON object with:
- `status`: `planned` or `blocked`
- `summary`: short planning summary
- `issues`: list of planned backlog items with `title`, `priority`, `acceptance`
- `next_action`: next stream or action to trigger
