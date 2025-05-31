#!/bin/bash

# 🚀 LANCEUR INTELLIGENT - SYSTÈME IA TRADING AVANCÉ
# ==================================================
# Détection automatique : Docker vs Bare-Metal

set -e  # Arrêter en cas d'erreur

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'affichage avec couleurs
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔸 $1${NC}"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Banner unifié
print_banner() {
    echo -e "${PURPLE}"
    cat << "EOF"
    ███████╗██╗ █████╗     ████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
    ██╔══██║██║██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
    ███████║██║███████║       ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗
    ██╔══██║██║██╔══██║       ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║
    ██║  ██║██║██║  ██║       ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                                    
                🤖 LANCEUR INTELLIGENT v2.0 - DÉTECTION AUTO
EOF
    echo -e "${NC}"
}

# Détecter l'environnement optimal
detect_environment() {
    print_step "Détection de l'environnement optimal..."
    
    # Variables de détection
    DOCKER_AVAILABLE=false
    DOCKER_COMPOSE_AVAILABLE=false
    PYTHON_MANAGED=false
    BARE_METAL_POSSIBLE=false
    
    # 1. Vérifier Docker
    if command -v docker &> /dev/null; then
        DOCKER_AVAILABLE=true
        print_info "Docker détecté: $(docker --version | cut -d' ' -f3 | cut -d',' -f1)"
        
        # Vérifier Docker Compose
        if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
            DOCKER_COMPOSE_AVAILABLE=true
            print_info "Docker Compose détecté"
        fi
    fi
    
    # 2. Vérifier Python et gestion des packages
    if command -v python3 &> /dev/null; then
        print_info "Python3 détecté: $(python3 --version)"
        
        # Tester si on peut installer des packages
        if python3 -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>/dev/null; then
            print_info "Environnement virtuel Python détecté"
            BARE_METAL_POSSIBLE=true
        elif pip3 list &> /dev/null && pip3 install --help | grep -q "\--user"; then
            print_info "Installation utilisateur Python possible"
            BARE_METAL_POSSIBLE=true
        else
            print_warning "Python système géré externalement (Ubuntu 23+)"
            PYTHON_MANAGED=true
        fi
    fi
    
    # 3. Déterminer le mode recommandé
    echo
    print_header "🔍 ANALYSE ENVIRONNEMENT"
    echo "================================"
    
    if $DOCKER_AVAILABLE && $DOCKER_COMPOSE_AVAILABLE; then
        print_status "✅ Docker + Compose disponibles"
        RECOMMENDED_MODE="docker"
    elif $BARE_METAL_POSSIBLE; then
        print_status "✅ Installation bare-metal possible"
        RECOMMENDED_MODE="bare-metal"
    elif $PYTHON_MANAGED; then
        print_warning "⚠️  Python géré externalement - Docker recommandé"
        if $DOCKER_AVAILABLE; then
            RECOMMENDED_MODE="docker"
        else
            RECOMMENDED_MODE="bare-metal-venv"
        fi
    else
        print_error "❌ Aucun environnement optimal détecté"
        RECOMMENDED_MODE="manual"
    fi
    
    echo "🎯 Mode recommandé: $RECOMMENDED_MODE"
    echo
}

# Afficher le menu de choix
show_mode_menu() {
    echo -e "${BLUE}🎯 CHOISIR LE MODE DE DÉPLOIEMENT${NC}"
    echo "================================="
    echo
    
    if $DOCKER_AVAILABLE && $DOCKER_COMPOSE_AVAILABLE; then
        echo -e "${GREEN}1. 🐳 Docker (Recommandé)${NC}"
        echo "   • Isolation complète des services"
        echo "   • Pas de conflits de dépendances"
        echo "   • Production-ready"
        echo
    else
        echo -e "${RED}1. 🐳 Docker (Non disponible)${NC}"
        echo "   • Docker non installé"
        echo
    fi
    
    if $BARE_METAL_POSSIBLE; then
        echo -e "${GREEN}2. ⚡ Bare-Metal (Disponible)${NC}"
        echo "   • Installation locale directe"
        echo "   • Performance native"
        echo "   • Contrôle total"
        echo
    else
        echo -e "${YELLOW}2. ⚡ Bare-Metal (Problématique)${NC}"
        echo "   • Python géré externellement"
        echo "   • Nécessite environnement virtuel"
        echo
    fi
    
    echo -e "${CYAN}3. 🔧 Bare-Metal avec Venv${NC}"
    echo "   • Création d'environnement virtuel"
    echo "   • Installation isolée"
    echo "   • Contournement restrictions système"
    echo
    
    echo -e "${PURPLE}4. 📋 Analyse détaillée${NC}"
    echo "   • Diagnostic complet système"
    echo "   • Recommandations personnalisées"
    echo
    
    echo "0. ❌ Quitter"
    echo
}

