# HEARTBEAT.md - DBA_DataEngineer

A cada ciclo de heartbeat (4h, offset :30):
1. Verificar issues abertas com label `dba` no repositório ativo.
2. Verificar se há migrations pendentes de rollback ou com falha.
3. Verificar schedules de retenção LGPD — alertar se houver vencimento próximo.
4. Pesquisar advisories de segurança nas engines de banco em uso.
5. Verificar incidentes P0 de dados (LGPD breach, corrupção de dados, perda de integridade referencial):
   - Se detectado: `sessions_list()` filtrando `kind=main, agentId in [ceo, arquiteto]` → `sessions_send()` com severidade, impacto e plano de mitigação.
   - Não aguardar próximo ciclo para P0 de dados.
6. Se não houver ação necessária, responder HEARTBEAT_OK.
