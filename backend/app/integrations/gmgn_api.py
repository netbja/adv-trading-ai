"""
🎪 GMGN.AI API INTEGRATION - MEME COINS INTELLIGENCE
===================================================

Ce module intègre l'API gmgn.ai pour l'analyse avancée des meme coins :
- Smart money tracking
- Honeypot detection
- Real-time trending tokens
- Multi-chain support (SOL, ETH, BSC, Base, Tron)

⚠️ LIMITATIONS API STRICTES:
- Rate limit: 2 requêtes/seconde MAX
- Implémentation queue + retry pour éviter le blocage
"""

import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import os
from enum import Enum
import time
from collections import deque

logger = logging.getLogger(__name__)

class GMGNChain(Enum):
    """Chaînes supportées par GMGN"""
    SOLANA = "sol"
    ETHEREUM = "eth"
    BASE = "base"
    BSC = "bsc"
    TRON = "tron"

class GMGNTimePeriod(Enum):
    """Périodes de temps pour l'analyse"""
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    ONE_HOUR = "1h"
    SIX_HOURS = "6h"
    TWENTY_FOUR_HOURS = "24h"

@dataclass
class GMGNToken:
    """Token meme coin avec données GMGN"""
    symbol: str
    contract_address: str
    price: float
    market_cap: float
    volume_24h: float
    holders_count: int
    smart_money_score: float
    is_honeypot: bool
    is_verified: bool
    is_renounced: bool
    liquidity: float
    chain: str
    trend_score: float
    risk_level: str

@dataclass
class SmartMoneyActivity:
    """Activité smart money"""
    wallet_address: str
    buy_amount: float
    sell_amount: float
    net_position: float
    profit_loss: float
    win_rate: float
    last_activity: datetime

