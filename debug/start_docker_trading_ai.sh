#!/bin/bash

# 🧠 SCRIPT DE DÉMARRAGE TRADING AI DOCKER
# Lance l'interface professionnelle complète en environnement Docker

set -e

echo "🧠 DÉMARRAGE TRADING AI PROFESSIONNEL EN DOCKER"
echo "="*60

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage coloré
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

# Vérifier Docker et Docker Compose
print_status "Vérification de Docker..."
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé"
    exit 1
fi

print_success "Docker et Docker Compose détectés"

# Vérifier/créer le fichier .env
if [ ! -f .env ]; then
    print_status "Création du fichier .env..."
    cp env.autonomous.example .env
    print_warning "Fichier .env créé depuis env.autonomous.example"
    print_warning "Modifiez .env si nécessaire avant le prochain démarrage"
fi

# Créer les répertoires nécessaires
print_status "Création des répertoires..."
mkdir -p {data,logs,backup}/{autonomous,postgres,grafana}
mkdir -p configs/{nginx,grafana,prometheus}

# Mode de démarrage
MODE=${1:-"simple"}

if [ "$MODE" = "professional" ] || [ "$MODE" = "pro" ]; then
    print_status "🏢 Démarrage en mode PROFESSIONNEL (avec Grafana + Prometheus)"
    COMPOSE_PROFILES="professional"
else
    print_status "🚀 Démarrage en mode SIMPLE (Interface uniquement)"
    COMPOSE_PROFILES=""
fi

# Arrêter les anciens containers si ils existent
print_status "Nettoyage des anciens containers..."
docker-compose -f docker-compose.autonomous.yml down 2>/dev/null || true

# Démarrer les services
print_status "Construction et démarrage des services..."

if [ "$COMPOSE_PROFILES" = "professional" ]; then
    COMPOSE_PROFILES=professional docker-compose -f docker-compose.autonomous.yml up --build -d
else
    docker-compose -f docker-compose.autonomous.yml up --build -d autonomous_trading postgres
fi

# Attendre que les services soient prêts
print_status "Attente du démarrage des services..."
sleep 10

# Vérifier la santé des services
print_status "Vérification de la santé des services..."

# PostgreSQL
if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "trading_ai_postgres_autonomous.*healthy"; then
    print_success "PostgreSQL est opérationnel"
else
    print_warning "PostgreSQL en cours de démarrage..."
fi

# Interface Trading AI
if curl -f http://localhost:8000/ &>/dev/null; then
    print_success "Interface Trading AI opérationnelle"
else
    print_warning "Interface Trading AI en cours de démarrage..."
fi

# Afficher les informations d'accès
echo ""
echo "🎉 TRADING AI DÉMARRÉ AVEC SUCCÈS!"
echo "="*60
echo ""
echo "📱 ACCÈS INTERFACE:"
echo "   URL: http://localhost:8000"
echo "   Compte: admin / TradingAI2025!"
echo ""
echo "🔍 SERVICES ACTIFS:"
docker-compose -f docker-compose.autonomous.yml ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}"
echo ""

if [ "$MODE" = "professional" ] || [ "$MODE" = "pro" ]; then
    echo "📊 SERVICES PROFESSIONNELS:"
    echo "   Grafana: http://localhost:3000 (admin/TradingAI2025!)"
    echo "   Prometheus: http://localhost:9090"
    echo ""
fi

echo "📋 COMMANDES UTILES:"
echo "   Logs en temps réel: docker-compose -f docker-compose.autonomous.yml logs -f"
echo "   Arrêter: docker-compose -f docker-compose.autonomous.yml down"
echo "   Redémarrer: $0"
echo ""

# Suivre les logs si demandé
if [ "$2" = "logs" ]; then
    print_status "📋 Suivi des logs en temps réel (Ctrl+C pour arrêter):"
    docker-compose -f docker-compose.autonomous.yml logs -f
fi

print_success "🚀 Système Trading AI opérationnel!" 