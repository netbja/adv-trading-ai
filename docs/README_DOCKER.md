# 🐳 TRADING AI PROFESSIONNEL - DOCKER

## 🎯 Vue d'ensemble

Interface de trading AI professionnelle avec authentification sécurisée et workflows temps réel, optimisée pour un déploiement Docker.

## 🚀 Démarrage rapide en Docker

### Prérequis
```bash
# Docker et Docker Compose installés
docker --version
docker-compose --version

# Si pas installés sur Ubuntu/Debian :
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Redémarrer la session ou faire : newgrp docker
```

### 🎯 Démarrage simple (Recommandé)
```bash
# Cloner et accéder au répertoire
cd adv-trading-ai

# Démarrage simple (Interface + PostgreSQL)
./start_docker_trading_ai.sh

# Ou en mode professionnel (+ Grafana + Prometheus)
./start_docker_trading_ai.sh professional

# Avec suivi des logs
./start_docker_trading_ai.sh simple logs
```

### 🌐 Accès à l'interface
- **Interface principale**: http://localhost:8000
- **Connexion**: `admin / TradingAI2025!`
- **Mode professionnel**: Grafana sur http://localhost:3000

## 🏗️ Architecture Docker

### Services disponibles

#### 🧠 Interface Trading AI (`autonomous_trading`)
- Port: `8000`
- Interface web professionnelle complète
- Workflows crypto, meme et forex temps réel
- Authentification DB sécurisée

#### 🗃️ PostgreSQL (`postgres`)
- Port: `5432` 
- Base de données pour utilisateurs et sessions
- Healthcheck intégré
- Backup automatique

#### 📊 Grafana (`grafana`) - Mode professionnel
- Port: `3000`
- Dashboards de monitoring
- Métriques système et trading

#### 📈 Prometheus (`prometheus`) - Mode professionnel
- Port: `9090`
- Collecte de métriques
- Alerting intégré

## ⚙️ Configuration

### Variables d'environnement (.env)
```bash
# Le fichier .env est créé automatiquement depuis env.autonomous.example
# Personnalisez selon vos besoins :

# Ports (si conflits)
AUTONOMOUS_PORT=8000
GRAFANA_PORT=3000
POSTGRES_PORT=5432

# Mots de passe
POSTGRES_PASSWORD=TradingDB2025!
GF_ADMIN_PASSWORD=TradingAI2025!

# Mode et configuration
DEMO_MODE=true
INITIAL_CAPITAL=200
LOG_LEVEL=INFO
```

### Configuration avancée
```bash
# Éditer la configuration
nano .env

# Redémarrer pour appliquer
./start_docker_trading_ai.sh
```

## 📋 Commandes utiles

### Gestion des containers
```bash
# Voir les services actifs
docker-compose -f docker-compose.autonomous.yml ps

# Logs en temps réel
docker-compose -f docker-compose.autonomous.yml logs -f

# Logs d'un service spécifique
docker-compose -f docker-compose.autonomous.yml logs -f autonomous_trading

# Arrêter tous les services
docker-compose -f docker-compose.autonomous.yml down

# Arrêter et supprimer les volumes
docker-compose -f docker-compose.autonomous.yml down -v
```

### Debug et maintenance
```bash
# Accéder au container Trading AI
docker exec -it trading_ai_autonomous bash

# Accéder à PostgreSQL
docker exec -it trading_ai_postgres_autonomous psql -U trader -d trading_ai

# Reconstruire l'image
docker-compose -f docker-compose.autonomous.yml build --no-cache autonomous_trading

# Voir l'utilisation des ressources
docker stats
```

### Sauvegarde et restauration
```bash
# Sauvegarder la base de données
docker exec trading_ai_postgres_autonomous pg_dump -U trader trading_ai > backup_$(date +%Y%m%d).sql

# Restaurer une sauvegarde
docker exec -i trading_ai_postgres_autonomous psql -U trader trading_ai < backup_20241225.sql
```

## 🔍 Monitoring et logs

