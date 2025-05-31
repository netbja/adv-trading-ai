#!/usr/bin/env python3
"""
🧪 TEST DE CONNECTIVITÉ APIs - TRADING AI BOT
Script pour valider toutes les connexions API avant lancement
"""

import os
import sys
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

def test_coingecko():
    """Test CoinGecko API (crypto data)"""
    print("🔍 Test CoinGecko...")
    try:
        api_key = os.getenv('COINGECKO_API_KEY')
        
        # Test sans clé (gratuit)
        if not api_key:
            url = "https://api.coingecko.com/api/v3/ping"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print("✅ CoinGecko: Connecté (gratuit)")
                
                # Test prix Bitcoin
                price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
                price_response = requests.get(price_url, timeout=10)
                if price_response.status_code == 200:
                    price_data = price_response.json()
                    btc_price = price_data['bitcoin']['usd']
                    print(f"   📊 Bitcoin: ${btc_price:,.2f}")
                return True
        else:
            # Test avec clé API
            headers = {'x-cg-demo-api-key': api_key}
            url = "https://api.coingecko.com/api/v3/ping"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ CoinGecko: Connecté (API Key)")
                return True
            
        print(f"❌ CoinGecko: HTTP {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ CoinGecko: {e}")
        return False

def test_alpha_vantage():
    """Test Alpha Vantage API (stocks/forex)"""
    print("🔍 Test Alpha Vantage...")
    try:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            print("⚠️ Alpha Vantage: Clé API manquante")
            return False
            
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={api_key}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'Global Quote' in data:
                price = data['Global Quote']['05. price']
                symbol = data['Global Quote']['01. symbol']
                print(f"✅ Alpha Vantage: Connecté")
                print(f"   📊 {symbol}: ${float(price):,.2f}")
                return True
            elif 'Error Message' in data:
                print(f"❌ Alpha Vantage: {data['Error Message']}")
                return False
            elif 'Note' in data:
                print(f"⚠️ Alpha Vantage: Rate limit - {data['Note']}")
                return False
            else:
                print(f"❌ Alpha Vantage: Format inattendu - {data}")
                return False
        else:
            print(f"❌ Alpha Vantage: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Alpha Vantage: {e}")
        return False

def test_yahoo_finance():
    """Test Yahoo Finance (via yfinance si disponible)"""
    print("🔍 Test Yahoo Finance...")
    try:
        # Test simple via API Yahoo
        url = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'chart' in data and data['chart']['result']:
                price_data = data['chart']['result'][0]['meta']
                price = price_data['regularMarketPrice']
                symbol = price_data['symbol']
                print(f"✅ Yahoo Finance: Connecté")
                print(f"   📊 {symbol}: ${price:,.2f}")
                return True
        
        print(f"❌ Yahoo Finance: HTTP {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ Yahoo Finance: {e}")
        return False

def test_reddit():
    """Test Reddit API"""
    print("🔍 Test Reddit...")
    try:
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            print("⚠️ Reddit: Identifiants manquants")
            return False
        
        # Authentification Reddit
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        data = {
            'grant_type': 'client_credentials'
        }
        headers = {'User-Agent': 'TradingBot/1.0'}
        
        # Obtenir token
        token_response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=auth,
            data=data,
            headers=headers,
            timeout=10
        )
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data['access_token']
            
            # Test requête avec token
            headers['Authorization'] = f"Bearer {access_token}"
            subreddit_response = requests.get(
                'https://oauth.reddit.com/r/cryptocurrency/hot.json?limit=1',
                headers=headers,
                timeout=10
            )
            
            if subreddit_response.status_code == 200:
                subreddit_data = subreddit_response.json()
                if 'data' in subreddit_data and 'children' in subreddit_data['data']:
                    posts = subreddit_data['data']['children']
                    if posts:
                        post_title = posts[0]['data']['title']
                        print("✅ Reddit: Connecté")
                        print(f"   📈 Dernier post: {post_title[:50]}...")
                        return True
        
        print(f"❌ Reddit: Échec authentification")
        return False
        
    except Exception as e:
        print(f"❌ Reddit: {e}")
        return False

