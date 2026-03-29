# Agent Access Control System

## Overview

The ClawDevs Panel includes a flexible agent access control system that allows administrators to restrict access to specific agents based on user permissions.

## How It Works

### Permission Logic

1. **Admins**: Always have full access to all agents
2. **No Permissions Configured**: If no permissions are set for an agent, all users have access
3. **Permissions Configured**: Only users with explicit permission can access the agent

### Access Check Points

The following endpoints validate agent permissions:
- `GET /chat/history/{agent_slug}` - Fetch chat history
- `POST /chat/stream` - Send messages to agent
- `POST /chat/rag/turn` - Persist RAG turns

## Setup

### 1. Database Migration

First, apply the migrations to add the `agent_permissions` table:

```bash
cd control-panel/backend
alembic upgrade head
```

### 2. Using the Setup Script

Configure permissions using the setup script:

#### Grant Access

```bash
python scripts/setup_agent_permissions.py grant-access \
  --agent-slug clawdevsai/searxng-runtime \
  --username po
```

#### List Permissions

```bash
python scripts/setup_agent_permissions.py list-permissions \
  --agent-slug clawdevsai/searxng-runtime
```

Output:
```
Users with access to 'clawdevsai/searxng-runtime':
  • po (viewer)
  • ceo (admin)
```

#### Revoke Access

```bash
python scripts/setup_agent_permissions.py revoke-access \
  --agent-slug clawdevsai/searxng-runtime \
  --username po
```

### 3. Using API Endpoints (Admin Only)

Administrators can also use the API to manage permissions:

#### Grant Access

```bash
curl -X POST http://localhost:8000/agent-permissions \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_slug": "clawdevsai/searxng-runtime",
    "user_id": "<USER_UUID>"
  }'
```

#### List Permissions

```bash
curl -X GET http://localhost:8000/agent-permissions/clawdevsai/searxng-runtime \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

#### Revoke Access

```bash
curl -X DELETE http://localhost:8000/agent-permissions/clawdevsai/searxng-runtime/<USER_UUID> \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

## Example: Restrict Access to searchng-runtime

To allow only the PO and CEO to access the `clawdevsai/searxng-runtime` agent:

```bash
# Grant access to PO
python scripts/setup_agent_permissions.py grant-access \
  --agent-slug clawdevsai/searxng-runtime \
  --username po

# Grant access to CEO
python scripts/setup_agent_permissions.py grant-access \
  --agent-slug clawdevsai/searxng-runtime \
  --username ceo

# Verify permissions
python scripts/setup_agent_permissions.py list-permissions \
  --agent-slug clawdevsai/searxng-runtime
```

## Error Handling

### Access Denied

If a user without permission tries to access an agent, they'll receive:

```json
{
  "detail": "Access denied to agent 'clawdevsai/searxng-runtime'"
}
```

HTTP Status: `403 Forbidden`

## Removing Restrictions

To remove all restrictions from an agent (allow all users):

```bash
# Revoke all permissions for the agent
# Users will regain access automatically
```

Since the logic checks if ANY permissions exist, revoking all permissions restores open access.

## Database Schema

```sql
CREATE TABLE agent_permissions (
    id UUID PRIMARY KEY,
    agent_slug VARCHAR NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_agent_permissions_agent_slug ON agent_permissions(agent_slug);
CREATE INDEX idx_agent_permissions_user_id ON agent_permissions(user_id);
```

## Notes

- Permissions are checked on every request
- Admins bypass all permission checks
- The system is designed to be flexible: no permissions = open access
- Each permission grants access to a specific agent for a specific user
- Permissions are created with the current timestamp

## Future Enhancements

Potential improvements:
- Group-based permissions (e.g., "team_name")
- Role-based permissions (e.g., "all POs")
- Time-based permissions (e.g., "until 2026-12-31")
- Frontend UI for managing permissions (Admin panel)
