#!/bin/bash

# 🧪 SCRIPT DE TEST - DÉVELOPPEMENT ORCHESTRATEUR AI MULTI-ASSETS
# Version avec Nginx + PostgreSQL "trader" + Multi-Assets workflows

echo "🚀 TESTS DÉVELOPPEMENT - ORCHESTRATEUR AI MULTI-ASSETS"
echo "======================================================="

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URLs de test
BASE_URL="http://localhost"
API_URL="$BASE_URL/api"

# Fonction pour tester une URL
test_endpoint() {
    local url=$1
    local description=$2
    local expected_code=${3:-200}
    
    echo -n "  📡 $description... "
    
    response=$(curl -s -w "%{http_code}" -o /tmp/test_response "$url" 2>/dev/null)
    http_code=$response
    
    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}✅ OK ($http_code)${NC}"
        return 0
    else
        echo -e "${RED}❌ ÉCHEC ($http_code)${NC}"
        return 1
    fi
}

# Test avec données JSON
test_json_endpoint() {
    local url=$1
    local description=$2
    
    echo -n "  📊 $description... "
    
    response=$(curl -s "$url" 2>/dev/null)
    
    if echo "$response" | jq . >/dev/null 2>&1; then
        echo -e "${GREEN}✅ JSON valide${NC}"
        echo "$response" | jq -r 'keys[]' 2>/dev/null | head -3 | sed 's/^/    📋 /'
        return 0
    else
        echo -e "${RED}❌ JSON invalide${NC}"
        echo "    🔍 Réponse: $response"
        return 1
    fi
}

echo ""
echo "🔍 1. TESTS INFRASTRUCTURE"
echo "------------------------"

# Test des services Docker
echo "  🐳 Vérification services Docker..."
if docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
    echo -e "    ${GREEN}✅ Services Docker actifs${NC}"
else
    echo -e "    ${RED}❌ Services Docker non actifs${NC}"
    echo "    💡 Lancez: docker-compose -f docker-compose.dev.yml up -d"
    exit 1
fi

# Test Nginx
test_endpoint "$BASE_URL" "Nginx proxy"

# Test Frontend via Nginx
test_endpoint "$BASE_URL/" "Frontend Vue3 via Nginx"

echo ""
echo "🎯 2. TESTS API BACKEND"
echo "----------------------"

# Tests API de base
test_endpoint "$API_URL/health" "Health check API"
test_json_endpoint "$API_URL/health" "Health check données"

echo ""
echo "🧠 3. TESTS ORCHESTRATEUR MULTI-ASSETS"
echo "--------------------------------------"

# Status orchestrateur
test_json_endpoint "$API_URL/orchestrator/status" "Status orchestrateur global"

# Recommandations globales
test_json_endpoint "$API_URL/orchestrator/recommendations" "Recommandations globales"

# Test de chaque asset type
assets=("meme_coins" "crypto_lt" "forex" "etf")
for asset in "${assets[@]}"; do
    test_json_endpoint "$API_URL/orchestrator/recommendations/$asset" "Recommandations $asset"
done

# Métriques et santé
test_json_endpoint "$API_URL/orchestrator/metrics" "Métriques orchestrateur"
test_json_endpoint "$API_URL/orchestrator/health" "Santé orchestrateur"

echo ""
echo "📊 4. TESTS SPÉCIFIQUES MULTI-ASSETS"
echo "-----------------------------------"

# Test des recommandations par asset avec analyse
for asset in "${assets[@]}"; do
    echo "  🔍 Analyse $asset:"
    response=$(curl -s "$API_URL/orchestrator/recommendations/$asset" 2>/dev/null)
    
    if echo "$response" | jq . >/dev/null 2>&1; then
        count=$(echo "$response" | jq -r '.recommendations | length' 2>/dev/null)
        active=$(echo "$response" | jq -r '.recommendations | length > 0' 2>/dev/null)
        
        if [ "$active" = "true" ]; then
            echo -e "    ${GREEN}✅ $count recommandations actives${NC}"
            # Afficher les détails des recommandations
            echo "$response" | jq -r '.recommendations[] | "    📋 \(.task_type) - \(.priority) - \(.frequency_minutes)min"' 2>/dev/null
        else
            echo -e "    ${YELLOW}⏸️ Aucune recommandation (normal selon conditions)${NC}"
        fi
    else
        echo -e "    ${RED}❌ Erreur de données${NC}"
    fi