def test_twitter():
    """Test Twitter API"""
    print("🔍 Test Twitter...")
    try:
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        if not bearer_token:
            print("⚠️ Twitter: Bearer token manquant")
            return False
        
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'TradingBot/1.0'
        }
        
        # Test recherche tweets
        url = "https://api.twitter.com/2/tweets/search/recent"
        params = {
            'query': 'bitcoin',
            'max_results': 10,
            'tweet.fields': 'created_at,public_metrics'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                tweet_count = len(data['data'])
                latest_tweet = data['data'][0]['text']
                print("✅ Twitter: Connecté")
                print(f"   🐦 Trouvé {tweet_count} tweets récents")
                print(f"   📝 Dernier: {latest_tweet[:50]}...")
                return True
            else:
                print("❌ Twitter: Pas de données récupérées")
                return False
        elif response.status_code == 401:
            print("❌ Twitter: Authentification invalide")
            return False
        elif response.status_code == 429:
            print("⚠️ Twitter: Rate limit atteint")
            return True  # Connexion OK mais rate limited
        else:
            print(f"❌ Twitter: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Twitter: {e}")
        return False

def test_alpaca():
    """Test Alpaca API (trading)"""
    print("🔍 Test Alpaca...")
    try:
        api_key = os.getenv('ALPACA_API_KEY')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        base_url = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
        
        if not api_key or not secret_key:
            print("⚠️ Alpaca: Identifiants manquants")
            return False
        
        headers = {
            'APCA-API-KEY-ID': api_key,
            'APCA-API-SECRET-KEY': secret_key
        }
        
        # Test account info
        response = requests.get(f'{base_url}/v2/account', headers=headers, timeout=10)
        
        if response.status_code == 200:
            account_data = response.json()
            buying_power = float(account_data.get('buying_power', 0))
            account_status = account_data.get('status', 'unknown')
            print("✅ Alpaca: Connecté")
            print(f"   💰 Buying Power: ${buying_power:,.2f}")
            print(f"   📊 Status: {account_status}")
            return True
        else:
            print(f"❌ Alpaca: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Alpaca: {e}")
        return False

def test_groq():
    """Test Groq API (AI)"""
    print("🔍 Test Groq...")
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("⚠️ Groq: Clé API manquante")
            return False
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test simple avec un prompt minimal
        data = {
            'messages': [{'role': 'user', 'content': 'Hello'}],
            'model': 'llama3-8b-8192',
            'max_tokens': 10
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and response_data['choices']:
                print("✅ Groq: Connecté")
                print("   🧠 Modèle IA opérationnel")
                return True
        
        print(f"❌ Groq: HTTP {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ Groq: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST DE CONNECTIVITÉ APIs - TRADING AI BOT")
    print("=" * 50)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Définir tous les tests
    tests = [
        ("CoinGecko (Crypto)", test_coingecko),
        ("Alpha Vantage (Stocks/Forex)", test_alpha_vantage),
        ("Yahoo Finance (Backup)", test_yahoo_finance),
        ("Reddit (Sentiment)", test_reddit),
        ("Twitter (Trends)", test_twitter),
        ("Alpaca (Trading)", test_alpaca),
        ("Groq (AI)", test_groq)
    ]
    
    # Exécuter tous les tests
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Test {name}...")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            results.append((name, False))
        print("-" * 30)
    
    # Afficher le résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    success_count = 0
    critical_apis = ["CoinGecko (Crypto)", "Alpaca (Trading)", "Groq (AI)"]
    critical_success = 0
    
    for name, success in results:
        status_emoji = "✅" if success else "❌"
        print(f"{status_emoji} {name}")
        
        if success:
            success_count += 1
            if name in critical_apis:
                critical_success += 1
        elif name in critical_apis:
            print(f"   ⚠️ API CRITIQUE EN ÉCHEC!")
    
    print(f"\n🎯 Score Global: {success_count}/{len(tests)} APIs fonctionnelles")
    print(f"🔥 APIs Critiques: {critical_success}/{len(critical_apis)} opérationnelles")
    
    # Évaluation finale
    if success_count == len(tests):
        print("\n🎉 PARFAIT! Tous les tests réussis.")
        print("🚀 Le système est prêt pour le lancement complet!")
        return 0
    elif critical_success == len(critical_apis) and success_count >= 5:
        print("\n✅ EXCELLENT! APIs critiques OK.")
        print("🚀 Le système peut être lancé avec succès!")
        return 0
    elif critical_success >= 2:
        print("\n⚠️ ACCEPTABLE. Quelques APIs optionnelles en échec.")
        print("🔄 Le système peut fonctionner mais avec limitations.")
        return 1
    else:
        print("\n🚨 PROBLÈME! Trop d'APIs critiques en échec.")
        print("🛠️ Vérifier la configuration avant de continuer.")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 