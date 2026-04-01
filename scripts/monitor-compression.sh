#!/bin/bash
# Monitor em tempo real para Phase 3
# Uso: ./monitor-compression.sh [intervalo-segundos]

INTERVAL=${1:-10}  # Default: 10 segundos
BACKEND_URL="http://localhost:8000"

echo "📊 Context-Mode Compression Monitor"
echo "===================================="
echo "Intervalo: ${INTERVAL}s | Pressione Ctrl+C para sair"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

format_number() {
  echo "$1" | awk '{printf "%-10s", $1}'
}

show_metrics() {
  local metrics=$(curl -s "$BACKEND_URL/api/context-mode/metrics" 2>/dev/null)

  if [ -z "$metrics" ]; then
    echo -e "${RED}❌ API não respondeu${NC}"
    return
  fi

  # Extrair valores
  local status=$(echo "$metrics" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
  local total=$(echo "$metrics" | grep -o '"total_compressions":[0-9]*' | cut -d: -f2 || echo "0")
  local rate=$(echo "$metrics" | grep -o '"compression_rate":"[^"]*"' | cut -d'"' -f4 || echo "0%")
  local saved=$(echo "$metrics" | grep -o '"tokens_saved_estimate":[0-9]*' | cut -d: -f2 || echo "0")
  local avg_ratio=$(echo "$metrics" | grep -o '"average_compression_ratio":[0-9.]*' | cut -d: -f2 || echo "0")

  # Determinar cor baseado no status
  if [ "$total" -gt 0 ]; then
    STATUS_COLOR=$GREEN
    STATUS_ICON="✅"
  else
    STATUS_COLOR=$YELLOW
    STATUS_ICON="⏳"
  fi

  # Exibir
  echo -e "$(date '+%H:%M:%S') ${STATUS_COLOR}${STATUS_ICON}${NC}"
  echo "  Status: $(format_number "$status")"
  echo "  Compressões: $(format_number "$total")"
  echo "  Taxa: $(format_number "$rate")"
  echo "  Tokens Salvos: $(format_number "$saved")"
  echo "  Ratio Médio: $(format_number "$avg_ratio")"
  echo ""
}

# Loop infinito
while true; do
  clear
  echo "📊 Context-Mode Compression Monitor"
  echo "===================================="
  echo "$(date '+%Y-%m-%d %H:%M:%S') • Intervalo: ${INTERVAL}s"
  echo ""

  show_metrics

  echo "Próxima atualização em ${INTERVAL}s... (Ctrl+C para sair)"
done
