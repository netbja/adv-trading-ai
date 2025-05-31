#!/bin/bash

# 🐳 LANCEUR DOCKER - SYSTÈME IA TRADING AVANCÉ
# ==============================================

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

# Banner
print_banner() {
    echo -e "${PURPLE}"
    cat << "EOF"
    ███████╗██╗ █████╗     ████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
    ██╔══██║██║██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
    ███████║██║███████║       ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗
    ██╔══██║██║██╔══██║       ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║
    ██║  ██║██║██║  ██║       ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                                    
                    🐳 DOCKER ORCHESTRATOR v2.0 - IA AVANCÉE
EOF
    echo -e "${NC}"
}

# Vérifier Docker
check_docker() {
    print_step "Vérification Docker..."
    
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
}

# Nettoyer les conteneurs existants
cleanup_containers() {
    print_step "Nettoyage des conteneurs existants..."
    
    # Arrêter et supprimer tous les conteneurs du projet
    $COMPOSE_CMD down --remove-orphans 2>/dev/null || true
    
    # Supprimer les conteneurs orphelins spécifiquement
    docker ps -a --filter "name=trading_" --format "{{.Names}}" | xargs docker rm -f 2>/dev/null || true
    
    print_status "Nettoyage terminé"
}

# Construire les images
build_images() {
    print_step "Construction des images Docker..."
    
    print_info "Construction de l'image backend..."
    $COMPOSE_CMD build backend
    
    print_info "Construction de l'image de tests..."
    $COMPOSE_CMD build ai_tests
    
    print_status "Images construites avec succès"
}

# Démarrer les services principaux
start_core_services() {
    print_step "Démarrage des services principaux..."
    
    print_info "Démarrage de la base de données et Redis..."
    $COMPOSE_CMD up -d database redis
    
    # Attendre que la DB soit prête
    print_info "Attente de la base de données..."
    for i in {1..30}; do
        if $COMPOSE_CMD exec -T database pg_isready -U trading_user -d trading_orchestrator 2>/dev/null; then
            print_status "Base de données prête"
            break
        fi
        sleep 2
        echo -n "."
    done
    echo
    
    print_info "Démarrage du backend..."
    $COMPOSE_CMD up -d backend
    
    # Attendre que l'API soit prête
    print_info "Attente de l'API backend..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_status "API backend prête"
            break
        fi
        sleep 2
        echo -n "."
    done
    echo
    
    print_info "Démarrage de Celery..."
    $COMPOSE_CMD up -d celery_worker celery_beat
    
    print_status "Services principaux démarrés"
}

# Lancer les tests IA
run_ai_tests() {
    print_step "Lancement des tests IA avancée..."
    
    print_info "Attente de stabilisation du système..."
    sleep 10
    
    print_info "Exécution des tests..."
    if $COMPOSE_CMD run --rm ai_tests; then
        print_status "Tests IA réussis! 🎉"
    else
        print_warning "Certains tests ont échoué, vérifie les logs"
    fi
}

# Afficher les logs
show_logs() {
    print_step "Affichage des logs..."
    
    case $1 in
        "backend")
            $COMPOSE_CMD logs -f backend
            ;;
        "celery")
            $COMPOSE_CMD logs -f celery_worker celery_beat
            ;;
        "database")
            $COMPOSE_CMD logs -f database
            ;;
        "all"|*)
            $COMPOSE_CMD logs -f
            ;;
    esac
}

# Monitoring des services
monitor_services() {
    print_step "Monitoring des services..."
    
    while true; do
        clear
        echo -e "${CYAN}📊 MONITORING SYSTÈME IA DOCKER${NC}"
        echo "=================================="
        echo "⏰ $(date)"
        echo
        
        # Status des conteneurs
        echo -e "${BLUE}🐳 STATUS CONTENEURS${NC}"
        $COMPOSE_CMD ps --format "table"
        echo
        
        # Health checks
        echo -e "${BLUE}💚 HEALTH CHECKS${NC}"
        
        # API Backend
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ API Backend: OPÉRATIONNEL${NC}"
        else
            echo -e "${RED}❌ API Backend: HORS SERVICE${NC}"
        fi
        
        # Database
        if $COMPOSE_CMD exec -T database pg_isready -U trading_user -d trading_orchestrator 2>/dev/null; then
            echo -e "${GREEN}✅ Database: CONNECTÉE${NC}"
        else
            echo -e "${RED}❌ Database: DÉCONNECTÉE${NC}"
        fi
        
        # Redis
        if $COMPOSE_CMD exec -T redis redis-cli ping 2>/dev/null | grep -q PONG; then
            echo -e "${GREEN}✅ Redis: ACTIF${NC}"
        else
            echo -e "${RED}❌ Redis: INACTIF${NC}"
        fi
        
        echo
        echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter le monitoring${NC}"
        sleep 5
    done
}

# Arrêter tous les services
stop_services() {
    print_step "Arrêt de tous les services..."
    
    $COMPOSE_CMD down --remove-orphans
    
    print_status "Tous les services arrêtés"
}

# Nettoyer complètement
full_cleanup() {
    print_step "Nettoyage complet du système..."
    
    # Arrêter tous les services
    $COMPOSE_CMD down --volumes --remove-orphans
    
    # Supprimer les images
    docker images --filter "reference=*trading*" -q | xargs docker rmi -f 2>/dev/null || true
    
    # Supprimer les volumes
    docker volume ls --filter "name=trading_" -q | xargs docker volume rm 2>/dev/null || true
    
    # Supprimer le réseau
    docker network rm trading_ai_network 2>/dev/null || true
    
    print_status "Nettoyage complet terminé"
}

