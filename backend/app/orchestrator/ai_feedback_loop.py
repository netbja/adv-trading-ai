"""
🧠 AI FEEDBACK LOOP - BOUCLE DE RÉTROACTION POSITIVE
====================================================

Ce module implémente l'intelligence auto-améliorante de l'orchestrateur :
- Analyse des performances passées
- Apprentissage automatique des patterns
- Optimisation continue des décisions
- Adaptation aux conditions de marché changeantes
"""

import logging
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

from database.connection import get_db_session
from app.orchestrator.decision_engine import DecisionEngine
from app.orchestrator.performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)

class LearningSignal(Enum):
    """Types de signaux d'apprentissage"""
    SUCCESS = "success"
    FAILURE = "failure" 
    OPTIMIZATION = "optimization"
    ADAPTATION = "adaptation"

@dataclass
class FeedbackData:
    """Données de rétroaction pour l'apprentissage"""
    timestamp: datetime
    asset_type: str
    decision_id: str
    market_conditions: Dict
    system_conditions: Dict
    action_taken: str
    result_metrics: Dict
    learning_signal: LearningSignal
    confidence_score: float

@dataclass
class LearningPattern:
    """Pattern appris par l'IA"""
    pattern_id: str
    market_signature: Dict  # Signature des conditions de marché
    system_signature: Dict  # Signature des conditions système
    optimal_action: str
    success_rate: float
    confidence: float
    usage_count: int
    last_updated: datetime

