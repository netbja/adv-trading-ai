#!/usr/bin/env python3
"""
🧠 AI ORCHESTRATOR - INTELLIGENT CRON REPLACEMENT
Enhanced with concepts from JavaScript workflows:
- Dual AI Synchronization
- Technical Analysis Integration  
- Advanced Feedback Loops
- Market Pattern Recognition
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import asyncpg
from groq import AsyncGroq
import numpy as np

# Import du bridge N8N
from .n8n_bridge import WorkflowOrchestrator

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketMode(Enum):
    """Modes de marché disponibles"""
    CRYPTO = "crypto"
    FOREX = "forex" 
    HYBRID = "hybrid"
    STANDBY = "standby"

class TradingStrategy(Enum):
    """Stratégies de trading disponibles"""
    MEME_SCALPING = "meme_scalping"
    TECHNICAL_ANALYSIS = "technical_analysis"
    FOREX_SESSIONS = "forex_sessions"
    DUAL_MARKET = "dual_market"

class UrgencyLevel(Enum):
    """Niveaux d'urgence pour les décisions"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

@dataclass
class MarketConditions:
    """État des conditions de marché (enhanced from JS)"""
    trend: str = "UNKNOWN"  # BULL/BEAR/CRAB
    volatility: str = "UNKNOWN"  # HIGH/MEDIUM/LOW
    volume: str = "UNKNOWN"  # HIGH/MEDIUM/LOW  
    sentiment: str = "UNKNOWN"  # BULLISH/BEARISH/NEUTRAL
    session: str = "UNKNOWN"  # LONDON/NY/ASIA/QUIET
    confidence: float = 0.0
    opportunities: int = 0
    last_update: float = 0
    
@dataclass
class StrategyPerformance:
    """Performance des stratégies (from Dual AI Sync)"""
    win_rate: float = 0.0
    avg_roi: float = 0.0
    total_trades: int = 0
    recent_trades: List[Dict] = None
    risk_score: float = 50.0
    best_conditions: Dict = None
    
    def __post_init__(self):
        if self.recent_trades is None:
            self.recent_trades = []

@dataclass 
class SharedIntelligence:
    """Intelligence partagée entre stratégies (from JS)"""
    market_conditions: MarketConditions
    meme_performance: StrategyPerformance  
    technical_performance: StrategyPerformance
    forex_performance: StrategyPerformance
    allocation: Dict[str, float]
    learned_patterns: Dict[str, Any]
    last_rebalance: float = 0
    
class EnvironmentState:
    """État de l'environnement système (enhanced)"""
    def __init__(self):
        self.api_health: Dict[str, float] = {}
        self.system_load: float = 0.0
        self.market_conditions = MarketConditions()
        self.active_processes: List[str] = []
        self.last_health_check: float = 0
        self.consecutive_failures: Dict[str, int] = {}
        
@dataclass
class AIDecision:
    """Décision prise par l'IA (enhanced)"""
    action: str
    strategy: TradingStrategy
    mode: MarketMode
    urgency: UrgencyLevel
    confidence: float
    reasoning: str
    parameters: Dict[str, Any]
    timestamp: float
    estimated_execution_time: int
    expected_roi: float = 0.0
    risk_level: str = "MEDIUM"
    
