#!/bin/bash

# 🚀 LANCEUR SYSTÈME IA AVANCÉE COMPLET
# ====================================

echo "🚀 LANCEMENT DU SYSTÈME IA TRADING AVANCÉ"
echo "=========================================="

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

# Vérifier les prérequis
check_prerequisites() {
    print_step "Vérification des prérequis..."
    
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
    
    # Docker (optionnel)
    if command -v docker &> /dev/null; then
        print_status "Docker trouvé: $(docker --version | cut -d' ' -f3 | cut -d',' -f1)"
    else
        print_warning "Docker non trouvé (optionnel pour certaines fonctionnalités)"
    fi
}

# Installer les dépendances
install_dependencies() {
    print_step "Installation des dépendances..."
    
    # Dépendances backend
    print_info "Installation des packages Python..."
    pip3 install -r requirements.txt 2>/dev/null || {
        print_info "Fichier requirements.txt non trouvé, installation manuelle..."
        pip3 install fastapi uvicorn sqlalchemy psycopg2-binary celery redis aiohttp \
                     numpy pandas scipy scikit-learn asyncpg psutil docker requests
    }
    
    # Dépendances spécifiques pour l'IA avancée
    print_info "Installation des packages d'IA avancée..."
    pip3 install numpy pandas scipy scikit-learn matplotlib seaborn plotly dash
    
    print_status "Dépendances installées"
}

# Démarrer la base de données
setup_database() {
    print_step "Configuration de la base de données..."
    
    # Vérifier si PostgreSQL est en cours d'exécution
    if pgrep -x "postgres" > /dev/null; then
        print_status "PostgreSQL est déjà en cours d'exécution"
    else
        print_info "Tentative de démarrage de PostgreSQL..."
        
        # Essayer différentes méthodes selon le système
        if command -v systemctl &> /dev/null; then
            sudo systemctl start postgresql 2>/dev/null && print_status "PostgreSQL démarré via systemctl" || \
            print_warning "Impossible de démarrer PostgreSQL automatiquement"
        elif command -v service &> /dev/null; then
            sudo service postgresql start 2>/dev/null && print_status "PostgreSQL démarré via service" || \
            print_warning "Impossible de démarrer PostgreSQL automatiquement"
        else
            print_warning "PostgreSQL doit être démarré manuellement"
        fi
    fi
    
    # Créer la base de données si elle n'existe pas
    print_info "Vérification de la base de données..."
    export DATABASE_URL="postgresql://trading_user:trading_pass@localhost/trading_orchestrator"
    
    # Initialiser les tables (si le script existe)
    if [ -f "backend/init_db.py" ]; then
        cd backend && python3 init_db.py && cd ..
        print_status "Base de données initialisée"
    else
        print_info "Script d'initialisation DB non trouvé, création automatique à venir"
    fi
}

# Démarrer Redis (pour Celery)
setup_redis() {
    print_step "Configuration de Redis..."
    
    if pgrep -x "redis-server" > /dev/null; then
        print_status "Redis est déjà en cours d'exécution"
    else
        print_info "Tentative de démarrage de Redis..."
        
        if command -v redis-server &> /dev/null; then
            redis-server --daemonize yes 2>/dev/null && print_status "Redis démarré" || \
            print_warning "Impossible de démarrer Redis automatiquement"
        else
            print_warning "Redis non installé - certaines fonctionnalités peuvent être limitées"
        fi
    fi
}

# Démarrer le backend FastAPI
start_backend() {
    print_step "Démarrage du backend FastAPI..."
    
    cd backend
    
    # Exporter les variables d'environnement
    export DATABASE_URL="postgresql://trading_user:trading_pass@localhost/trading_orchestrator"
    export REDIS_URL="redis://localhost:6379"
    export DEBUG=true
    
    print_info "Variables d'environnement configurées"
    print_info "Démarrage d'Uvicorn sur le port 8000..."
    
    # Démarrer en arrière-plan
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    echo $BACKEND_PID > ../backend.pid
    
    # Attendre que le serveur soit prêt
    print_info "Attente du démarrage du serveur..."
    sleep 5
    
    # Vérifier si le serveur répond
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend FastAPI démarré avec succès (PID: $BACKEND_PID)"
    else
        print_error "Échec du démarrage du backend"
        cat ../backend.log
        exit 1
    fi
    
    cd ..
}

# Démarrer les workers Celery
start_celery() {
    print_step "Démarrage des workers Celery..."
    
    cd backend
    
    # Démarrer le worker Celery
    print_info "Démarrage du worker Celery..."
    nohup celery -A app.core.celery worker --loglevel=info > ../celery.log 2>&1 &
    CELERY_PID=$!
    echo $CELERY_PID > ../celery.pid
    
    # Démarrer le scheduler Celery Beat
    print_info "Démarrage du scheduler Celery Beat..."
    nohup celery -A app.core.celery beat --loglevel=info > ../celery-beat.log 2>&1 &
    CELERY_BEAT_PID=$!
    echo $CELERY_BEAT_PID > ../celery-beat.pid
    
    sleep 3
    print_status "Workers Celery démarrés (Worker PID: $CELERY_PID, Beat PID: $CELERY_BEAT_PID)"
    
    cd ..
}

# Lancer les tests complets
run_advanced_tests() {
    print_step "Lancement des tests IA avancée..."
    
    print_info "Attente de stabilisation du système..."
    sleep 10
    
    print_info "Démarrage des tests grandeur nature..."
    python3 test_advanced_ai_complete.py
    
    if [ $? -eq 0 ]; then
        print_status "Tests réussis! Système prêt pour la production!"
    else
        print_warning "Certains tests ont échoué, vérifiez les logs"
    fi
}