class AIFeedbackLoop:
    """
    🧠 BOUCLE DE RÉTROACTION IA POSITIVE
    
    Cette classe implémente l'apprentissage continu de l'orchestrateur :
    - Collecte automatique des métriques de performance
    - Identification des patterns de succès/échec
    - Optimisation des décisions futures
    - Adaptation aux nouvelles conditions
    """
    
    def __init__(self, decision_engine: DecisionEngine, performance_tracker: PerformanceTracker):
        self.decision_engine = decision_engine
        self.performance_tracker = performance_tracker
        self.learned_patterns: Dict[str, LearningPattern] = {}
        self.feedback_history: List[FeedbackData] = []
        self.learning_rate = 0.1
        self.confidence_threshold = 0.7
        
        # Métriques d'apprentissage
        self.total_learning_cycles = 0
        self.patterns_discovered = 0
        self.decisions_optimized = 0
        self.adaptation_score = 0.0
        
        logger.info("🧠 AI Feedback Loop initialisé - Apprentissage continu activé")

    async def process_feedback(self, feedback: FeedbackData) -> Dict:
        """
        🔄 Traiter une rétroaction et déclencher l'apprentissage
        
        Args:
            feedback: Données de rétroaction à analyser
            
        Returns:
            Dict contenant les insights de l'apprentissage
        """
        try:
            # 1. Stocker la rétroaction
            self.feedback_history.append(feedback)
            
            # 2. Analyser et apprendre
            learning_insights = await self._analyze_and_learn(feedback)
            
            # 3. Mettre à jour les patterns
            await self._update_patterns(feedback, learning_insights)
            
            # 4. Optimiser les décisions futures
            optimization_impact = await self._optimize_future_decisions(feedback)
            
            # 5. Calculer le score d'adaptation
            self.adaptation_score = await self._calculate_adaptation_score()
            
            self.total_learning_cycles += 1
            
            result = {
                "feedback_processed": True,
                "learning_insights": learning_insights,
                "optimization_impact": optimization_impact,
                "adaptation_score": self.adaptation_score,
                "patterns_count": len(self.learned_patterns),
                "learning_cycle": self.total_learning_cycles
            }
            
            logger.info(f"🧠 Feedback traité - Cycle #{self.total_learning_cycles} - Score adaptation: {self.adaptation_score:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur traitement feedback: {e}")
            return {"feedback_processed": False, "error": str(e)}

    async def _analyze_and_learn(self, feedback: FeedbackData) -> Dict:
        """🔍 Analyser la rétroaction et extraire des insights"""
        
        insights = {
            "market_pattern_detected": False,
            "system_correlation_found": False,
            "new_strategy_learned": False,
            "confidence_adjustment": 0.0
        }
        
        try:
            # Analyser les conditions de marché lors du succès/échec
            market_signature = self._extract_market_signature(feedback.market_conditions)
            system_signature = self._extract_system_signature(feedback.system_conditions)
            
            # Rechercher des patterns similaires
            similar_patterns = self._find_similar_patterns(market_signature, system_signature)
            
            if feedback.learning_signal == LearningSignal.SUCCESS:
                insights = await self._learn_from_success(feedback, similar_patterns)
            elif feedback.learning_signal == LearningSignal.FAILURE:
                insights = await self._learn_from_failure(feedback, similar_patterns)
            
            # Ajuster la confiance globale
            insights["confidence_adjustment"] = self._calculate_confidence_adjustment(feedback)
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse apprentissage: {e}")
            
        return insights

    async def _learn_from_success(self, feedback: FeedbackData, similar_patterns: List[LearningPattern]) -> Dict:
        """✅ Apprendre des succès pour renforcer les bonnes décisions"""
        
        insights = {
            "success_pattern_reinforced": False,
            "new_optimal_strategy": None,
            "confidence_boost": 0.0
        }
        
        try:
            # Renforcer les patterns existants
            for pattern in similar_patterns:
                pattern.success_rate = min(1.0, pattern.success_rate + self.learning_rate)
                pattern.confidence = min(1.0, pattern.confidence + 0.05)
                pattern.usage_count += 1
                pattern.last_updated = datetime.utcnow()
                insights["success_pattern_reinforced"] = True
            
            # Créer un nouveau pattern si aucun similaire
            if not similar_patterns:
                new_pattern = self._create_new_pattern(feedback, success_bias=True)
                if new_pattern:
                    self.learned_patterns[new_pattern.pattern_id] = new_pattern
                    self.patterns_discovered += 1
                    insights["new_optimal_strategy"] = new_pattern.optimal_action
            
            # Boost de confiance pour ce type de décision
            insights["confidence_boost"] = min(0.2, feedback.confidence_score * 0.1)
            
        except Exception as e:
            logger.error(f"❌ Erreur apprentissage succès: {e}")
            
        return insights

    async def _learn_from_failure(self, feedback: FeedbackData, similar_patterns: List[LearningPattern]) -> Dict:
        """❌ Apprendre des échecs pour éviter les erreurs"""
        
        insights = {
            "failure_pattern_identified": False,
            "strategy_adjustment": None,
            "confidence_penalty": 0.0
        }
        
        try:
            # Pénaliser les patterns qui ont échoué
            for pattern in similar_patterns:
                pattern.success_rate = max(0.0, pattern.success_rate - self.learning_rate)
                pattern.confidence = max(0.1, pattern.confidence - 0.1)
                pattern.last_updated = datetime.utcnow()
                insights["failure_pattern_identified"] = True
            
            # Marquer cette combinaison comme problématique
            failure_signature = {
                "market": self._extract_market_signature(feedback.market_conditions),
                "system": self._extract_system_signature(feedback.system_conditions),
                "action": feedback.action_taken,
                "avoid": True
            }
            
            # Chercher une stratégie alternative
            alternative_action = await self._find_alternative_strategy(feedback)
            if alternative_action:
                insights["strategy_adjustment"] = alternative_action
            
            # Pénalité de confiance
            insights["confidence_penalty"] = min(0.3, feedback.confidence_score * 0.15)
            
        except Exception as e:
            logger.error(f"❌ Erreur apprentissage échec: {e}")
            
        return insights

    def _extract_market_signature(self, market_conditions: Dict) -> Dict:
        """📊 Extraire une signature des conditions de marché"""
        
        signature = {}
        
        try:
            # Volatilité (par tranches)
            volatility = market_conditions.get("volatility", 0.2)
            if volatility > 0.8:
                signature["volatility_level"] = "high"
            elif volatility < 0.4:
                signature["volatility_level"] = "low"
            else:
                signature["volatility_level"] = "medium"
            
            # Tendance
            trend = market_conditions.get("trend_strength", 0.0)
            signature["trend"] = "bullish" if trend > 0.1 else "bearish" if trend < -0.1 else "neutral"
            
            # Session de trading (pour forex)
            hour = datetime.utcnow().hour
            if 8 <= hour <= 17:
                signature["trading_session"] = "active"
            else:
                signature["trading_session"] = "inactive"
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction signature marché: {e}")
            
        return signature

    def _extract_system_signature(self, system_conditions: Dict) -> Dict:
        """🖥️ Extraire une signature des conditions système"""
        
        signature = {}
        
        try:
            # CPU
            cpu = system_conditions.get("cpu_usage", 30)
            signature["cpu_load"] = "high" if cpu > 80 else "medium" if cpu > 50 else "low"
            
            # Mémoire
            memory = system_conditions.get("memory_usage", 40)
            signature["memory_load"] = "high" if memory > 85 else "medium" if memory > 60 else "low"
            
            # Connexions
            connections = system_conditions.get("active_connections", 5)
            signature["connection_load"] = "high" if connections > 20 else "low"
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction signature système: {e}")
            
        return signature

    def _find_similar_patterns(self, market_sig: Dict, system_sig: Dict) -> List[LearningPattern]:
        """🔍 Trouver des patterns similaires dans l'historique"""
        
        similar = []
        
        try:
            for pattern in self.learned_patterns.values():
                market_similarity = self._calculate_signature_similarity(
                    market_sig, pattern.market_signature
                )
                system_similarity = self._calculate_signature_similarity(
                    system_sig, pattern.system_signature
                )
                
                # Seuil de similarité
                if market_similarity > 0.7 and system_similarity > 0.5:
                    similar.append(pattern)
                    
        except Exception as e:
            logger.error(f"❌ Erreur recherche patterns similaires: {e}")
            
        return similar

    def _calculate_signature_similarity(self, sig1: Dict, sig2: Dict) -> float:
        """📏 Calculer la similarité entre deux signatures"""
        
        if not sig1 or not sig2:
            return 0.0
            
        common_keys = set(sig1.keys()) & set(sig2.keys())
        if not common_keys:
            return 0.0
            
        matches = sum(1 for key in common_keys if sig1[key] == sig2[key])
        return matches / len(common_keys)

    def _create_new_pattern(self, feedback: FeedbackData, success_bias: bool = False) -> Optional[LearningPattern]:
        """🆕 Créer un nouveau pattern d'apprentissage"""
        
        try:
            pattern_id = f"pattern_{len(self.learned_patterns)}_{feedback.asset_type}_{int(datetime.utcnow().timestamp())}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                market_signature=self._extract_market_signature(feedback.market_conditions),
                system_signature=self._extract_system_signature(feedback.system_conditions),
                optimal_action=feedback.action_taken,
                success_rate=0.8 if success_bias else 0.3,
                confidence=feedback.confidence_score,
                usage_count=1,
                last_updated=datetime.utcnow()
            )
            
            return pattern
            
        except Exception as e:
            logger.error(f"❌ Erreur création nouveau pattern: {e}")
            return None

    async def _optimize_future_decisions(self, feedback: FeedbackData) -> Dict:
        """⚡ Optimiser les décisions futures basées sur l'apprentissage"""
        
        optimization = {
            "decision_rules_updated": False,
            "frequency_adjustments": {},
            "priority_rebalancing": {},
            "new_thresholds": {}
        }
        
        try:
            # Ajuster les fréquences selon la performance
            if feedback.learning_signal == LearningSignal.SUCCESS:
                # Augmenter la fréquence des actions qui réussissent
                optimization["frequency_adjustments"][feedback.action_taken] = "increase"
            elif feedback.learning_signal == LearningSignal.FAILURE:
                # Diminuer la fréquence des actions qui échouent
                optimization["frequency_adjustments"][feedback.action_taken] = "decrease"
            
            # Mettre à jour les seuils de décision
            await self._update_decision_thresholds(feedback, optimization)
            
            self.decisions_optimized += 1
            optimization["decision_rules_updated"] = True
            
        except Exception as e:
            logger.error(f"❌ Erreur optimisation décisions: {e}")
            
        return optimization

    async def _update_decision_thresholds(self, feedback: FeedbackData, optimization: Dict):
        """🎯 Mettre à jour les seuils de décision"""
        
        try:
            # Ajuster les seuils de volatilité pour les meme coins
            if feedback.asset_type == "meme_coins":
                current_volatility = feedback.market_conditions.get("volatility", 0.8)
                
                if feedback.learning_signal == LearningSignal.SUCCESS and current_volatility < 0.8:
                    # Si succès avec volatilité plus faible, assouplir le seuil
                    new_threshold = max(0.6, current_volatility - 0.05)
                    optimization["new_thresholds"]["meme_coins_volatility"] = new_threshold
                elif feedback.learning_signal == LearningSignal.FAILURE and current_volatility >= 0.8:
                    # Si échec malgré volatilité élevée, durcir le seuil
                    new_threshold = min(1.0, current_volatility + 0.05)
                    optimization["new_thresholds"]["meme_coins_volatility"] = new_threshold
                    
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour seuils: {e}")

    async def _calculate_adaptation_score(self) -> float:
        """📈 Calculer le score d'adaptation de l'IA"""
        
        try:
            if not self.feedback_history:
                return 0.0
            
            # Calculer le taux de succès récent
            recent_feedback = self.feedback_history[-20:]  # 20 derniers feedbacks
            success_count = sum(1 for f in recent_feedback if f.learning_signal == LearningSignal.SUCCESS)
            success_rate = success_count / len(recent_feedback) if recent_feedback else 0.0
            
            # Facteur d'amélioration (compare les 10 premiers vs 10 derniers)
            if len(self.feedback_history) >= 20:
                early_success = sum(1 for f in self.feedback_history[:10] if f.learning_signal == LearningSignal.SUCCESS) / 10
                recent_success = sum(1 for f in self.feedback_history[-10:] if f.learning_signal == LearningSignal.SUCCESS) / 10
                improvement_factor = (recent_success - early_success + 1) / 2  # Normaliser entre 0 et 1
            else:
                improvement_factor = 0.5
            
            # Score final (pondération: 60% succès récent, 40% amélioration)
            adaptation_score = (success_rate * 0.6) + (improvement_factor * 0.4)
            
            return min(1.0, max(0.0, adaptation_score))
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul score adaptation: {e}")
            return 0.0

    async def get_learning_insights(self) -> Dict:
        """📊 Obtenir les insights de l'apprentissage en cours"""
        
        try:
            insights = {
                "total_learning_cycles": self.total_learning_cycles,
                "patterns_discovered": self.patterns_discovered,
                "decisions_optimized": self.decisions_optimized,
                "adaptation_score": self.adaptation_score,
                "confidence_level": self.confidence_threshold,
                "top_patterns": await self._get_top_patterns(),
                "learning_trends": await self._get_learning_trends(),
                "optimization_impact": await self._calculate_optimization_impact()
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération insights: {e}")
            return {}

    async def _get_top_patterns(self) -> List[Dict]:
        """🏆 Obtenir les meilleurs patterns appris"""
        
        try:
            # Trier par taux de succès et confiance
            sorted_patterns = sorted(
                self.learned_patterns.values(),
                key=lambda p: p.success_rate * p.confidence,
                reverse=True
            )
            
            top_patterns = []
            for pattern in sorted_patterns[:5]:  # Top 5
                top_patterns.append({
                    "pattern_id": pattern.pattern_id,
                    "optimal_action": pattern.optimal_action,
                    "success_rate": round(pattern.success_rate, 3),
                    "confidence": round(pattern.confidence, 3),
                    "usage_count": pattern.usage_count,
                    "market_conditions": pattern.market_signature
                })
                
            return top_patterns
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération top patterns: {e}")
            return []

    async def _get_learning_trends(self) -> Dict:
        """📈 Analyser les tendances d'apprentissage"""
        
        try:
            if len(self.feedback_history) < 10:
                return {"status": "insufficient_data"}
            
            # Analyser les 50 derniers feedbacks
            recent_feedback = self.feedback_history[-50:]
            
            # Taux de succès par asset
            success_by_asset = {}
            for feedback in recent_feedback:
                asset = feedback.asset_type
                if asset not in success_by_asset:
                    success_by_asset[asset] = {"success": 0, "total": 0}
                
                success_by_asset[asset]["total"] += 1
                if feedback.learning_signal == LearningSignal.SUCCESS:
                    success_by_asset[asset]["success"] += 1
            
            # Calculer les taux
            trends = {}
            for asset, data in success_by_asset.items():
                trends[asset] = {
                    "success_rate": round(data["success"] / data["total"], 3) if data["total"] > 0 else 0,
                    "total_decisions": data["total"]
                }
            
            return trends
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse tendances: {e}")
            return {}

    async def _calculate_optimization_impact(self) -> Dict:
        """⚡ Calculer l'impact des optimisations"""
        
        try:
            if self.decisions_optimized == 0:
                return {"impact": "no_optimizations_yet"}
            
            # Comparer les performances avant/après optimisations
            optimization_impact = {
                "decisions_optimized": self.decisions_optimized,
                "patterns_effectiveness": len([p for p in self.learned_patterns.values() if p.success_rate > 0.7]),
                "learning_velocity": self.total_learning_cycles / max(1, len(self.feedback_history)),
                "adaptation_trend": "improving" if self.adaptation_score > 0.6 else "stable" if self.adaptation_score > 0.4 else "learning"
            }
            
            return optimization_impact
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul impact optimisation: {e}")
            return {}

    async def trigger_learning_cycle(self) -> Dict:
        """🔄 Déclencher manuellement un cycle d'apprentissage"""
        
        try:
            logger.info("🧠 Déclenchement cycle d'apprentissage manuel")
            
            # Analyser les performances récentes
            recent_metrics = await self.performance_tracker.get_recent_metrics()
            
            # Créer un feedback de type optimisation
            optimization_feedback = FeedbackData(
                timestamp=datetime.utcnow(),
                asset_type="global",
                decision_id=f"optimization_{int(datetime.utcnow().timestamp())}",
                market_conditions=recent_metrics.get("market_conditions", {}),
                system_conditions=recent_metrics.get("system_status", {}),
                action_taken="optimization_review",
                result_metrics=recent_metrics,
                learning_signal=LearningSignal.OPTIMIZATION,
                confidence_score=0.8
            )
            
            # Traiter le feedback
            result = await self.process_feedback(optimization_feedback)
            
            logger.info(f"🧠 Cycle d'apprentissage terminé - Score adaptation: {self.adaptation_score:.3f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur cycle d'apprentissage: {e}")
            return {"success": False, "error": str(e)}

# Instance globale pour l'injection de dépendance
_ai_feedback_loop: Optional[AIFeedbackLoop] = None

def get_ai_feedback_loop() -> AIFeedbackLoop:
    """🧠 Obtenir l'instance de la boucle de rétroaction IA"""
    global _ai_feedback_loop
    if _ai_feedback_loop is None:
        from app.orchestrator.decision_engine import get_decision_engine
        from app.orchestrator.performance_tracker import get_performance_tracker
        
        _ai_feedback_loop = AIFeedbackLoop(
            decision_engine=get_decision_engine(),
            performance_tracker=get_performance_tracker()
        )
    
    return _ai_feedback_loop 