# Lancer le mode Docker - INTÉGRÉ
launch_docker_mode() {
    print_header "🐳 LANCEMENT MODE DOCKER"
    echo
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker non trouvé! Installe Docker d'abord."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose non trouvé! Installe Docker Compose."
        exit 1
    fi
    
    # Détecter la version de compose
    if docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        COMPOSE_CMD="docker-compose"
    fi
    
    print_status "Docker et Docker Compose détectés"
    print_info "Commande Compose: $COMPOSE_CMD"
    
    # Menu Docker
    echo
    echo -e "${BLUE}🐳 MENU DOCKER${NC}"
    echo "==============="
    echo "1. 🚀 Lancement complet (recommandé)"
    echo "2. 🔧 Construction des images"
    echo "3. ⚡ Démarrage services principaux"
    echo "4. 🧪 Tests IA avancée"
    echo "5. 📊 Monitoring temps réel"
    echo "6. 🎨 Interface web (frontend)"
    echo "7. 🛑 Arrêter les services"
    echo "8. 🧹 Nettoyage complet"
    echo "0. ↩️  Retour menu principal"
    echo
    
    read -p "Choix Docker (0-8): " docker_choice
    
    case $docker_choice in
        1)
            print_info "🚀 Lancement complet Docker..."
            docker_cleanup
            docker_build
            docker_start_services
            docker_run_tests
            print_status "🎉 Système Docker opérationnel!"
            ;;
        2)
            print_info "🔧 Construction images Docker..."
            docker_build
            ;;
        3)
            print_info "⚡ Démarrage services Docker..."
            docker_start_services
            ;;
        4)
            print_info "🧪 Tests IA Docker..."
            docker_run_tests
            ;;
        5)
            print_info "📊 Monitoring Docker..."
            docker_monitoring
            ;;
        6)
            print_info "🎨 Interface web Docker..."
            docker_frontend
            ;;
        7)
            print_info "🛑 Arrêt services Docker..."
            docker_stop
            ;;
        8)
            print_info "🧹 Nettoyage Docker..."
            docker_cleanup_full
            ;;
        0)
            return 0
            ;;
        *)
            print_error "Option Docker invalide"
            return 1
            ;;
    esac
}

# Fonctions Docker intégrées
docker_cleanup() {
    print_step "Nettoyage conteneurs existants..."
    $COMPOSE_CMD down --remove-orphans 2>/dev/null || true
    docker ps -a --filter "name=trading_" --format "{{.Names}}" | xargs docker rm -f 2>/dev/null || true
    print_status "Nettoyage terminé"
}

docker_build() {
    print_step "Construction des images Docker..."
    $COMPOSE_CMD build backend ai_tests
    print_status "Images construites"
}

docker_start_services() {
    print_step "Démarrage des services principaux..."
    
    # Base de données et Redis
    $COMPOSE_CMD up -d database redis
    print_info "Attente base de données..."
    sleep 10
    
    # Backend
    $COMPOSE_CMD up -d backend
    print_info "Attente API backend..."
    sleep 15
    
    # Celery
    $COMPOSE_CMD up -d celery_worker celery_beat
    
    print_status "Services principaux démarrés"
    print_info "🌐 API: http://localhost:8000"
    print_info "❤️  Health: http://localhost:8000/health"
    print_info "📚 Docs: http://localhost:8000/docs"
}

docker_run_tests() {
    print_step "Lancement tests IA Docker..."
    sleep 5
    if $COMPOSE_CMD run --rm ai_tests; then
        print_status "Tests IA réussis! 🎉"
    else
        print_warning "Certains tests ont échoué"
    fi
}

