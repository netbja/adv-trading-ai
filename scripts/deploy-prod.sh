#!/bin/bash

# 🚀 DÉPLOIEMENT PRODUCTION - TRADING AI SYSTEM
# Script de déploiement automatisé avec vérifications

set -e  # Arrêter en cas d'erreur

echo "🚀 ===== DÉPLOIEMENT PRODUCTION TRADING AI ====="

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# 1. Vérifications pré-déploiement
log "📋 Vérifications pré-déploiement..."

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
    error "Le fichier .env est manquant. Copiez env.example vers .env et configurez vos variables."
fi

# Vérifier les variables critiques
source .env
required_vars=(
    "POSTGRES_PASSWORD"
    "REDIS_PASSWORD"
    "GROQ_API_KEY"
    "ALPACA_API_KEY"
    "ALPACA_SECRET_KEY"
    "JWT_SECRET_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        error "Variable d'environnement manquante: $var"
    fi
done

success "✅ Variables d'environnement validées"

# 2. Vérifier Docker et Docker Compose
if ! command -v docker &> /dev/null; then
    error "Docker n'est pas installé"
fi

if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose n'est pas installé"
fi

success "✅ Docker et Docker Compose disponibles"

# 3. Arrêter les services existants s'ils sont en cours
log "🛑 Arrêt des services existants..."
docker-compose -f docker-compose.prod.yml down --remove-orphans || true

# 4. Nettoyer les images obsolètes
log "🧹 Nettoyage des images obsolètes..."
docker system prune -f

# 5. Build des images
log "🏗️ Build des images Docker..."
docker-compose -f docker-compose.prod.yml build --no-cache

# 6. Démarrage des services
log "▶️ Démarrage des services en mode production..."
docker-compose -f docker-compose.prod.yml up -d

# 7. Vérification de la santé des services
log "🩺 Vérification de la santé des services..."

check_service() {
    local service=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    log "Vérification de $service..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            success "✅ $service est opérationnel"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    error "❌ $service n'est pas disponible après $max_attempts tentatives"
}

# Attendre que les services démarrent
sleep 10

# Vérifier les services un par un
check_service "Frontend" "http://localhost/"
check_service "Backend API" "http://localhost/health"
check_service "Prometheus" "http://localhost:9090/-/healthy"
check_service "Grafana" "http://localhost:3001/api/health"

# 8. Affichage du statut final
log "📊 Statut des conteneurs:"
docker-compose -f docker-compose.prod.yml ps

# 9. Logs des dernières erreurs s'il y en a
log "📋 Derniers logs des services:"
docker-compose -f docker-compose.prod.yml logs --tail=10

# 10. URLs d'accès
echo ""
success "🎉 DÉPLOIEMENT RÉUSSI !"
echo ""
echo "📱 URLs d'accès:"
echo "  🌐 Application:     http://localhost"
echo "  🔧 API Backend:     http://localhost:8000"
echo "  📊 Grafana:         http://localhost:3001"
echo "  📈 Prometheus:      http://localhost:9090"
echo ""
echo "📚 Commandes utiles:"
echo "  📋 Logs en temps réel:  docker-compose -f docker-compose.prod.yml logs -f"
echo "  🛑 Arrêter:             docker-compose -f docker-compose.prod.yml down"
echo "  🔄 Redémarrer:          ./scripts/deploy-prod.sh"
echo ""
echo "🔐 Pensez à:"
echo "  - Configurer HTTPS avec Let's Encrypt"
echo "  - Sauvegarder régulièrement la base de données"
echo "  - Surveiller les métriques dans Grafana"
echo "" 