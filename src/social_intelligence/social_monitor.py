#!/usr/bin/env python3
"""
📱 SOCIAL INTELLIGENCE MONITOR
Surveille X(Twitter), Telegram, Discord, Reddit pour optimiser les décisions de trading
OBJECTIF: 200€/mois → 2000€/mois (ROI 10x)
"""

import asyncio
import aiohttp
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class SentimentLevel(Enum):
    """Niveaux de sentiment"""
    EXTREMELY_BULLISH = "extremely_bullish"
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"
    EXTREMELY_BEARISH = "extremely_bearish"

class SocialPlatform(Enum):
    """Plateformes sociales"""
    TWITTER = "twitter"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    REDDIT = "reddit"
    DEXSCREENER_COMMENTS = "dexscreener"

@dataclass
class SocialSignal:
    """Signal des réseaux sociaux"""
    platform: SocialPlatform
    content: str
    author: str
    timestamp: datetime
    engagement: int  # likes, retweets, views
    sentiment: SentimentLevel
    token_mentions: List[str]
    influence_score: float  # 0-1
    reliability_score: float  # 0-1
    hash_id: str
    
    def __post_init__(self):
        if not self.hash_id:
            content_hash = hashlib.md5(
                f"{self.platform.value}_{self.author}_{self.content}_{self.timestamp}".encode()
            ).hexdigest()
            self.hash_id = content_hash[:12]

