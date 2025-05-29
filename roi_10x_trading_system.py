#!/usr/bin/env python3
"""
💰 ROI 10X TRADING SYSTEM 
OBJECTIF: 200€/mois → 2000€/mois (ROI 10x)
Système complet avec intelligence sociale + RPC optimisé + automatisation
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# Imports de nos systèmes
from src.infrastructure.rpc_optimizer import AutoTradingRPCManager
from src.social_intelligence.social_monitor import SocialTradingIntegrator
from zero_mindset_trading_system import ZeroMindsetTradingSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TradingOpportunity:
    """Opportunité de trading détectée"""
    token: str
    action: str  # BUY/SELL
    confidence: float
    expected_roi: float
    risk_level: str
    reasoning: List[str]
    social_signals: Dict
    technical_signals: Dict
    urgency: str
    timestamp: datetime

class ROI10xPerformanceTracker:
    """Tracker de performance pour atteindre ROI 10x"""
    
    def __init__(self, monthly_budget: float = 200.0, target_roi: float = 10.0):
        self.monthly_budget = monthly_budget
        self.target_roi = target_roi
        self.target_monthly_profit = monthly_budget * target_roi
        
        # Métriques de performance
        self.trades_executed = 0
        self.successful_trades = 0
        self.total_profit = 0.0
        self.total_invested = 0.0
        self.monthly_profits = []
        self.start_date = datetime.now()
        
        # Tracking détaillé
        self.trade_history = []
        self.daily_performance = {}
        self.roi_progression = []
        
    def calculate_current_roi(self) -> float:
        """Calcule ROI actuel"""
        if self.total_invested == 0:
            return 0.0
        return (self.total_profit / self.total_invested) * 100
        
    def calculate_monthly_performance(self) -> Dict:
        """Calcule performance mensuelle"""
        current_month_profit = sum(self.monthly_profits[-1:]) if self.monthly_profits else 0.0
        
        progress_to_target = (current_month_profit / self.target_monthly_profit) * 100
        
        return {
            "monthly_target": self.target_monthly_profit,
            "current_monthly_profit": current_month_profit,
            "progress_percentage": progress_to_target,
            "roi_target": self.target_roi,
            "current_roi": self.calculate_current_roi(),
            "days_in_month": datetime.now().day,
            "projected_monthly": current_month_profit * (30 / datetime.now().day) if datetime.now().day > 0 else 0
        }
        
    def is_on_track_for_10x(self) -> bool:
        """Vérifie si on est sur la bonne voie pour 10x ROI"""
        performance = self.calculate_monthly_performance()
        return performance["progress_percentage"] >= 80  # 80% du target minimum

class AdvancedOpportunityDetector:
    """Détecteur avancé d'opportunités de trading"""
    
    def __init__(self):
        self.social_integrator = SocialTradingIntegrator()
        self.rpc_manager = AutoTradingRPCManager()
        
        # Configurations pour ROI 10x
        self.min_confidence_threshold = 0.75  # Haute confiance requise
        self.min_expected_roi = 0.15  # Minimum 15% ROI par trade
        self.max_risk_level = "MEDIUM"  # Pas de high risk
        
        # Tokens à surveiller (Solana ecosystem)
        self.monitored_tokens = [
            "SOL", "BONK", "WIF", "PEPE", "JUP", "RAY", 
            "ORCA", "SRM", "STEP", "COPE", "FIDA"
        ]
        
        # Stratégies multiples
        self.strategies = {
            "social_momentum": {"weight": 0.4, "enabled": True},
            "technical_breakout": {"weight": 0.3, "enabled": True}, 
            "whale_following": {"weight": 0.2, "enabled": True},
            "news_catalyst": {"weight": 0.1, "enabled": True}
        }

    async def scan_for_opportunities(self) -> List[TradingOpportunity]:
        """Scan complet pour détecter opportunités ROI 10x"""
        logger.info("🔍 Scan d'opportunités ROI 10x...")
        
        opportunities = []
        
        # 1. Analyse sociale de tous les tokens
        social_signals = await self.social_integrator.get_social_trading_signals(self.monitored_tokens)
        
        # 2. Pour chaque token, évaluer opportunité
        for token in self.monitored_tokens:
            opportunity = await self._evaluate_token_opportunity(token, social_signals.get(token, {}))
            
            if opportunity and self._meets_roi_10x_criteria(opportunity):
                opportunities.append(opportunity)
                
        # 3. Trier par potentiel de profit
        opportunities.sort(key=lambda x: x.expected_roi * x.confidence, reverse=True)
        
        logger.info(f"✅ {len(opportunities)} opportunités détectées")
        return opportunities[:5]  # Top 5 seulement
        
    async def _evaluate_token_opportunity(self, token: str, social_signal: Dict) -> Optional[TradingOpportunity]:
        """Évalue opportunité pour un token spécifique"""
        if not social_signal:
            return None
            
        # Calculer score global
        opportunity_score = await self._calculate_opportunity_score(token, social_signal)
        
        if opportunity_score["total_score"] < 0.6:  # Seuil minimum
            return None
            
        return TradingOpportunity(
            token=token,
            action=social_signal.get("action", "HOLD"),
            confidence=opportunity_score["confidence"],
            expected_roi=opportunity_score["expected_roi"],
            risk_level=opportunity_score["risk_level"],
            reasoning=opportunity_score["reasoning"],
            social_signals=social_signal,
            technical_signals=opportunity_score["technical_data"],
            urgency=social_signal.get("urgency", "LOW"),
            timestamp=datetime.now()
        )
        
    async def _calculate_opportunity_score(self, token: str, social_signal: Dict) -> Dict:
        """Calcule score d'opportunité avancé"""
        
        # Score social (40%)
        social_score = self._calculate_social_score(social_signal)
        
        # Score technique simulé (30%) - à intégrer avec vraies données
        technical_score = await self._calculate_technical_score(token)
        
        # Score momentum (20%)
        momentum_score = self._calculate_momentum_score(social_signal)
        
        # Score risque/reward (10%)
        risk_reward_score = self._calculate_risk_reward_score(social_signal)
        
        # Score total pondéré
        total_score = (
            social_score * 0.4 +
            technical_score * 0.3 +
            momentum_score * 0.2 +
            risk_reward_score * 0.1
        )
        
        # Estimer ROI basé sur signaux
        expected_roi = self._estimate_roi_potential(social_signal, technical_score)
        
        return {
            "total_score": total_score,
            "confidence": min(social_signal.get("confidence", 0.5) + technical_score * 0.2, 1.0),
            "expected_roi": expected_roi,
            "risk_level": social_signal.get("risk_level", "MEDIUM"),
            "reasoning": [
                f"Social score: {social_score:.2f}",
                f"Technical score: {technical_score:.2f}",
                f"Momentum: {momentum_score:.2f}",
                f"Risk/Reward: {risk_reward_score:.2f}"
            ],
            "technical_data": {
                "score": technical_score,
                "momentum": momentum_score
            }
        }
        
    def _calculate_social_score(self, social_signal: Dict) -> float:
        """Calcule score social (0-1)"""
        sentiment = social_signal.get("social_sentiment", "neutral")
        confidence = social_signal.get("confidence", 0.0)
        urgency = social_signal.get("urgency", "LOW")
        
        base_score = confidence
        
        # Bonus sentiment
        sentiment_bonus = {
            "extremely_bullish": 0.3,
            "bullish": 0.2,
            "neutral": 0.0,
            "bearish": -0.2,
            "extremely_bearish": -0.3
        }.get(sentiment, 0.0)
        
        # Bonus urgence
        urgency_bonus = {
            "HIGH": 0.2,
            "MEDIUM": 0.1,
            "LOW": 0.0
        }.get(urgency, 0.0)
        
        return max(0.0, min(1.0, base_score + sentiment_bonus + urgency_bonus))
        
    async def _calculate_technical_score(self, token: str) -> float:
        """Calcule score technique (simulation - à remplacer par vraie analyse)"""
        import random
        
        # Simuler analyse technique
        # Dans le vrai système: RSI, MACD, Volume, Support/Resistance, etc.
        rsi = random.uniform(20, 80)
        volume_spike = random.choice([True, False])
        breakout_pattern = random.choice([True, False])
        
        score = 0.5  # Base
        
        if rsi < 30:  # Oversold
            score += 0.2
        elif rsi > 70:  # Overbought
            score -= 0.1
            
        if volume_spike:
            score += 0.2
            
        if breakout_pattern:
            score += 0.3
            
        return max(0.0, min(1.0, score))
        
    def _calculate_momentum_score(self, social_signal: Dict) -> float:
        """Calcule score momentum"""
        urgency = social_signal.get("urgency", "LOW")
        strength = social_signal.get("strength", 0.5)
        
        urgency_multiplier = {
            "HIGH": 1.0,
            "MEDIUM": 0.7,
            "LOW": 0.4
        }.get(urgency, 0.4)
        
        return strength * urgency_multiplier
        
    def _calculate_risk_reward_score(self, social_signal: Dict) -> float:
        """Calcule score risque/récompense"""
        risk_level = social_signal.get("risk_level", "MEDIUM")
        confidence = social_signal.get("confidence", 0.5)
        
        risk_penalty = {
            "LOW": 0.0,
            "MEDIUM": -0.1,
            "HIGH": -0.3,
            "VERY_HIGH": -0.5
        }.get(risk_level, -0.1)
        
        return max(0.0, confidence + risk_penalty)
        
    def _estimate_roi_potential(self, social_signal: Dict, technical_score: float) -> float:
        """Estime potentiel ROI d'un trade"""
        action = social_signal.get("action", "HOLD")
        confidence = social_signal.get("confidence", 0.5)
        strength = social_signal.get("strength", 0.5)
        urgency = social_signal.get("urgency", "LOW")
        
        if action == "HOLD":
            return 0.0
            
        # Base ROI selon force du signal
        base_roi = strength * 0.3  # Max 30% base
        
        # Bonus confiance
        confidence_bonus = confidence * 0.2  # Max 20% bonus
        
        # Bonus technique
        technical_bonus = technical_score * 0.15  # Max 15% bonus
        
        # Bonus urgence
        urgency_bonus = {
            "HIGH": 0.1,   # 10% bonus
            "MEDIUM": 0.05, # 5% bonus
            "LOW": 0.0
        }.get(urgency, 0.0)
        
        total_roi = base_roi + confidence_bonus + technical_bonus + urgency_bonus
        
        return min(0.8, total_roi)  # Cap à 80% ROI par trade
        
    def _meets_roi_10x_criteria(self, opportunity: TradingOpportunity) -> bool:
        """Vérifie si opportunité peut contribuer au ROI 10x"""
        return (
            opportunity.confidence >= self.min_confidence_threshold and
            opportunity.expected_roi >= self.min_expected_roi and
            opportunity.risk_level in ["LOW", "MEDIUM"] and
            opportunity.action in ["BUY", "STRONG_BUY"]
        )