# Fonction de nettoyage
cleanup() {
    print_step "Nettoyage en cours..."
    
    # Arrêter les processus
    if [ -f backend.pid ]; then
        BACKEND_PID=$(cat backend.pid)
        kill $BACKEND_PID 2>/dev/null && print_info "Backend arrêté"
        rm backend.pid
    fi
    
    if [ -f celery.pid ]; then
        CELERY_PID=$(cat celery.pid)
        kill $CELERY_PID 2>/dev/null && print_info "Celery worker arrêté"
        rm celery.pid
    fi
    
    if [ -f celery-beat.pid ]; then
        CELERY_BEAT_PID=$(cat celery-beat.pid)
        kill $CELERY_BEAT_PID 2>/dev/null && print_info "Celery beat arrêté"
        rm celery-beat.pid
    fi
    
    print_status "Nettoyage terminé"
}

# Trap pour nettoyage automatique
trap cleanup EXIT INT TERM

# Menu principal
show_menu() {
    echo
    echo -e "${BLUE}🎯 MENU PRINCIPAL${NC}"
    echo "================="
    echo "1. 🚀 Lancement complet (recommandé)"
    echo "2. 🔧 Installation des dépendances seulement"
    echo "3. ⚡ Démarrage backend seulement"
    echo "4. 🧪 Tests IA avancée seulement"
    echo "5. 📊 Monitoring en temps réel"
    echo "6. 🛑 Arrêt de tous les services"
    echo "7. ❌ Quitter"
    echo
    read -p "Choix (1-7): " choice
}

# Monitoring en temps réel
start_monitoring() {
    print_step "Démarrage du monitoring en temps réel..."
    
    while true; do
        clear
        echo -e "${CYAN}📊 MONITORING SYSTÈME IA AVANCÉE${NC}"
        echo "=================================="
        echo "⏰ $(date)"
        echo
        
        # Status API
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ API Backend: ACTIF${NC}"
        else
            echo -e "${RED}❌ API Backend: INACTIF${NC}"
        fi
        
        # Status processus
        if [ -f backend.pid ] && kill -0 $(cat backend.pid) 2>/dev/null; then
            echo -e "${GREEN}✅ Backend PID: $(cat backend.pid)${NC}"
        else
            echo -e "${RED}❌ Backend: NON DÉMARRÉ${NC}"
        fi
        
        if [ -f celery.pid ] && kill -0 $(cat celery.pid) 2>/dev/null; then
            echo -e "${GREEN}✅ Celery Worker PID: $(cat celery.pid)${NC}"
        else
            echo -e "${YELLOW}⚠️  Celery Worker: NON DÉMARRÉ${NC}"
        fi
        
        # Métriques système
        echo
        echo -e "${PURPLE}📈 MÉTRIQUES SYSTÈME${NC}"
        echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
        echo "RAM: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
        
        # Logs récents
        echo
        echo -e "${BLUE}📝 LOGS RÉCENTS (dernières 3 lignes)${NC}"
        if [ -f backend.log ]; then
            tail -n 3 backend.log | sed 's/^/   /'
        fi
        
        echo
        echo "Appuyez sur Ctrl+C pour arrêter le monitoring"
        sleep 5
    done
}

# Exécution du menu
main() {
    echo -e "${PURPLE}"
    cat << "EOF"
    ███╗   ███╗██████╗ ██╗  ██╗    ██████╗ ██████╗  ██████╗ 
    ████╗ ████║██╔══██╗██║  ██║    ██╔══██╗██╔══██╗██╔═══██╗
    ██╔████╔██║██║  ██║███████║    ██████╔╝██████╔╝██║   ██║
    ██║╚██╔╝██║██║  ██║██╔══██║    ██╔═══╝ ██╔══██╗██║   ██║
    ██║ ╚═╝ ██║██████╔╝██║  ██║    ██║     ██║  ██║╚██████╔╝
    ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                                                              
           AI TRADING ORCHESTRATOR v2.0 - SYSTÈME COMPLET
EOF
    echo -e "${NC}"
    
    while true; do
        show_menu
        
        case $choice in
            1)
                print_step "🚀 LANCEMENT COMPLET DU SYSTÈME"
                check_prerequisites
                install_dependencies
                setup_database
                setup_redis
                start_backend
                start_celery
                run_advanced_tests
                print_status "🎉 Système complètement opérationnel!"
                ;;
            2)
                check_prerequisites
                install_dependencies
                ;;
            3)
                setup_database
                setup_redis
                start_backend
                start_celery
                ;;
            4)
                run_advanced_tests
                ;;
            5)
                start_monitoring
                ;;
            6)
                cleanup
                print_status "Tous les services arrêtés"
                ;;
            7)
                print_info "Au revoir! 👋"
                exit 0
                ;;
            *)
                print_error "Option invalide"
                ;;
        esac
        
        echo
        read -p "Appuyez sur Entrée pour continuer..."
    done
}

# Point d'entrée
if [ "$1" = "--auto" ]; then
    print_step "🚀 MODE AUTOMATIQUE - LANCEMENT COMPLET"
    check_prerequisites
    install_dependencies
    setup_database
    setup_redis
    start_backend
    start_celery
    run_advanced_tests
else
    main
fi 