class SocialTrendDetector:
    """Détecteur de tendances sociales"""
    
    def __init__(self):
        self.signals_cache: Dict[str, SocialSignal] = {}
        self.trending_tokens: Dict[str, Dict] = {}
        self.influencer_list: Set[str] = set()
        self.sentiment_weights = {
            SentimentLevel.EXTREMELY_BULLISH: 2.0,
            SentimentLevel.BULLISH: 1.0,
            SentimentLevel.NEUTRAL: 0.0,
            SentimentLevel.BEARISH: -1.0,
            SentimentLevel.EXTREMELY_BEARISH: -2.0
        }
        
        # Mots-clés pour détecter opportunités
        self.bullish_keywords = [
            "moon", "rocket", "pump", "gem", "bullish", "breakout", 
            "ath", "new high", "golden cross", "accumulate", "buy the dip",
            "100x", "1000x", "next solana", "early", "presale",
            "launch", "listing", "partnerships", "burning", "buyback"
        ]
        
        self.bearish_keywords = [
            "dump", "crash", "rugpull", "scam", "bearish", "resistance", 
            "breakdown", "sell", "exit", "warning", "red flag",
            "overvalued", "bubble", "correction", "support broken"
        ]
        
        self.urgency_keywords = [
            "now", "urgent", "last chance", "limited time", "ending soon",
            "breaking", "just launched", "live now", "happening now"
        ]

    async def analyze_social_sentiment(self, token_symbol: str, hours_back: int = 24) -> Dict:
        """Analyse le sentiment social pour un token"""
        logger.info(f"📱 Analyse sentiment social pour {token_symbol}")
        
        # Récupérer tous les signaux pour ce token
        relevant_signals = self._get_token_signals(token_symbol, hours_back)
        
        if not relevant_signals:
            return {
                "token": token_symbol,
                "sentiment": "neutral",
                "confidence": 0.0,
                "signals_count": 0,
                "recommendation": "HOLD"
            }
            
        # Calculer sentiment global
        sentiment_analysis = self._calculate_sentiment_score(relevant_signals)
        
        # Détecter signaux urgents
        urgent_signals = self._detect_urgent_signals(relevant_signals)
        
        # Analyser l'engagement
        engagement_analysis = self._analyze_engagement_trend(relevant_signals)
        
        # Détecter influence
        influencer_signals = self._filter_influencer_signals(relevant_signals)
        
        return {
            "token": token_symbol,
            "sentiment": sentiment_analysis["level"],
            "sentiment_score": sentiment_analysis["score"],
            "confidence": sentiment_analysis["confidence"],
            "signals_count": len(relevant_signals),
            "urgent_signals": len(urgent_signals),
            "engagement_trend": engagement_analysis["trend"],
            "influencer_mentions": len(influencer_signals),
            "recommendation": self._generate_trading_recommendation(sentiment_analysis, urgent_signals, engagement_analysis),
            "risk_level": self._assess_social_risk(relevant_signals),
            "key_signals": self._extract_key_signals(relevant_signals, limit=5),
            "analysis_timestamp": datetime.now()
        }
        
    def _get_token_signals(self, token: str, hours_back: int) -> List[SocialSignal]:
        """Récupère signaux pour un token"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        relevant_signals = []
        for signal in self.signals_cache.values():
            if (signal.timestamp >= cutoff_time and 
                token.upper() in [t.upper() for t in signal.token_mentions]):
                relevant_signals.append(signal)
                
        return sorted(relevant_signals, key=lambda x: x.timestamp, reverse=True)
        
    def _calculate_sentiment_score(self, signals: List[SocialSignal]) -> Dict:
        """Calcule score de sentiment pondéré"""
        if not signals:
            return {"level": "neutral", "score": 0.0, "confidence": 0.0}
            
        total_score = 0.0
        total_weight = 0.0
        
        for signal in signals:
            sentiment_value = self.sentiment_weights[signal.sentiment]
            weight = signal.influence_score * signal.reliability_score * (signal.engagement + 1)
            
            total_score += sentiment_value * weight
            total_weight += weight
            
        if total_weight == 0:
            return {"level": "neutral", "score": 0.0, "confidence": 0.0}
            
        average_score = total_score / total_weight
        
        # Déterminer niveau
        if average_score >= 1.5:
            level = "extremely_bullish"
        elif average_score >= 0.5:
            level = "bullish"
        elif average_score >= -0.5:
            level = "neutral"
        elif average_score >= -1.5:
            level = "bearish"
        else:
            level = "extremely_bearish"
            
        # Calculer confiance basée sur volume de signaux et consensus
        confidence = min(1.0, (len(signals) / 50) * 0.7 + abs(average_score) * 0.3)
        
        return {
            "level": level,
            "score": average_score,
            "confidence": confidence
        }
        
    def _detect_urgent_signals(self, signals: List[SocialSignal]) -> List[SocialSignal]:
        """Détecte signaux urgents"""
        urgent_signals = []
        
        for signal in signals:
            content_lower = signal.content.lower()
            urgency_score = 0
            
            for keyword in self.urgency_keywords:
                if keyword in content_lower:
                    urgency_score += 1
                    
            # Signal récent avec high engagement
            if signal.timestamp >= datetime.now() - timedelta(hours=2):
                urgency_score += 2
                
            if signal.engagement > 1000:  # High engagement
                urgency_score += 1
                
            if urgency_score >= 2:
                urgent_signals.append(signal)
                
        return urgent_signals
        
    def _analyze_engagement_trend(self, signals: List[SocialSignal]) -> Dict:
        """Analyse trend d'engagement"""
        if len(signals) < 5:
            return {"trend": "insufficient_data", "growth_rate": 0.0}
            
        # Diviser en périodes récente vs ancienne
        recent_signals = [s for s in signals if s.timestamp >= datetime.now() - timedelta(hours=6)]
        older_signals = [s for s in signals if s.timestamp < datetime.now() - timedelta(hours=6)]
        
        recent_avg = sum(s.engagement for s in recent_signals) / len(recent_signals) if recent_signals else 0
        older_avg = sum(s.engagement for s in older_signals) / len(older_signals) if older_signals else 0
        
        if older_avg == 0:
            growth_rate = 100.0 if recent_avg > 0 else 0.0
        else:
            growth_rate = ((recent_avg - older_avg) / older_avg) * 100
            
        if growth_rate >= 50:
            trend = "explosive_growth"
        elif growth_rate >= 20:
            trend = "strong_growth"
        elif growth_rate >= 5:
            trend = "growing"
        elif growth_rate >= -5:
            trend = "stable"
        elif growth_rate >= -20:
            trend = "declining"
        else:
            trend = "fading"
            
        return {"trend": trend, "growth_rate": growth_rate}
        
    def _filter_influencer_signals(self, signals: List[SocialSignal]) -> List[SocialSignal]:
        """Filtre signaux d'influenceurs"""
        return [s for s in signals if s.author in self.influencer_list or s.influence_score > 0.7]
        
    def _generate_trading_recommendation(self, sentiment: Dict, urgent_signals: List, engagement: Dict) -> str:
        """Génère recommandation de trading basée sur analyse sociale"""
        sentiment_level = sentiment["level"]
        confidence = sentiment["confidence"]
        urgency_count = len(urgent_signals)
        engagement_trend = engagement["trend"]
        
        # Signaux d'achat forts
        if (sentiment_level == "extremely_bullish" and 
            confidence > 0.7 and 
            urgency_count > 2 and 
            engagement_trend in ["explosive_growth", "strong_growth"]):
            return "STRONG_BUY"
            
        # Signaux d'achat modérés
        if (sentiment_level in ["extremely_bullish", "bullish"] and 
            confidence > 0.5 and 
            engagement_trend in ["growing", "strong_growth"]):
            return "BUY"
            
        # Signaux de vente forts
        if (sentiment_level == "extremely_bearish" and 
            confidence > 0.7):
            return "STRONG_SELL"
            
        # Signaux de vente modérés
        if (sentiment_level in ["extremely_bearish", "bearish"] and 
            confidence > 0.5):
            return "SELL"
            
        return "HOLD"
        
    def _assess_social_risk(self, signals: List[SocialSignal]) -> str:
        """Évalue risque basé sur signaux sociaux"""
        if not signals:
            return "UNKNOWN"
            
        # Facteurs de risque
        scam_keywords = ["rugpull", "scam", "warning", "red flag", "avoid"]
        hype_keywords = ["moon", "100x", "1000x", "rocket", "gem"]
        
        scam_mentions = sum(1 for s in signals 
                           for keyword in scam_keywords 
                           if keyword in s.content.lower())
        
        hype_mentions = sum(1 for s in signals 
                           for keyword in hype_keywords 
                           if keyword in s.content.lower())
        
        total_signals = len(signals)
        scam_ratio = scam_mentions / total_signals if total_signals > 0 else 0
        hype_ratio = hype_mentions / total_signals if total_signals > 0 else 0
        
        if scam_ratio > 0.3:
            return "VERY_HIGH"
        elif hype_ratio > 0.5 and scam_ratio > 0.1:
            return "HIGH"  # Trop de hype + quelques warnings
        elif hype_ratio > 0.7:
            return "MEDIUM"  # Beaucoup de hype mais pas de warnings
        elif scam_ratio > 0.1:
            return "MEDIUM"  # Quelques warnings
        else:
            return "LOW"
            
    def _extract_key_signals(self, signals: List[SocialSignal], limit: int = 5) -> List[Dict]:
        """Extrait signaux clés les plus importants"""
        # Trier par importance (influence * engagement * récence)
        def importance_score(signal):
            recency_bonus = 1.0
            if signal.timestamp >= datetime.now() - timedelta(hours=1):
                recency_bonus = 2.0
            elif signal.timestamp >= datetime.now() - timedelta(hours=6):
                recency_bonus = 1.5
                
            return (signal.influence_score * 
                   signal.reliability_score * 
                   (signal.engagement + 1) * 
                   recency_bonus)
        
        top_signals = sorted(signals, key=importance_score, reverse=True)[:limit]
        
        return [
            {
                "platform": signal.platform.value,
                "author": signal.author,
                "content": signal.content[:200] + "..." if len(signal.content) > 200 else signal.content,
                "sentiment": signal.sentiment.value,
                "engagement": signal.engagement,
                "influence_score": signal.influence_score,
                "timestamp": signal.timestamp.isoformat()
            }
            for signal in top_signals
        ]

