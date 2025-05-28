#!/bin/bash
# 🚀 SETUP TRADING-AI - SCRIPT IDEMPOTENT
# Ce script peut être exécuté plusieurs fois sans problème

set -euo pipefail  # Arrêt en cas d'erreur

# ===== CONFIGURATION =====
TRADING_AI_DIR="${TRADING_AI_DIR:-${HOME}/adv-trading-ai}"
BACKUP_EXISTING="${BACKUP_EXISTING:-true}"
FORCE_RECREATE="${FORCE_RECREATE:-false}"
GIT_ONLY="${GIT_ONLY:-auto}"  # auto, true, false

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ===== FONCTIONS UTILITAIRES =====
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour créer un répertoire de façon idempotente
create_dir_safe() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        log_info "Créé: $dir"
    else
        log_info "Existe déjà: $dir"
    fi
}

# Fonction pour créer un fichier de façon idempotente
create_file_safe() {
    local file="$1"
    local content="$2"
    local backup_suffix="$3"
    
    if [[ -f "$file" ]]; then
        if [[ "$FORCE_RECREATE" == "true" ]]; then
            if [[ "$BACKUP_EXISTING" == "true" ]]; then
                cp "$file" "${file}.backup.${backup_suffix}"
                log_warning "Sauvegardé: $file -> ${file}.backup.${backup_suffix}"
            fi
            echo "$content" > "$file"
            log_info "Recréé (forcé): $file"
        else
            log_info "Existe déjà (ignoré): $file"
        fi
    else
        echo "$content" > "$file"
        log_success "Créé: $file"
    fi
}

