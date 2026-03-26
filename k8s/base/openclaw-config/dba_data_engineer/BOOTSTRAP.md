# BOOTSTRAP.md - DBA_DataEngineer

## Environment Initialization

1. Load environment variables.
2. Initialize `/data/openclaw/backlog/database/` directory.
3. Configure 4h cron (offset :30) to poll issues with label `dba`.
4. Check connectivity with development bank if available.
5. Register status: `dba_data_engineer ready`.