docker_monitoring() {
    print_step "Monitoring Docker..."
    $COMPOSE_CMD --profile monitoring up -d prometheus grafana 2>/dev/null || print_warning "Monitoring non disponible"
    
    while true; do
        clear
        echo -e "${CYAN}📊 MONITORING DOCKER${NC}"
        echo "==================="
        echo "⏰ $(date)"
        echo
        
        $COMPOSE_CMD ps
        echo
        
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ API: OPÉRATIONNEL${NC}"
        else
            echo -e "${RED}❌ API: HORS SERVICE${NC}"
        fi
        
        echo -e "${YELLOW}Ctrl+C pour arrêter${NC}"
        sleep 5
    done
}

docker_frontend() {
    print_step "Démarrage interface web..."
    docker_start_services
    $COMPOSE_CMD up -d frontend
    print_status "Interface web démarrée"
    print_info "🌐 Interface: http://localhost"
    print_info "🔧 API Backend: http://localhost:8000"
}

docker_stop() {
    print_step "Arrêt services Docker..."
    $COMPOSE_CMD down --remove-orphans
    print_status "Services arrêtés"
}

docker_cleanup_full() {
    print_step "Nettoyage complet Docker..."
    $COMPOSE_CMD down --volumes --remove-orphans
    docker images --filter "reference=*trading*" -q | xargs docker rmi -f 2>/dev/null || true
    docker volume ls --filter "name=trading_" -q | xargs docker volume rm 2>/dev/null || true
    print_status "Nettoyage complet terminé"
}

# Lancer le mode Bare-Metal avec venv
launch_bare_metal_venv() {
    print_header "🔧 LANCEMENT BARE-METAL AVEC VENV"
    echo
    
    # Créer environnement virtuel si nécessaire
    if [ ! -d "venv" ]; then
        print_step "Création de l'environnement virtuel..."
        python3 -m venv venv
        print_status "Environnement virtuel créé"
    fi
    
    # Activer l'environnement virtuel
    print_step "Activation de l'environnement virtuel..."
    source venv/bin/activate
    print_status "Environnement virtuel activé"
    
    # Installer les dépendances
    print_step "Installation des dépendances..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        print_info "Installation des dépendances de base..."
        pip install fastapi uvicorn sqlalchemy psycopg2-binary celery redis aiohttp \
                   numpy pandas scipy scikit-learn asyncpg psutil requests
    fi
    
    print_status "Dépendances installées dans l'environnement virtuel"
    
    # Lancer le système
    launch_bare_metal_core
}

# Lancer le mode Bare-Metal direct
launch_bare_metal_direct() {
    print_header "⚡ LANCEMENT BARE-METAL DIRECT"
    echo
    
    # Vérifier les prérequis
    check_bare_metal_prerequisites
    
    # Installer les dépendances
    install_bare_metal_dependencies
    
    # Lancer le système
    launch_bare_metal_core
}

# Vérifier les prérequis bare-metal
check_bare_metal_prerequisites() {
    print_step "Vérification des prérequis bare-metal..."
    
    # Python
    if command -v python3 &> /dev/null; then
        print_status "Python3 trouvé: $(python3 --version)"
    else
        print_error "Python3 non trouvé!"
        exit 1
    fi
    
    # Pip
    if command -v pip3 &> /dev/null; then
        print_status "Pip3 trouvé"
    else
        print_error "Pip3 non trouvé!"
        exit 1
    fi
    
    # PostgreSQL (optionnel)
    if command -v psql &> /dev/null; then
        print_status "PostgreSQL trouvé"
    else
        print_warning "PostgreSQL non trouvé (installation automatique recommandée)"
    fi
    
    # Redis (optionnel)
    if command -v redis-server &> /dev/null; then
        print_status "Redis trouvé"
    else
        print_warning "Redis non trouvé (installation automatique recommandée)"
    fi
}

# Installer les dépendances bare-metal
install_bare_metal_dependencies() {
    print_step "Installation des dépendances bare-metal..."
    
    # Essayer installation avec requirements.txt
    if [ -f "requirements.txt" ]; then
        print_info "Installation via requirements.txt..."
        if pip3 install -r requirements.txt --user 2>/dev/null; then
            print_status "Dépendances installées avec --user"
        else
            print_warning "Échec installation --user, tentative sans..."
            pip3 install -r requirements.txt
        fi
    else
        print_info "Installation manuelle des dépendances..."
        pip3 install --user fastapi uvicorn sqlalchemy psycopg2-binary celery redis aiohttp \
                     numpy pandas scipy scikit-learn asyncpg psutil requests 2>/dev/null || \
        pip3 install fastapi uvicorn sqlalchemy psycopg2-binary celery redis aiohttp \
                     numpy pandas scipy scikit-learn asyncpg psutil requests
    fi
    
    print_status "Dépendances installées"
}

