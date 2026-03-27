# Database Migrations

This document tracks schema changes made to the control panel database.

## Auto-Migration System

The control panel uses SQLModel ORM which automatically creates and updates database tables based on Python model definitions. When the application starts, `SQLModel.metadata.create_all()` is called to ensure all tables and columns exist.

**No manual migration scripts are required.** Changes to models are automatically applied when the application runs.

---

## Migration: Phase 1 - Failure Detection & Self-Healing

**Date:** 2026-03-27
**Models Changed:** Task, Agent
**Status:** Implemented via SQLModel auto-migration

### Task Model Changes

Added failure tracking and escalation columns:

```python
# Failure tracking fields
failure_count: int = Field(default=0, index=True)
consecutive_failures: int = Field(default=0)
last_error: Optional[str] = None
error_reason: Optional[str] = None
last_failed_at: Optional[datetime] = None

# Escalation fields
escalated_to_agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id", index=True)
escalation_reason: Optional[str] = None
escalated_at: Optional[datetime] = None

# Cost tracking fields (Phase 3 preparation)
estimated_cost: Optional[float] = None
actual_cost: float = Field(default=0.0)
cost_tier: Optional[str] = Field(default=None)
```

**SQL Equivalent (for reference):**
```sql
ALTER TABLE tasks ADD COLUMN failure_count INTEGER DEFAULT 0;
ALTER TABLE tasks ADD COLUMN consecutive_failures INTEGER DEFAULT 0;
ALTER TABLE tasks ADD COLUMN last_error TEXT;
ALTER TABLE tasks ADD COLUMN error_reason TEXT;
ALTER TABLE tasks ADD COLUMN last_failed_at TIMESTAMP;
ALTER TABLE tasks ADD COLUMN escalated_to_agent_id UUID REFERENCES agents(id);
ALTER TABLE tasks ADD COLUMN escalation_reason TEXT;
ALTER TABLE tasks ADD COLUMN escalated_at TIMESTAMP;
ALTER TABLE tasks ADD COLUMN estimated_cost FLOAT;
ALTER TABLE tasks ADD COLUMN actual_cost FLOAT DEFAULT 0.0;
ALTER TABLE tasks ADD COLUMN cost_tier VARCHAR;
CREATE INDEX idx_tasks_failure_count ON tasks(failure_count);
CREATE INDEX idx_tasks_escalated_to_agent_id ON tasks(escalated_to_agent_id);
```

### Agent Model Changes

Added escalation capability fields:

```python
# Escalation capability
can_escalate: bool = Field(default=False)
max_escalations: int = Field(default=0)
escalations_handled: int = Field(default=0)
```

**SQL Equivalent (for reference):**
```sql
ALTER TABLE agents ADD COLUMN can_escalate BOOLEAN DEFAULT FALSE;
ALTER TABLE agents ADD COLUMN max_escalations INTEGER DEFAULT 0;
ALTER TABLE agents ADD COLUMN escalations_handled INTEGER DEFAULT 0;
```

---

## Migration: Phase 2 - RAG Memory Integration (Upcoming)

**Expected Date:** 2026-03-28
**Models Affected:** MemoryEntry

### Planned Changes

Add vector embedding support:

```python
# Vector embedding columns
embedding: Optional[List[float]] = Field(default=None)  # pgvector type
chunk_index: int = Field(default=0)
source_file_path: Optional[str] = None
embedding_model: str = Field(default="mistral")
```

**Dependencies:**
- PostgreSQL pgvector extension must be enabled
- `pip install pgvector`

---

## Migration: Phase 3 - Governance Enforcement (Upcoming)

**Expected Date:** 2026-03-29
**Models Affected:** Task (already prepared)
**Status:** Cost fields already added in Phase 1

No new migrations required; cost fields already added in Phase 1.

---

## Running Migrations

**Automatic (Recommended):**
Simply start the application. SQLModel will automatically:
1. Create all tables if they don't exist
2. Add any new columns to existing tables
3. Create indexes as defined

```bash
cd control-panel/backend
python -m uvicorn app.main:app --reload
```

**Manual Verification:**
Connect to PostgreSQL and verify tables:

```sql
-- Check Task table
\d tasks

-- Check Agent table
\d agents

-- List all indexes
\di
```

---

## Rollback Plan

If a migration causes issues, SQLModel cannot automatically rollback changes. To rollback:

1. **Remove columns manually via SQL:**
```sql
ALTER TABLE tasks DROP COLUMN failure_count CASCADE;
```

2. **Or restore from backup**

3. **Revert the Python model changes**

---

## Notes

- All changes use sensible defaults (`default=0`, `default=False`, `default=None`)
- Foreign keys are properly defined with cascade delete options
- Indexes are created on frequently-queried columns (failure_count, escalated_to_agent_id)
- Cost fields added in Phase 1 but not enforced until Phase 3
- Phase 2 will require pgvector extension; ensure it's enabled before Phase 2 deployment

---

## Verification Checklist

After each phase deployment:

- [ ] Application starts without errors
- [ ] No SQL constraint violations
- [ ] All indexes created successfully
- [ ] Foreign key relationships working
- [ ] Default values applied correctly
- [ ] No data loss in existing records
