#!/bin/bash

# 🧪 LAUNCH PAPER TRADING SYSTEM
# ===============================
# Script pour démarrer le système complet avec paper trading

echo "🧪 LANCEMENT SYSTÈME PAPER TRADING AI"
echo "====================================="

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Docker et Docker Compose sont disponibles"

# Variables
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-3000}

echo "📋 Configuration:"
echo "   Backend: http://localhost:$BACKEND_PORT"
echo "   Frontend: http://localhost:$FRONTEND_PORT"
echo "   Mode: Paper Trading (Dry Run)"

# Créer les répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p logs
mkdir -p backups

# Copier les dépendances Python si nécessaire
if [ ! -f "backend/requirements.txt" ]; then
    echo "⚠️  Création du fichier requirements.txt..."
    cat > backend/requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.0
asyncpg==0.29.0
redis==5.0.1
celery==5.3.4
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
aiofiles==23.2.1
jinja2==3.1.2
prometheus-client==0.19.0
structlog==23.2.0
psutil==5.9.6
aiohttp==3.9.1
numpy==1.25.2
pandas==2.1.4
scipy==1.11.4
scikit-learn==1.3.2
loguru==0.7.2
python-dotenv==1.0.0
EOF
fi

echo "🚀 Démarrage du système..."

# Arrêter les services existants
echo "🛑 Arrêt des services existants..."
docker-compose down 2>/dev/null || true

# Démarrer les services
echo "▶️  Démarrage avec Docker Compose..."
docker-compose -f docker-compose.yml up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."

# Vérifier le backend
echo "🔍 Vérification du backend..."
for i in {1..30}; do
    if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
        echo "✅ Backend prêt sur http://localhost:$BACKEND_PORT"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Timeout: Le backend n'est pas accessible"
        echo "📋 Logs du backend:"
        docker-compose logs backend
        exit 1
    fi
    sleep 2
done

# Vérifier le frontend
echo "🔍 Vérification du frontend..."
for i in {1..30}; do
    if curl -s http://localhost:$FRONTEND_PORT > /dev/null 2>&1; then
        echo "✅ Frontend prêt sur http://localhost:$FRONTEND_PORT"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Timeout: Le frontend n'est pas accessible"
        echo "📋 Logs du frontend:"
        docker-compose logs frontend
        exit 1
    fi
    sleep 2
done

echo ""
echo "🎉 SYSTÈME DÉMARRÉ AVEC SUCCÈS!"
echo "==============================="
echo ""
echo "📊 INTERFACES DISPONIBLES:"
echo "   🌐 Frontend:     http://localhost:$FRONTEND_PORT"
echo "   🔧 API Backend:  http://localhost:$BACKEND_PORT"
echo "   📚 API Docs:     http://localhost:$BACKEND_PORT/docs"
echo "   🧠 AI Modules:   http://localhost:$BACKEND_PORT/api/advanced-ai/*"
echo "   🧪 Trading API:  http://localhost:$BACKEND_PORT/trading/*"
echo ""
echo "🧪 PAPER TRADING PRÊT:"
echo "   1. Va sur http://localhost:$FRONTEND_PORT"
echo "   2. Clique sur 'Paper Trading' dans le menu"
echo "   3. Configure tes clés API (mode paper)"
echo "   4. Lance les trades de démonstration"
echo ""
echo "💡 PROCHAINES ÉTAPES:"
echo "   • Configure tes clés API Alpaca/Binance"
echo "   • Teste le paper trading"
echo "   • Lance les stratégies IA"
echo "   • Surveille les performances"
echo ""
echo "🛑 Pour arrêter le système:"
echo "   docker-compose down"
echo ""
echo "📋 Pour voir les logs:"
echo "   docker-compose logs -f [service]"
echo ""

# Afficher les logs en temps réel si demandé
read -p "👀 Voulez-vous voir les logs en temps réel? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📋 Logs en temps réel (Ctrl+C pour arrêter):"
    docker-compose logs -f
fi 