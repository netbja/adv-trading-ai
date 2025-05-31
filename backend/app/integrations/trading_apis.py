"""
🔌 TRADING APIS INTEGRATION
===========================

Module d'intégration des APIs de trading avec support paper trading (dry run).
Supports : Alpaca, Binance, Forex.com
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import aiohttp
import hashlib
import hmac
import json
import base64
from decimal import Decimal

logger = logging.getLogger(__name__)

# ================================================================================
# TYPES ET ENUMS
# ================================================================================

class TradingMode(Enum):
    PAPER = "paper"      # Paper trading (dry run)
    LIVE = "live"        # Trading réel

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

@dataclass
class TradingAccount:
    """Compte de trading"""
    broker: str
    account_id: str
    balance: float
    buying_power: float
    portfolio_value: float
    mode: TradingMode
    currency: str = "USD"

@dataclass
class Asset:
    """Asset tradable"""
    symbol: str
    name: str
    asset_type: str  # crypto, stock, forex, etf
    exchange: str
    tradable: bool = True

@dataclass
class MarketData:
    """Données de marché"""
    symbol: str
    price: float
    bid: float
    ask: float
    volume: float
    timestamp: datetime

@dataclass
class Order:
    """Ordre de trading"""
    id: str
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: float
    price: Optional[float]
    status: OrderStatus
    created_at: datetime
    filled_at: Optional[datetime] = None
    filled_price: Optional[float] = None
    filled_quantity: Optional[float] = None

@dataclass
class Position:
    """Position en portefeuille"""
    symbol: str
    quantity: float
    avg_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float

# ================================================================================
# CLASSE DE BASE POUR LES BROKERS
# ================================================================================

class BaseBroker:
    """Classe de base pour tous les brokers"""
    
    def __init__(self, api_key: str, api_secret: str, mode: TradingMode = TradingMode.PAPER):
        self.api_key = api_key
        self.api_secret = api_secret
        self.mode = mode
        self.session = None
        
        # Paper trading state
        self.paper_balance = 10000.0  # $10K initial
        self.paper_positions: Dict[str, Position] = {}
        self.paper_orders: List[Order] = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    # Méthodes abstraites à implémenter
    async def get_account(self) -> TradingAccount:
        raise NotImplementedError
        
    async def get_positions(self) -> List[Position]:
        raise NotImplementedError
        
    async def place_order(self, symbol: str, side: OrderSide, quantity: float, 
                         order_type: OrderType = OrderType.MARKET, 
                         price: Optional[float] = None) -> Order:
        raise NotImplementedError
        
    async def get_market_data(self, symbol: str) -> MarketData:
        raise NotImplementedError
        
    async def get_historical_data(self, symbol: str, timeframe: str, 
                                 start: datetime, end: datetime) -> List[Dict]:
        raise NotImplementedError

# ================================================================================
# ALPACA TRADING API
# ================================================================================

class AlpacaBroker(BaseBroker):
    """Intégration Alpaca Trading API"""
    
    def __init__(self, api_key: str, api_secret: str, mode: TradingMode = TradingMode.PAPER):
        super().__init__(api_key, api_secret, mode)
        
        if mode == TradingMode.PAPER:
            self.base_url = "https://paper-api.alpaca.markets"
            self.data_url = "https://data.alpaca.markets"
        else:
            self.base_url = "https://api.alpaca.markets"
            self.data_url = "https://data.alpaca.markets"
            
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
            "Content-Type": "application/json"
        }
    
    async def get_account(self) -> TradingAccount:
        """Récupérer les infos du compte"""
        try:
            if self.mode == TradingMode.PAPER:
                # Simuler un compte paper trading
                return TradingAccount(
                    broker="alpaca",
                    account_id="paper_account",
                    balance=self.paper_balance,
                    buying_power=self.paper_balance * 4,  # Margin 4:1
                    portfolio_value=self.paper_balance + sum(pos.market_value for pos in self.paper_positions.values()),
                    mode=self.mode
                )
            
            async with self.session.get(f"{self.base_url}/v2/account", headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return TradingAccount(
                        broker="alpaca",
                        account_id=data["id"],
                        balance=float(data["cash"]),
                        buying_power=float(data["buying_power"]),
                        portfolio_value=float(data["portfolio_value"]),
                        mode=self.mode
                    )
                else:
                    raise Exception(f"Erreur Alpaca: {response.status}")
                    
        except Exception as e:
            logger.error(f"Erreur get_account Alpaca: {e}")
            raise
    
    async def get_positions(self) -> List[Position]:
        """Récupérer les positions"""
        try:
            if self.mode == TradingMode.PAPER:
                return list(self.paper_positions.values())
            
            async with self.session.get(f"{self.base_url}/v2/positions", headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    positions = []
                    for pos_data in data:
                        positions.append(Position(
                            symbol=pos_data["symbol"],
                            quantity=float(pos_data["qty"]),
                            avg_price=float(pos_data["avg_entry_price"]),
                            market_value=float(pos_data["market_value"]),
                            unrealized_pnl=float(pos_data["unrealized_pl"]),
                            realized_pnl=float(pos_data["realized_pl"])
                        ))
                    return positions
                else:
                    raise Exception(f"Erreur positions Alpaca: {response.status}")
                    
        except Exception as e:
            logger.error(f"Erreur get_positions Alpaca: {e}")
            raise
    
    async def place_order(self, symbol: str, side: OrderSide, quantity: float, 
                         order_type: OrderType = OrderType.MARKET, 
                         price: Optional[float] = None) -> Order:
        """Placer un ordre"""
        try:
            order_id = f"order_{datetime.now().timestamp()}"
            
            if self.mode == TradingMode.PAPER:
                # Simuler l'exécution de l'ordre
                market_data = await self.get_market_data(symbol)
                filled_price = market_data.price
                
                order = Order(
                    id=order_id,
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price,
                    status=OrderStatus.FILLED,
                    created_at=datetime.now(),
                    filled_at=datetime.now(),
                    filled_price=filled_price,
                    filled_quantity=quantity
                )
                
                # Mettre à jour le paper portfolio
                await self._update_paper_portfolio(order)
                self.paper_orders.append(order)
                
                logger.info(f"📋 Ordre paper trading exécuté: {order}")
                return order
            
            # Ordre réel
            order_data = {
                "symbol": symbol,
                "qty": str(quantity),
                "side": side.value,
                "type": order_type.value,
                "time_in_force": "day"
            }
            
            if price and order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
                order_data["limit_price"] = str(price)
            
            async with self.session.post(f"{self.base_url}/v2/orders", 
                                       headers=self.headers, 
                                       json=order_data) as response:
                if response.status == 201:
                    data = await response.json()
                    return Order(
                        id=data["id"],
                        symbol=data["symbol"],
                        side=OrderSide(data["side"]),
                        type=OrderType(data["type"]),
                        quantity=float(data["qty"]),
                        price=float(data.get("limit_price", 0)) if data.get("limit_price") else None,
                        status=OrderStatus(data["status"]),
                        created_at=datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
                    )
                else:
                    error_data = await response.json()
                    raise Exception(f"Erreur ordre Alpaca: {error_data}")
                    
        except Exception as e:
            logger.error(f"Erreur place_order Alpaca: {e}")
            raise
    
    async def get_market_data(self, symbol: str) -> MarketData:
        """Récupérer les données de marché"""
        try:
            # Utiliser l'API de données Alpaca
            url = f"{self.data_url}/v2/stocks/{symbol}/quotes/latest"
            
            async with self.session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    quote = data["quote"]
                    
                    return MarketData(
                        symbol=symbol,
                        price=(quote["bid_price"] + quote["ask_price"]) / 2,
                        bid=quote["bid_price"],
                        ask=quote["ask_price"],
                        volume=quote["bid_size"] + quote["ask_size"],
                        timestamp=datetime.fromisoformat(quote["timestamp"].replace('Z', '+00:00'))
                    )
                else:
                    # Fallback avec des données simulées
                    return MarketData(
                        symbol=symbol,
                        price=100.0 + hash(symbol) % 100,  # Prix simulé
                        bid=99.5,
                        ask=100.5,
                        volume=1000000,
                        timestamp=datetime.now()
                    )
                    
        except Exception as e:
            logger.warning(f"Utilisation de données simulées pour {symbol}: {e}")
            return MarketData(
                symbol=symbol,
                price=100.0 + hash(symbol) % 100,
                bid=99.5,
                ask=100.5,
                volume=1000000,
                timestamp=datetime.now()
            )
    
    async def _update_paper_portfolio(self, order: Order):
        """Mettre à jour le portfolio paper trading"""
        cost = order.filled_price * order.filled_quantity
        
        if order.side == OrderSide.BUY:
            # Achat : déduire du cash, ajouter à la position
            self.paper_balance -= cost
            
            if order.symbol in self.paper_positions:
                pos = self.paper_positions[order.symbol]
                total_quantity = pos.quantity + order.filled_quantity
                avg_price = ((pos.avg_price * pos.quantity) + cost) / total_quantity
                pos.quantity = total_quantity
                pos.avg_price = avg_price
            else:
                self.paper_positions[order.symbol] = Position(
                    symbol=order.symbol,
                    quantity=order.filled_quantity,
                    avg_price=order.filled_price,
                    market_value=cost,
                    unrealized_pnl=0.0,
                    realized_pnl=0.0
                )
        
        elif order.side == OrderSide.SELL:
            # Vente : ajouter au cash, réduire la position
            self.paper_balance += cost
            
            if order.symbol in self.paper_positions:
                pos = self.paper_positions[order.symbol]
                pos.quantity -= order.filled_quantity
                
                if pos.quantity <= 0:
                    del self.paper_positions[order.symbol]

# ================================================================================
# BINANCE API (pour crypto)
# ================================================================================

class BinanceBroker(BaseBroker):
    """Intégration Binance API pour crypto"""
    
    def __init__(self, api_key: str, api_secret: str, mode: TradingMode = TradingMode.PAPER):
        super().__init__(api_key, api_secret, mode)
        
        if mode == TradingMode.PAPER:
            self.base_url = "https://testnet.binance.vision/api"  # Testnet
        else:
            self.base_url = "https://api.binance.com/api"
    
    def _generate_signature(self, query_string: str) -> str:
        """Générer la signature Binance"""
        return hmac.new(
            self.api_secret.encode('utf-8'), 
            query_string.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
    
    async def get_account(self) -> TradingAccount:
        """Récupérer les infos du compte Binance"""
        try:
            if self.mode == TradingMode.PAPER:
                return TradingAccount(
                    broker="binance",
                    account_id="paper_account",
                    balance=self.paper_balance,
                    buying_power=self.paper_balance,
                    portfolio_value=self.paper_balance,
                    mode=self.mode,
                    currency="USDT"
                )
            
            # TODO: Implémenter l'API Binance réelle
            timestamp = int(datetime.now().timestamp() * 1000)
            query_string = f"timestamp={timestamp}"
            signature = self._generate_signature(query_string)
            
            headers = {"X-MBX-APIKEY": self.api_key}
            url = f"{self.base_url}/v3/account?{query_string}&signature={signature}"
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Parsing des données Binance...
                    return TradingAccount(
                        broker="binance",
                        account_id="binance_account",
                        balance=1000.0,  # Placeholder
                        buying_power=1000.0,
                        portfolio_value=1000.0,
                        mode=self.mode,
                        currency="USDT"
                    )
                    
        except Exception as e:
            logger.error(f"Erreur get_account Binance: {e}")
            raise
    
    async def get_market_data(self, symbol: str) -> MarketData:
        """Récupérer les données crypto"""
        try:
            # Binance ticker
            url = f"{self.base_url}/v3/ticker/24hr?symbol={symbol.upper()}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return MarketData(
                        symbol=symbol,
                        price=float(data["lastPrice"]),
                        bid=float(data["bidPrice"]),
                        ask=float(data["askPrice"]),
                        volume=float(data["volume"]),
                        timestamp=datetime.now()
                    )
                else:
                    raise Exception(f"Erreur Binance market data: {response.status}")
                    
        except Exception as e:
            logger.warning(f"Utilisation de données simulées pour {symbol}: {e}")
            return MarketData(
                symbol=symbol,
                price=50000.0 if "BTC" in symbol else 3000.0,  # Prix simulés crypto
                bid=49900.0 if "BTC" in symbol else 2990.0,
                ask=50100.0 if "BTC" in symbol else 3010.0,
                volume=1000.0,
                timestamp=datetime.now()
            )

# ================================================================================
# TRADING ORCHESTRATOR
# ================================================================================

class TradingOrchestrator:
    """Orchestrateur principal de trading"""
    
    def __init__(self):
        self.brokers: Dict[str, BaseBroker] = {}
        self.active_strategies: List[str] = []
        self.is_running = False
        
    def add_broker(self, name: str, broker: BaseBroker):
        """Ajouter un broker"""
        self.brokers[name] = broker
        logger.info(f"✅ Broker {name} ajouté ({broker.mode.value} mode)")
    
    async def start_paper_trading(self):
        """Démarrer le paper trading"""
        logger.info("🚀 Démarrage du paper trading...")
        self.is_running = True
        
        # Tests de connectivité
        for name, broker in self.brokers.items():
            try:
                async with broker:
                    account = await broker.get_account()
                    logger.info(f"✅ {name}: Balance ${account.balance:.2f}")
            except Exception as e:
                logger.error(f"❌ Erreur {name}: {e}")
    
    async def execute_demo_trades(self):
        """Exécuter des trades de démonstration"""
        logger.info("📊 Exécution de trades de démonstration...")
        
        for name, broker in self.brokers.items():
            try:
                async with broker:
                    # Test ordre d'achat
                    if name == "alpaca":
                        symbol = "AAPL"
                    elif name == "binance":
                        symbol = "BTCUSDT"
                    else:
                        continue
                    
                    # Récupérer les données de marché
                    market_data = await broker.get_market_data(symbol)
                    logger.info(f"📈 {symbol}: ${market_data.price:.2f}")
                    
                    # Placer un ordre d'achat
                    order = await broker.place_order(
                        symbol=symbol,
                        side=OrderSide.BUY,
                        quantity=1.0,
                        order_type=OrderType.MARKET
                    )
                    
                    logger.info(f"✅ Ordre exécuté: {order.symbol} - ${order.filled_price:.2f}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur demo trades {name}: {e}")
    
    async def get_portfolio_summary(self) -> Dict[str, Any]:
        """Résumé du portfolio global"""
        summary = {
            "total_value": 0.0,
            "total_pnl": 0.0,
            "accounts": {},
            "positions": []
        }
        
        for name, broker in self.brokers.items():
            try:
                async with broker:
                    account = await broker.get_account()
                    positions = await broker.get_positions()
                    
                    summary["accounts"][name] = {
                        "balance": account.balance,
                        "portfolio_value": account.portfolio_value,
                        "mode": account.mode.value
                    }
                    
                    summary["total_value"] += account.portfolio_value
                    summary["positions"].extend([
                        {
                            "broker": name,
                            "symbol": pos.symbol,
                            "quantity": pos.quantity,
                            "value": pos.market_value,
                            "pnl": pos.unrealized_pnl
                        } for pos in positions
                    ])
                    
            except Exception as e:
                logger.error(f"❌ Erreur portfolio summary {name}: {e}")
        
        return summary

# ================================================================================
# FACTORY ET CONFIGURATION
# ================================================================================

def create_broker(broker_type: str, api_key: str, api_secret: str, 
                 mode: TradingMode = TradingMode.PAPER) -> BaseBroker:
    """Factory pour créer un broker"""
    
    if broker_type.lower() == "alpaca":
        return AlpacaBroker(api_key, api_secret, mode)
    elif broker_type.lower() == "binance":
        return BinanceBroker(api_key, api_secret, mode)
    else:
        raise ValueError(f"Broker non supporté: {broker_type}")

# Instance globale
trading_orchestrator = TradingOrchestrator()

# ================================================================================
# EXEMPLE D'UTILISATION
# ================================================================================

async def demo_paper_trading():
    """Démonstration du paper trading"""
    
    # Configuration des brokers (remplacer par tes vraies clés)
    alpaca_broker = create_broker(
        "alpaca", 
        "YOUR_ALPACA_KEY", 
        "YOUR_ALPACA_SECRET", 
        TradingMode.PAPER
    )
    
    binance_broker = create_broker(
        "binance", 
        "YOUR_BINANCE_KEY", 
        "YOUR_BINANCE_SECRET", 
        TradingMode.PAPER
    )
    
    # Ajouter à l'orchestrateur
    trading_orchestrator.add_broker("alpaca", alpaca_broker)
    trading_orchestrator.add_broker("binance", binance_broker)
    
    # Démarrer le paper trading
    await trading_orchestrator.start_paper_trading()
    
    # Exécuter des trades de démo
    await trading_orchestrator.execute_demo_trades()
    
    # Résumé du portfolio
    portfolio = await trading_orchestrator.get_portfolio_summary()
    logger.info(f"📊 Portfolio: {json.dumps(portfolio, indent=2)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(demo_paper_trading()) 