class GroqAIEngine:
    """Moteur IA utilisant Groq pour les analyses ultra-rapides (enhanced)"""
    
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.3-70b-versatile"
        
    async def analyze_market_opportunity(self, market_data: Dict, shared_intelligence: SharedIntelligence) -> Dict:
        """Analyse les opportunités avec intelligence partagée"""
        prompt = f"""You are an ELITE TRADING AI ORCHESTRATOR with DUAL STRATEGY INTELLIGENCE.

CURRENT MARKET STATE:
- Trend: {market_data.get('trend', 'UNKNOWN')}
- Volatility: {market_data.get('volatility', 'UNKNOWN')}
- Volume: {market_data.get('volume', 'UNKNOWN')}
- Forex Session: {market_data.get('forex_session', 'UNKNOWN')}
- Time: {datetime.now().strftime('%H:%M UTC')}
- System Load: {market_data.get('system_load', 0)}%
- API Health: {market_data.get('api_health', {})}

STRATEGY PERFORMANCE (from shared intelligence):
- MEME Strategy: {shared_intelligence.meme_performance.win_rate:.1%} win rate, {shared_intelligence.meme_performance.total_trades} trades
- TECHNICAL Strategy: {shared_intelligence.technical_performance.win_rate:.1%} win rate, {shared_intelligence.technical_performance.total_trades} trades
- FOREX Strategy: {shared_intelligence.forex_performance.win_rate:.1%} win rate, {shared_intelligence.forex_performance.total_trades} trades

CURRENT ALLOCATION:
- Meme: {shared_intelligence.allocation.get('meme', 33):.0f}%
- Technical: {shared_intelligence.allocation.get('technical', 33):.0f}%
- Forex: {shared_intelligence.allocation.get('forex', 33):.0f}%

LEARNED PATTERNS:
{json.dumps(shared_intelligence.learned_patterns, indent=2)[:500]}...

DECISION MATRIX:
🟢 FOREX SESSIONS:
- LONDON (7-16 UTC): High volatility EUR/GBP, ideal for forex technical
- NEW_YORK (13-22 UTC): Peak volatility USD pairs, best session
- ASIA (21-6 UTC): Lower volatility JPY pairs, crypto focus
- QUIET: Focus on crypto meme opportunities

🟡 STRATEGY OPTIMIZATION:
- If MEME performing well: Increase allocation, scan aggressively
- If TECHNICAL strong: Focus on established tokens, RSI/MACD signals
- If FOREX profitable: Follow session timing, major pairs

🔴 ADAPTIVE ALLOCATION:
- Underperforming strategy: Reduce allocation, analyze failures
- Strong performers: Increase allocation up to 60% max
- Risk management: Never exceed 20% position size

TASK: Choose OPTIMAL strategy with DYNAMIC ALLOCATION based on performance.

RESPOND WITH VALID JSON:
{{
    "primary_strategy": "MEME_SCALPING|TECHNICAL_ANALYSIS|FOREX_SESSIONS|DUAL_MARKET",
    "recommended_mode": "CRYPTO|FOREX|HYBRID|STANDBY", 
    "action": "SCAN_AGGRESSIVE|SCAN_NORMAL|SCAN_LIGHT|FOREX_SCAN_LONDON|FOREX_SCAN_NY|FOREX_SCAN_ASIA|TECHNICAL_SCAN|REBALANCE_ALLOCATION",
    "urgency": 1-5,
    "confidence": 0.0-1.0,
    "reasoning": "Strategy choice explanation with performance justification",
    "wait_time_seconds": 30-1800,
    "allocation_changes": {{"meme": 0.33, "technical": 0.33, "forex": 0.33}},
    "expected_roi": 0.0-1.0,
    "risk_level": "LOW|MEDIUM|HIGH",
    "focus_areas": ["specific areas to prioritize"],
    "forex_session": "LONDON|NEW_YORK|ASIA|QUIET"
}}"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=600
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Groq analysis error: {e}")
            return self._intelligent_fallback(market_data, shared_intelligence)
            
    def _intelligent_fallback(self, market_data: Dict, shared_intelligence: SharedIntelligence) -> Dict:
        """Fallback intelligent basé sur les performances et sessions"""
        current_hour = datetime.utcnow().hour
        
        # Analyser performances
        meme_perf = shared_intelligence.meme_performance.win_rate
        tech_perf = shared_intelligence.technical_performance.win_rate
        forex_perf = shared_intelligence.forex_performance.win_rate
        
        # Choisir la meilleure stratégie
        best_strategy = "MEME_SCALPING"
        if tech_perf > meme_perf and tech_perf > forex_perf:
            best_strategy = "TECHNICAL_ANALYSIS"
        elif forex_perf > meme_perf and forex_perf > tech_perf:
            best_strategy = "FOREX_SESSIONS"
            
        # Adapter selon session
        if 7 <= current_hour < 16:  # London
            action = "FOREX_SCAN_LONDON" if best_strategy == "FOREX_SESSIONS" else "TECHNICAL_SCAN"
            mode = "FOREX" if best_strategy == "FOREX_SESSIONS" else "HYBRID"
        elif 13 <= current_hour < 22:  # NY  
            action = "FOREX_SCAN_NY" if best_strategy == "FOREX_SESSIONS" else "SCAN_AGGRESSIVE"
            mode = "FOREX" if best_strategy == "FOREX_SESSIONS" else "HYBRID"
        else:  # Crypto focus
            action = "SCAN_NORMAL"
            mode = "CRYPTO"
            
        return {
            "primary_strategy": best_strategy,
            "recommended_mode": mode,
            "action": action,
            "urgency": 2,
            "confidence": 0.6,
            "reasoning": f"Groq failed, using performance-based fallback: {best_strategy} (WR: {max(meme_perf, tech_perf, forex_perf):.1%})",
            "wait_time_seconds": 300,
            "allocation_changes": shared_intelligence.allocation,
            "expected_roi": 0.05,
            "risk_level": "MEDIUM",
            "focus_areas": ["fallback_strategy"],
            "forex_session": self._get_current_forex_session()
        }
            
    def _get_current_forex_session(self) -> str:
        """Détermine la session Forex actuelle"""
        hour = datetime.utcnow().hour
        if 7 <= hour < 16:
            return "LONDON"
        elif 13 <= hour < 22:
            return "NEW_YORK"
        elif 21 <= hour < 6:
            return "ASIA"
        else:
            return "QUIET"

class TechnicalAnalysisEngine:
    """Moteur d'analyse technique (from JS workflows)"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
        """Calcule le RSI"""
        if len(prices) < period + 1:
            return None
            
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
                
        if len(gains) < period:
            return None
            
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    @staticmethod
    def calculate_technical_score(market_data: Dict) -> float:
        """Calcule un score technique global"""
        score = 50.0  # Base neutre
        
        # Volatilité
        if market_data.get('volatility') == 'HIGH':
            score += 15
        elif market_data.get('volatility') == 'LOW':
            score -= 10
            
        # Volume
        if market_data.get('volume') == 'HIGH':
            score += 10
            
        # Trend
        if market_data.get('trend') == 'BULL':
            score += 20
        elif market_data.get('trend') == 'BEAR':
            score -= 15
            
        return min(100, max(0, score))