class ROI10xTradingSystem:
    """Système de trading optimisé pour ROI 10x"""
    
    def __init__(self, monthly_budget: float = 200.0):
        self.monthly_budget = monthly_budget
        self.performance_tracker = ROI10xPerformanceTracker(monthly_budget)
        self.opportunity_detector = AdvancedOpportunityDetector()
        self.zero_mindset_system = ZeroMindsetTradingSystem()
        
        # Configuration agressive pour ROI 10x
        self.max_trades_per_day = 8
        self.max_position_size = monthly_budget * 0.15  # 15% max par trade
        self.profit_taking_threshold = 0.25  # Prendre profits à 25%
        self.stop_loss_threshold = 0.08  # Stop loss à 8%
        
    async def initialize_roi_10x_system(self) -> Dict:
        """Initialise système pour ROI 10x"""
        logger.info("💰 Initialisation système ROI 10x...")
        
        # 1. Initialiser tous les sous-systèmes
        mindset_status = await self.zero_mindset_system.initialize_anti_mindset_system()
        social_status = await self.opportunity_detector.social_integrator.start_social_intelligence_system()
        
        # 2. Configuration spéciale ROI 10x
        self.active = True
        
        return {
            "system": "ROI 10X TRADING",
            "status": "ACTIVE",
            "target": f"{self.monthly_budget}€ → {self.monthly_budget * 10}€/mois",
            "roi_target": "1000%",
            "automation_level": "100%",
            "subsystems": {
                "zero_mindset": mindset_status["status"],
                "social_intelligence": social_status["status"],
                "opportunity_detection": "ACTIVE",
                "performance_tracking": "ACTIVE"
            },
            "trading_config": {
                "max_trades_per_day": self.max_trades_per_day,
                "max_position_size": f"{self.max_position_size}€",
                "profit_target": "25%",
                "stop_loss": "8%"
            },
            "expected_timeline": "2-4 semaines pour validation, puis scaling"
        }
        
    async def run_roi_10x_trading_loop(self):
        """Boucle principale de trading ROI 10x"""
        logger.info("🚀 Démarrage boucle trading ROI 10x...")
        
        cycle = 0
        last_scan_time = datetime.now()
        
        while self.active:
            try:
                cycle += 1
                current_time = datetime.now()
                
                # 1. Scan opportunités (toutes les 2 minutes)
                if current_time - last_scan_time >= timedelta(minutes=2):
                    opportunities = await self.opportunity_detector.scan_for_opportunities()
                    last_scan_time = current_time
                    
                    # 2. Exécuter trades sur meilleures opportunités
                    if opportunities:
                        await self._execute_opportunities(opportunities)
                        
                # 3. Rapport de performance (tous les 20 cycles)
                if cycle % 20 == 0:
                    await self._generate_roi_performance_report(cycle)
                    
                # 4. Vérifier si objectif ROI 10x atteint
                if self.performance_tracker.is_on_track_for_10x():
                    logger.info("🎉 ROI 10x track validé!")
                    
                await asyncio.sleep(30)  # 30 secondes entre cycles
                
            except Exception as e:
                logger.error(f"❌ Erreur dans cycle ROI 10x: {e}")
                await asyncio.sleep(60)
                
    async def _execute_opportunities(self, opportunities: List[TradingOpportunity]):
        """Exécute les meilleures opportunités de trading"""
        executed_today = self._count_daily_trades()
        
        for opportunity in opportunities[:3]:  # Top 3 seulement
            if executed_today >= self.max_trades_per_day:
                logger.info("📊 Limite quotidienne de trades atteinte")
                break
                
            if await self._should_execute_trade(opportunity):
                result = await self._execute_trade(opportunity)
                if result["success"]:
                    executed_today += 1
                    self._update_performance_tracking(opportunity, result)
                    
    async def _should_execute_trade(self, opportunity: TradingOpportunity) -> bool:
        """Détermine si trade doit être exécuté"""
        # Vérifications de sécurité
        current_performance = self.performance_tracker.calculate_monthly_performance()
        
        # Ne pas trader si trop de pertes récentes
        if current_performance["current_roi"] < -20:  # Max 20% loss
            logger.warning("🛑 Trading suspendu - pertes excessives")
            return False
            
        # Vérifier position size
        if opportunity.expected_roi * self.max_position_size < 10:  # Min 10€ profit attendu
            return False
            
        return True
        
    async def _execute_trade(self, opportunity: TradingOpportunity) -> Dict:
        """Exécute un trade"""
        logger.info(f"💰 Exécution trade {opportunity.token}: {opportunity.action}")
        
        # Calculer position size
        position_size = min(self.max_position_size, 
                           self.monthly_budget * opportunity.confidence * 0.2)
        
        # Simuler exécution (remplacer par vraie API)
        import random
        success = random.choice([True, True, True, False])  # 75% succès
        
        if success:
            actual_roi = opportunity.expected_roi * random.uniform(0.7, 1.3)
            profit = position_size * actual_roi
        else:
            actual_roi = -0.05  # Petite perte
            profit = position_size * actual_roi
            
        result = {
            "success": success,
            "token": opportunity.token,
            "action": opportunity.action,
            "position_size": position_size,
            "actual_roi": actual_roi,
            "profit": profit,
            "timestamp": datetime.now()
        }
        
        logger.info(f"✅ Trade exécuté: {profit:.2f}€ profit")
        return result
        
    def _update_performance_tracking(self, opportunity: TradingOpportunity, result: Dict):
        """Met à jour tracking de performance"""
        self.performance_tracker.trades_executed += 1
        
        if result["success"] and result["profit"] > 0:
            self.performance_tracker.successful_trades += 1
            
        self.performance_tracker.total_profit += result["profit"]
        self.performance_tracker.total_invested += result["position_size"]
        
        # Ajouter à historique
        self.performance_tracker.trade_history.append({
            "opportunity": opportunity,
            "result": result
        })
        
    def _count_daily_trades(self) -> int:
        """Compte trades exécutés aujourd'hui"""
        today = datetime.now().date()
        return len([
            trade for trade in self.performance_tracker.trade_history
            if trade["result"]["timestamp"].date() == today
        ])
        
    async def _generate_roi_performance_report(self, cycle: int):
        """Génère rapport de performance ROI"""
        performance = self.performance_tracker.calculate_monthly_performance()
        current_roi = self.performance_tracker.calculate_current_roi()
        
        print(f"\n💰 RAPPORT ROI 10X - CYCLE #{cycle}")
        print("="*50)
        print(f"🎯 Objectif mensuel: {performance['monthly_target']:.2f}€")
        print(f"💵 Profit actuel: {performance['current_monthly_profit']:.2f}€")
        print(f"📈 Progression: {performance['progress_percentage']:.1f}%")
        print(f"📊 ROI actuel: {current_roi:.1f}%")
        print(f"🔮 Projection mois: {performance['projected_monthly']:.2f}€")
        print(f"📈 Trades: {self.performance_tracker.successful_trades}/{self.performance_tracker.trades_executed}")
        
        if performance["progress_percentage"] >= 100:
            print("🎉 OBJECTIF ROI 10X ATTEINT!")
        elif performance["progress_percentage"] >= 80:
            print("✅ Sur la bonne voie pour ROI 10x")
        else:
            print("⚠️ Besoin d'optimiser pour atteindre ROI 10x")
            
        print("="*50)
        
    def get_roi_dashboard(self) -> Dict:
        """Dashboard ROI complet"""
        performance = self.performance_tracker.calculate_monthly_performance()
        
        return {
            "roi_target": "10x (1000%)",
            "monthly_target": f"{self.monthly_budget * 10}€",
            "current_progress": f"{performance['progress_percentage']:.1f}%",
            "current_profit": f"{performance['current_monthly_profit']:.2f}€",
            "current_roi": f"{self.performance_tracker.calculate_current_roi():.1f}%",
            "trades_success_rate": f"{(self.performance_tracker.successful_trades/max(1, self.performance_tracker.trades_executed)*100):.1f}%",
            "daily_trades": self._count_daily_trades(),
            "status": "ON_TRACK" if performance["progress_percentage"] >= 80 else "NEEDS_OPTIMIZATION",
            "system_active": self.active
        }

