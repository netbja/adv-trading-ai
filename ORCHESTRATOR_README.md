# 🧠 AI Trading Orchestrator

**Remplacement intelligent des CRONs traditionnels par de l'IA**

L'Orchestrateur AI utilise Groq pour prendre des décisions intelligentes sur quand et comment exécuter vos stratégies de trading, en basculant automatiquement entre Crypto et Forex selon les conditions de marché.

## 🎯 **Fonctionnalités**

### ✨ **Intelligence Artificielle**
- **Groq LLama 3.3 70B** pour des analyses ultra-rapides
- **Décisions contextuelles** basées sur les conditions de marché
- **Apprentissage adaptatif** des patterns de réussite
- **Fallback intelligent** si l'IA est indisponible

### 🔄 **Dual Market Support**
- **Crypto** : Trading 24/7 sur Pump.fun, DexScreener
- **Forex** : Sessions Londres/NY/Asie avec TraderMade API
- **Mode Hybrid** : Multi-asset simultané
- **Mode Standby** : Attente intelligente

### 🌉 **Integration N8N**
- **Bridge transparent** avec vos workflows existants
- **Déclenchement intelligent** via webhooks
- **Paramètres dynamiques** selon les conditions
- **Monitoring des exécutions**

### 📊 **Monitoring Avancé**
- **API REST** pour contrôle et statut
- **Métriques Prometheus** pour Grafana
- **Logs structurés** avec timestamps
- **Health checks** automatiques

## 🚀 **Démarrage Rapide**

### 1. **Prérequis**
```bash
# Vérifier que vous avez votre clé Groq
echo $GROQ_API_KEY

# Si pas de clé, obtenez-en une sur https://console.groq.com/
```

### 2. **Configuration**
```bash
# Copier le template d'environnement
cp env.example .env

# Éditer avec vos clés API
nano .env
```

**Variables critiques à configurer :**
```bash
GROQ_API_KEY=your_real_groq_key_here
TRADERMADE_API_KEY=your_tradermade_key  # Ou "demo" pour test
```

### 3. **Lancement**
```bash
# Script de démarrage simple
./start_orchestrator.sh

# Ou manuellement
docker-compose up -d ai_orchestrator
```

### 4. **Vérification**
```bash
# Vérifier le statut
curl http://localhost:8080/status

# Voir les logs en temps réel
docker-compose logs -f ai_orchestrator
```

## 📡 **API Endpoints**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Health check simple |
| `/status` | GET | Statut complet + métriques |
| `/metrics` | GET | Métriques Prometheus |
| `/decisions` | GET | Historique des décisions IA |
| `/workflows/available` | GET | Workflows N8N disponibles |
| `/control/start` | POST | Démarrer l'orchestrateur |
| `/control/stop` | POST | Arrêter l'orchestrateur |

### **Exemples d'utilisation**

```bash
# Statut du système
curl -s http://localhost:8080/status | jq

# Dernières décisions de l'IA
curl -s http://localhost:8080/decisions?limit=5 | jq

# Métriques pour Grafana
curl http://localhost:8080/metrics
```

## 🧠 **Comment ça fonctionne**

### **Cycle de Décision IA**

```
1. 🔍 ANALYSER L'ENVIRONNEMENT
   ├── Santé des APIs (Pump.fun, DexScreener, TraderMade)
   ├── Session Forex active (Londres/NY/Asie)
   ├── Charge système
   └── Historique des performances

2. 🤖 CONSULTER L'IA (GROQ)
   ├── Prompt contextuel avec toutes les données
   ├── Recommandation de mode (Crypto/Forex/Hybrid)
   ├── Action spécifique (Scan agressif/normal/léger)
   └── Timing optimal pour prochaine décision

3. ⚡ EXÉCUTER VIA N8N
   ├── Déclencher les bons workflows
   ├── Transmettre paramètres contextuels
   └── Monitorer l'exécution

4. 📊 APPRENDRE
   ├── Analyser les résultats
   ├── Ajuster les futurs patterns
   └── Optimiser les timings
```

### **Intelligence Adaptive**

L'orchestrateur apprend de ses décisions :

- **Taux de succès** par mode de marché
- **Timings optimaux** selon les sessions
- **Patterns de volatilité** efficaces
- **Corrélations API health/performance**

## 🎛️ **Configuration Avancée**

### **Variables d'Environnement**

