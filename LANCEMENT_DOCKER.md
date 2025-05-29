# 🐳 GUIDE LANCEMENT DOCKER - SYSTÈME AUTONOME

## 🎯 **POUR TOI : DÉMARRAGE IMMÉDIAT SANS APIs**

Tu as raison, tu es en Docker et sans clés API pour le moment. J'ai créé une **version complète** qui fonctionne en **mode simulation** !

---

## 🎮 **CHOISIR TON MODE**

### **Mode ACCESSIBLE** (recommandé pour débuter)
Interface web simple avec analytics intégrées
```bash
# Dans .env
PROFESSIONAL_MODE=false

# Lancer
docker-compose -f docker-compose.autonomous.yml up -d
```

### **Mode PROFESSIONNEL** (pour utilisateurs avancés)
Ajoute Grafana + Prometheus pour visualisations avancées
```bash
# Dans .env
PROFESSIONAL_MODE=true

# Lancer avec profil professionnel
docker-compose -f docker-compose.autonomous.yml --profile professional up -d
```

## 🚀 **LANCEMENT RAPIDE**

### **1. Copier configuration**
```bash
cp env.autonomous.example .env
```

### **2. Lancer le système complet**
```bash
docker-compose -f docker-compose.autonomous.yml up -d
```

**C'est tout !** 🎉

---

## 📊 **ACCÈS INTERFACES**

### **🧠 Interface Principale (Système Autonome)**
```
http://localhost:8000
```
- Dashboard temps réel
- Performance en live  
- Progression des milestones
- Stats de trading

### **📈 Grafana (Monitoring Avancé)**
```
http://localhost:3000
User: admin
Pass: TradingAI2025!
```

### **🔍 API Health Check**
```
http://localhost:8000/health
http://localhost:8000/dashboard
```

---

## 🎮 **MODE SIMULATION ACTIVÉ**

Le système démarre en **mode simulation** avec :

```
✅ AUCUNE API PAYANTE REQUISE
✅ Simulation intelligente de trading
✅ Données de marché simulées réalistes
✅ Croissance basée sur algorithmes optimisés
✅ Interface web complète
✅ Monitoring Grafana
✅ Base de données pour historique
```

### **Progression Simulée Réaliste**

```
🎯 Capital initial: 200€
📈 Target quotidien: ~0.49% (+/- volatilité)
💰 Croissance composée automatique
🔄 Réinvestissement intelligent 80-90%
📊 Milestones progressifs
```

---

## 🔧 **COMMANDES DOCKER UTILES**

### **Voir les logs en temps réel**
```bash
# Tous les services
docker-compose -f docker-compose.autonomous.yml logs -f

# Système autonome seulement
docker logs -f trading_ai_autonomous
```

### **Statut des services**
```bash
docker-compose -f docker-compose.autonomous.yml ps
```

### **Redémarrer le système**
```bash
docker-compose -f docker-compose.autonomous.yml restart autonomous_trading
```

### **Arrêter tout**
```bash
docker-compose -f docker-compose.autonomous.yml down
```

### **Nettoyer et relancer**
```bash
docker-compose -f docker-compose.autonomous.yml down -v
docker-compose -f docker-compose.autonomous.yml up -d --build
```

---

## 📈 **ÉVOLUTION VERS APIs RÉELLES**

### **Quand Tu Auras du Capital (1000€+)**

1. **Éditer `.env`**
```bash
# Changer DEMO_MODE
DEMO_MODE=false

# Ajouter vraies clés APIs
OPENAI_API_KEY=your_real_key
GROQ_API_KEY=your_real_key
TWITTER_API_KEY=your_real_key
```

2. **Redémarrer**
```bash
docker-compose -f docker-compose.autonomous.yml restart
```

### **Migration Progressive**
```
Phase 1: SIMULATION (0-500€)
→ Test du système, validation algorithmes

Phase 2: APIs GRATUITES (500-1000€)  
→ Vraies données mais APIs limitées

Phase 3: APIs PREMIUM (1000€+)
→ Système complet avec tout optimisé
```

---

## 🛡️ **SÉCURITÉ & PERSISTENCE**

### **Données Persistantes**
```bash
# Les données sont sauvées dans :
./data/autonomous/     # Données système
./logs/autonomous/     # Logs application
./backup/autonomous/   # Backups automatiques
```

## ⭐ **INTERFACES DISPONIBLES**

### **Mode Accessible**
- **🎯 Dashboard Principal** : http://localhost
  - Login: `admin` / `TradingAI2025!`
  - Interface complète avec crypto, forex, analytics

### **Mode Professionnel** (si activé)
- **🎯 Dashboard Principal** : http://localhost 
- **📊 Grafana Avancé** : http://localhost:3000
  - Login: `admin` / `TradingAI2025!`
  - Visualisations professionnelles pré-configurées
- **📈 Prometheus Métriques** : http://localhost:9090
  - Métriques brutes pour analystes

## 🧠 **APRÈS LE LANCEMENT**