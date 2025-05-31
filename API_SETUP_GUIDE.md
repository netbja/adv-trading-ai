# 🔑 GUIDE D'OBTENTION DES CLÉS API - TRADING AI BOT

## 🟢 PHASE 1 : APIs GRATUITES (À FAIRE EN PREMIER)

### 1. **COINGECKO** (Gratuit pour commencer)
```
🌐 Site : https://www.coingecko.com/en/api
📝 Inscription : Compte gratuit requis
⏱️ Limite : 50 appels/minute
💰 Coût : GRATUIT (puis $129/mois pour Pro)

Étapes :
1. Créer un compte sur coingecko.com
2. Aller dans "Developers" > "API"  
3. Copier votre clé API gratuite
4. Noter : COINGECKO_API_KEY="cg-xxxxx"
```

### 2. **ALPHA VANTAGE** (Gratuit)
```
🌐 Site : https://www.alphavantage.co/support/#api-key
📝 Inscription : Email requis
⏱️ Limite : 500 appels/jour (25/min)
💰 Coût : GRATUIT (puis $49/mois pour Premium)

Étapes :
1. Aller sur alphavantage.co
2. Cliquer "Get your free API key today"
3. Remplir le formulaire simple
4. Noter : ALPHA_VANTAGE_API_KEY="ABCD1234"
```

### 3. **REDDIT API** (Gratuit)
```
🌐 Site : https://www.reddit.com/prefs/apps
📝 Inscription : Compte Reddit requis
⏱️ Limite : 100 requêtes/minute
💰 Coût : GRATUIT

Étapes :
1. Se connecter à Reddit
2. Aller dans "User Settings" > "Privacy & Security"
3. Scroll down vers "App Authorization"
4. Cliquer "Create Application"
5. Type: "script"
6. Noter : 
   REDDIT_CLIENT_ID="xxxxx"
   REDDIT_CLIENT_SECRET="xxxxx"
```

### 4. **TWITTER API** (Gratuit Limited)
```
🌐 Site : https://developer.twitter.com/en/portal/dashboard
📝 Inscription : Compte Twitter + validation
⏱️ Limite : 500K tweets/mois
💰 Coût : GRATUIT (puis $100/mois pour plus)

Étapes :
1. Aller sur developer.twitter.com
2. "Sign up for free account"
3. Décrire ton use case (trading bot research)
4. Attendre validation (1-2 jours)
5. Créer une App
6. Noter : TWITTER_BEARER_TOKEN="AAAAAxxxx"
```

### 5. **YAHOO FINANCE** (Gratuit via Python)
```
💡 Pas de clé requise ! Via bibliothèque yfinance
📦 Installation : pip install yfinance
🚀 Prêt à utiliser immédiatement
```

## 🟡 PHASE 2 : APIs PAYANTES (Une fois le système testé)

### 6. **DEXSCREENER** (Freemium)
```
🌐 Site : https://dexscreener.com/
📝 Contact : Via Discord ou Telegram
⏱️ Limite : Gratuit limité, puis $50/mois
💰 Pro nécessaire pour WebSocket temps réel

Note : Commencer avec l'API gratuite, upgrade si nécessaire
```

### 7. **LUNARCRUSH** (Payant)
```
🌐 Site : https://lunarcrush.com/
📝 Plan : $99/mois minimum
⏱️ Limite : Selon plan
💰 Essential pour sentiment analysis crypto

À activer une fois les tests gratuits validés
```

---

## ⚡ ORDRE DE PRIORITÉ POUR COMMENCER

1. ✅ **COINGECKO** (gratuit) - IMMÉDIAT
2. ✅ **ALPHA VANTAGE** (gratuit) - IMMÉDIAT  
3. ✅ **REDDIT** (gratuit) - IMMÉDIAT
4. 🔄 **TWITTER** (gratuit, validation 1-2j) - DÉMARRER MAINTENANT
5. 📦 **YAHOO FINANCE** (gratuit, pas de clé) - PRÊT

## 🎯 RÉSULTAT ATTENDU

Avec ces 5 APIs, tu auras :
- 📊 Prix crypto en temps réel (CoinGecko)
- 📈 Données stocks/forex/ETF (Alpha Vantage + Yahoo)
- 🧠 Sentiment Reddit crypto (Reddit API)
- 🐦 Trends Twitter crypto (Twitter API)
- 💰 Données historiques gratuites (Yahoo Finance)

**Budget Phase 1 : 0€/mois** 🎉 