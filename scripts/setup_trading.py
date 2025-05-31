#!/usr/bin/env python3
"""
🔧 SETUP TRADING - Configuration des brokers
============================================

Script pour configurer facilement les brokers de trading avec tes clés API.
Support paper trading et validation des connexions.
"""

import asyncio
import logging
import json
from typing import Dict, Any
import os
import sys

# Ajouter le chemin du backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.integrations.trading_apis import (
    create_broker, TradingMode, TradingOrchestrator,
    AlpacaBroker, BinanceBroker
)

logger = logging.getLogger(__name__)

# ================================================================================
# CONFIGURATION DES CLÉS API
# ================================================================================

# ⚠️ REMPLACE CES CLÉS PAR TES VRAIES CLÉS API
API_KEYS = {
    "alpaca": {
        "api_key": "YOUR_ALPACA_API_KEY",
        "api_secret": "YOUR_ALPACA_SECRET_KEY"
    },
    "binance": {
        "api_key": "YOUR_BINANCE_API_KEY", 
        "api_secret": "YOUR_BINANCE_SECRET_KEY"
    },
    "forex": {
        "api_key": "YOUR_FOREX_API_KEY",
        "api_secret": "YOUR_FOREX_SECRET_KEY"
    }
}

# ================================================================================
# FONCTIONS DE CONFIGURATION
# ================================================================================

async def test_broker_connection(broker_name: str, broker_config: Dict[str, str], mode: TradingMode = TradingMode.PAPER):
    """Tester la connexion à un broker"""
    try:
        print(f"\n🔌 Test de connexion {broker_name} ({mode.value})...")
        
        broker = create_broker(
            broker_name,
            broker_config["api_key"],
            broker_config["api_secret"],
            mode
        )
        
        async with broker:
            # Test account
            account = await broker.get_account()
            print(f"  ✅ Compte: ${account.balance:.2f} balance")
            
            # Test market data
            if broker_name == "alpaca":
                symbol = "AAPL"
            elif broker_name == "binance":
                symbol = "BTCUSDT"
            else:
                symbol = "EURUSD"
            
            market_data = await broker.get_market_data(symbol)
            print(f"  ✅ Market data: {symbol} = ${market_data.price:.2f}")
            
            return True, account, market_data
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False, None, None

async def setup_paper_trading():
    """Configuration complète du paper trading"""
    print("🧪 CONFIGURATION PAPER TRADING")
    print("=" * 50)
    
    orchestrator = TradingOrchestrator()
    successful_brokers = []
    
    for broker_name, config in API_KEYS.items():
        if config["api_key"] == f"YOUR_{broker_name.upper()}_API_KEY":
            print(f"\n⚠️  {broker_name}: Clés API non configurées (utilise des clés par défaut)")
            continue
            
        success, account, market_data = await test_broker_connection(broker_name, config, TradingMode.PAPER)
        
        if success:
            broker = create_broker(
                broker_name,
                config["api_key"], 
                config["api_secret"],
                TradingMode.PAPER
            )
            orchestrator.add_broker(broker_name, broker)
            successful_brokers.append(broker_name)
    
    if successful_brokers:
        print(f"\n🚀 Paper trading configuré avec succès!")
        print(f"   Brokers actifs: {', '.join(successful_brokers)}")
        
        # Test des trades de démonstration
        print(f"\n📊 Exécution de trades de démonstration...")
        await orchestrator.start_paper_trading()
        await orchestrator.execute_demo_trades()
        
        # Résumé du portfolio
        portfolio = await orchestrator.get_portfolio_summary()
        print(f"\n💰 Portfolio Summary:")
        print(f"   Total Value: ${portfolio['total_value']:.2f}")
        print(f"   Positions: {len(portfolio['positions'])}")
        
        return orchestrator
    else:
        print(f"\n❌ Aucun broker configuré avec succès")
        return None

async def demo_trading_strategies():
    """Démonstration des stratégies de trading"""
    print("\n🎯 DÉMONSTRATION STRATÉGIES DE TRADING")
    print("=" * 50)
    
    strategies = {
        "meme_coins": {
            "description": "Scalping meme coins haute volatilité",
            "assets": ["DOGEUSDT", "SHIBUSDT"],
            "capital": 0.2,
            "timeframe": "5m"
        },
        "crypto_lt": {
            "description": "DCA crypto long terme", 
            "assets": ["BTCUSDT", "ETHUSDT"],
            "capital": 0.4,
            "timeframe": "1d"
        },
        "forex": {
            "description": "Grid trading forex",
            "assets": ["EURUSD", "GBPUSD"],
            "capital": 0.25,
            "timeframe": "4h"
        },
        "etf": {
            "description": "Allocation ETF diversifiée",
            "assets": ["SPY", "QQQ"],
            "capital": 0.15,
            "timeframe": "1w"
        }
    }
    
    for strategy_name, config in strategies.items():
        print(f"\n📈 {strategy_name.upper()}:")
        print(f"   Description: {config['description']}")
        print(f"   Assets: {', '.join(config['assets'])}")
        print(f"   Capital: {config['capital']*100}%")
        print(f"   Timeframe: {config['timeframe']}")