class IntelligentOrchestrator:
    """Orchestrateur principal enhanced avec dual AI sync"""
    
    def __init__(self):
        self.is_running = False
        self.ai_engine = GroqAIEngine()
        self.technical_engine = TechnicalAnalysisEngine()
        self.workflow_orchestrator = WorkflowOrchestrator()
        self.environment = EnvironmentState()
        self.decision_history: List[AIDecision] = []
        self.current_mode = MarketMode.STANDBY
        
        # Shared Intelligence (from JS dual sync)
        self.shared_intelligence = SharedIntelligence(
            market_conditions=MarketConditions(),
            meme_performance=StrategyPerformance(),
            technical_performance=StrategyPerformance(),
            forex_performance=StrategyPerformance(),
            allocation={"meme": 0.33, "technical": 0.33, "forex": 0.33},
            learned_patterns={}
        )
        
        self.performance_metrics = {
            "total_decisions": 0,
            "successful_decisions": 0,
            "mode_switches": 0,
            "avg_response_time": 0,
            "successful_workflows": 0,
            "failed_workflows": 0,
            "adaptation_rate": 0.0,
            "learning_velocity": 0.0
        }
        
    async def start(self):
        """Démarre l'orchestration intelligente avec feedback loops"""
        logger.info("🚀 Starting Enhanced Intelligent AI Orchestrator...")
        logger.info("🔄 Dual AI Synchronization: ACTIVE")
        logger.info("📊 Technical Analysis Engine: LOADED")
        logger.info("🧠 Shared Intelligence: INITIALIZED")
        
        self.is_running = True
        
        while self.is_running:
            try:
                # 1. Analyser l'environnement (enhanced)
                await self._update_environment_state()
                
                # 2. Synchroniser intelligence partagée
                await self._synchronize_shared_intelligence()
                
                # 3. Demander conseil à l'IA avec contexte partagé
                market_data = await self._prepare_enhanced_market_data()
                ai_analysis = await self.ai_engine.analyze_market_opportunity(
                    market_data, self.shared_intelligence
                )
                
                # 4. Convertir en décision structurée
                decision = self._create_enhanced_decision(ai_analysis)
                
                # 5. Exécuter la décision via N8N
                execution_result = await self._execute_decision_via_n8n(decision)
                
                # 6. Feedback loop et apprentissage
                await self._learn_from_decision(decision, execution_result)
                
                # 7. Rebalancer allocation si nécessaire
                await self._rebalance_strategy_allocation(ai_analysis)
                
                # 8. Attendre intelligemment
                wait_time = decision.parameters.get('wait_time_seconds', 300)
                logger.info(f"🧠 Next decision in {wait_time}s - {decision.reasoning}")
                logger.info(f"📊 Strategy: {decision.strategy.value} | Mode: {decision.mode.value}")
                logger.info(f"🎯 Confidence: {decision.confidence:.2f} | Expected ROI: {decision.expected_roi:.1%}")
                
                await asyncio.sleep(wait_time)
                
            except KeyboardInterrupt:
                logger.info("🛑 Shutting down orchestrator...")
                break
            except Exception as e:
                logger.error(f"❌ Orchestrator error: {e}")
                await asyncio.sleep(60)
                
    async def _synchronize_shared_intelligence(self):
        """Synchronise l'intelligence partagée entre stratégies"""
        # Mettre à jour conditions de marché
        market_conditions = await self._analyze_enhanced_market_conditions()
        self.shared_intelligence.market_conditions = market_conditions
        
        # Analyser patterns récents
        if len(self.decision_history) >= 10:
            patterns = await self._extract_learning_patterns()
            self.shared_intelligence.learned_patterns.update(patterns)
            
        # Calculer métriques d'adaptation
        self.performance_metrics["adaptation_rate"] = self._calculate_adaptation_rate()
        self.performance_metrics["learning_velocity"] = self._calculate_learning_velocity()
        
    async def _analyze_enhanced_market_conditions(self) -> MarketConditions:
        """Analyse avancée des conditions de marché"""
        conditions = MarketConditions()
        
        # Session Forex
        now_utc = datetime.utcnow()
        hour = now_utc.hour
        
        if 7 <= hour < 16:
            conditions.session = "LONDON"
            conditions.volatility = "HIGH"
        elif 13 <= hour < 22:
            conditions.session = "NEW_YORK" 
            conditions.volatility = "VERY_HIGH"
        elif 21 <= hour < 6:
            conditions.session = "ASIA"
            conditions.volatility = "MEDIUM"
        else:
            conditions.session = "QUIET"
            conditions.volatility = "LOW"
            
        # Analyse technique des conditions
        technical_score = self.technical_engine.calculate_technical_score({
            'volatility': conditions.volatility,
            'session': conditions.session
        })
        
        if technical_score > 70:
            conditions.trend = "BULL"
            conditions.sentiment = "BULLISH"
        elif technical_score < 30:
            conditions.trend = "BEAR"
            conditions.sentiment = "BEARISH"
        else:
            conditions.trend = "CRAB"
            conditions.sentiment = "NEUTRAL"
            
        conditions.confidence = technical_score / 100
        conditions.last_update = time.time()
        
        return conditions
        
    async def _prepare_enhanced_market_data(self) -> Dict:
        """Prépare données enrichies pour l'analyse IA"""
        base_data = await self._prepare_market_data()
        
        # Ajouter intelligence partagée
        base_data.update({
            "trend": self.shared_intelligence.market_conditions.trend,
            "volume": self.shared_intelligence.market_conditions.volume,
            "sentiment": self.shared_intelligence.market_conditions.sentiment,
            "meme_performance": {
                "win_rate": self.shared_intelligence.meme_performance.win_rate,
                "total_trades": self.shared_intelligence.meme_performance.total_trades,
                "risk_score": self.shared_intelligence.meme_performance.risk_score
            },
            "technical_performance": {
                "win_rate": self.shared_intelligence.technical_performance.win_rate,
                "total_trades": self.shared_intelligence.technical_performance.total_trades,
                "risk_score": self.shared_intelligence.technical_performance.risk_score
            },
            "current_allocation": self.shared_intelligence.allocation,
            "adaptation_rate": self.performance_metrics["adaptation_rate"],
            "learning_velocity": self.performance_metrics["learning_velocity"]
        })
        
        return base_data
        
    def _create_enhanced_decision(self, analysis: Dict) -> AIDecision:
        """Convertit l'analyse IA en décision structurée (enhanced)"""
        return AIDecision(
            action=analysis.get("action", "WAIT"),
            strategy=TradingStrategy(analysis.get("primary_strategy", "meme_scalping").lower()),
            mode=MarketMode(analysis.get("recommended_mode", "standby").lower()),
            urgency=UrgencyLevel(analysis.get("urgency", 2)),
            confidence=analysis.get("confidence", 0.5),
            reasoning=analysis.get("reasoning", "No reasoning provided"),
            parameters={
                "wait_time_seconds": analysis.get("wait_time_seconds", 300),
                "focus_areas": analysis.get("focus_areas", []),
                "forex_session": analysis.get("forex_session", "UNKNOWN"),
                "allocation_changes": analysis.get("allocation_changes", {}),
                "expected_roi": analysis.get("expected_roi", 0.0),
                "risk_level": analysis.get("risk_level", "MEDIUM")
            },
            timestamp=time.time(),
            estimated_execution_time=60,
            expected_roi=analysis.get("expected_roi", 0.0),
            risk_level=analysis.get("risk_level", "MEDIUM")
        )
        
    async def _rebalance_strategy_allocation(self, ai_analysis: Dict):
        """Rebalance l'allocation entre stratégies"""
        new_allocation = ai_analysis.get("allocation_changes", {})
        
        if new_allocation and new_allocation != self.shared_intelligence.allocation:
            old_allocation = self.shared_intelligence.allocation.copy()
            self.shared_intelligence.allocation.update(new_allocation)
            self.shared_intelligence.last_rebalance = time.time()
            
            logger.info(f"💰 Strategy Rebalancing:")
            for strategy, percentage in new_allocation.items():
                old_pct = old_allocation.get(strategy, 0)
                change = percentage - old_pct
                logger.info(f"  {strategy.upper()}: {old_pct:.1%} → {percentage:.1%} ({change:+.1%})")
                
    async def _extract_learning_patterns(self) -> Dict:
        """Extrait des patterns d'apprentissage des décisions récentes"""
        recent_decisions = self.decision_history[-50:]  # 50 dernières décisions
        
        patterns = {
            "successful_strategies": {},
            "optimal_timing": {},
            "risk_patterns": {},
            "session_performance": {}
        }
        
        for decision in recent_decisions:
            strategy = decision.strategy.value
            hour = datetime.fromtimestamp(decision.timestamp).hour
            
            # Patterns de succès par stratégie
            if strategy not in patterns["successful_strategies"]:
                patterns["successful_strategies"][strategy] = {"count": 0, "avg_confidence": 0}
                
            patterns["successful_strategies"][strategy]["count"] += 1
            patterns["successful_strategies"][strategy]["avg_confidence"] += decision.confidence
            
            # Patterns de timing optimal
            if hour not in patterns["optimal_timing"]:
                patterns["optimal_timing"][hour] = {"decisions": 0, "avg_roi": 0}
                
            patterns["optimal_timing"][hour]["decisions"] += 1
            patterns["optimal_timing"][hour]["avg_roi"] += decision.expected_roi
            
        # Normaliser les moyennes
        for strategy_data in patterns["successful_strategies"].values():
            if strategy_data["count"] > 0:
                strategy_data["avg_confidence"] /= strategy_data["count"]
                
        for timing_data in patterns["optimal_timing"].values():
            if timing_data["decisions"] > 0:
                timing_data["avg_roi"] /= timing_data["decisions"]
                
        return patterns
        
    def _calculate_adaptation_rate(self) -> float:
        """Calcule le taux d'adaptation du système"""
        if len(self.decision_history) < 10:
            return 0.0
            
        recent_decisions = self.decision_history[-10:]
        mode_changes = 0
        
        for i in range(1, len(recent_decisions)):
            if recent_decisions[i].mode != recent_decisions[i-1].mode:
                mode_changes += 1
                
        return mode_changes / len(recent_decisions)
        
    def _calculate_learning_velocity(self) -> float:
        """Calcule la vélocité d'apprentissage"""
        if len(self.decision_history) < 20:
            return 0.0
            
        first_half = self.decision_history[-20:-10]
        second_half = self.decision_history[-10:]
        
        first_avg_confidence = sum(d.confidence for d in first_half) / len(first_half)
        second_avg_confidence = sum(d.confidence for d in second_half) / len(second_half)
        
        return second_avg_confidence - first_avg_confidence

    # ... rest of existing methods with minor enhancements
    async def _update_environment_state(self):
        """Met à jour l'état de l'environnement"""
        self.environment.api_health = await self._check_api_health()
        self.environment.market_conditions = await self._analyze_enhanced_market_conditions()
        self.environment.system_load = await self._get_system_load()
        self.environment.last_health_check = time.time()
        
    async def _check_api_health(self) -> Dict[str, float]:
        """Vérifie la santé des APIs critiques (enhanced)"""
        apis = {
            "pump_fun": "https://api.pump.fun/tokens/trending?limit=1",
            "dexscreener": "https://api.dexscreener.com/latest/dex/search/?q=solana",
            "tradermade_forex": "https://api.tradermade.com/api/v1/live?currency=EURUSD&api_key=demo",
            "coingecko": "https://api.coingecko.com/api/v3/ping",
            "birdeye": "https://public-api.birdeye.so/defi/tokenlist?offset=0&limit=1"
        }
        
        health_scores = {}
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            for name, url in apis.items():
                try:
                    start_time = time.time()
                    headers = {}
                    if name == "birdeye" and os.getenv('BIRDEYE_API_KEY'):
                        headers['X-API-KEY'] = os.getenv('BIRDEYE_API_KEY')
                        
                    async with session.get(url, headers=headers) as response:
                        response_time = time.time() - start_time
                        
                        if response.status == 200:
                            # Score basé sur le temps de réponse
                            if response_time < 1.0:
                                health_scores[name] = 1.0
                            elif response_time < 3.0:
                                health_scores[name] = 0.8
                            elif response_time < 5.0:
                                health_scores[name] = 0.6
                            else:
                                health_scores[name] = 0.3
                                
                            # Reset consecutive failures
                            self.environment.consecutive_failures[name] = 0
                        else:
                            health_scores[name] = 0.0
                            self.environment.consecutive_failures[name] = \
                                self.environment.consecutive_failures.get(name, 0) + 1
                            
                except Exception:
                    health_scores[name] = 0.0
                    self.environment.consecutive_failures[name] = \
                        self.environment.consecutive_failures.get(name, 0) + 1
                    
        return health_scores
        
    async def _get_system_load(self) -> float:
        """Obtient la charge système actuelle"""
        try:
            import psutil
            return psutil.cpu_percent(interval=1) / 100.0
        except:
            import random
            return random.uniform(0.1, 0.9)
            
    async def _prepare_market_data(self) -> Dict:
        """Prépare les données pour l'analyse IA"""
        return {
            "crypto_volatility": self.environment.market_conditions.volatility,
            "forex_session": self.environment.market_conditions.session,
            "system_load": int(self.environment.system_load * 100),
            "api_health": self.environment.api_health,
            "current_mode": self.current_mode.value,
            "time_utc": datetime.utcnow().isoformat(),
            "consecutive_failures": self.environment.consecutive_failures
        }
        
    async def _execute_decision_via_n8n(self, decision: AIDecision) -> Dict:
        """Exécute la décision via les workflows N8N"""
        logger.info(f"🎯 Executing: {decision.action} | Strategy: {decision.strategy.value}")
        logger.info(f"💭 Reasoning: {decision.reasoning}")
        logger.info(f"🎯 Confidence: {decision.confidence:.2f} | Expected ROI: {decision.expected_roi:.1%}")
        
        self.decision_history.append(decision)
        self.performance_metrics["total_decisions"] += 1
        
        if decision.mode != self.current_mode:
            old_mode = self.current_mode
            self.current_mode = decision.mode
            self.performance_metrics["mode_switches"] += 1
            logger.info(f"🔄 Mode switch: {old_mode.value} → {decision.mode.value}")
        
        try:
            execution_result = await self.workflow_orchestrator.execute_ai_decision(
                decision.action,
                decision.mode.value,
                decision.parameters
            )
            
            if execution_result.get("executed_workflows", 0) > 0:
                self.performance_metrics["successful_workflows"] += 1
                logger.info(f"✅ Successfully executed {execution_result['executed_workflows']} workflow(s)")
            else:
                self.performance_metrics["failed_workflows"] += 1
                logger.warning("⚠️  No workflows executed")
                
            return execution_result
            
        except Exception as e:
            logger.error(f"❌ Failed to execute decision via N8N: {e}")
            self.performance_metrics["failed_workflows"] += 1
            return {"success": False, "error": str(e)}
            
    async def _learn_from_decision(self, decision: AIDecision, execution_result: Dict):
        """Apprend de la décision exécutée (enhanced with strategy performance)"""
        success = execution_result.get("executed_workflows", 0) > 0
        
        if success:
            self.performance_metrics["successful_decisions"] += 1
            
            # Mettre à jour performance de la stratégie
            strategy_performance = getattr(
                self.shared_intelligence, 
                f"{decision.strategy.value.split('_')[0]}_performance"
            )
            
            strategy_performance.total_trades += 1
            if len(strategy_performance.recent_trades) >= 10:
                strategy_performance.recent_trades.pop(0)
                
            trade_result = {
                "timestamp": decision.timestamp,
                "confidence": decision.confidence,
                "expected_roi": decision.expected_roi,
                "success": success,
                "risk_level": decision.risk_level
            }
            strategy_performance.recent_trades.append(trade_result)
            
            # Recalculer win rate
            recent_successes = sum(1 for trade in strategy_performance.recent_trades if trade["success"])
            strategy_performance.win_rate = recent_successes / len(strategy_performance.recent_trades)
            
        success_rate = self.performance_metrics["successful_decisions"] / self.performance_metrics["total_decisions"]
        logger.info(f"📈 Decision #{self.performance_metrics['total_decisions']} - Success rate: {success_rate:.2%}")
        
    async def stop(self):
        """Arrête l'orchestrateur"""
        self.is_running = False
        logger.info("🛑 Enhanced Orchestrator stopped")
        
    def get_status(self) -> Dict:
        """Retourne le statut actuel de l'orchestrateur (enhanced)"""
        return {
            "is_running": self.is_running,
            "current_mode": self.current_mode.value,
            "last_decision": self.decision_history[-1].action if self.decision_history else None,
            "performance_metrics": self.performance_metrics,
            "environment_health": {
                "api_health": self.environment.api_health,
                "system_load": self.environment.system_load,
                "market_session": self.environment.market_conditions.session,
                "volatility": self.environment.market_conditions.volatility,
                "consecutive_failures": self.environment.consecutive_failures
            },
            "shared_intelligence": {
                "market_conditions": asdict(self.shared_intelligence.market_conditions),
                "strategy_allocation": self.shared_intelligence.allocation,
                "meme_performance": asdict(self.shared_intelligence.meme_performance),
                "technical_performance": asdict(self.shared_intelligence.technical_performance),
                "forex_performance": asdict(self.shared_intelligence.forex_performance),
                "learned_patterns_count": len(self.shared_intelligence.learned_patterns)
            },
            "success_rate": (
                self.performance_metrics["successful_decisions"] / 
                max(self.performance_metrics["total_decisions"], 1)
            )
        }

# Fonction principale pour démarrer l'orchestrateur
async def main():
    """Point d'entrée principal"""
    orchestrator = IntelligentOrchestrator()
    
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        await orchestrator.stop()
        
if __name__ == "__main__":
    asyncio.run(main()) 