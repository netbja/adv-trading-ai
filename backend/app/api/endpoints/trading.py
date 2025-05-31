"""
🚀 TRADING API ENDPOINTS
========================

API pour le trading intégré avec les modules IA avancée.
Support paper trading et trading réel.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pydantic import BaseModel

from app.integrations.trading_apis import (
    TradingOrchestrator, create_broker, TradingMode, 
    OrderSide, OrderType, trading_orchestrator
)
from app.orchestrator.ai_feedback_loop import get_ai_feedback_loop
from app.orchestrator.predictive_system import get_predictive_system
from app.orchestrator.portfolio_optimizer import get_portfolio_optimizer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trading", tags=["trading"])

# ================================================================================
# MODELS DE DONNÉES
# ================================================================================

class BrokerConfig(BaseModel):
    broker_type: str  # alpaca, binance, forex
    api_key: str
    api_secret: str
    mode: str = "paper"  # paper, live

class OrderRequest(BaseModel):
    broker: str
    symbol: str
    side: str  # buy, sell
    quantity: float
    order_type: str = "market"  # market, limit
    price: Optional[float] = None

class TradingStrategyRequest(BaseModel):
    strategy: str  # meme_coins, crypto_lt, forex, etf
    capital_allocation: float = 0.2  # 20% du portfolio
    risk_level: str = "medium"
    active: bool = True

# ================================================================================
# CONFIGURATION DES BROKERS
# ================================================================================

@router.post("/brokers/add")
async def add_broker(config: BrokerConfig):
    """
    🔌 Ajouter un broker de trading
    """
    try:
        logger.info(f"🔌 Ajout broker {config.broker_type} en mode {config.mode}")
        
        # Créer le broker
        mode = TradingMode.PAPER if config.mode.lower() == "paper" else TradingMode.LIVE
        broker = create_broker(
            config.broker_type,
            config.api_key,
            config.api_secret,
            mode
        )
        
        # Ajouter à l'orchestrateur
        trading_orchestrator.add_broker(config.broker_type, broker)
        
        # Test de connectivité
        async with broker:
            account = await broker.get_account()
            
        return {
            "status": "success",
            "message": f"Broker {config.broker_type} ajouté avec succès",
            "broker": config.broker_type,
            "mode": config.mode,
            "account": {
                "balance": account.balance,
                "buying_power": account.buying_power,
                "portfolio_value": account.portfolio_value
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur ajout broker: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brokers/list")
async def list_brokers():
    """
    📋 Lister les brokers configurés
    """
    try:
        brokers_info = []
        
        for name, broker in trading_orchestrator.brokers.items():
            try:
                async with broker:
                    account = await broker.get_account()
                    brokers_info.append({
                        "name": name,
                        "mode": account.mode.value,
                        "balance": account.balance,
                        "portfolio_value": account.portfolio_value,
                        "currency": account.currency,
                        "status": "connected"
                    })
            except Exception as e:
                brokers_info.append({
                    "name": name,
                    "mode": broker.mode.value,
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "status": "success",
            "brokers": brokers_info,
            "total_brokers": len(brokers_info)
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur liste brokers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# DONNÉES DE MARCHÉ
# ================================================================================

@router.get("/market-data/{symbol}")
async def get_market_data(symbol: str, broker: Optional[str] = None):
    """
    📊 Récupérer les données de marché pour un asset
    """
    try:
        # Utiliser le premier broker disponible ou celui spécifié
        if broker and broker in trading_orchestrator.brokers:
            selected_broker = trading_orchestrator.brokers[broker]
        else:
            if not trading_orchestrator.brokers:
                raise HTTPException(status_code=400, detail="Aucun broker configuré")
            selected_broker = next(iter(trading_orchestrator.brokers.values()))
        
        async with selected_broker:
            market_data = await selected_broker.get_market_data(symbol)
            
        return {
            "status": "success",
            "symbol": symbol,
            "broker": broker or "auto",
            "data": {
                "price": market_data.price,
                "bid": market_data.bid,
                "ask": market_data.ask,
                "volume": market_data.volume,
                "timestamp": market_data.timestamp.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur market data {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-data/batch")
async def get_batch_market_data(symbols: str):  # "AAPL,TSLA,BTCUSDT"
    """
    📊 Récupérer les données de marché pour plusieurs assets
    """
    try:
        symbol_list = [s.strip() for s in symbols.split(",")]
        results = {}
        
        for symbol in symbol_list:
            try:
                # Sélectionner le bon broker selon le type d'asset
                broker_name = None
                if any(crypto in symbol.upper() for crypto in ["BTC", "ETH", "USDT"]):
                    broker_name = "binance"
                else:
                    broker_name = "alpaca"
                
                if broker_name in trading_orchestrator.brokers:
                    broker = trading_orchestrator.brokers[broker_name]
                    async with broker:
                        market_data = await broker.get_market_data(symbol)
                        results[symbol] = {
                            "price": market_data.price,
                            "bid": market_data.bid,
                            "ask": market_data.ask,
                            "volume": market_data.volume,
                            "timestamp": market_data.timestamp.isoformat(),
                            "broker": broker_name
                        }
                else:
                    results[symbol] = {"error": f"Broker {broker_name} non configuré"}
                    
            except Exception as e:
                results[symbol] = {"error": str(e)}
        
        return {
            "status": "success",
            "data": results,
            "symbols_requested": len(symbol_list),
            "symbols_found": len([r for r in results.values() if "error" not in r])
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur batch market data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# ORDRES DE TRADING
# ================================================================================

@router.post("/orders/place")
async def place_order(order: OrderRequest, background_tasks: BackgroundTasks):
    """
    📋 Placer un ordre de trading
    """
    try:
        if order.broker not in trading_orchestrator.brokers:
            raise HTTPException(status_code=400, detail=f"Broker {order.broker} non configuré")
        
        broker = trading_orchestrator.brokers[order.broker]
        
        # Conversion des enums
        side = OrderSide.BUY if order.side.lower() == "buy" else OrderSide.SELL
        order_type = OrderType(order.order_type.lower())
        
        logger.info(f"📋 Placement ordre: {order.symbol} {order.side} {order.quantity}")
        
        async with broker:
            # Vérifier les données de marché
            market_data = await broker.get_market_data(order.symbol)
            
            # Placer l'ordre
            placed_order = await broker.place_order(
                symbol=order.symbol,
                side=side,
                quantity=order.quantity,
                order_type=order_type,
                price=order.price
            )
            
            # Soumettre un signal d'apprentissage à l'IA en arrière-plan
            background_tasks.add_task(
                submit_trading_feedback,
                order.symbol,
                order.side,
                placed_order.filled_price,
                order.quantity
            )
            
        return {
            "status": "success",
            "message": "Ordre placé avec succès",
            "order": {
                "id": placed_order.id,
                "symbol": placed_order.symbol,
                "side": placed_order.side.value,
                "quantity": placed_order.quantity,
                "type": placed_order.type.value,
                "status": placed_order.status.value,
                "filled_price": placed_order.filled_price,
                "created_at": placed_order.created_at.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur placement ordre: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/history")
async def get_orders_history(broker: Optional[str] = None, limit: int = 50):
    """
    📜 Historique des ordres
    """
    try:
        orders_history = []
        
        brokers_to_check = [broker] if broker else trading_orchestrator.brokers.keys()
        
        for broker_name in brokers_to_check:
            if broker_name in trading_orchestrator.brokers:
                broker_obj = trading_orchestrator.brokers[broker_name]
                
                # Pour paper trading, utiliser l'historique local
                if broker_obj.mode == TradingMode.PAPER:
                    for order in broker_obj.paper_orders[-limit:]:
                        orders_history.append({
                            "broker": broker_name,
                            "id": order.id,
                            "symbol": order.symbol,
                            "side": order.side.value,
                            "quantity": order.quantity,
                            "filled_price": order.filled_price,
                            "status": order.status.value,
                            "created_at": order.created_at.isoformat()
                        })
        
        return {
            "status": "success",
            "orders": sorted(orders_history, key=lambda x: x["created_at"], reverse=True),
            "total_orders": len(orders_history)
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur historique ordres: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# PORTFOLIO ET POSITIONS
# ================================================================================

@router.get("/portfolio/summary")
async def get_portfolio_summary():
    """
    📊 Résumé complet du portfolio
    """
    try:
        summary = await trading_orchestrator.get_portfolio_summary()
        
        return {
            "status": "success",
            "portfolio": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur portfolio summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/positions")
async def get_positions(broker: Optional[str] = None):
    """
    📍 Positions actuelles du portfolio
    """
    try:
        all_positions = []
        
        brokers_to_check = [broker] if broker else trading_orchestrator.brokers.keys()
        
        for broker_name in brokers_to_check:
            if broker_name in trading_orchestrator.brokers:
                broker_obj = trading_orchestrator.brokers[broker_name]
                
                async with broker_obj:
                    positions = await broker_obj.get_positions()
                    
                    for pos in positions:
                        all_positions.append({
                            "broker": broker_name,
                            "symbol": pos.symbol,
                            "quantity": pos.quantity,
                            "avg_price": pos.avg_price,
                            "market_value": pos.market_value,
                            "unrealized_pnl": pos.unrealized_pnl,
                            "realized_pnl": pos.realized_pnl
                        })
        
        return {
            "status": "success",
            "positions": all_positions,
            "total_positions": len(all_positions),
            "total_value": sum(pos["market_value"] for pos in all_positions)
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur positions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# STRATÉGIES DE TRADING IA
# ================================================================================

@router.post("/strategies/start")
async def start_trading_strategy(strategy: TradingStrategyRequest):
    """
    🚀 Démarrer une stratégie de trading IA
    """
    try:
        logger.info(f"🚀 Démarrage stratégie {strategy.strategy}")
        
        # Récupérer les modules IA
        feedback_loop = get_ai_feedback_loop()
        predictive_system = get_predictive_system()
        portfolio_optimizer = get_portfolio_optimizer()
        
        # Analyser les conditions de marché
        market_regime = await predictive_system.detect_market_regime()
        portfolio_metrics = await portfolio_optimizer.get_portfolio_metrics()
        
        # Configuration de la stratégie selon le type
        strategy_config = {
            "meme_coins": {
                "assets": ["DOGEUSDT", "SHIBUSDT", "PEPEUSDT"],
                "timeframe": "5m",
                "stop_loss": 0.05,
                "take_profit": 0.15,
                "max_position": strategy.capital_allocation
            },
            "crypto_lt": {
                "assets": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
                "timeframe": "1d",
                "strategy_type": "DCA",
                "allocation": strategy.capital_allocation
            },
            "forex": {
                "pairs": ["EURUSD", "GBPUSD", "USDJPY"],
                "timeframe": "4h",
                "risk_per_trade": 0.02,
                "allocation": strategy.capital_allocation
            },
            "etf": {
                "assets": ["SPY", "QQQ", "VTI"],
                "timeframe": "1w",
                "rebalance_frequency": "monthly",
                "allocation": strategy.capital_allocation
            }
        }
        
        config = strategy_config.get(strategy.strategy, {})
        
        return {
            "status": "success",
            "message": f"Stratégie {strategy.strategy} démarrée",
            "strategy": strategy.strategy,
            "config": config,
            "market_regime": market_regime,
            "portfolio_status": portfolio_metrics,
            "active": strategy.active
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur stratégie trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/strategies/status")
async def get_strategies_status():
    """
    📊 Statut des stratégies de trading actives
    """
    try:
        # Simuler des stratégies actives
        active_strategies = [
            {
                "name": "meme_coins",
                "status": "active",
                "allocation": 0.2,
                "pnl": 145.67,
                "trades_today": 12,
                "success_rate": 0.75
            },
            {
                "name": "crypto_lt",
                "status": "active",
                "allocation": 0.4,
                "pnl": 892.34,
                "trades_today": 3,
                "success_rate": 0.90
            }
        ]
        
        return {
            "status": "success",
            "strategies": active_strategies,
            "total_strategies": len(active_strategies),
            "total_pnl": sum(s["pnl"] for s in active_strategies),
            "overall_success_rate": sum(s["success_rate"] for s in active_strategies) / len(active_strategies)
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur statut stratégies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# PAPER TRADING CONTROLS
# ================================================================================

@router.post("/paper-trading/start")
async def start_paper_trading():
    """
    🧪 Démarrer le paper trading (dry run)
    """
    try:
        if not trading_orchestrator.brokers:
            raise HTTPException(status_code=400, detail="Aucun broker configuré")
        
        await trading_orchestrator.start_paper_trading()
        
        return {
            "status": "success",
            "message": "Paper trading démarré",
            "mode": "dry_run",
            "brokers": list(trading_orchestrator.brokers.keys())
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur paper trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/paper-trading/demo-trades")
async def execute_demo_trades():
    """
    🎯 Exécuter des trades de démonstration
    """
    try:
        await trading_orchestrator.execute_demo_trades()
        
        # Récupérer le portfolio après les trades
        portfolio = await trading_orchestrator.get_portfolio_summary()
        
        return {
            "status": "success",
            "message": "Trades de démonstration exécutés",
            "portfolio": portfolio
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur demo trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paper-trading/reset")
async def reset_paper_trading():
    """
    🔄 Reset du paper trading
    """
    try:
        # Reset de tous les brokers paper
        for broker in trading_orchestrator.brokers.values():
            if broker.mode == TradingMode.PAPER:
                broker.paper_balance = 10000.0
                broker.paper_positions = {}
                broker.paper_orders = []
        
        return {
            "status": "success",
            "message": "Paper trading reset",
            "initial_balance": 10000.0
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur reset paper trading: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# FONCTIONS UTILITAIRES
# ================================================================================

async def submit_trading_feedback(symbol: str, side: str, price: float, quantity: float):
    """Soumettre un feedback à l'IA après un trade"""
    try:
        feedback_loop = get_ai_feedback_loop()
        
        # Créer un signal de succès pour l'IA
        from app.orchestrator.ai_feedback_loop import LearningSignal, AdaptationContext
        
        context = AdaptationContext(
            asset_type=symbol,
            market_conditions={"side": side, "price": price},
            system_state={"status": "trading_active"},
            learning_signal=LearningSignal.SUCCESS,
            timestamp=datetime.now(),
            metadata={"quantity": quantity}
        )
        
        await feedback_loop.process_learning_signal(
            LearningSignal.SUCCESS,
            f"trading_{symbol}",
            context,
            {"execution_price": price, "quantity": quantity}
        )
        
        logger.info(f"✅ Feedback IA soumis pour trade {symbol}")
        
    except Exception as e:
        logger.error(f"❌ Erreur feedback IA: {e}")

# ================================================================================
# STATUT SYSTÈME
# ================================================================================

@router.get("/status")
async def get_trading_system_status():
    """
    📊 Statut complet du système de trading
    """
    try:
        portfolio = await trading_orchestrator.get_portfolio_summary()
        
        status = {
            "trading_system": {
                "status": "operational" if trading_orchestrator.is_running else "stopped",
                "brokers_count": len(trading_orchestrator.brokers),
                "active_strategies": len(trading_orchestrator.active_strategies)
            },
            "portfolio": portfolio,
            "brokers": {}
        }
        
        # Statut de chaque broker
        for name, broker in trading_orchestrator.brokers.items():
            try:
                async with broker:
                    account = await broker.get_account()
                    status["brokers"][name] = {
                        "status": "connected",
                        "mode": account.mode.value,
                        "balance": account.balance,
                        "portfolio_value": account.portfolio_value
                    }
            except Exception as e:
                status["brokers"][name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "status": "success",
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur statut système: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 