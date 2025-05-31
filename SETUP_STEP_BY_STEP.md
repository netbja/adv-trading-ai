# 🚀 GUIDE COMPLET DE LANCEMENT - TRADING AI ORCHESTRATOR

## 📋 CHECKLIST GÉNÉRALE

- [ ] **Étape 1** : Obtenir les clés API (voir API_SETUP_GUIDE.md)
- [ ] **Étape 2** : Configuration environnement
- [ ] **Étape 3** : Installation dépendances  
- [ ] **Étape 4** : Tests de connectivité APIs
- [ ] **Étape 5** : Lancement système
- [ ] **Étape 6** : Validation et monitoring

---

## 🔧 ÉTAPE 2 : CONFIGURATION ENVIRONNEMENT

### 2.1 - Créer le fichier .env principal

```bash
# Se placer dans le répertoire du projet
cd /home/sysnet/adv-trading-ai

# Créer le fichier .env avec tes clés API
cp .env.example .env
nano .env
```

### 2.2 - Template .env complet à remplir

```bash
# ============================================
# 🔑 CLÉS API - PHASE 1 (GRATUITES)
# ============================================

# COINGECKO (crypto data)
COINGECKO_API_KEY="cg-xxxxxxxxxxxxxxx"

# ALPHA VANTAGE (stocks/forex/crypto)  
ALPHA_VANTAGE_API_KEY="ABCD1234EFGH5678"

# REDDIT (sentiment analysis)
REDDIT_CLIENT_ID="xxxxxxxxxx"
REDDIT_CLIENT_SECRET="xxxxxxxxxxxxxxxx"
REDDIT_USER_AGENT="TradingBot/1.0"

# TWITTER (trends & sentiment)
TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAxxxxxxxxx"

# ============================================
# 📈 TRADING & BROKERS
# ============================================

# ALPACA (déjà configuré)
ALPACA_API_KEY="PK_xxxxxxxxxxxx"
ALPACA_SECRET_KEY="xxxxxxxxxxxx"
ALPACA_BASE_URL="https://paper-api.alpaca.markets"  # Paper trading

# ============================================
# 🧠 AI & LLM  
# ============================================

# GROQ (déjà configuré)
GROQ_API_KEY="gsk_xxxxxxxxxxxx"

# OPENAI (déjà configuré)
OPENAI_API_KEY="sk-xxxxxxxxxxxx"

# ============================================
# 📱 NOTIFICATIONS
# ============================================

# TELEGRAM (déjà configuré)
TELEGRAM_BOT_TOKEN="xxxxxxxxxxxx"
TELEGRAM_CHAT_ID="xxxxxxxxxxxx"

# ============================================
# 🐳 DOCKER & DATABASE
# ============================================

# Database
POSTGRES_DB="trading_ai"
POSTGRES_USER="trading_user"
POSTGRES_PASSWORD="trading_secure_password_2024"
POSTGRES_HOST="database"
POSTGRES_PORT="5432"

# Redis
REDIS_HOST="redis"
REDIS_PORT="6379"
REDIS_PASSWORD=""

# ============================================
# 🔧 CONFIGURATION SYSTÈME
# ============================================

# Environment
ENVIRONMENT="development"
DEBUG="true"
LOG_LEVEL="INFO"

# Security
SECRET_KEY="ton_secret_key_super_secure_ici"

# API Rate Limits
API_RATE_LIMIT_PER_MINUTE="60"
COINGECKO_RATE_LIMIT="50"
ALPHA_VANTAGE_RATE_LIMIT="25"
```

---

## 📦 ÉTAPE 3 : INSTALLATION DÉPENDANCES

### 3.1 - Installer les nouvelles bibliothèques API

```bash
# Ajouter les dépendances pour les nouvelles APIs
cd /home/sysnet/adv-trading-ai

# Mettre à jour requirements.txt avec les nouvelles APIs
echo "
# APIs Data
yfinance==0.2.28
pycoingecko==3.1.0
alpha-vantage==2.3.1
praw==7.7.1
tweepy==4.14.0
requests-ratelimiter==0.4.2

# Data Analysis
ta==0.10.2
pandas-ta==0.3.14b0
" >> backend/requirements.txt
```

### 3.2 - Rebuild des containers Docker

```bash
# Arrêter les services actuels
docker-compose down

# Rebuild avec les nouvelles dépendances
docker-compose build --no-cache

# Redémarrer
docker-compose up -d
```

---

## 🧪 ÉTAPE 4 : TESTS DE CONNECTIVITÉ

### 4.1 - Script de test des APIs

```bash
# Créer un script de test
nano test_apis.py
```

### 4.2 - Code du script de test