done

echo ""
echo "🌐 5. TESTS NGINX & ROUTING"
echo "--------------------------"

# Test routing spécifique
test_endpoint "$BASE_URL/api/orchestrator/status" "Routing API via Nginx"
test_endpoint "$BASE_URL/health" "Health check via Nginx"

echo ""
echo "🎨 6. TESTS FRONTEND ASSETS"
echo "---------------------------"

# Test des assets frontend (si accessibles)
test_endpoint "$BASE_URL/assets" "Assets frontend" 404  # Normal si pas d'assets
test_endpoint "$BASE_URL/favicon.ico" "Favicon" 404     # Normal si pas configuré

echo ""
echo "💾 7. TESTS BASE DE DONNÉES"
echo "--------------------------"

# Test connexion PostgreSQL
echo -n "  🐘 Connexion PostgreSQL... "
if docker-compose -f docker-compose.dev.yml exec -T postgres psql -U trader -d trading_ai -c "SELECT version();" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Connexion OK${NC}"
    
    # Test tables
    echo -n "  📊 Tables orchestrateur... "
    table_count=$(docker-compose -f docker-compose.dev.yml exec -T postgres psql -U trader -d trading_ai -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')
    if [ "$table_count" -gt 0 ]; then
        echo -e "${GREEN}✅ $table_count tables${NC}"
    else
        echo -e "${YELLOW}⚠️ Aucune table (migrations à faire?)${NC}"
    fi
else
    echo -e "${RED}❌ Connexion échouée${NC}"
fi

echo ""
echo "📈 8. ANALYSE FINALE"
echo "-------------------"

# Récupérer le status global
echo "  🔍 Status global orchestrateur:"
response=$(curl -s "$API_URL/orchestrator/status" 2>/dev/null)
if echo "$response" | jq . >/dev/null 2>&1; then
    running=$(echo "$response" | jq -r '.orchestrator.running // false' 2>/dev/null)
    success_rate=$(echo "$response" | jq -r '.orchestrator.success_rate // 0' 2>/dev/null)
    
    if [ "$running" = "true" ]; then
        echo -e "    ${GREEN}🟢 Orchestrateur ACTIF${NC}"
    else
        echo -e "    ${YELLOW}🔴 Orchestrateur ARRÊTÉ${NC}"
    fi
    
    echo "    📊 Taux de succès: $success_rate%"
    
    # Conditions du marché
    volatility=$(echo "$response" | jq -r '.market_conditions.volatility // "N/A"' 2>/dev/null)
    echo "    📈 Volatilité marché: $volatility"
fi

echo ""
echo "🎯 RECOMMANDATIONS D'AMÉLIORATION"
echo "================================="

# Vérifications et suggestions
if ! docker-compose -f docker-compose.dev.yml ps | grep -q "nginx.*Up"; then
    echo -e "${YELLOW}⚠️ Nginx non détecté - vérifiez la configuration${NC}"
fi

if ! curl -s "$BASE_URL" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Frontend non accessible via Nginx - vérifiez les proxies${NC}"
fi

echo ""
echo "✅ TESTS TERMINÉS"
echo "================="
echo -e "${BLUE}💡 Pour démarrer l'orchestrateur: curl -X POST $API_URL/orchestrator/start${NC}"
echo -e "${BLUE}🌐 Interface web: $BASE_URL${NC}"
echo -e "${BLUE}📊 API docs: $API_URL/docs${NC}" 