#!/bin/bash
# 🛡️ SCRIPT DE BACKUP AUTOMATIQUE - TRADING AI SYSTEM
# Sauvegarde de tous les volumes Docker et configurations

set -e

# Configuration
BACKUP_DIR="/backup/trading-ai"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="trading_ai_backup_${DATE}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}"
    echo "=================================="
    echo "$1"
    echo "=================================="
    echo -e "${NC}"
}

# Fonction principale de backup
backup_trading_system() {
    print_header "🛡️ BACKUP TRADING AI SYSTEM"
    
    # Créer le répertoire de backup
    mkdir -p "$BACKUP_PATH"
    
    print_info "Backup vers: $BACKUP_PATH"
    
    # 1. Backup des volumes Docker
    backup_docker_volumes
    
    # 2. Backup de la base de données
    backup_database
    
    # 3. Backup des configurations
    backup_configurations
    
    # 4. Backup du code source
    backup_source_code
    
    # 5. Créer l'archive finale
    create_final_archive
    
    # 6. Nettoyer les anciens backups
    cleanup_old_backups
    
    print_success "🎉 Backup terminé avec succès!"
    print_info "📁 Archive: ${BACKUP_PATH}.tar.gz"
}

# Backup des volumes Docker
backup_docker_volumes() {
    print_info "Sauvegarde des volumes Docker..."
    
    # Liste des volumes critiques
    VOLUMES=(
        "trading_postgres_data"
        "trading_redis_data"
        "trading_backend_logs"
        "trading_celery_logs"
        "trading_frontend_ssl"
    )
    
    for volume in "${VOLUMES[@]}"; do
        if docker volume inspect "$volume" > /dev/null 2>&1; then
            print_info "Backup volume: $volume"
            docker run --rm \
                -v "$volume":/source \
                -v "$BACKUP_PATH/volumes":/backup \
                alpine:latest \
                tar czf "/backup/${volume}.tar.gz" -C /source .
            print_success "Volume $volume sauvegardé"
        else
            print_warning "Volume $volume non trouvé"
        fi
    done
}

# Backup de la base de données (dump SQL)
backup_database() {
    print_info "Sauvegarde de la base de données PostgreSQL..."
    
    # Vérifier si le conteneur DB est actif
    if docker ps | grep -q "trading_db"; then
        docker exec trading_db pg_dump \
            -U trading_user \
            -d trading_orchestrator \
            --verbose \
            --no-owner \
            --no-privileges \
            > "$BACKUP_PATH/database_dump.sql"
        
        # Compression du dump
        gzip "$BACKUP_PATH/database_dump.sql"
        print_success "Base de données sauvegardée"
    else
        print_warning "Conteneur DB non actif - dump ignoré"
    fi
}

# Backup des configurations
backup_configurations() {
    print_info "Sauvegarde des configurations..."
    
    CONFIG_DIR="$BACKUP_PATH/configs"
    mkdir -p "$CONFIG_DIR"
    
    # Fichiers de configuration critiques
    CONFIG_FILES=(
        "docker-compose.yml"
        "docker-compose-pro.yml"
        ".env"
        "CONFIG_TEMPLATE.env"
        "backend/Dockerfile"
        "frontend/Dockerfile.prod"
        "nginx/nginx.conf"
        "monitoring/prometheus.yml"
    )
    
    for config in "${CONFIG_FILES[@]}"; do
        if [ -f "$config" ]; then
            cp "$config" "$CONFIG_DIR/"
            print_success "Config $config sauvegardée"
        else
            print_warning "Config $config non trouvée"
        fi
    done
}

# Backup du code source (sans node_modules, etc.)
backup_source_code() {
    print_info "Sauvegarde du code source..."
    
    # Créer archive du code source (en excluant les gros répertoires)
    tar czf "$BACKUP_PATH/source_code.tar.gz" \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='venv' \
        --exclude='logs' \
        --exclude='*.log' \
        backend/ frontend/ scripts/ docs/ \
        *.py *.sh *.md 2>/dev/null || true
    
    print_success "Code source sauvegardé"
}