# Core du lancement bare-metal
launch_bare_metal_core() {
    print_step "Configuration des services..."
    
    # Démarrer PostgreSQL
    setup_database_bare_metal
    
    # Démarrer Redis
    setup_redis_bare_metal
    
    # Démarrer le backend
    start_backend_bare_metal
    
    # Démarrer Celery
    start_celery_bare_metal
    
    # Lancer les tests
    run_tests_bare_metal
    
    print_status "🎉 Système bare-metal opérationnel!"
}

# Configuration base de données bare-metal
setup_database_bare_metal() {
    print_step "Configuration PostgreSQL..."
    
    if pgrep -x "postgres" > /dev/null; then
        print_status "PostgreSQL déjà en cours d'exécution"
    else
        print_info "Tentative de démarrage PostgreSQL..."
        
        # Essayer différentes méthodes
        if command -v systemctl &> /dev/null; then
            sudo systemctl start postgresql 2>/dev/null && print_status "PostgreSQL démarré" || \
            print_warning "Impossible de démarrer PostgreSQL automatiquement"
        elif command -v service &> /dev/null; then
            sudo service postgresql start 2>/dev/null && print_status "PostgreSQL démarré" || \
            print_warning "PostgreSQL doit être démarré manuellement"
        else
            print_warning "PostgreSQL doit être démarré manuellement"
        fi
    fi
}

# Configuration Redis bare-metal
setup_redis_bare_metal() {
    print_step "Configuration Redis..."
    
    if pgrep -x "redis-server" > /dev/null; then
        print_status "Redis déjà en cours d'exécution"
    else
        print_info "Tentative de démarrage Redis..."
        
        if command -v redis-server &> /dev/null; then
            redis-server --daemonize yes 2>/dev/null && print_status "Redis démarré" || \
            print_warning "Impossible de démarrer Redis automatiquement"
        else
            print_warning "Redis non installé"
        fi
    fi
}

# Démarrage backend bare-metal
start_backend_bare_metal() {
    print_step "Démarrage du backend..."
    
    cd backend
    
    export DATABASE_URL="postgresql://trading_user:trading_pass@localhost/trading_orchestrator"
    export REDIS_URL="redis://localhost:6379"
    export DEBUG=true
    
    print_info "Démarrage d'Uvicorn..."
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid
    
    sleep 5
    
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend démarré (PID: $BACKEND_PID)"
    else
        print_error "Échec démarrage backend"
    fi
    
    cd ..
}

# Démarrage Celery bare-metal
start_celery_bare_metal() {
    print_step "Démarrage Celery..."
    
    cd backend
    
    nohup celery -A app.core.celery worker --loglevel=info > ../celery.log 2>&1 &
    CELERY_PID=$!
    echo $CELERY_PID > ../celery.pid
    
    nohup celery -A app.core.celery beat --loglevel=info > ../celery-beat.log 2>&1 &
    CELERY_BEAT_PID=$!
    echo $CELERY_BEAT_PID > ../celery-beat.pid
    
    sleep 3
    print_status "Celery démarré (Worker: $CELERY_PID, Beat: $CELERY_BEAT_PID)"
    
    cd ..
}

# Tests bare-metal
run_tests_bare_metal() {
    print_step "Lancement des tests..."
    
    sleep 10
    python3 test_advanced_ai_complete.py
    
    if [ $? -eq 0 ]; then
        print_status "Tests réussis!"
    else
        print_warning "Certains tests ont échoué"
    fi
}

