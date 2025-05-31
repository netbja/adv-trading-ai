# 🐳 AI Trading Orchestrator - Docker Edition

## 🚀 Déploiement Complet avec Docker

Ce guide te permet de déployer l'ensemble du système AI Trading Orchestrator avec tous ses modules avancés en utilisant Docker.

## 📋 Prérequis

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **4 GB RAM** minimum
- **2 CPU cores** recommandé
- **10 GB espace disque** libre

## 🏗️ Architecture Docker

```
┌─────────────────────────────────────────────────────────┐
│                   AI TRADING ORCHESTRATOR               │
├─────────────────────────────────────────────────────────┤
│  🐳 CONTAINERS                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │   Backend   │ │   Database  │ │    Redis    │      │
│  │  FastAPI    │ │ PostgreSQL  │ │   Cache     │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │   Celery    │ │ Celery Beat │ │  AI Tests   │      │
│  │   Worker    │ │  Scheduler  │ │   Suite     │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
├─────────────────────────────────────────────────────────┤
│  🧠 MODULES IA AVANCÉE                                 │
│  • AI Feedback Loop - Apprentissage continu            │
│  • Predictive System - Prédictions multi-horizon       │
│  • Security Supervisor - Surveillance complète         │
│  • Portfolio Optimizer - Optimisation intelligente     │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Lancement Rapide

### Option 1: Lancement Automatique (Recommandé)

```bash
# Lancement complet automatique
./launch_docker_ai_system.sh --auto
```

### Option 2: Menu Interactif

```bash
# Menu avec options avancées
./launch_docker_ai_system.sh
```

### Option 3: Commandes Docker Manuelles

```bash
# Construction et démarrage
docker compose build
docker compose up -d

# Tests IA avancée
docker compose run --rm ai_tests
```

## 📊 Services et Ports

| Service | Port | Description | Health Check |
|---------|------|-------------|--------------|
| Backend API | 8000 | FastAPI + IA Modules | http://localhost:8000/health |
| PostgreSQL | 5432 | Base de données | Interne |
| Redis | 6379 | Cache et queues | Interne |
| Prometheus | 9090 | Monitoring (optionnel) | http://localhost:9090 |
| Grafana | 3000 | Dashboards (optionnel) | http://localhost:3000 |

## 🧪 Tests et Validation

### Tests IA Complets

```bash
# Lancer tous les tests IA
docker compose run --rm ai_tests

# Logs des tests
docker compose logs ai_tests
```

### Monitoring en Temps Réel

```bash
# Monitoring avec le script
./launch_docker_ai_system.sh monitoring

# Status des containers
docker compose ps

# Logs en temps réel
docker compose logs -f
```

## 🔧 Configuration Avancée

### Variables d'Environnement

```bash
# Database
DATABASE_URL=postgresql://trading_user:trading_pass@database:5432/trading_orchestrator

# Redis
REDIS_URL=redis://redis:6379/0

# Application
DEBUG=true
ENVIRONMENT=docker
PYTHONPATH=/app
```

### Profiles Docker Compose

```bash
# Avec monitoring
docker compose --profile monitoring up -d

# Avec logging avancé
docker compose --profile logging up -d

# Tests seulement
docker compose --profile testing run ai_tests
```

## 📈 Monitoring et Logs

### Accès aux Logs

```bash
# Logs backend
docker compose logs -f backend

# Logs Celery
docker compose logs -f celery_worker celery_beat

# Logs base de données
docker compose logs -f database

# Tous les logs
docker compose logs -f
```

### Métriques de Performance

```bash
# Status des containers
docker stats

# Utilisation des volumes
docker system df

# Health checks
docker compose exec backend curl localhost:8000/health
```

## 🔍 Dépannage

### Problèmes Courants

1. **Port déjà utilisé**
   ```bash
   # Vérifier les ports
   netstat -tlnp | grep :8000
   
   # Changer le port dans docker-compose.yml
   ports:
     - "8001:8000"  # Utiliser 8001 au lieu de 8000
   ```

2. **Manque de mémoire**
   ```bash
   # Vérifier la mémoire
   docker system df
   docker system prune
   
   # Ajuster les ressources dans docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 512M
   ```

3. **Base de données non prête**
   ```bash
   # Attendre que la DB soit prête
   docker compose exec database pg_isready -U trading_user
   
   # Reinitialiser si nécessaire
   docker compose down -v
   docker compose up -d database
   ```

### Commandes de Dépannage

```bash
# Redémarrage complet
docker compose down --remove-orphans
docker compose up -d

# Reconstruction des images
docker compose build --no-cache

# Nettoyage complet
./launch_docker_ai_system.sh cleanup
```

## 🔐 Sécurité

### Configuration Sécurisée

```bash
# Créer un réseau isolé
docker network create trading_secure

# Utiliser des secrets Docker
echo "trading_pass" | docker secret create db_password -
```

### Scanner les Vulnérabilités

```bash
# Scanner les images
docker scout cves trading_backend

# Mettre à jour les images
docker compose pull
docker compose up -d
```

## 📊 API et Endpoints

### Endpoints Principaux

- **Health Check**: `GET /health`
- **API Docs**: `GET /docs` 
- **AI Feedback**: `POST /api/advanced-ai/feedback/learn`
- **Predictions**: `POST /api/advanced-ai/prediction/forecast`
- **Security**: `POST /api/advanced-ai/security/health-check`
- **Portfolio**: `POST /api/advanced-ai/portfolio/optimize`

### Tests d'API

```bash
# Test de base
curl http://localhost:8000/health

# Test complet
curl -X POST http://localhost:8000/api/advanced-ai/feedback/learn \
  -H "Content-Type: application/json" \
  -d '{"signal_type":"SUCCESS","component":"test"}'
```

## 🚀 Production

### Optimisations Production

```bash
# Variables d'environnement production
export DEBUG=false
export ENVIRONMENT=production
export LOG_LEVEL=WARNING

# Déploiement avec ressources limitées
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Sauvegarde et Restauration

```bash
# Sauvegarde de la DB
docker compose exec database pg_dump -U trading_user trading_orchestrator > backup.sql

# Restauration
docker compose exec -T database psql -U trading_user trading_orchestrator < backup.sql
```

## 🎯 Résultats Attendus

Après un déploiement réussi, tu devrais voir :

```
🏆 SYSTÈME 100% AUTONOME EN DOCKER!
   ✅ Tous les containers fonctionnent parfaitement
   ✅ Communication inter-services opérationnelle
   ✅ Scalabilité Docker validée
   ✅ Isolation et sécurité containers confirmées
   ✅ Orchestration microservices réussie

🚀 LE SYSTÈME DOCKER EST PRÊT POUR LA PRODUCTION!
   🐳 Déploiement conteneurisé validé
   📊 Monitoring intégré fonctionnel
   🔄 Auto-scaling prêt
```

## 📞 Support

En cas de problème :

1. Vérifier les logs : `docker compose logs`
2. Consulter le monitoring : `./launch_docker_ai_system.sh monitoring`
3. Redémarrer : `docker compose restart`
4. Nettoyage complet : `./launch_docker_ai_system.sh cleanup`

---

**🎉 Bon trading avec l'IA ! 🤖💰** 