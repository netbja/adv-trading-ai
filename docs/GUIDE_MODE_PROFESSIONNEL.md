# 🎯 GUIDE MODE PROFESSIONNEL - GRAFANA & PROMETHEUS

## 🎮 **DEUX MODES AU CHOIX**

### **MODE ACCESSIBLE** (par défaut)
- Interface web intégrée avec analytics
- Simple et immédiat à utiliser
- Parfait pour débuter sans connaissances techniques

### **MODE PROFESSIONNEL** (optionnel)
- Dashboards Grafana avancés
- Métriques Prometheus détaillées  
- Pour utilisateurs expérimentés ou évolution future

---

## 🚀 **ACTIVATION MODE PROFESSIONNEL**

### **1. Configuration**
Éditer le fichier `.env` :
```bash
# Activer le mode professionnel
PROFESSIONAL_MODE=true

# Ports Grafana/Prometheus (optionnel)
GRAFANA_PORT=3000
PROMETHEUS_PORT=9090
```

### **2. Démarrage avec Grafana**
```bash
# Démarrer avec le profil professionnel
docker-compose -f docker-compose.autonomous.yml --profile professional up -d

# Ou démarrer tout
docker-compose -f docker-compose.autonomous.yml up -d
```

---

## 📊 **ACCÈS AUX INTERFACES**

### **Interface Trading AI** (toujours disponible)
- **URL** : http://localhost
- **Login** : admin / TradingAI2025!
- **Usage** : Dashboard intégré, simple et complet

### **Grafana** (mode professionnel uniquement)
- **URL** : http://localhost:3000
- **Login** : admin / TradingAI2025!
- **Usage** : Visualisations avancées et métriques

### **Prometheus** (mode professionnel uniquement)
- **URL** : http://localhost:9090
- **Usage** : Consultation métriques brutes

---

## 🧭 **GUIDE GRAFANA POUR DÉBUTANTS**

### **Premier Accès**
1. Aller sur http://localhost:3000
2. Login: `admin` / `TradingAI2025!`
3. Dashboard automatiquement configuré : "🧠 Trading AI - Dashboard Autonome"

### **Navigation Grafana**
```
📊 Dashboards → Trading AI → Dashboard Autonome
📈 Explore → Voir les métriques en temps réel
⚙️ Configuration → Sources de données (Prometheus auto-configuré)
```

### **Métriques Disponibles**
- `trading_capital_current` → Capital actuel en €
- `trading_return_percentage` → Rendement total en %
- `trading_system_efficiency` → Efficacité du système
- `trading_uptime_days` → Jours de fonctionnement
- `trading_trades_successful_total` → Trades réussis
- `trading_trades_failed_total` → Trades échoués

### **Personnaliser les Graphiques**
1. Clic sur titre d'un panel → **Edit**
2. Modifier la requête dans "Query"
3. Changer l'apparence dans "Visualization"
4. Sauvegarder avec **Save**

---

## 💡 **EXEMPLES PRATIQUES**

### **Créer un Nouveau Panel**
1. Dashboard → **Add panel**
2. **Query** : `trading_capital_current`
3. **Visualization** : Time series (ligne)
4. **Title** : "Évolution Capital"
5. **Save dashboard**

### **Alertes Simples**
1. Panel → **Edit** → **Alert**
2. **Condition** : `trading_capital_current < 180`
3. **Message** : "Capital faible détecté"
4. **Save**

### **Requêtes Utiles**
```promql
# Taux de réussite des trades
trading_trades_successful_total / (trading_trades_successful_total + trading_trades_failed_total) * 100

# Croissance quotidienne moyenne
rate(trading_capital_current[1d])

# Performance vs objectif
trading_system_efficiency / 100
```

---

## 🔄 **BASCULER ENTRE LES MODES**

### **Retour Mode Accessible**
```bash
# Éditer .env
PROFESSIONAL_MODE=false

# Redémarrer sans Grafana
docker-compose -f docker-compose.autonomous.yml up -d autonomous_trading postgres nginx
```

### **Réactivation Mode Pro**
```bash
# Réactiver dans .env
PROFESSIONAL_MODE=true

# Redémarrer avec tout
docker-compose -f docker-compose.autonomous.yml --profile professional up -d
```

---

## 🛠️ **AVANTAGES DE CHAQUE MODE**

### **Mode Accessible** ✅
- **Plus simple** : Interface unified, tout en un
- **Plus rapide** : Pas de courbe d'apprentissage
- **Moins de ressources** : Plus léger
- **Auto-suffisant** : Analytics intégrées

### **Mode Professionnel** 💪
- **Plus puissant** : Grafana = visualisations illimitées
- **Plus flexible** : Dashboards personnalisables
- **Plus de données** : Métriques Prometheus détaillées
- **Évolutif** : Ajout facile de nouvelles métriques

---

## 🎯 **RECOMMANDATIONS**

### **Commencer en Mode Accessible** 
- Découvrir le système
- Comprendre le fonctionnement
- Voir les premiers résultats

### **Évoluer vers Mode Pro quand :**
- Capital > 1000€
- Besoin de métriques personnalisées
- Envie d'analyser plus finement
- Curiosité pour Grafana

---

## 🔧 **DÉPANNAGE GRAFANA**

### **Grafana ne se lance pas**
```bash
# Vérifier les logs
docker-compose logs grafana

# Recréer le volume
docker-compose down
docker volume rm adv-trading-ai_grafana_autonomous_data
docker-compose --profile professional up -d
```

### **Dashboard vide**
1. Vérifier Prometheus : http://localhost:9090
2. Grafana → Configuration → Data sources → Prometheus
3. Test connection

### **Pas de données**
```bash
# Vérifier métriques trading
curl http://localhost:8000/metrics

# Vérifier mode professionnel activé
curl http://localhost:8000/dashboard
```

---

## 📚 **RESSOURCES APPRENTISSAGE**

### **Grafana Basics**
- Documentation officielle : https://grafana.com/docs/
- Tutoriels vidéo : "Grafana for beginners"
- Sandbox : https://play.grafana.org/

### **Prometheus Queries**
- Guide PromQL : https://prometheus.io/docs/prometheus/latest/querying/
- Exemples : https://prometheus.io/docs/prometheus/latest/querying/examples/

---

**💡 Conseil** : Commence en mode accessible, puis active le mode pro quand tu veux plus de contrôle ! Les deux interfaces sont complémentaires. 