# Créer l'archive finale
create_final_archive() {
    print_info "Création de l'archive finale..."
    
    cd "$BACKUP_DIR"
    tar czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME/"
    
    # Supprimer le répertoire temporaire
    rm -rf "$BACKUP_NAME"
    
    # Taille de l'archive
    ARCHIVE_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
    print_success "Archive créée: ${BACKUP_NAME}.tar.gz (${ARCHIVE_SIZE})"
}

# Nettoyer les anciens backups (garder 7 derniers)
cleanup_old_backups() {
    print_info "Nettoyage des anciens backups..."
    
    cd "$BACKUP_DIR"
    
    # Garder seulement les 7 derniers backups
    ls -t trading_ai_backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm -f
    
    REMAINING=$(ls trading_ai_backup_*.tar.gz 2>/dev/null | wc -l)
    print_success "Nettoyage terminé ($REMAINING backups conservés)"
}

# Fonction de restauration
restore_from_backup() {
    print_header "🔄 RESTAURATION DEPUIS BACKUP"
    
    if [ -z "$1" ]; then
        print_error "Usage: $0 restore <backup_file.tar.gz>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Fichier de backup non trouvé: $BACKUP_FILE"
        exit 1
    fi
    
    print_warning "⚠️  ATTENTION: Cette opération va écraser les données actuelles!"
    read -p "Continuer? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Restauration annulée"
        exit 0
    fi
    
    # Arrêter les services
    print_info "Arrêt des services..."
    docker-compose down
    
    # Extraire l'archive
    TEMP_DIR="/tmp/trading_restore_$$"
    mkdir -p "$TEMP_DIR"
    tar xzf "$BACKUP_FILE" -C "$TEMP_DIR"
    
    # Restaurer les volumes
    print_info "Restauration des volumes..."
    for volume_backup in "$TEMP_DIR"/*/volumes/*.tar.gz; do
        if [ -f "$volume_backup" ]; then
            volume_name=$(basename "$volume_backup" .tar.gz)
            print_info "Restauration volume: $volume_name"
            
            # Supprimer l'ancien volume et en créer un nouveau
            docker volume rm "$volume_name" 2>/dev/null || true
            docker volume create "$volume_name"
            
            # Restaurer les données
            docker run --rm \
                -v "$volume_name":/target \
                -v "$volume_backup":/backup.tar.gz \
                alpine:latest \
                sh -c "cd /target && tar xzf /backup.tar.gz"
            
            print_success "Volume $volume_name restauré"
        fi
    done
    
    # Restaurer la base de données
    if [ -f "$TEMP_DIR"/*/database_dump.sql.gz ]; then
        print_info "Restauration de la base de données..."
        
        # Redémarrer seulement la DB
        docker-compose up -d database
        sleep 10
        
        # Restaurer le dump
        gunzip -c "$TEMP_DIR"/*/database_dump.sql.gz | \
        docker exec -i trading_db psql -U trading_user -d trading_orchestrator
        
        print_success "Base de données restaurée"
    fi
    
    # Nettoyer
    rm -rf "$TEMP_DIR"
    
    print_success "🎉 Restauration terminée!"
    print_info "Vous pouvez maintenant redémarrer les services avec:"
    print_info "docker-compose up -d"
}

# Vérifier l'action demandée
case "${1:-backup}" in
    "backup")
        backup_trading_system
        ;;
    "restore")
        restore_from_backup "$2"
        ;;
    *)
        echo "Usage: $0 [backup|restore] [backup_file.tar.gz]"
        echo ""
        echo "Exemples:"
        echo "  $0 backup                          # Créer un backup"
        echo "  $0 restore backup_20240131.tar.gz  # Restaurer depuis un backup"
        exit 1
        ;;
esac