# Analyse détaillée du système
detailed_analysis() {
    print_header "🔍 ANALYSE DÉTAILLÉE DU SYSTÈME"
    echo "=================================="
    echo
    
    print_step "Informations système..."
    echo "OS: $(uname -s) $(uname -r)"
    echo "Architecture: $(uname -m)"
    echo "Distribution: $(lsb_release -d 2>/dev/null | cut -f2 || echo "Non détectée")"
    echo
    
    print_step "Outils disponibles..."
    command -v docker && echo "Docker: $(docker --version)" || echo "Docker: Non installé"
    command -v docker-compose && echo "Docker Compose: $(docker-compose --version)" || echo "Docker Compose: Non installé"
    command -v python3 && echo "Python3: $(python3 --version)" || echo "Python3: Non installé"
    command -v pip3 && echo "Pip3: $(pip3 --version)" || echo "Pip3: Non installé"
    command -v psql && echo "PostgreSQL: $(psql --version)" || echo "PostgreSQL: Non installé"
    command -v redis-server && echo "Redis: $(redis-server --version)" || echo "Redis: Non installé"
    echo
    
    print_step "Recommandations..."
    
    if $DOCKER_AVAILABLE && $DOCKER_COMPOSE_AVAILABLE; then
        echo "🎯 RECOMMANDATION: Utiliser Docker"
        echo "   ✅ Installation la plus simple et fiable"
        echo "   ✅ Isolation complète des services"
        echo "   ✅ Pas de conflits de dépendances"
        echo "   ✅ Production-ready"
    elif $PYTHON_MANAGED; then
        echo "🎯 RECOMMANDATION: Installer Docker ou utiliser venv"
        echo "   ⚠️  Python géré externalement (Ubuntu 23+)"
        echo "   💡 Solution 1: Installer Docker"
        echo "   💡 Solution 2: Utiliser environnement virtuel Python"
    else
        echo "🎯 RECOMMANDATION: Installation bare-metal possible"
        echo "   ✅ Python installable directement"
        echo "   ⚠️  Nécessite installation manuelle PostgreSQL/Redis"
    fi
    
    echo
    read -p "Appuyez sur Entrée pour revenir au menu..."
}

# Menu principal
main_menu() {
    while true; do
        detect_environment
        show_mode_menu
        
        read -p "Choix (0-4): " choice
        
        case $choice in
            1)
                if $DOCKER_AVAILABLE && $DOCKER_COMPOSE_AVAILABLE; then
                    launch_docker_mode
                else
                    print_error "Docker non disponible!"
                    read -p "Appuyez sur Entrée pour continuer..."
                fi
                ;;
            2)
                if $BARE_METAL_POSSIBLE; then
                    launch_bare_metal_direct
                else
                    print_error "Installation bare-metal problématique!"
                    print_info "Utilise l'option 3 (avec venv) à la place."
                    read -p "Appuyez sur Entrée pour continuer..."
                fi
                ;;
            3)
                launch_bare_metal_venv
                ;;
            4)
                detailed_analysis
                ;;
            0)
                print_info "Au revoir! 👋"
                exit 0
                ;;
            *)
                print_error "Option invalide"
                read -p "Appuyez sur Entrée pour continuer..."
                ;;
        esac
        
        echo
    done
}

# Point d'entrée avec options
case "${1:-menu}" in
    "--docker"|"docker")
        print_banner
        launch_docker_mode "${@:2}"
        ;;
    "--bare-metal"|"bare-metal")
        print_banner
        launch_bare_metal_direct
        ;;
    "--venv"|"venv")
        print_banner
        launch_bare_metal_venv
        ;;
    "--auto"|"auto")
        print_banner
        detect_environment
        if [ "$RECOMMENDED_MODE" = "docker" ]; then
            launch_docker_mode
        elif [ "$RECOMMENDED_MODE" = "bare-metal" ]; then
            launch_bare_metal_direct
        elif [ "$RECOMMENDED_MODE" = "bare-metal-venv" ]; then
            launch_bare_metal_venv
        else
            print_error "Aucun mode automatique déterminé"
            main_menu
        fi
        ;;
    "--help"|"help")
        echo "Usage: $0 [docker|bare-metal|venv|auto|help]"
        echo
        echo "Options:"
        echo "  docker      - Forcer le mode Docker"
        echo "  bare-metal  - Forcer l'installation bare-metal"
        echo "  venv        - Forcer l'utilisation d'un environnement virtuel"
        echo "  auto        - Détection automatique du meilleur mode"
        echo "  help        - Afficher cette aide"
        echo "  (aucun)     - Menu interactif avec détection"
        ;;
    *)
        print_banner
        main_menu
        ;;
esac 