### Localisation des logs
```bash
logs/
├── autonomous/        # Logs de l'interface Trading AI
├── postgres/         # Logs PostgreSQL
└── grafana/          # Logs Grafana (mode pro)
```

### Monitoring en temps réel
```bash
# Voir tous les logs
./start_docker_trading_ai.sh simple logs

# Filtrer par service
docker-compose -f docker-compose.autonomous.yml logs -f autonomous_trading | grep ERROR

# Métriques système (mode professionnel)
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
```

## 🔧 Résolution de problèmes

### Problèmes courants

**Port 8000 déjà utilisé**
```bash
# Changer le port dans .env
echo "AUTONOMOUS_PORT=8001" >> .env
./start_docker_trading_ai.sh
```

**PostgreSQL ne démarre pas**
```bash
# Vérifier les logs
docker-compose -f docker-compose.autonomous.yml logs postgres

# Nettoyer les volumes corrompus
docker-compose -f docker-compose.autonomous.yml down -v
./start_docker_trading_ai.sh
```

**Interface ne répond pas**
```bash
# Vérifier le healthcheck
docker ps

# Redémarrer le service
docker-compose -f docker-compose.autonomous.yml restart autonomous_trading

# Vérifier les logs
docker-compose -f docker-compose.autonomous.yml logs autonomous_trading
```

**Mémoire insuffisante**
```bash
# Augmenter les limites dans docker-compose.autonomous.yml
# mem_limit: 2g  # au lieu de 1g

# Ou désactiver les limites temporairement
# Commenter les lignes mem_limit dans le fichier
```

### Debug avancé
```bash
# Mode debug détaillé
echo "LOG_LEVEL=DEBUG" >> .env
./start_docker_trading_ai.sh

# Analyser l'utilisation mémoire/CPU
docker stats trading_ai_autonomous

# Inspecter la configuration
docker inspect trading_ai_autonomous
```

## 🔒 Sécurité Docker

### Bonnes pratiques appliquées
- ✅ Utilisateur non-root dans les containers
- ✅ Variables d'environnement pour secrets
- ✅ Réseaux Docker isolés
- ✅ Healthchecks pour tous les services
- ✅ Limites mémoire définies

### Renforcement (optionnel)
```bash
# Utiliser secrets Docker (production)
# Ajouter dans docker-compose.yml :
secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt

# Scanner les vulnérabilités
docker scout cves trading_ai_autonomous

# Mettre à jour les images de base
docker-compose -f docker-compose.autonomous.yml pull
./start_docker_trading_ai.sh
```

## 🚀 Déploiement production

### Checklist pré-production
- [ ] Changer tous les mots de passe par défaut
- [ ] Configurer les vraies APIs (pas demo)
- [ ] Activer HTTPS (Nginx avec certificats)
- [ ] Configurer les sauvegardes automatiques
- [ ] Mettre en place le monitoring externe
- [ ] Tester la haute disponibilité

### Variables production
```bash
# .env de production
DEMO_MODE=false
POSTGRES_PASSWORD=VotreMotDePasseFort!
GF_ADMIN_PASSWORD=VotreMotDePasseGrafana!

# APIs réelles
OPENAI_API_KEY=votre_clé_openai
GROQ_API_KEY=votre_clé_groq
TELEGRAM_BOT_TOKEN=votre_token_telegram
```

## 📚 Référence rapide

### Scripts disponibles
- `./start_docker_trading_ai.sh` - Démarrage simple
- `./start_docker_trading_ai.sh professional` - Mode professionnel
- `./start_docker_trading_ai.sh simple logs` - Avec logs

### URLs importantes
- Interface Trading AI: http://localhost:8000
- Grafana (mode pro): http://localhost:3000  
- Prometheus (mode pro): http://localhost:9090
- PostgreSQL: localhost:5432

### Comptes par défaut
- **Trading AI**: admin / TradingAI2025!
- **Grafana**: admin / TradingAI2025!
- **PostgreSQL**: trader / TradingDB2025!

---

**🐳 Déployé avec Docker pour une facilité maximale !** 