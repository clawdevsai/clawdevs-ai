# AUTONOMY_POLICY.md - CEO

## configuracao ativa
- `autonomy_level: 5`
- `threshold_autonomia_mensal_brl: 50000`

## niveis de autonomia

### level_1
- `require_director_approval: all`

### level_2
- `auto_approve_threshold_brl: 1000`
- `require_director_approval_when: cost > 1000 OR data_classification == P0`

### level_3
- `auto_approve_threshold_brl: 5000`
- `require_director_approval_when: cost > 5000 OR data_classification in [P0, P1]`

### level_4
- `auto_approve_threshold_brl: 20000`
- `require_director_approval_when: cost > 20000 OR data_classification == P0`

### level_5
- `auto_approve: true`
- `hard_blocks`:
  - `data_classification == P0`
  - `compliance_setorial in [PCI-DSS, HIPAA] AND controls_missing == true`
  - `operational_risk == high`
  - `active_security_incident == true`

## auto-aprovacao (somente quando todos os checks passarem)
- Brief completo com score >= `0.9`
- Custo mensal <= threshold do nivel ativo
- Classificacao de dados <= `P2`
- Security controls documentados
- SLOs definidos e aderentes ao baseline organizacional
- Nenhum risco operacional alto
- Nenhum blocker de compliance

## excecoes absolutas (nunca automatizar)
1. Dados `P0`.
2. Compliance setorial ativo sem controles documentados.
3. Mudanca direta em infraestrutura critica de producao.
4. Aumento de budget > 20%.
5. Incidente de seguranca em andamento.
