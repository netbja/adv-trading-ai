#!/bin/bash

# 🧪 TEST COMPLET ORCHESTRATEUR AI
# Script de test pour tous les workflows multi-assets

BASE_URL="http://localhost:8080/api/orchestrator"

echo "🚀 TESTS ORCHESTRATEUR AI - WORKFLOWS MULTI-ASSETS"
echo "=================================================="

# 1. Test statut global
echo "📊 1. STATUT GLOBAL"
curl -s "$BASE_URL/status" | jq '.orchestrator | {running, total_tasks, success_rate}'
echo ""

# 2. Test recommandations par asset
echo "💡 2. RECOMMANDATIONS PAR ASSET"
echo ""

echo "🪙 MEME COINS (volatilité > 0.8 requise):"
curl -s "$BASE_URL/recommendations/meme_coins" | jq '.recommendations | length as $count | if $count > 0 then . else "❌ Pas de recommandations (volatilité trop faible)" end'
echo ""

echo "₿ CRYPTO LONG TERME (volatilité < 0.4 idéale):"
curl -s "$BASE_URL/recommendations/crypto_lt" | jq '.recommendations[] | {task_type, priority, frequency_minutes, reason}'
echo ""

echo "💱 FOREX (8h-17h UTC requis):"
FOREX_RECS=$(curl -s "$BASE_URL/recommendations/forex" | jq '.recommendations | length' 2>/dev/null || echo "0")
if [ "${FOREX_RECS:-0}" -eq 0 ]; then
    echo "❌ Pas de recommandations (hors session trading)"
else
    curl -s "$BASE_URL/recommendations/forex" | jq '.recommendations[] | {task_type, priority, frequency_minutes}'
fi
echo ""

echo "📈 ETF (toujours actif):"
curl -s "$BASE_URL/recommendations/etf" | jq '.recommendations[] | {task_type, priority, frequency_minutes, reason}'
echo ""

# 3. Test conditions de marché
echo "📊 3. CONDITIONS DE MARCHÉ ACTUELLES"
curl -s "$BASE_URL/recommendations" | jq '{market_conditions, system_status}' | jq '.market_conditions as $market | .system_status as $system | {
    "💹 Volatilité": $market.volatility,
    "📈 Tendance": $market.trend_strength, 
    "💻 CPU": "\($system.cpu_usage // 0)%",
    "🧠 RAM": "\($system.memory_usage // 0)%",
    "🔗 Connexions": ($system.active_connections // 0)
}'
echo ""

# 4. Test métriques
echo "📈 4. MÉTRIQUES PERFORMANCE"
curl -s "$BASE_URL/metrics" | jq '.metrics | {orchestrator_running, total_tasks, global_success_rate, average_execution_time}'
echo ""

# 5. Test santé
echo "🏥 5. SANTÉ SYSTÈME"
curl -s "$BASE_URL/health" | jq '.health | {status, running, success_rate, message}'
echo ""

# 6. Résumé intelligent
echo "🧠 6. RÉSUMÉ INTELLIGENT"
echo "====================="

# Analyser les conditions et donner un résumé avec gestion d'erreurs
VOLATILITY=$(curl -s "$BASE_URL/recommendations" | jq '.market_conditions.volatility // 0' 2>/dev/null)
SYSTEM_CPU=$(curl -s "$BASE_URL/recommendations" | jq '.system_status.cpu_usage // 0' 2>/dev/null)
HOUR=$(date +%H)

echo "⏰ Heure actuelle: ${HOUR}h UTC"
echo "📊 Volatilité: ${VOLATILITY:-N/A}"
echo "💻 CPU: ${SYSTEM_CPU:-0}%"
echo ""

# Utiliser awk au lieu de bc pour éviter les dépendances
if [ "${VOLATILITY:-0}" != "null" ] && [ "${VOLATILITY:-0}" != "0" ]; then
    VOLATILITY_INT=$(echo "$VOLATILITY * 100" | awk '{print int($1)}' 2>/dev/null || echo "0")
    
    if [ "${VOLATILITY_INT:-0}" -gt 80 ]; then
        echo "🔥 VOLATILITÉ ÉLEVÉE → Meme coins actifs !"
    elif [ "${VOLATILITY_INT:-0}" -lt 40 ]; then
        echo "😴 PÉRIODE CALME → Crypto long terme + ETF optimaux"
    else
        echo "📊 CONDITIONS NORMALES → ETF + workflows standards"
    fi
else
    echo "📊 CONDITIONS NORMALES → ETF + workflows standards"
fi

if [ "${HOUR:-12}" -ge 8 ] && [ "${HOUR:-12}" -le 17 ]; then
    echo "💱 SESSION FOREX ACTIVE → Trading recommandé"
else
    echo "🌙 HORS SESSION FOREX → Pas de trading forex"
fi

echo ""
echo "✅ Tests terminés !" 