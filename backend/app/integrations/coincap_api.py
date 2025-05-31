"""
💰 COINCAP API INTEGRATION - CRYPTO MARKET DATA
===============================================

Ce module intègre l'API CoinCap pour les données crypto générales :
- Market data en temps réel
- Historique des prix
- Informations sur les exchanges
- Données gratuites et illimitées
"""

import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import os

logger = logging.getLogger(__name__)

@dataclass
class CoinCapAsset:
    """Asset crypto CoinCap"""
    id: str
    rank: int
    symbol: str
    name: str
    supply: float
    max_supply: Optional[float]
    market_cap_usd: float
    volume_usd_24h: float
    price_usd: float
    change_percent_24h: float
    vwap_24h: float

@dataclass
class CoinCapCandle:
    """Chandelier OHLCV"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class CoinCapExchange:
    """Information exchange"""
    id: str
    name: str
    rank: int
    percent_total_volume: float
    volume_usd: float
    trading_pairs: int
    socket: bool
    exchange_url: str

class CoinCapAPIClient:
    """
    💰 CLIENT API COINCAP
    
    Interface avec l'API CoinCap pour les données crypto :
    - Données marché en temps réel
    - Historique des prix
    - Informations exchanges
    - API gratuite et illimitée
    """
    
    def __init__(self):
        self.api_key = os.getenv("COINCAP_API_KEY")
        self.base_url = os.getenv("COINCAP_BASE_URL", "https://api.coincap.io/v2")
        
        # Headers
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "TradingAI-Orchestrator/1.0"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Rate limiting
        self.last_request = 0
        self.min_interval = 0.1  # 100ms entre requêtes (très généreux)
        
        logger.info("💰 CoinCap API Client initialisé")

    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Faire une requête à l'API CoinCap"""
        
        try:
            # Rate limiting léger
            now = datetime.utcnow().timestamp()
            if now - self.last_request < self.min_interval:
                await asyncio.sleep(self.min_interval - (now - self.last_request))
            
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            async with aiohttp.ClientSession(
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as session:
                async with session.get(url, params=params) as response:
                    self.last_request = datetime.utcnow().timestamp()
                    
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f"❌ Erreur CoinCap API {response.status}: {await response.text()}")
                        return {"error": f"HTTP {response.status}"}
                        
        except Exception as e:
            logger.error(f"❌ Erreur requête CoinCap: {e}")
            return {"error": str(e)}

    async def get_top_assets(self, limit: int = 100) -> List[CoinCapAsset]:
        """
        📊 Obtenir les top assets crypto
        
        Args:
            limit: Nombre d'assets à récupérer (max 2000)
            
        Returns:
            Liste des top assets
        """
        try:
            params = {"limit": min(limit, 2000)}
            data = await self._make_request("assets", params)
            
            if "error" in data:
                logger.error(f"❌ Erreur top assets: {data['error']}")
                return []
            
            assets = []
            if "data" in data:
                for asset_data in data["data"]:
                    try:
                        asset = CoinCapAsset(
                            id=asset_data.get("id", ""),
                            rank=int(asset_data.get("rank", 0)),
                            symbol=asset_data.get("symbol", ""),
                            name=asset_data.get("name", ""),
                            supply=float(asset_data.get("supply", 0)),
                            max_supply=float(asset_data.get("maxSupply", 0)) if asset_data.get("maxSupply") else None,
                            market_cap_usd=float(asset_data.get("marketCapUsd", 0)),
                            volume_usd_24h=float(asset_data.get("volumeUsd24Hr", 0)),
                            price_usd=float(asset_data.get("priceUsd", 0)),
                            change_percent_24h=float(asset_data.get("changePercent24Hr", 0)),
                            vwap_24h=float(asset_data.get("vwap24Hr", 0))
                        )
                        assets.append(asset)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur parsing asset: {e}")
                        continue
            
            logger.info(f"📊 Récupéré {len(assets)} top assets")
            return assets
            
        except Exception as e:
            logger.error(f"❌ Erreur get_top_assets: {e}")
            return []

    async def get_asset_by_id(self, asset_id: str) -> Optional[CoinCapAsset]:
        """
        🔍 Obtenir un asset par ID
        
        Args:
            asset_id: ID de l'asset (ex: 'bitcoin', 'ethereum')
            
        Returns:
            Asset si trouvé, None sinon
        """
        try:
            data = await self._make_request(f"assets/{asset_id}")
            
            if "error" in data:
                logger.error(f"❌ Erreur asset {asset_id}: {data['error']}")
                return None
            
            if "data" in data:
                asset_data = data["data"]
                return CoinCapAsset(
                    id=asset_data.get("id", ""),
                    rank=int(asset_data.get("rank", 0)),
                    symbol=asset_data.get("symbol", ""),
                    name=asset_data.get("name", ""),
                    supply=float(asset_data.get("supply", 0)),
                    max_supply=float(asset_data.get("maxSupply", 0)) if asset_data.get("maxSupply") else None,
                    market_cap_usd=float(asset_data.get("marketCapUsd", 0)),
                    volume_usd_24h=float(asset_data.get("volumeUsd24Hr", 0)),
                    price_usd=float(asset_data.get("priceUsd", 0)),
                    change_percent_24h=float(asset_data.get("changePercent24Hr", 0)),
                    vwap_24h=float(asset_data.get("vwap24Hr", 0))
                )
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erreur get_asset_by_id: {e}")
            return None

    async def get_asset_history(self, 
                              asset_id: str,
                              interval: str = "d1",
                              start: Optional[datetime] = None,
                              end: Optional[datetime] = None) -> List[CoinCapCandle]:
        """
        📈 Obtenir l'historique des prix d'un asset
        
        Args:
            asset_id: ID de l'asset
            interval: Intervalle (m1, m5, m15, m30, h1, h2, h6, h12, d1)
            start: Date de début
            end: Date de fin
            
        Returns:
            Liste des chandelles OHLCV
        """
        try:
            params = {"interval": interval}
            
            if start:
                params["start"] = int(start.timestamp() * 1000)
            
            if end:
                params["end"] = int(end.timestamp() * 1000)
            
            data = await self._make_request(f"assets/{asset_id}/history", params)
            
            if "error" in data:
                logger.error(f"❌ Erreur historique {asset_id}: {data['error']}")
                return []
            
            candles = []
            if "data" in data:
                for point in data["data"]:
                    try:
                        candle = CoinCapCandle(
                            timestamp=datetime.fromtimestamp(int(point.get("time", 0)) / 1000),
                            open=float(point.get("priceUsd", 0)),
                            high=float(point.get("priceUsd", 0)),  # CoinCap ne fournit que le prix
                            low=float(point.get("priceUsd", 0)),
                            close=float(point.get("priceUsd", 0)),
                            volume=0.0  # Volume non disponible dans l'historique
                        )
                        candles.append(candle)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur parsing candle: {e}")
                        continue
            
            logger.info(f"📈 Récupéré {len(candles)} points historiques pour {asset_id}")
            return candles
            
        except Exception as e:
            logger.error(f"❌ Erreur get_asset_history: {e}")
            return []

    async def get_exchanges(self, limit: int = 50) -> List[CoinCapExchange]:
        """
        🏛️ Obtenir la liste des exchanges
        
        Args:
            limit: Nombre d'exchanges à récupérer
            
        Returns:
            Liste des exchanges
        """
        try:
            params = {"limit": limit}
            data = await self._make_request("exchanges", params)
            
            if "error" in data:
                logger.error(f"❌ Erreur exchanges: {data['error']}")
                return []
            
            exchanges = []
            if "data" in data:
                for exchange_data in data["data"]:
                    try:
                        exchange = CoinCapExchange(
                            id=exchange_data.get("id", ""),
                            name=exchange_data.get("name", ""),
                            rank=int(exchange_data.get("rank", 0)),
                            percent_total_volume=float(exchange_data.get("percentTotalVolume", 0)),
                            volume_usd=float(exchange_data.get("volumeUsd", 0)),
                            trading_pairs=int(exchange_data.get("tradingPairs", 0)),
                            socket=bool(exchange_data.get("socket", False)),
                            exchange_url=exchange_data.get("exchangeUrl", "")
                        )
                        exchanges.append(exchange)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur parsing exchange: {e}")
                        continue
            
            logger.info(f"🏛️ Récupéré {len(exchanges)} exchanges")
            return exchanges
            
        except Exception as e:
            logger.error(f"❌ Erreur get_exchanges: {e}")
            return []

    async def search_assets(self, query: str) -> List[CoinCapAsset]:
        """
        🔍 Rechercher des assets
        
        Args:
            query: Terme de recherche (nom ou symbole)
            
        Returns:
            Liste des assets correspondants
        """
        try:
            params = {"search": query}
            data = await self._make_request("assets", params)
            
            if "error" in data:
                logger.error(f"❌ Erreur recherche '{query}': {data['error']}")
                return []
            
            assets = []
            if "data" in data:
                for asset_data in data["data"]:
                    try:
                        # Filtrer par pertinence
                        name = asset_data.get("name", "").lower()
                        symbol = asset_data.get("symbol", "").lower()
                        query_lower = query.lower()
                        
                        if query_lower in name or query_lower in symbol:
                            asset = CoinCapAsset(
                                id=asset_data.get("id", ""),
                                rank=int(asset_data.get("rank", 0)),
                                symbol=asset_data.get("symbol", ""),
                                name=asset_data.get("name", ""),
                                supply=float(asset_data.get("supply", 0)),
                                max_supply=float(asset_data.get("maxSupply", 0)) if asset_data.get("maxSupply") else None,
                                market_cap_usd=float(asset_data.get("marketCapUsd", 0)),
                                volume_usd_24h=float(asset_data.get("volumeUsd24Hr", 0)),
                                price_usd=float(asset_data.get("priceUsd", 0)),
                                change_percent_24h=float(asset_data.get("changePercent24Hr", 0)),
                                vwap_24h=float(asset_data.get("vwap24Hr", 0))
                            )
                            assets.append(asset)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur parsing asset recherche: {e}")
                        continue
            
            logger.info(f"🔍 Trouvé {len(assets)} assets pour '{query}'")
            return assets[:20]  # Limiter à 20 résultats
            
        except Exception as e:
            logger.error(f"❌ Erreur search_assets: {e}")
            return []

    async def get_market_summary(self) -> Dict[str, Any]:
        """
        📊 Obtenir un résumé du marché global
        
        Returns:
            Résumé des métriques de marché
        """
        try:
            # Récupérer les top 10 assets
            top_assets = await self.get_top_assets(10)
            
            if not top_assets:
                return {"error": "Impossible de récupérer les données"}
            
            # Calculer les métriques globales
            total_market_cap = sum(asset.market_cap_usd for asset in top_assets)
            total_volume_24h = sum(asset.volume_usd_24h for asset in top_assets)
            
            # Moyennes pondérées
            weighted_change = sum(
                asset.change_percent_24h * asset.market_cap_usd 
                for asset in top_assets
            ) / total_market_cap if total_market_cap > 0 else 0
            
            # Dominance Bitcoin
            btc_dominance = 0
            if top_assets and top_assets[0].symbol == "BTC":
                btc_dominance = (top_assets[0].market_cap_usd / total_market_cap) * 100
            
            summary = {
                "timestamp": datetime.utcnow().isoformat(),
                "total_market_cap_usd": total_market_cap,
                "total_volume_24h_usd": total_volume_24h,
                "average_change_24h": round(weighted_change, 2),
                "btc_dominance_percent": round(btc_dominance, 2),
                "top_assets": [
                    {
                        "symbol": asset.symbol,
                        "name": asset.name,
                        "price_usd": asset.price_usd,
                        "change_24h": asset.change_percent_24h,
                        "market_cap_usd": asset.market_cap_usd
                    }
                    for asset in top_assets[:5]
                ],
                "market_sentiment": self._determine_market_sentiment(weighted_change),
                "data_source": "CoinCap"
            }
            
            logger.info("📊 Résumé marché généré avec succès")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Erreur get_market_summary: {e}")
            return {"error": str(e)}

    def _determine_market_sentiment(self, change_24h: float) -> str:
        """📈 Déterminer le sentiment du marché"""
        
        if change_24h > 5:
            return "très_haussier"
        elif change_24h > 2:
            return "haussier"
        elif change_24h > -2:
            return "neutre"
        elif change_24h > -5:
            return "baissier"
        else:
            return "très_baissier"

    async def get_multiple_assets(self, asset_ids: List[str]) -> List[CoinCapAsset]:
        """
        📊 Obtenir plusieurs assets en une fois
        
        Args:
            asset_ids: Liste des IDs d'assets
            
        Returns:
            Liste des assets trouvés
        """
        try:
            # CoinCap ne supporte pas les requêtes multiples directement
            # On fait des requêtes individuelles avec de l'asyncio
            tasks = [self.get_asset_by_id(asset_id) for asset_id in asset_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            assets = []
            for result in results:
                if isinstance(result, CoinCapAsset):
                    assets.append(result)
                elif isinstance(result, Exception):
                    logger.warning(f"⚠️ Erreur récupération asset: {result}")
            
            logger.info(f"📊 Récupéré {len(assets)}/{len(asset_ids)} assets demandés")
            return assets
            
        except Exception as e:
            logger.error(f"❌ Erreur get_multiple_assets: {e}")
            return []

# Instance globale
_coincap_client: Optional[CoinCapAPIClient] = None

def get_coincap_client() -> CoinCapAPIClient:
    """💰 Obtenir l'instance du client CoinCap"""
    global _coincap_client
    if _coincap_client is None:
        _coincap_client = CoinCapAPIClient()
    return _coincap_client 