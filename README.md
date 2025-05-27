# 🚀 Advanced Trading AI System

## 📋 Vue d'ensemble

Système de trading automatisé multi-niveaux avec:

- **Meme Scalping** (5min-1h)
- **Technical Trading** (1h-4h)
- **Shared AI Brain** pour optimisation
- **Monitoring Grafana** temps réel
- **Multi-chain support**

## structure du projet

### Structure détaillée

/opt/trading-ai/
├── README.md                   # Documentation principale
├── docker-compose.yml          # Stack complète
├── .env                        # Variables d'environnement
├── .gitignore                  # Fichiers à ignorer
├── configs/                    # Configurations
│   ├── nginx/
│   │   └── nginx.conf          # Reverse proxy
│   │   └── frontend/
│   │   │   └── index.html      # Page web
│   ├── grafana/
│   │   ├── dashboards/         # Dashboards JSON
│   │   │   └── trading-master-dashboard.json
│   │   │   └── n8n-workflows.json
│   │   │   └── system-metrics.json
│   │   ├── provisioning/       # Auto-provisioning
│   │   │   └── dashboards/     # Dashboards YAML
│   │   │       └── dashboards.yml
│   │   │   └── datasources/    # Datasources YAML
│   │   │       └── datasources.yml
│   │   └── grafana.ini         # Config Grafana
│   ├── prometheus/
│   │   └── prometheus.yml      # Config monitoring
│   └── postgres/
│       └── init.sql           # Schema initial
│
├── scripts/                    # Scripts utilitaires
│   ├── backup.sh              # Backup automatique
│   ├── restore.sh             # Restauration
│   ├── deploy.sh              # Déploiement
│   └── monitoring.sh          # Healthcheck
│
├── n8n-workflows/             # Workflows N8N
│   ├── 01-meme-scalping.json     # Workflow principal
│   ├── 02-technical-trading.json # Workflow technique (futur)
│   └── 03-shared-brain.json      # AI partagé (futur)
│
├── src/                       # Code source custom
│   ├── api/                   # API custom si besoin
│   ├── utils/                 # Utilitaires
│   └── monitoring/            # Scripts monitoring
│
├── data/                      # Données (gitignore)
│   ├── postgres/              # Base de données
│   ├── grafana/               # Dashboards + config
│   ├── n8n/                   # Workflows sauvés
│   └── prometheus/            # Métriques historiques
│
├── logs/                      # Logs centralisés (gitignore)
│   ├── postgres/
│   ├── grafana/
│   ├── n8n/
│   └── nginx/
│
└── backup/                    # Backups (gitignore)
    └── postgres/              # Dumps quotidiens

### 🏗️ Architecture

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   N8N Workflows │    │   PostgreSQL    │    │     Grafana     │
│   - Meme Scalp  │◄──►│   - Trades      │◄──►│   - Dashboard   │
│   - Technical   │    │   - Portfolio   │    │   - Alerts      │
│   - Shared AI   │    │   - Metrics     │    │   - Reports     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │   Prometheus    │    │    Telegram     │
│   - Reverse     │    │   - Metrics     │    │   - Alerts      │
│   - SSL/TLS     │    │   - Monitoring  │    │   - Reports     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Démarrage rapide

```bash
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
# PostgreSQL: localhost:5432
```

## 📊 Services

| Service | Port | Description |
|---------|------|-------------|
| N8N | 5678 | Workflows automation |
| Grafana | 3000 | Monitoring dashboards |
| PostgreSQL | 5432 | Base de données |
| Prometheus | 9090 | Métriques |
| Nginx | 80/443 | Reverse proxy |

## 🛠️ Gestion

```bash
# Backup
./scripts/backup.sh

# Restauration
./scripts/restore.sh backup_20241127.sql

# Monitoring
./scripts/monitoring.sh

# Logs
docker-compose logs -f [service]
```

## 📈 Workflows

1. **Meme Scalping**: Scanner Pump.fun + AI Analysis
2. **Technical Trading**: Multi-timeframe analysis  
3. **Shared Brain**: Optimisation cross-strategy

## 🔒 Sécurité

- Authentification sur tous les services
- SSL/TLS avec Nginx
- Sauvegarde automatique
- Logs centralisés

## 📞 Support

- Documentation: `./docs/`
- Logs: `./logs/`
- Issues: GitHub Issues

---
Créé le 2025-05-27 | Version 1.0