# Interface de lancement 
async def launch_roi_10x_system():
    """Lance système ROI 10x"""
    print("💰 LANCEMENT SYSTÈME ROI 10X")
    print("="*50)
    print("🎯 OBJECTIF: 200€/mois → 2000€/mois")
    print("📈 ROI TARGET: 1000% (10x)")
    print("🤖 AUTOMATISATION COMPLÈTE")
    print("📱 INTELLIGENCE SOCIALE INTÉGRÉE")
    print("⚡ RPC OPTIMISÉ POUR PERFORMANCE")
    print("="*50)
    
    budget = float(input("\n💰 Budget mensuel (défaut 200€): ") or "200")
    
    system = ROI10xTradingSystem(budget)
    
    # Initialisation
    status = await system.initialize_roi_10x_system()
    print("\n🚀 INITIALISATION ROI 10X:")
    print(json.dumps(status, indent=2, default=str))
    
    # Confirmation
    print(f"\n⚠️ PRÊT À DÉMARRER TRADING AUTOMATIQUE")
    print(f"💰 Budget: {budget}€/mois")
    print(f"🎯 Objectif: {budget * 10}€/mois")
    
    confirm = input("\n🚀 Démarrer? (y/N): ").lower()
    if confirm != 'y':
        print("❌ Annulé")
        return
        
    # Lancer système
    try:
        await system.run_roi_10x_trading_loop()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt système ROI 10x")
        
        # Dashboard final
        dashboard = system.get_roi_dashboard()
        print("\n📊 DASHBOARD FINAL ROI 10X:")
        print(json.dumps(dashboard, indent=2))

def main():
    """Point d'entrée"""
    asyncio.run(launch_roi_10x_system())

if __name__ == "__main__":
    main() 