```python
#!/usr/bin/env python3
"""
🧪 TEST DE CONNECTIVITÉ APIs
Script pour valider toutes les connexions API
"""

import os
from dotenv import load_dotenv
import requests
import yfinance as yf
from pycoingecko import CoinGeckoAPI
import praw
import tweepy

load_dotenv()

def test_coingecko():
    try:
        cg = CoinGeckoAPI(api_key=os.getenv('COINGECKO_API_KEY'))
        ping = cg.ping()
        print("✅ CoinGecko: Connecté")
        
        # Test prix Bitcoin
        btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
        print(f"   📊 Bitcoin: ${btc_price['bitcoin']['usd']:,.2f}")
        return True
    except Exception as e:
        print(f"❌ CoinGecko: {e}")
        return False

def test_alpha_vantage():
    try:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if 'Global Quote' in data:
            price = data['Global Quote']['05. price']
            print(f"✅ Alpha Vantage: Connecté")
            print(f"   📊 AAPL: ${float(price):,.2f}")
            return True
        else:
            print(f"❌ Alpha Vantage: {data}")
            return False
    except Exception as e:
        print(f"❌ Alpha Vantage: {e}")
        return False

def test_yahoo_finance():
    try:
        ticker = yf.Ticker("BTC-USD")
        price = ticker.info['regularMarketPrice']
        print(f"✅ Yahoo Finance: Connecté")
        print(f"   📊 BTC-USD: ${price:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Yahoo Finance: {e}")
        return False

def test_reddit():
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'TradingBot/1.0')
        )
        
        # Test lecture subreddit
        subreddit = reddit.subreddit('cryptocurrency')
        posts = list(subreddit.hot(limit=1))
        
        if posts:
            print("✅ Reddit: Connecté")
            print(f"   📈 Dernier post: {posts[0].title[:50]}...")
            return True
        else:
            print("❌ Reddit: Pas de posts récupérés")
            return False
    except Exception as e:
        print(f"❌ Reddit: {e}")
        return False

def test_twitter():
    try:
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        if not bearer_token:
            print("❌ Twitter: Bearer token manquant")
            return False
            
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Test recherche
        tweets = client.search_recent_tweets(query="bitcoin", max_results=10)
        
        if tweets.data:
            print("✅ Twitter: Connecté")
            print(f"   🐦 Trouvé {len(tweets.data)} tweets récents sur Bitcoin")
            return True
        else:
            print("❌ Twitter: Pas de tweets récupérés")
            return False
    except Exception as e:
        print(f"❌ Twitter: {e}")
        return False

def main():
    print("🧪 TEST DE CONNECTIVITÉ APIs")
    print("=" * 40)
    
    tests = [
        ("CoinGecko", test_coingecko),
        ("Alpha Vantage", test_alpha_vantage),
        ("Yahoo Finance", test_yahoo_finance),
        ("Reddit", test_reddit),
        ("Twitter", test_twitter)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Test {name}...")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 40)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 40)
    
    success_count = 0
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
        if success:
            success_count += 1
    
    print(f"\n🎯 Score: {success_count}/{len(tests)} APIs fonctionnelles")
    
    if success_count == len(tests):
        print("🎉 Tous les tests réussis! Le système est prêt.")
    elif success_count >= 3:
        print("⚠️ Quelques APIs en échec, mais suffisant pour commencer.")
    else:
        print("🚨 Trop d'APIs en échec. Vérifier la configuration.")

if __name__ == "__main__":
    main()
```

---

## 🚀 ÉTAPE 5 : LANCEMENT SYSTÈME

### 5.1 - Test de connectivité

```bash
# Exécuter le test dans le container
docker-compose exec backend python test_apis.py
```

### 5.2 - Lancement orchestrateur complet

```bash
# Option 1: Via le script unifié
./launch_complete_ai_system.sh

# Option 2: Via Docker directement  
docker-compose up -d
docker-compose logs -f backend
```

### 5.3 - Accès interface web

```bash
# Frontend Vue3
http://localhost:3000

# API Documentation  
http://localhost:8000/docs

# Monitoring (optionnel)
http://localhost:3001  # Grafana
```

---

## 📊 ÉTAPE 6 : VALIDATION & MONITORING

### 6.1 - Endpoints à tester

```bash
# Test santé système
curl http://localhost:8000/health

# Test modules IA
curl http://localhost:8000/api/advanced-ai/status

# Test recommandations
curl http://localhost:8000/api/advanced-ai/recommendations

# Test feedback loop
curl http://localhost:8000/api/advanced-ai/ai-insights
```

### 6.2 - Logs à surveiller

```bash
# Logs backend principal
docker-compose logs -f backend

# Logs worker Celery
docker-compose logs -f celery_worker

# Logs tests IA
docker-compose logs -f ai_tests
```

---

## 🎯 RÉSULTAT ATTENDU

Après ces étapes, tu auras :

✅ **Système fonctionnel** avec 5 APIs connectées  
✅ **4 modules IA** opérationnels (meme coins, crypto LT, forex, ETF)  
✅ **Interface web** Vue3 moderne  
✅ **Monitoring temps réel** des performances  
✅ **Tests automatisés** validés  

**🚀 Prêt pour la simulation et le paper trading !**

---

## 🆘 DÉPANNAGE COURANT

### Problème: APIs en échec
```bash
# Vérifier les variables d'environnement
docker-compose exec backend env | grep API

# Test connectivité réseau
docker-compose exec backend ping google.com
```

### Problème: Containers en échec
```bash
# Logs détaillés
docker-compose logs backend

# Restart clean
docker-compose down && docker-compose up -d
```

### Problème: Interface non accessible
```bash
# Vérifier les ports
docker-compose ps
netstat -tlnp | grep :3000
``` 