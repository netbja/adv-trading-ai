# 🚀 Advanced Trading AI System

## 📋 Vue d'ensemble

Système de trading automatisé multi-niveaux avec:
- **Meme Scalping** (5min-1h) 
- **Technical Trading** (1h-4h)
- **Shared AI Brain** pour optimisation
- **Monitoring Grafana** temps réel
- **Multi-chain support**

## 🏗️ Architecture

```
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