# ===== VÉRIFICATIONS PRÉALABLES =====
check_dependencies() {
    log_info "Vérification des dépendances..."
    
    # Mode développement (laptop) vs production (serveur)
    local git_only="${GIT_ONLY:-false}"
    local required_deps=("git")
    local optional_deps=("docker" "docker-compose")
    local missing_required=()
    local missing_optional=()
    
    # Vérifier Git (obligatoire)
    for dep in "${required_deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_required+=("$dep")
        fi
    done
    
    # Vérifier Docker (optionnel selon le mode)
    for dep in "${optional_deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_optional+=("$dep")
        fi
    done
    
    # Erreur si Git manquant
    if [[ ${#missing_required[@]} -gt 0 ]]; then
        log_error "Dépendances critiques manquantes: ${missing_required[*]}"
        log_info "Installation: sudo apt update && sudo apt install -y git"
        exit 1
    fi
    
    # Avertissement si Docker manquant
    if [[ ${#missing_optional[@]} -gt 0 ]]; then
        log_warning "Dépendances Docker manquantes: ${missing_optional[*]}"
        log_info "Mode DÉVELOPPEMENT détecté (création structure Git uniquement)"
        log_info "Pour la production, installer: sudo apt install -y docker.io docker-compose"
        export GIT_ONLY=true
    else
        log_success "Mode PRODUCTION détecté (Docker disponible)"
        export GIT_ONLY=false
    fi
    
    log_success "Vérification terminée - Mode: ${GIT_ONLY}"
}

# ===== CRÉATION DE LA STRUCTURE =====
create_project_structure() {
    log_info "Création de la structure du projet dans: $TRADING_AI_DIR"
    
    # Répertoires principaux
    create_dir_safe "$TRADING_AI_DIR"
    
    # Structure de données
    create_dir_safe "$TRADING_AI_DIR/data/postgres"
    create_dir_safe "$TRADING_AI_DIR/data/grafana"
    create_dir_safe "$TRADING_AI_DIR/data/n8n"
    create_dir_safe "$TRADING_AI_DIR/data/prometheus"
    create_dir_safe "$TRADING_AI_DIR/data/loki"
    create_dir_safe "$TRADING_AI_DIR/data/alertmanager"
    create_dir_safe "$TRADING_AI_DIR/data/loki/chunks"
    create_dir_safe "$TRADING_AI_DIR/data/loki/rules"
    create_dir_safe "$TRADING_AI_DIR/data/loki/tsdb-compactor"
    sudo chown -R 472:472 ./data/grafana
    sudo chown -R 65534:65534 ./data/prometheus

    
    # Structure de logs
    create_dir_safe "$TRADING_AI_DIR/logs/postgres"
    create_dir_safe "$TRADING_AI_DIR/logs/grafana"
    create_dir_safe "$TRADING_AI_DIR/logs/n8n"
    create_dir_safe "$TRADING_AI_DIR/logs/nginx"
    
    # Structure de backup
    create_dir_safe "$TRADING_AI_DIR/backup/postgres"
    
    # Structure de configuration
    create_dir_safe "$TRADING_AI_DIR/configs/nginx/frontend"
    create_dir_safe "$TRADING_AI_DIR/configs/grafana/dashboards"
    create_dir_safe "$TRADING_AI_DIR/configs/grafana/provisioning/dashboards"
    create_dir_safe "$TRADING_AI_DIR/configs/grafana/provisioning/datasources"
    create_dir_safe "$TRADING_AI_DIR/configs/prometheus"
    create_dir_safe "$TRADING_AI_DIR/configs/postgres"
    
    # Structure de développement
    create_dir_safe "$TRADING_AI_DIR/scripts"
    create_dir_safe "$TRADING_AI_DIR/n8n-workflows"
    create_dir_safe "$TRADING_AI_DIR/docs"
    log_success "Structure créée avec succès"
}

# ===== CRÉATION DES FICHIERS DE CONFIGURATION =====
create_env_file() {
    local env_content="# ===== TRADING AI CONFIGURATION =====
# Base
COMPOSE_PROJECT_NAME=trading-ai
TZ=Europe/Paris

# Réseaux
NETWORK_SUBNET=172.20.0.0/16

# PostgreSQL
POSTGRES_DB=trading_ai
POSTGRES_USER=trader
POSTGRES_PASSWORD=TradingDB2025!_$(date +%s | tail -c 6)
POSTGRES_PORT=5432

# N8N
N8N_USER=admin
N8N_PASSWORD=TradingN8N2025!_$(date +%s | tail -c 6)
N8N_DB=n8n

# Grafana
GF_ADMIN_PASSWORD=TradingAI2025!_$(date +%s | tail -c 6)
GF_SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo 'fallback-secret-key-$(date +%s)')

# Prometheus
PROMETHEUS_RETENTION=30d

# Backup
BACKUP_RETENTION=7

# APIs Keys (à compléter)
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional: Paths (pour référence, non utilisables dans volumes)
# TRADING_AI_PATH=/opt/trading-ai
# DATA_PATH=\${TRADING_AI_PATH}/data
# LOGS_PATH=\${TRADING_AI_PATH}/logs"

    create_file_safe "$TRADING_AI_DIR/.env" "$env_content" "$(date +%Y%m%d_%H%M%S)"
}

create_gitignore() {
    local gitignore_content="# ===== TRADING AI GITIGNORE =====

# Données sensibles
data/
logs/
backup/
*.log

# Variables d'environnement
.env
.env.local
.env.production

# Docker
.docker/

# Backups
*.backup.*
*.dump
*.sql.gz

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node modules (si API custom)
node_modules/
npm-debug.log*

# Python (si scripts Python)
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# Temporary files
*.tmp
*.temp
*~"

    create_file_safe "$TRADING_AI_DIR/.gitignore" "$gitignore_content" "$(date +%Y%m%d_%H%M%S)"
}

create_docker_compose() {
    local compose_content='# 🐳 DOCKER SETUP COMPLET - TRADING AI STACK
version: '"'"'3.8'"'"'

services:
  # 🌐 NGINX REVERSE PROXY + FRONTEND
  nginx:
    image: nginx:alpine
    container_name: trading_ai_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./configs/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./configs/nginx/frontend:/usr/share/nginx/html:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - grafana
      - n8n
    networks:
      - trading_network
    restart: unless-stopped

  # 📊 GRAFANA
  grafana:
    image: grafana/grafana:latest
    container_name: trading_ai_grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GF_ADMIN_PASSWORD:-TradingAI2025!}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - ./data/grafana:/var/lib/grafana
      - ./logs/grafana:/var/log/grafana
      - ./configs/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./configs/grafana/dashboards:/var/lib/grafana/dashboards:ro
    networks:
      - trading_network
    restart: unless-stopped
    user: "472:472"
    depends_on:
      - postgres

  # 🗃️ POSTGRESQL
  postgres:
    image: postgres:15-alpine
    container_name: trading_ai_postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-trading_ai}
      POSTGRES_USER: ${POSTGRES_USER:-trader}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-TradingDB2025!}
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - ./backup/postgres:/backup
      - ./logs/postgres:/var/log/postgresql
      - ./configs/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - trading_network
    restart: unless-stopped
    ports:
      - "${POSTGRES_PORT:-5432}:5432"

  # 🔧 N8N
  n8n:
    image: n8nio/n8n:latest
    container_name: trading_ai_n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD:-TradingN8N2025!}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${N8N_DB:-n8n}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-trader}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-TradingDB2025!}
    volumes:
      - ./data/n8n:/home/node/.n8n
      - ./logs/n8n:/var/log/n8n
    networks:
      - trading_network
    restart: unless-stopped
    depends_on:
      - postgres
    ports:
      - "5678:5678"

networks:
  trading_network:
    driver: bridge'

    create_file_safe "$TRADING_AI_DIR/docker-compose.yml" "$compose_content" "$(date +%Y%m%d_%H%M%S)"
}