# Menu principal avec navigation améliorée
show_main_menu() {
    echo -e "${BLUE}🎯 MENU PRINCIPAL - SYSTÈME IA DOCKER${NC}"
    echo "=================================="
    echo
    echo "1. 🚀 Déploiement complet"
    echo "2. 🔧 Gestion des services"
    echo "3. 📊 Monitoring et statuts"
    echo "4. 🧪 Tests et validation"
    echo "5. 🗃️  Gestion des données"
    echo "6. 🔍 Logs et diagnostics"
    echo "7. 🛠️  Configuration avancée"
    echo "8. 📚 Documentation"
    echo "9. 🧹 Nettoyage du système"
    echo
    echo "🌐 Options Frontend:"
    echo "f. 🎨 Démarrer avec interface web (port 80)"
    echo "m. 📈 Démarrer avec monitoring (port 3000/9090)"
    echo
    echo "0. ❌ Quitter"
    echo -e "${YELLOW}💡 Astuce: Appuyez sur 'q' ou ESC pour quitter rapidement${NC}"
    echo
}

# Fonction pour lire l'input avec gestion ESC
read_user_input() {
    local prompt="$1"
    local input
    
    # Configuration pour capturer les touches spéciales
    while true; do
        printf "$prompt"
        
        # Lecture caractère par caractère pour capturer ESC
        read -n1 -s input
        
        case "$input" in
            $'\e') # ESC
                echo
                print_info "Au revoir! 👋"
                exit 0
                ;;
            'q'|'Q') # Touche q pour quitter
                echo
                print_info "Au revoir! 👋"
                exit 0
                ;;
            [0-9]) # Chiffres valides
                echo "$input"
                return 0
                ;;
            '') # Entrée
                echo
                return 0
                ;;
            *) # Autres touches, afficher et continuer
                echo "$input"
                return 0
                ;;
        esac
    done
}

# Menu logs
show_logs_menu() {
    echo
    echo "📝 Choisir les logs à afficher:"
    echo "1. Backend"
    echo "2. Celery" 
    echo "3. Database"
    echo "4. Tous"
    read -p "Choix (1-4): " log_choice
    
    case $log_choice in
        1) show_logs "backend" ;;
        2) show_logs "celery" ;;
        3) show_logs "database" ;;
        4) show_logs "all" ;;
        *) show_logs "all" ;;
    esac
}

# Démarrage avec frontend
start_with_frontend() {
    print_step "Démarrage avec interface web..."
    
    start_core_services
    
    print_info "Démarrage de l'interface web..."
    $COMPOSE_CMD --profile frontend up -d nginx
    
    print_status "Interface web démarrée"
    print_info "🌐 Interface: http://localhost"
    print_info "📚 API Docs: http://localhost/docs"
    print_info "🔍 Health: http://localhost/health"
}

# Fonction principale
main() {
    print_banner
    check_docker
    
    while true; do
        show_main_menu
        
        choice=$(read_user_input "Choix (0-9): ")
        
        case $choice in
            1)
                print_header "🚀 LANCEMENT COMPLET DU SYSTÈME IA"
                cleanup_containers
                build_images
                start_core_services
                run_ai_tests
                print_status "🎉 Système complètement opérationnel!"
                print_info "API: http://localhost:8000"
                print_info "Health: http://localhost:8000/health"
                print_info "Docs: http://localhost:8000/docs"
                ;;
            2)
                cleanup_containers
                build_images
                ;;
            3)
                start_core_services
                ;;
            4)
                run_ai_tests
                ;;
            5)
                monitor_services
                ;;
            6)
                show_logs_menu
                ;;
            7)
                stop_services
                ;;
            8)
                full_cleanup
                ;;
            9)
                print_info "Au revoir! 👋"
                exit 0
                ;;
            f)
                start_with_frontend
                ;;
            m)
                start_with_monitoring
                monitor_services
                ;;
            *)
                print_error "Option invalide"
                ;;
        esac
        
        echo
        read -p "Appuyez sur Entrée pour continuer..."
    done
}

# Point d'entrée avec options
case "${1:-menu}" in
    "--auto"|"auto")
        print_banner
        check_docker
        print_header "🚀 MODE AUTOMATIQUE - LANCEMENT COMPLET"
        cleanup_containers
        build_images
        start_core_services
        run_ai_tests
        print_status "🎉 Déploiement automatique terminé!"
        ;;
    "--monitoring"|"monitoring")
        print_banner
        check_docker
        cleanup_containers
        build_images
        start_with_monitoring
        monitor_services
        ;;
    "--cleanup"|"cleanup")
        check_docker
        full_cleanup
        ;;
    "--help"|"help")
        echo "Usage: $0 [auto|monitoring|cleanup|help]"
        echo
        echo "Options:"
        echo "  auto        - Lancement automatique complet"
        echo "  monitoring  - Lancement avec monitoring avancé"
        echo "  cleanup     - Nettoyage complet du système"
        echo "  help        - Afficher cette aide"
        echo "  (aucun)     - Menu interactif"
        ;;
    *)
        main
        ;;
esac 