async def validate_all_connections():
    """Valider toutes les connexions API"""
    print("🔍 VALIDATION DES CONNEXIONS API")
    print("=" * 50)
    
    results = {}
    
    for broker_name, config in API_KEYS.items():
        if config["api_key"] == f"YOUR_{broker_name.upper()}_API_KEY":
            results[broker_name] = {"status": "not_configured", "message": "Clés API non configurées"}
            continue
        
        # Test paper mode
        success_paper, account_paper, market_paper = await test_broker_connection(
            broker_name, config, TradingMode.PAPER
        )
        
        # Test live mode (sans placer d'ordres)
        success_live, account_live, market_live = await test_broker_connection(
            broker_name, config, TradingMode.LIVE
        )
        
        results[broker_name] = {
            "paper_mode": success_paper,
            "live_mode": success_live,
            "account_balance": account_paper.balance if account_paper else 0,
            "status": "ready" if success_paper else "error"
        }
    
    # Affichage du résumé
    print(f"\n📋 RÉSUMÉ DES CONNEXIONS:")
    for broker, result in results.items():
        status_emoji = "✅" if result["status"] == "ready" else "❌" if result["status"] == "error" else "⚠️"
        print(f"   {status_emoji} {broker.capitalize()}: {result['status']}")
    
    ready_brokers = [name for name, result in results.items() if result["status"] == "ready"]
    print(f"\n🎯 Brokers prêts pour trading: {len(ready_brokers)}/{len(API_KEYS)}")
    
    return results

def update_api_keys():
    """Interface pour mettre à jour les clés API"""
    print("🔧 CONFIGURATION DES CLÉS API")
    print("=" * 50)
    print("Pour configurer tes clés API, modifie les variables suivantes dans ce script:")
    print()
    
    for broker_name, config in API_KEYS.items():
        print(f"{broker_name.upper()}:")
        print(f'  api_key: "{config["api_key"]}"')
        print(f'  api_secret: "{config["api_secret"]}"')
        print()
    
    print("💡 CONSEILS:")
    print("1. Commence par les clés paper trading/testnet")
    print("2. Alpaca: utilise paper-api.alpaca.markets")
    print("3. Binance: utilise testnet.binance.vision")
    print("4. Teste les connexions avant le trading réel")
    print("5. Garde tes clés secrètes et sécurisées")

async def quick_paper_test():
    """Test rapide du paper trading"""
    print("⚡ TEST RAPIDE PAPER TRADING")
    print("=" * 50)
    
    # Test avec des clés factices pour la démo
    test_orchestrator = TradingOrchestrator()
    
    # Ajouter des brokers avec des clés de demo
    demo_alpaca = create_broker("alpaca", "demo_key", "demo_secret", TradingMode.PAPER)
    demo_binance = create_broker("binance", "demo_key", "demo_secret", TradingMode.PAPER)
    
    test_orchestrator.add_broker("alpaca", demo_alpaca)
    test_orchestrator.add_broker("binance", demo_binance)
    
    # Démarrer le paper trading
    await test_orchestrator.start_paper_trading()
    
    # Exécuter des trades de démo
    await test_orchestrator.execute_demo_trades()
    
    # Résumé
    portfolio = await test_orchestrator.get_portfolio_summary()
    print(f"\n✅ Paper trading opérationnel!")
    print(f"   Portfolio value: ${portfolio['total_value']:.2f}")
    print(f"   Positions: {len(portfolio['positions'])}")

async def main():
    """Menu principal"""
    print("🚀 SETUP TRADING AI - CONFIGURATION")
    print("=" * 50)
    print("1. Valider les connexions API")
    print("2. Configurer le paper trading")
    print("3. Test rapide (sans vraies clés)")
    print("4. Voir les stratégies disponibles")
    print("5. Configurer les clés API")
    print("0. Quitter")
    
    while True:
        choice = input("\n➡️  Choisis une option (0-5): ").strip()
        
        if choice == "0":
            print("👋 À bientôt!")
            break
        elif choice == "1":
            await validate_all_connections()
        elif choice == "2":
            await setup_paper_trading()
        elif choice == "3":
            await quick_paper_test()
        elif choice == "4":
            await demo_trading_strategies()
        elif choice == "5":
            update_api_keys()
        else:
            print("❌ Option invalide")

if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Arrêt du script")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc() 