```bash
# IA Configuration
GROQ_API_KEY=xxx                    # Clé Groq (REQUIS)
OPENAI_API_KEY=xxx                  # Backup OpenAI (optionnel)

# Trading APIs
TRADERMADE_API_KEY=xxx              # Forex data
BIRDEYE_API_KEY=xxx                 # Crypto data additionnelle

# Orchestrateur
ORCHESTRATOR_PORT=8080              # Port API
LOG_LEVEL=INFO                      # DEBUG/INFO/WARNING/ERROR

# Notifications
TELEGRAM_BOT_TOKEN=xxx              # Bot Telegram
TELEGRAM_CHAT_ID=xxx                # Chat pour alertes
```

### **Customisation des Prompts**

Le prompt IA peut être modifié dans `src/orchestrator/ai_orchestrator.py` :

```python
class GroqAIEngine:
    def __init__(self):
        self.model = "llama-3.3-70b-versatile"  # Modèle Groq
        # Ajuster selon vos besoins
```

### **Webhooks N8N**

L'orchestrateur déclenche ces webhooks N8N :

```
/webhook/crypto-aggressive-scan     # Scan crypto agressif
/webhook/crypto-normal-scan         # Scan crypto normal  
/webhook/crypto-light-monitoring    # Monitoring léger
/webhook/forex-london-session       # Session Londres
/webhook/forex-newyork-session      # Session New York
/webhook/forex-asia-session         # Session Asie
/webhook/health-monitor-check       # Vérification santé
/webhook/deep-market-analysis       # Analyse profonde
```

## 📊 **Monitoring avec Grafana**

### **Métriques Disponibles**

```
orchestrator_decisions_total          # Total décisions
orchestrator_successful_decisions     # Décisions réussies
orchestrator_success_rate            # Taux de succès
orchestrator_mode_switches_total      # Changements de mode
orchestrator_system_load             # Charge système
orchestrator_market_volatility       # Volatilité marché
orchestrator_running                 # État running
api_health_*                         # Santé des APIs
```

### **Dashboard Grafana**

Créer un dashboard avec ces queries :

```promql
# Taux de succès
orchestrator_success_rate * 100

# Décisions par heure
rate(orchestrator_decisions_total[1h]) * 3600

# Santé des APIs
avg(api_health_pump_fun, api_health_dexscreener)
```

## 🔧 **Développement**

### **Structure du Code**

```
src/orchestrator/
├── ai_orchestrator.py      # Orchestrateur principal
├── n8n_bridge.py          # Bridge vers N8N
├── api_server.py          # API REST
└── main.py               # Point d'entrée
```

### **Tests**

```bash
# Installer les dépendances de dev
pip install -r requirements.txt

# Lancer les tests
pytest tests/

# Test simple du bridge N8N
python -m src.orchestrator.n8n_bridge
```

### **Debug**

```bash
# Logs détaillés
docker-compose logs -f ai_orchestrator

# Mode debug
echo "LOG_LEVEL=DEBUG" >> .env
docker-compose restart ai_orchestrator

# Tester l'API manuellement
curl -X POST http://localhost:8080/control/force-decision
```

## 🚨 **Troubleshooting**

### **Problèmes Courants**

| Problème | Solution |
|----------|----------|
| `GROQ_API_KEY missing` | Vérifier `.env` et redémarrer |
| `N8N webhooks fail` | Vérifier que N8N est démarré |
| `API timeouts` | Augmenter les timeouts dans le code |
| `Memory issues` | Réduire l'historique des décisions |

### **Logs Utiles**

```bash
# Orchestrateur principal
docker-compose logs ai_orchestrator

# N8N workflows
docker-compose logs n8n

# Base de données
docker-compose logs postgres

# Tous les services
docker-compose logs
```

### **Reset Complet**

```bash
# Arrêter tout
docker-compose down

# Nettoyer les données (ATTENTION : supprime tout)
sudo rm -rf data/orchestrator logs/orchestrator

# Redémarrer
./start_orchestrator.sh
```

## 🎯 **Prochaines Étapes**

1. **Tester les workflows crypto** existants
2. **Créer les workflows Forex** manquants
3. **Configurer Grafana** avec les métriques
4. **Ajouter plus d'APIs** de données
5. **Implémenter le machine learning** pour l'apprentissage

## 💡 **Support**

L'orchestrateur est conçu pour être **autonome et intelligent**. Il prend des décisions en continu sans intervention humaine, mais reste **observable et contrôlable** via l'API REST.

**L'IA fait le travail, vous gardez le contrôle !** 🚀 