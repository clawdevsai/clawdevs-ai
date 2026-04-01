#!/bin/bash
# Phase 3: Production Validation - Ativar todos os 15 agents
# Objetivo: Validar context-mode compression em produção com ciclos reais

set -e

echo "🚀 PHASE 3: Production Validation"
echo "=================================="
echo ""
echo "Iniciando validação de context-mode em produção..."
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Configurações
BACKEND_URL="http://localhost:8000"
MONITORING_INTERVAL=15  # segundos entre checks
TOTAL_DURATION=3600     # 1 hora em segundos
CHECK_CYCLES=$((TOTAL_DURATION / MONITORING_INTERVAL))

# Array com os 15 agents
AGENTS=(
  "arquiteto"
  "ceo"
  "database_healer"
  "dba_data_engineer"
  "dev_backend"
  "dev_frontend"
  "dev_mobile"
  "devops_sre"
  "final_consolidation"
  "memory_curator"
  "po"
  "qa_engineer"
  "security_engineer"
  "ux_designer"
  "agent_reviver"
)

echo "📋 Agents a ativar: ${#AGENTS[@]} agentes"
for agent in "${AGENTS[@]}"; do
  echo "  • $agent"
done
echo ""

# Função: Status inicial
check_initial_status() {
  echo "📊 Status Inicial:"
  echo "  Verificando status da API..."

  local status=$(curl -s "$BACKEND_URL/api/context-mode/status" | grep -o '"status":"[^"]*"')
  echo "  → $status"

  local metrics=$(curl -s "$BACKEND_URL/api/context-mode/metrics")
  echo "  → Metrics: $metrics"
  echo ""
}

# Função: Triggar um agent
trigger_agent() {
  local agent_slug=$1
  echo "  🎯 Disparando: $agent_slug..."

  # Simular requisição para executar o agent
  # Em produção real, seria via OpenClaw API ou CLI
  curl -s -X POST "$BACKEND_URL/sessions" \
    -H "Content-Type: application/json" \
    -d "{\"agent_slug\":\"$agent_slug\",\"auto_run\":true}" \
    2>/dev/null || echo "  ⚠️  Agent dispatch não respondeu (esperado em início)"
}

# Função: Disparar todos os agents
trigger_all_agents() {
  echo "🔥 Disparando todos os 15 agents..."
  echo ""

  for agent in "${AGENTS[@]}"; do
    trigger_agent "$agent" &  # Background para paralelismo
  done

  wait  # Aguardar todos os disparos terminarem
  echo "✅ Todos os agents foram disparados"
  echo ""
}

# Função: Monitorar métricas em tempo real
monitor_metrics() {
  echo "📈 Monitorando compressão em tempo real..."
  echo "   (Intervalo: ${MONITORING_INTERVAL}s, Duração total: ${TOTAL_DURATION}s)"
  echo ""
  echo "Ciclo | Tempo | Total Compressões | Taxa | Tokens Salvos | Status"
  echo "------|-------|-------------------|------|---------------|--------"

  local cycle=0
  local start_time=$(date +%s)

  while [ $cycle -lt $CHECK_CYCLES ]; do
    local current_time=$(date +%s)
    local elapsed=$((current_time - start_time))

    # Buscar métricas
    local response=$(curl -s "$BACKEND_URL/api/context-mode/metrics")

    # Extrair valores (com fallback para 0 se não encontrado)
    local total_compressions=$(echo "$response" | grep -o '"total_compressions":[0-9]*' | cut -d: -f2 || echo "0")
    local compression_rate=$(echo "$response" | grep -o '"compression_rate":"[^"]*"' | cut -d'"' -f4 || echo "0%")
    local tokens_saved=$(echo "$response" | grep -o '"tokens_saved_estimate":[0-9]*' | cut -d: -f2 || echo "0")
    local status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "waiting")

    # Converter tempo para MM:SS
    local mins=$((elapsed / 60))
    local secs=$((elapsed % 60))
    local time_fmt=$(printf "%02d:%02d" $mins $secs)

    # Exibir linha de progresso
    printf "%4d | %s | %17s | %4s | %13s | %s\n" \
      "$cycle" "$time_fmt" "$total_compressions" "$compression_rate" "$tokens_saved" "$status"

    # Se houver compressões, já temos validação
    if [ "$total_compressions" -gt 0 ]; then
      echo ""
      echo "✨ COMPRESSÃO DETECTADA!"
      echo "   • Total de compressões: $total_compressions"
      echo "   • Taxa: $compression_rate"
      echo "   • Tokens salvos: $tokens_saved"
      break
    fi

    cycle=$((cycle + 1))
    sleep $MONITORING_INTERVAL
  done

  echo ""
}

# Função: Relatório final
final_report() {
  echo "📋 Relatório Final"
  echo "==================="
  echo ""

  # Buscar métricas finais
  local metrics=$(curl -s "$BACKEND_URL/api/context-mode/metrics")
  local summary=$(curl -s "$BACKEND_URL/api/context-mode/summary")

  echo "📊 Métricas de Compressão:"
  echo "$metrics" | python3 -m json.tool 2>/dev/null || echo "$metrics"
  echo ""

  echo "💰 Resumo de Economia:"
  echo "$summary" | python3 -m json.tool 2>/dev/null || echo "$summary"
  echo ""

  # Análise
  local total=$(echo "$metrics" | grep -o '"total_compressions":[0-9]*' | cut -d: -f2 || echo "0")

  if [ "$total" -gt 0 ]; then
    echo "✅ VALIDAÇÃO SUCESSO!"
    echo "   Context-mode está funcionando em produção"
    echo "   Compressions detectadas: $total"
  else
    echo "⏳ Validação em progresso"
    echo "   Aguarde agentes executarem ferramentas >5KB"
  fi
  echo ""
}

# Executar pipeline completo
main() {
  check_initial_status
  trigger_all_agents
  monitor_metrics
  final_report

  echo "🎉 Phase 3 Completa!"
  echo ""
  echo "Próximos passos:"
  echo "  1. Aguardar ~1h para dados reais acumularem"
  echo "  2. Verificar /api/context-mode/summary para economia final"
  echo "  3. Phase 4: Memory + Cron Optimization (semana próxima)"
  echo ""
  echo "Dashboard em tempo real:"
  echo "  curl http://localhost:8000/api/context-mode/metrics"
}

main