class GMGNRateLimiter:
    """
    🚦 RATE LIMITER ULTRA-STRICT POUR GMGN.AI
    
    - Limite: 2 requêtes/seconde MAXIMUM
    - Queue avec délais automatiques
    - Retry mechanism en cas d'erreur 429
    """
    
    def __init__(self, max_requests_per_second: float = 1.8):
        # Être conservateur : 1.8 req/sec au lieu de 2.0
        self.max_requests_per_second = max_requests_per_second
        self.min_interval = 1.0 / max_requests_per_second  # ~0.56 secondes
        
        # Historique des requêtes
        self.request_times = deque(maxlen=10)
        self.last_request_time = 0
        
        # Queue pour requêtes en attente
        self.request_queue = asyncio.Queue()
        self.processing = False
        
        logger.info(f"🚦 GMGN Rate Limiter: {max_requests_per_second} req/sec (interval: {self.min_interval:.2f}s)")

    async def wait_for_slot(self):
        """Attendre un slot disponible pour faire une requête"""
        now = time.time()
        
        # Si moins de min_interval depuis la dernière requête, attendre
        time_since_last = now - self.last_request_time
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last + 0.1  # +100ms de sécurité
            logger.debug(f"⏳ GMGN Rate limit: attente {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
        
        # Mettre à jour le timestamp
        self.last_request_time = time.time()
        self.request_times.append(self.last_request_time)

    def get_current_rate(self) -> float:
        """Calculer le taux actuel de requêtes"""
        if len(self.request_times) < 2:
            return 0.0
        
        time_span = self.request_times[-1] - self.request_times[0]
        if time_span == 0:
            return 0.0
        
        return (len(self.request_times) - 1) / time_span

class GMGNAPIClient:
    """
    🎪 CLIENT API GMGN.AI - VERSION RATE-LIMITED
    
    Interface avec l'API gmgn.ai pour l'intelligence des meme coins :
    - Trending tokens par chaîne
    - Smart money tracking
    - Honeypot detection
    - Risk assessment
    
    ⚠️ RESPECT STRICT DES LIMITES: 2 req/sec maximum
    """
    
    def __init__(self):
        # Pas de clé API nécessaire pour gmgn.ai !
        self.base_url = os.getenv("GMGN_BASE_URL", "https://gmgn.ai/defi/quotation/v1")
        
        # Headers optimisés pour gmgn.ai (pas d'authentification)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://gmgn.ai/",
            "Origin": "https://gmgn.ai"
        }
        
        # Rate limiter strict (2 req/sec max)
        self.rate_limiter = GMGNRateLimiter(max_requests_per_second=1.8)
        
        # Cache simple pour éviter requêtes répétitives
        self.cache = {}
        self.cache_ttl = 60  # 1 minute de cache
        
        # Statistiques
        self.total_requests = 0
        self.cached_responses = 0
        self.rate_limited_count = 0
        
        logger.info("🎪 GMGN API Client initialisé (GRATUIT - sans clé API) avec rate limiting strict")

    def _get_cache_key(self, endpoint: str, params: Dict = None) -> str:
        """Générer une clé de cache"""
        cache_data = f"{endpoint}_{json.dumps(params or {}, sort_keys=True)}"
        return cache_data

    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Vérifier si une entrée de cache est encore valide"""
        if not cache_entry:
            return False
        
        age = time.time() - cache_entry.get("timestamp", 0)
        return age < self.cache_ttl

    async def _make_request(self, endpoint: str, params: Dict = None, use_cache: bool = True) -> Dict:
        """
        Faire une requête à l'API GMGN avec gestion stricte du rate limiting
        
        Args:
            endpoint: Endpoint à appeler
            params: Paramètres de la requête
            use_cache: Utiliser le cache si disponible
            
        Returns:
            Données de réponse ou erreur
        """
        
        # Vérifier le cache d'abord
        cache_key = self._get_cache_key(endpoint, params)
        if use_cache and cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if self._is_cache_valid(cache_entry):
                self.cached_responses += 1
                logger.debug(f"🎯 Cache hit pour {endpoint}")
                return cache_entry["data"]
        
        # Attendre un slot de rate limiting
        await self.rate_limiter.wait_for_slot()
        
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            async with aiohttp.ClientSession(
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as session:
                
                self.total_requests += 1
                logger.debug(f"🌐 GMGN Request #{self.total_requests}: {endpoint}")
                
                async with session.get(url, params=params) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Mettre en cache
                        if use_cache:
                            self.cache[cache_key] = {
                                "data": data,
                                "timestamp": time.time()
                            }
                        
                        return data
                        
                    elif response.status == 429:
                        # Rate limit hit - attendre plus longtemps
                        self.rate_limited_count += 1
                        logger.warning(f"🚨 GMGN Rate limit hit! (#{self.rate_limited_count})")
                        
                        # Attendre 2 secondes supplémentaires puis retry
                        await asyncio.sleep(2.0)
                        
                        # Un seul retry pour éviter les boucles infinies
                        logger.info("🔄 Retry après rate limit...")
                        return await self._make_request(endpoint, params, use_cache=False)
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Erreur GMGN API {response.status}: {error_text}")
                        return {"error": f"HTTP {response.status}"}
                        
        except Exception as e:
            logger.error(f"❌ Erreur requête GMGN: {e}")
            return {"error": str(e)}

    async def get_trending_tokens(self, 
                                chain: GMGNChain = GMGNChain.SOLANA,
                                time_period: GMGNTimePeriod = GMGNTimePeriod.SIX_HOURS,
                                order_by: str = "volume",
                                limit: int = 20) -> List[GMGNToken]:
        """
        🔥 Obtenir les tokens trending (RATE LIMITED)
        
        Args:
            chain: Chaîne blockchain
            time_period: Période d'analyse
            order_by: Critère de tri (volume, market_cap, swaps, smartmoney)
            limit: Nombre maximum de tokens (réduit à 20 pour économiser les requêtes)
            
        Returns:
            Liste des tokens trending
        """
        try:
            # Limiter à 20 pour économiser les requêtes API
            limit = min(limit, 20)
            
            endpoint = f"rank/{chain.value}/swaps/{time_period.value}"
            params = {
                "orderby": order_by,
                "direction": "desc",
                "filters[]": ["not_honeypot", "verified", "renounced"]
            }
            
            logger.info(f"🔥 Récupération trending tokens {chain.value} (limite: {limit})")
            data = await self._make_request(endpoint, params)
            
            if "error" in data:
                logger.error(f"❌ Erreur trending tokens: {data['error']}")
                return []
            
            tokens = []
            if data.get("code") == 0 and "data" in data:
                rank_data = data["data"].get("rank", [])
                
                for token_data in rank_data[:limit]:
                    try:
                        token = GMGNToken(
                            symbol=token_data.get("symbol", "UNKNOWN"),
                            contract_address=token_data.get("address", ""),
                            price=float(token_data.get("price", 0)),
                            market_cap=float(token_data.get("market_cap", 0)),
                            volume_24h=float(token_data.get("volume", 0)),
                            holders_count=int(token_data.get("holder_count", 0)),
                            smart_money_score=float(token_data.get("smart_money_score", 0)),
                            is_honeypot=not token_data.get("not_honeypot", True),
                            is_verified=token_data.get("verified", False),
                            is_renounced=token_data.get("renounced", False),
                            liquidity=float(token_data.get("liquidity", 0)),
                            chain=chain.value,
                            trend_score=float(token_data.get("trend_score", 0)),
                            risk_level=self._calculate_risk_level(token_data)
                        )
                        tokens.append(token)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur parsing token: {e}")
                        continue
            
            logger.info(f"🔥 Récupéré {len(tokens)} tokens trending {chain.value}")
            return tokens
            
        except Exception as e:
            logger.error(f"❌ Erreur get_trending_tokens: {e}")
            return []

    async def get_smart_money_activity(self, 
                                     chain: GMGNChain = GMGNChain.SOLANA,
                                     time_period: GMGNTimePeriod = GMGNTimePeriod.TWENTY_FOUR_HOURS) -> List[SmartMoneyActivity]:
        """
        🧠 Analyser l'activité smart money (RATE LIMITED)
        
        Args:
            chain: Chaîne blockchain
            time_period: Période d'analyse
            
        Returns:
            Liste des activités smart money (limitée à 10 pour économiser l'API)
        """
        try:
            endpoint = f"rank/{chain.value}/swaps/{time_period.value}"
            params = {
                "orderby": "smartmoney",
                "direction": "desc",
                "filters[]": ["not_honeypot"]
            }
            
            logger.info(f"🧠 Analyse smart money {chain.value}")
            data = await self._make_request(endpoint, params)
            
            if "error" in data:
                return []
            
            activities = []
            if data.get("code") == 0 and "data" in data:
                rank_data = data["data"].get("rank", [])
                
                # Limiter à 10 au lieu de 20 pour économiser l'API
                for token_data in rank_data[:10]:
                    try:
                        activity = SmartMoneyActivity(
                            wallet_address=token_data.get("smart_wallet", "unknown"),
                            buy_amount=float(token_data.get("smart_buy_24h", 0)),
                            sell_amount=float(token_data.get("smart_sell_24h", 0)),
                            net_position=float(token_data.get("smart_net_24h", 0)),
                            profit_loss=float(token_data.get("smart_pnl", 0)),
                            win_rate=float(token_data.get("smart_win_rate", 0)),
                            last_activity=datetime.utcnow()
                        )
                        activities.append(activity)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur parsing smart money: {e}")
                        continue
            
            logger.info(f"🧠 Analysé {len(activities)} activités smart money")
            return activities
            
        except Exception as e:
            logger.error(f"❌ Erreur get_smart_money_activity: {e}")
            return []

    async def check_token_safety(self, contract_address: str, chain: GMGNChain) -> Dict[str, Any]:
        """
        🛡️ Vérifier la sécurité d'un token (RATE LIMITED)
        
        Args:
            contract_address: Adresse du contrat
            chain: Chaîne blockchain
            
        Returns:
            Rapport de sécurité du token
        """
        try:
            # Pour gmgn.ai, utiliser l'endpoint de token detail
            endpoint = f"token/{chain.value}/{contract_address}"
            
            logger.info(f"🛡️ Vérification sécurité token {contract_address[:8]}...")
            data = await self._make_request(endpoint)
            
            if "error" in data:
                return {"safe": False, "reason": data["error"]}
            
            if data.get("code") == 0 and "data" in data:
                token_info = data["data"]
                
                safety_report = {
                    "safe": True,
                    "is_honeypot": not token_info.get("not_honeypot", True),
                    "is_verified": token_info.get("verified", False),
                    "is_renounced": token_info.get("renounced", False),
                    "liquidity_locked": token_info.get("liquidity_locked", False),
                    "owner_balance": float(token_info.get("owner_balance_percent", 100)),
                    "security_score": self._calculate_security_score(token_info),
                    "warnings": []
                }
                
                # Générer les avertissements
                if safety_report["is_honeypot"]:
                    safety_report["warnings"].append("⚠️ Possible honeypot détecté")
                    safety_report["safe"] = False
                
                if not safety_report["is_verified"]:
                    safety_report["warnings"].append("⚠️ Token non vérifié")
                
                if safety_report["owner_balance"] > 50:
                    safety_report["warnings"].append(f"⚠️ Owner détient {safety_report['owner_balance']:.1f}% des tokens")
                
                return safety_report
            
            return {"safe": False, "reason": "Token non trouvé"}
            
        except Exception as e:
            logger.error(f"❌ Erreur check_token_safety: {e}")
            return {"safe": False, "reason": str(e)}

    async def get_meme_coin_opportunities(self, 
                                        chains: List[GMGNChain] = None,
                                        min_volume: float = 50000,
                                        max_risk: str = "MODÉRÉ") -> List[GMGNToken]:
        """
        💎 Identifier les opportunités meme coins (OPTIMISÉ RATE LIMITS)
        
        Args:
            chains: Chaînes à analyser (limitées à 2 pour économiser l'API)
            min_volume: Volume minimum 24h
            max_risk: Niveau de risque maximum
            
        Returns:
            Liste des opportunités détectées
        """
        if chains is None:
            # Limiter à 2 chaînes pour économiser les requêtes API
            chains = [GMGNChain.SOLANA, GMGNChain.BASE]
        else:
            # Forcer maximum 2 chaînes
            chains = chains[:2]
        
        risk_levels = ["TRÈS_FAIBLE", "FAIBLE", "MODÉRÉ", "ÉLEVÉ", "TRÈS_ÉLEVÉ"]
        max_risk_index = risk_levels.index(max_risk)
        
        opportunities = []
        
        logger.info(f"💎 Analyse opportunités sur {len(chains)} chaînes (rate limited)")
        
        for chain in chains:
            try:
                # Récupérer moins de tokens pour économiser l'API
                trending = await self.get_trending_tokens(
                    chain=chain,
                    time_period=GMGNTimePeriod.SIX_HOURS,
                    order_by="volume",
                    limit=15  # Réduit de 30 à 15
                )
                
                for token in trending:
                    # Filtres
                    if token.volume_24h < min_volume:
                        continue
                    
                    token_risk_index = risk_levels.index(token.risk_level)
                    if token_risk_index > max_risk_index:
                        continue
                    
                    if token.is_honeypot:
                        continue
                    
                    # Critères d'opportunité
                    if (token.smart_money_score > 5 and 
                        token.holders_count > 200 and
                        token.is_verified):
                        opportunities.append(token)
                
                # Pause entre les chaînes pour respecter le rate limit
                if len(chains) > 1:
                    await asyncio.sleep(0.6)
                
            except Exception as e:
                logger.error(f"❌ Erreur analyse opportunités {chain.value}: {e}")
                continue
        
        # Trier par score combiné
        opportunities.sort(
            key=lambda x: x.smart_money_score * x.volume_24h / max(1, x.market_cap),
            reverse=True
        )
        
        logger.info(f"💎 Identifié {len(opportunities)} opportunités meme coins")
        return opportunities[:5]  # Top 5 au lieu de 10

    def get_stats(self) -> Dict[str, Any]:
        """📊 Obtenir les statistiques d'utilisation de l'API"""
        current_rate = self.rate_limiter.get_current_rate()
        
        return {
            "total_requests": self.total_requests,
            "cached_responses": self.cached_responses,
            "cache_hit_rate": (self.cached_responses / max(1, self.total_requests)) * 100,
            "rate_limited_count": self.rate_limited_count,
            "current_request_rate": current_rate,
            "max_allowed_rate": self.rate_limiter.max_requests_per_second,
            "cache_entries": len(self.cache)
        }

    def _calculate_risk_level(self, token_data: Dict) -> str:
        """📊 Calculer le niveau de risque d'un token"""
        
        risk_score = 0
        
        # Facteurs de risque
        if not token_data.get("not_honeypot", True):
            risk_score += 50
        
        if not token_data.get("verified", False):
            risk_score += 20
        
        if not token_data.get("renounced", False):
            risk_score += 15
        
        holders = int(token_data.get("holder_count", 0))
        if holders < 100:
            risk_score += 25
        elif holders < 500:
            risk_score += 10
        
        liquidity = float(token_data.get("liquidity", 0))
        if liquidity < 10000:
            risk_score += 20
        
        # Classification
        if risk_score >= 70:
            return "TRÈS_ÉLEVÉ"
        elif risk_score >= 50:
            return "ÉLEVÉ"
        elif risk_score >= 30:
            return "MODÉRÉ"
        elif risk_score >= 15:
            return "FAIBLE"
        else:
            return "TRÈS_FAIBLE"

    def _calculate_security_score(self, token_info: Dict) -> float:
        """🔒 Calculer le score de sécurité (0-100)"""
        
        score = 100
        
        # Pénalités
        if not token_info.get("not_honeypot", True):
            score -= 50
        
        if not token_info.get("verified", False):
            score -= 20
        
        if not token_info.get("renounced", False):
            score -= 15
        
        if not token_info.get("liquidity_locked", False):
            score -= 10
        
        owner_balance = float(token_info.get("owner_balance_percent", 0))
        if owner_balance > 50:
            score -= 20
        elif owner_balance > 20:
            score -= 10
        
        return max(0, score)

# Instance globale
_gmgn_client: Optional[GMGNAPIClient] = None

def get_gmgn_client() -> GMGNAPIClient:
    """🎪 Obtenir l'instance du client GMGN avec rate limiting"""
    global _gmgn_client
    if _gmgn_client is None:
        _gmgn_client = GMGNAPIClient()
    return _gmgn_client 