create_nginx_frontend() {
    local index_html_content='<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Trading AI Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: '"'"'Segoe UI'"'"', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; min-height: 100vh; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; }
        .card {
            background: rgba(255, 255, 255, 0.1); padding: 25px; border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2); transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        .btn {
            display: inline-block; padding: 12px 24px; margin: 10px;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white; text-decoration: none; border-radius: 8px;
            transition: all 0.3s ease;
        }
        .btn:hover { background: linear-gradient(45deg, #ee5a24, #ff6b6b); }
        .status { display: flex; justify-content: space-around; margin-bottom: 30px; }
        .status-item { text-align: center; }
        .status-value { font-size: 2rem; font-weight: bold; }
        .status-online { color: #00d4aa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Advanced Trading AI System</h1>
            <p>Dual AI Architecture - Health Monitoring - Auto Learning</p>
        </div>

        <div class="status">
            <div class="status-item">
                <div class="status-value status-online">●</div>
                <div>System</div>
            </div>
            <div class="status-item">
                <div class="status-value">3</div>
                <div>Active Trades</div>
            </div>
            <div class="status-item">
                <div class="status-value">+12.5%</div>
                <div>Daily P&L</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 Grafana Monitoring</h3>
                <p>Analytics, dashboards, performance metrics</p>
                <a href="http://localhost:3000" class="btn" target="_blank">Open Grafana</a>
            </div>
            <div class="card">
                <h3>🔧 N8N Workflows</h3>
                <p>Trading workflows, AI orchestration</p>
                <a href="http://localhost:5678" class="btn" target="_blank">Open N8N</a>
            </div>
            <div class="card">
                <h3>🗃️ PostgreSQL</h3>
                <p>Database management and queries</p>
                <a href="#" class="btn">Database Info</a>
            </div>
        </div>
    </div>
</body>
</html>'

    create_file_safe "$TRADING_AI_DIR/configs/nginx/frontend/index.html" "$index_html_content" "$(date +%Y%m%d_%H%M%S)"
}

create_readme() {
    local readme_content="# 🚀 Advanced Trading AI System

## 📋 Vue d'ensemble

Système de trading automatisé multi-niveaux avec:
- **Meme Scalping** (5min-1h) 
- **Technical Trading** (1h-4h)
- **Health Monitor IA** (30s)
- **Monitoring Grafana** temps réel
- **Multi-chain support**

## 🏗️ Architecture

\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   N8N Workflows │    │   PostgreSQL    │    │     Grafana     │
│   - Meme Scalp  │◄──►│   - Trades      │◄──►│   - Dashboard   │
│   - Technical   │    │   - Portfolio   │    │   - Alerts      │
│   - Health AI   │    │   - Metrics     │    │   - Reports     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
\`\`\`

## 🚀 Démarrage rapide

\`\`\`bash
# 1. Cloner et configurer
git clone <repo>
cd adv-trading-ai

# 2. Configurer les variables
cp .env.example .env
nano .env  # Ajouter vos API keys

# 3. Lancer la stack
docker-compose up -d

# 4. Accès aux services
# N8N: http://localhost:5678
# Grafana: http://localhost:3000
# Frontend: http://localhost
\`\`\`

## 📊 Services

| Service | Port | Description |
|---------|------|-------------|
| N8N | 5678 | Workflows automation |
| Grafana | 3000 | Monitoring dashboards |
| PostgreSQL | 5432 | Base de données |
| Nginx | 80 | Frontend & reverse proxy |

## 📈 Workflows

1. **Meme Scalping**: Scanner Pump.fun + AI Analysis (5-15min)
2. **Technical Trading**: Multi-timeframe analysis (1-4h)
3. **Health Monitor**: API/RPC monitoring + auto-adjustment (30s)

## 🔒 Sécurité

- Authentification sur tous les services
- Sauvegarde automatique PostgreSQL
- Logs centralisés
- Monitoring proactif

---
Créé le $(date +%Y-%m-%d) | Version 2.0"

    create_file_safe "$TRADING_AI_DIR/README.md" "$readme_content" "$(date +%Y%m%d_%H%M%S)"
}

# ===== CRÉATION DE FICHIERS SUPPLÉMENTAIRES =====
create_additional_configs() {
    # PostgreSQL init.sql
    local postgres_init="-- 🗃️ POSTGRESQL INITIALIZATION
-- Schema pour Trading AI System

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";

-- Table des trades
CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_type VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    amount DECIMAL(18,8) NOT NULL,
    price DECIMAL(18,8) NOT NULL,
    status VARCHAR(20) DEFAULT 'OPEN',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des métriques de santé
CREATE TABLE IF NOT EXISTS health_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    latency_ms INTEGER,
    error_message TEXT,
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour performance
CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS idx_trades_created_at ON trades(created_at);
CREATE INDEX IF NOT EXISTS idx_health_checked_at ON health_metrics(checked_at);"

    create_file_safe "$TRADING_AI_DIR/configs/postgres/init.sql" "$postgres_init" "$(date +%Y%m%d_%H%M%S)"

    # Grafana datasources
    local grafana_datasources="apiVersion: 1

datasources:
  - name: PostgreSQL
    type: postgres
    access: proxy
    url: postgres:5432
    database: \${POSTGRES_DB:-trading_ai}
    user: \${POSTGRES_USER:-trader}
    secureJsonData:
      password: \${POSTGRES_PASSWORD:-TradingDB2025!}
    jsonData:
      sslmode: disable
      postgresVersion: 1500
      timescaledb: false"

    create_file_safe "$TRADING_AI_DIR/configs/grafana/provisioning/datasources/datasources.yml" "$grafana_datasources" "$(date +%Y%m%d_%H%M%S)"

    # Grafana dashboards provisioning
    local grafana_dashboards="apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards"

    create_file_safe "$TRADING_AI_DIR/configs/grafana/provisioning/dashboards/dashboards.yml" "$grafana_dashboards" "$(date +%Y%m%d_%H%M%S)"
}

# ===== INITIALISATION GIT =====
init_git_repo() {
    log_info "Initialisation du repository Git..."
    
    cd "$TRADING_AI_DIR"
    
    if [[ ! -d ".git" ]]; then
        git init
        log_success "Repository Git initialisé"
    else
        log_info "Repository Git existe déjà"
    fi
    
    # Ajouter les fichiers de base
    if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
        git add .gitignore README.md docker-compose.yml configs/ n8n-workflows/ scripts/ 2>/dev/null || true
        if git diff --staged --quiet 2>/dev/null; then
            log_info "Aucun changement à commiter"
        else
            git commit -m "Initial commit: Project structure and configuration" 2>/dev/null || log_info "Commit initial"
            log_success "Commit initial créé"
        fi
    else
        log_info "Working directory propre"
    fi
}

# ===== VÉRIFICATIONS FINALES =====
final_checks() {
    log_info "Vérifications finales..."
    
    # Vérifier les répertoires critiques
    local critical_dirs=(
        "$TRADING_AI_DIR/configs"
        "$TRADING_AI_DIR/n8n-workflows"
        "$TRADING_AI_DIR/scripts"
    )
    
    for dir in "${critical_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            log_error "Répertoire critique manquant: $dir"
            exit 1
        fi
    done
    
    log_success "Toutes les vérifications sont OK"
}

# ===== AFFICHAGE FINAL =====
show_summary() {
    echo ""
    log_success "===== INSTALLATION TERMINÉE ====="
    echo ""
    echo -e "${GREEN}📁 Projet créé dans:${NC} $TRADING_AI_DIR"
    echo ""
    
    if [[ "${GIT_ONLY:-false}" == "true" ]]; then
        echo -e "${BLUE}🔧 LAPTOP/DÉVELOPPEMENT - Prochaines étapes:${NC}"
        echo "1. cd $TRADING_AI_DIR"
        echo "2. git add . && git commit -m 'Complete project structure'"
        echo "3. git remote add origin <your-github-repo>"
        echo "4. git push -u origin main"
        echo ""
        echo -e "${YELLOW}📤 Pour le déploiement production:${NC}"
        echo "• Cloner sur serveur avec Docker"
        echo "• Configurer .env avec API keys"
        echo "• Lancer: docker-compose up -d"
    else
        echo -e "${BLUE}🔧 PRODUCTION - Prochaines étapes:${NC}"
        echo "1. cd $TRADING_AI_DIR"
        echo "2. nano .env  # Configurer vos API keys"
        echo "3. docker-compose up -d  # Lancer la stack"
        echo ""
        echo -e "${BLUE}🌐 Services après démarrage:${NC}"
        echo "• N8N: http://localhost:5678"
        echo "• Grafana: http://localhost:3000" 
        echo "• Frontend: http://localhost"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Le projet est prêt pour Git et le déploiement${NC}"
    echo ""
}

# ===== FONCTION PRINCIPALE =====
main() {
    echo ""
    log_info "===== SETUP TRADING-AI v2.0 ====="
    log_info "Installation idempotente dans: $TRADING_AI_DIR"
    echo ""
    
    check_dependencies
    create_project_structure
    create_env_file
    create_gitignore  
    create_docker_compose
    create_nginx_frontend
    create_readme
    create_additional_configs
    init_git_repo
    final_checks
    show_summary
}

# ===== EXÉCUTION =====
# Vérifier si le script est exécuté directement
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
