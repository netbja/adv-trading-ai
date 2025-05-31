#!/bin/bash

# 🚀 QUICK START - TRADING AI ORCHESTRATOR
# =========================================
# Script de démarrage rapide avec configuration guided

set -e

echo "🚀 QUICK START - TRADING AI ORCHESTRATOR"
echo "========================================="
echo ""

# Fonction pour afficher les étapes
show_step() {
    echo "📋 ÉTAPE $1: $2"
    echo "----------------------------------------"
}

# Vérifier si nous sommes dans le bon répertoire
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erreur: Exécuter ce script depuis le répertoire du projet"
    exit 1
fi

show_step "1" "CONFIGURATION ENVIRONNEMENT"

# Vérifier si .env existe
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    
    if [ -f "CONFIG_TEMPLATE.env" ]; then
        cp CONFIG_TEMPLATE.env .env
        echo "✅ Fichier .env créé depuis le template"
    else
        echo "⚠️ Template non trouvé, création d'un .env minimal..."
        cat > .env << EOF
# Configuration minimale pour démarrer
POSTGRES_DB="trading_ai"
POSTGRES_USER="trading_user" 
POSTGRES_PASSWORD="trading_secure_password_2024"
POSTGRES_HOST="database"
POSTGRES_PORT="5432"
REDIS_HOST="redis"
REDIS_PORT="6379"
ENVIRONMENT="development"
DEBUG="true"
DOCKER_ENV="true"
SECRET_KEY="votre_secret_key_ici"

# APIs à configurer
COINGECKO_API_KEY=""
ALPHA_VANTAGE_API_KEY=""
ALPACA_API_KEY=""
ALPACA_SECRET_KEY=""
GROQ_API_KEY=""
EOF
    fi
    
    echo ""
    echo "🔧 CONFIGURATION REQUISE:"
    echo "  1. Éditer le fichier .env avec vos clés API"
    echo "  2. Voir API_SETUP_GUIDE.md pour obtenir les clés"
    echo ""
    echo "📝 Voulez-vous éditer .env maintenant? (y/n)"
    read -r response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ Fichier .env trouvé"
fi

echo ""
show_step "2" "INSTALLATION DÉPENDANCES"

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non installé. Installer Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose non installé."
    exit 1
fi

echo "✅ Docker disponible"

echo ""
show_step "3" "TEST APIS (Optionnel)"

echo "🧪 Voulez-vous tester les APIs avant le lancement? (y/n)"
read -r test_apis
if [[ "$test_apis" == "y" || "$test_apis" == "Y" ]]; then
    echo "🔍 Lancement du test APIs..."
    python3 test_apis.py || {
        echo ""
        echo "⚠️ Certains tests ont échoué."
        echo "📋 Actions recommandées:"
        echo "  1. Vérifier vos clés API dans .env"
        echo "  2. Voir API_SETUP_GUIDE.md"
        echo "  3. Continuer quand même (APIs optionnelles)"
        echo ""
        echo "🤔 Continuer malgré les échecs? (y/n)"
        read -r continue_anyway
        if [[ "$continue_anyway" != "y" && "$continue_anyway" != "Y" ]]; then
            echo "🛑 Arrêt du script. Configurez les APIs et relancez."
            exit 1
        fi
    }
    echo "✅ Tests APIs terminés"
fi

echo ""
show_step "4" "LANCEMENT SYSTÈME DOCKER"

echo "🐳 Arrêt des anciens containers..."
docker-compose down 2>/dev/null || true

echo "🔨 Build des images Docker..."
docker-compose build

echo "🚀 Démarrage des services..."
docker-compose up -d

echo ""
echo "⏳ Attente du démarrage des services..."
sleep 10

echo ""
show_step "5" "VÉRIFICATION STATUT"

echo "📊 Statut des containers:"
docker-compose ps

echo ""
echo "🌐 Services disponibles:"
echo "  Frontend Vue3:     http://localhost:3000"
echo "  API Documentation: http://localhost:8000/docs"
echo "  API Health:        http://localhost:8000/health"

echo ""
echo "📋 Commandes utiles:"
echo "  Logs backend:      docker-compose logs -f backend"
echo "  Logs worker:       docker-compose logs -f celery_worker"
echo "  Arrêter:          docker-compose down"
echo "  Redémarrer:       docker-compose restart"

echo ""
show_step "6" "TEST FONCTIONNEL"

echo "🧪 Test de connectivité backend..."
sleep 5

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend opérationnel"
    
    echo "🧠 Test modules IA..."
    if curl -s http://localhost:8000/api/advanced-ai/status > /dev/null 2>&1; then
        echo "✅ Modules IA accessibles"
    else
        echo "⚠️ Modules IA en cours de démarrage..."
    fi
else
    echo "⚠️ Backend en cours de démarrage..."
    echo "   Vérifier avec: docker-compose logs backend"
fi

echo ""
echo "🎉 INSTALLATION TERMINÉE!"
echo "========================="
echo ""
echo "🚀 Votre système Trading AI est déployé!"
echo ""
echo "📱 Prochaines étapes:"
echo "  1. Ouvrir http://localhost:3000 (Frontend)"
echo "  2. Configurer les APIs manquantes si nécessaire"
echo "  3. Lancer les premiers tests de trading"
echo "  4. Monitorer avec: docker-compose logs -f"
echo ""
echo "📚 Documentation:"
echo "  - API_SETUP_GUIDE.md (Configuration APIs)"
echo "  - SETUP_STEP_BY_STEP.md (Guide détaillé)"
echo ""
echo "💡 Support: Voir les logs avec docker-compose logs [service]"
echo ""
echo "✨ Happy Trading! 📈🤖" 