class SocialDataCollector:
    """Collecteur de données des réseaux sociaux"""
    
    def __init__(self):
        self.session = None
        self.detector = SocialTrendDetector()
        
        # Configuration APIs (à remplir avec vraies clés)
        self.api_configs = {
            "twitter_bearer_token": "YOUR_TWITTER_BEARER_TOKEN",
            "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
            "reddit_client_id": "YOUR_REDDIT_CLIENT_ID",
            "reddit_client_secret": "YOUR_REDDIT_CLIENT_SECRET"
        }
        
        # Canaux Telegram crypto populaires
        self.telegram_channels = [
            "@CryptoGemHunters",
            "@SolanaCalls", 
            "@CryptoMoonshots",
            "@DeFiPulse",
            "@WhaleAlerts"
        ]
        
        # Subreddits crypto
        self.reddit_subreddits = [
            "CryptoMoonShots",
            "SolanaTrading", 
            "CryptoCurrency",
            "CryptoGemHunters",
            "DegenCrypto"
        ]
        
        # Accounts Twitter influents
        self.twitter_influencers = [
            "@elonmusk",
            "@VitalikButerin", 
            "@aantonop",
            "@naval",
            "@balajis"
        ]

    async def start_social_monitoring(self):
        """Lance monitoring continu des réseaux sociaux"""
        logger.info("📱 Démarrage monitoring réseaux sociaux...")
        
        self.session = aiohttp.ClientSession()
        
        # Lancer collecteurs en parallèle
        tasks = [
            asyncio.create_task(self._monitor_twitter()),
            asyncio.create_task(self._monitor_telegram()),
            asyncio.create_task(self._monitor_reddit()),
            asyncio.create_task(self._monitor_dexscreener())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Erreur monitoring social: {e}")
        finally:
            if self.session:
                await self.session.close()
                
    async def _monitor_twitter(self):
        """Monitore Twitter/X"""
        while True:
            try:
                # Simuler récupération tweets crypto
                # Dans la vraie version: utiliser Twitter API v2
                await self._simulate_twitter_data()
                await asyncio.sleep(60)  # Check chaque minute
            except Exception as e:
                logger.error(f"Erreur Twitter monitoring: {e}")
                await asyncio.sleep(300)
                
    async def _monitor_telegram(self):
        """Monitore Telegram"""
        while True:
            try:
                # Simuler récupération messages Telegram
                # Dans la vraie version: utiliser Telegram Bot API
                await self._simulate_telegram_data()
                await asyncio.sleep(30)  # Check plus fréquent
            except Exception as e:
                logger.error(f"Erreur Telegram monitoring: {e}")
                await asyncio.sleep(180)
                
    async def _monitor_reddit(self):
        """Monitore Reddit"""
        while True:
            try:
                # Simuler récupération posts Reddit
                # Dans la vraie version: utiliser Reddit API
                await self._simulate_reddit_data()
                await asyncio.sleep(300)  # Check toutes les 5 minutes
            except Exception as e:
                logger.error(f"Erreur Reddit monitoring: {e}")
                await asyncio.sleep(300)
                
    async def _monitor_dexscreener(self):
        """Monitore comments DexScreener"""
        while True:
            try:
                # Simuler récupération comments DexScreener
                # Dans la vraie version: scraper DexScreener comments
                await self._simulate_dexscreener_data()
                await asyncio.sleep(120)  # Check toutes les 2 minutes
            except Exception as e:
                logger.error(f"Erreur DexScreener monitoring: {e}")
                await asyncio.sleep(300)
                
    async def _simulate_twitter_data(self):
        """Simule données Twitter (remplacer par vraie API)"""
        import random
        
        sample_tweets = [
            {"content": "$SOL looking ready to break out! 🚀 Volume increasing, RSI oversold. This could be the gem we've been waiting for!", "author": "CryptoTrader123", "engagement": 150},
            {"content": "New Solana meme coin just launched! $BONK early entry opportunity 💎", "author": "SolanaWhale", "engagement": 89},
            {"content": "Market looking bearish, time to take profits on altcoins", "author": "TradingGuru", "engagement": 203},
            {"content": "$PEPE pump incoming! Technical analysis shows bullish divergence 📈", "author": "MemeKing", "engagement": 67}
        ]
        
        for tweet_data in random.sample(sample_tweets, 2):
            signal = self._create_signal_from_tweet(tweet_data)
            self.detector.signals_cache[signal.hash_id] = signal
            
        logger.debug(f"📱 Twitter: {len(sample_tweets)} signaux collectés")
        
    def _create_signal_from_tweet(self, tweet_data: Dict) -> SocialSignal:
        """Crée signal à partir de tweet"""
        content = tweet_data["content"]
        
        # Extraire mentions de tokens
        token_mentions = re.findall(r'\$([A-Z]{3,6})', content)
        
        # Analyser sentiment
        sentiment = self._analyze_content_sentiment(content)
        
        return SocialSignal(
            platform=SocialPlatform.TWITTER,
            content=content,
            author=tweet_data["author"],
            timestamp=datetime.now(),
            engagement=tweet_data["engagement"],
            sentiment=sentiment,
            token_mentions=token_mentions,
            influence_score=random.uniform(0.3, 0.9),
            reliability_score=random.uniform(0.5, 0.95),
            hash_id=""
        )
        
    def _analyze_content_sentiment(self, content: str) -> SentimentLevel:
        """Analyse sentiment du contenu"""
        content_lower = content.lower()
        
        bullish_count = sum(1 for word in self.detector.bullish_keywords if word in content_lower)
        bearish_count = sum(1 for word in self.detector.bearish_keywords if word in content_lower)
        
        if bullish_count >= 3:
            return SentimentLevel.EXTREMELY_BULLISH
        elif bullish_count >= 1 and bearish_count == 0:
            return SentimentLevel.BULLISH
        elif bearish_count >= 3:
            return SentimentLevel.EXTREMELY_BEARISH
        elif bearish_count >= 1 and bullish_count == 0:
            return SentimentLevel.BEARISH
        else:
            return SentimentLevel.NEUTRAL
            
    async def _simulate_telegram_data(self):
        """Simule données Telegram"""
        # Implémentation similaire à Twitter
        pass
        
    async def _simulate_reddit_data(self):
        """Simule données Reddit"""
        # Implémentation similaire à Twitter
        pass
        
    async def _simulate_dexscreener_data(self):
        """Simule données DexScreener"""
        # Implémentation similaire à Twitter
        pass

class SocialTradingIntegrator:
    """Intègre intelligence sociale dans décisions de trading"""
    
    def __init__(self):
        self.detector = SocialTrendDetector()
        self.collector = SocialDataCollector()
        
    async def get_social_trading_signals(self, tokens: List[str]) -> Dict:
        """Obtient signaux de trading basés sur analyse sociale"""
        results = {}
        
        for token in tokens:
            social_analysis = await self.detector.analyze_social_sentiment(token)
            
            # Convertir en signal de trading
            trading_signal = self._convert_to_trading_signal(social_analysis)
            results[token] = trading_signal
            
        return results
        
    def _convert_to_trading_signal(self, social_analysis: Dict) -> Dict:
        """Convertit analyse sociale en signal de trading"""
        recommendation = social_analysis["recommendation"]
        confidence = social_analysis["confidence"]
        
        # Mapping vers signaux de trading
        signal_mapping = {
            "STRONG_BUY": {"action": "BUY", "strength": 0.9, "urgency": "HIGH"},
            "BUY": {"action": "BUY", "strength": 0.7, "urgency": "MEDIUM"},
            "HOLD": {"action": "HOLD", "strength": 0.5, "urgency": "LOW"},
            "SELL": {"action": "SELL", "strength": 0.7, "urgency": "MEDIUM"},
            "STRONG_SELL": {"action": "SELL", "strength": 0.9, "urgency": "HIGH"}
        }
        
        base_signal = signal_mapping.get(recommendation, signal_mapping["HOLD"])
        
        return {
            "action": base_signal["action"],
            "strength": base_signal["strength"] * confidence,
            "urgency": base_signal["urgency"],
            "social_sentiment": social_analysis["sentiment"],
            "confidence": confidence,
            "risk_level": social_analysis["risk_level"],
            "reasoning": f"Social sentiment: {social_analysis['sentiment']} ({social_analysis['signals_count']} signals)",
            "key_factors": [
                f"Sentiment: {social_analysis['sentiment']}",
                f"Engagement trend: {social_analysis['engagement_trend']}",
                f"Urgent signals: {social_analysis['urgent_signals']}",
                f"Risk level: {social_analysis['risk_level']}"
            ]
        }
        
    async def start_social_intelligence_system(self):
        """Lance système complet d'intelligence sociale"""
        logger.info("🧠 Démarrage système d'intelligence sociale...")
        
        # Démarrer collecte en arrière-plan
        asyncio.create_task(self.collector.start_social_monitoring())
        
        return {
            "status": "ACTIVE",
            "monitoring_platforms": ["Twitter", "Telegram", "Reddit", "DexScreener"],
            "update_frequency": "Real-time",
            "features": [
                "Sentiment analysis temps réel",
                "Détection trends émergents",
                "Signaux d'influenceurs",
                "Analyse engagement",
                "Détection signaux urgents",
                "Évaluation risques sociaux"
            ]
        }

# Test et exemple d'utilisation
async def test_social_intelligence():
    """Test du système d'intelligence sociale"""
    integrator = SocialTradingIntegrator()
    
    # Démarrer le système
    status = await integrator.start_social_intelligence_system()
    print("🧠 STATUS SYSTÈME SOCIAL:")
    print(json.dumps(status, indent=2))
    
    # Attendre un peu pour collecter des données
    await asyncio.sleep(5)
    
    # Analyser quelques tokens
    test_tokens = ["SOL", "BONK", "PEPE"]
    signals = await integrator.get_social_trading_signals(test_tokens)
    
    print("\n📊 SIGNAUX SOCIAUX:")
    for token, signal in signals.items():
        print(f"\n🪙 {token}:")
        print(json.dumps(signal, indent=2))

if __name__ == "__main__":
    asyncio.run(test_social_intelligence()) 