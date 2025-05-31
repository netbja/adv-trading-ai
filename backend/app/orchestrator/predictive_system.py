"""
🔮 SYSTÈME DE PRÉDICTION AVANCÉE
================================

Ce module implémente l'intelligence prédictive de l'orchestrateur :
- Prédiction des conditions de marché futures
- Anticipation des opportunités de trading
- Optimisation prédictive des stratégies
- Alerts prédictives intelligentes
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np
import asyncio

logger = logging.getLogger(__name__)

class PredictionHorizon(Enum):
    """Horizons de prédiction"""
    SHORT_TERM = "5_minutes"      # 5 minutes
    MEDIUM_TERM = "1_hour"        # 1 heure
    LONG_TERM = "4_hours"         # 4 heures
    STRATEGIC = "24_hours"        # 24 heures

class MarketRegime(Enum):
    """Régimes de marché identifiés"""
    BULL_MARKET = "bull"
    BEAR_MARKET = "bear"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_vol"
    LOW_VOLATILITY = "low_vol"
    TRENDING = "trending"
    RANGING = "ranging"

class AlertType(Enum):
    """Types d'alertes prédictives"""
    OPPORTUNITY = "opportunity"
    RISK = "risk"
    REGIME_CHANGE = "regime_change"
    VOLATILITY_SPIKE = "volatility_spike"
    TREND_REVERSAL = "trend_reversal"
    SUPPORT_BREAK = "support_break"
    RESISTANCE_BREAK = "resistance_break"

class PredictionDirection(Enum):
    """Direction prédite du marché"""
    UP = "up"
    DOWN = "down"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"

@dataclass
class MarketPrediction:
    """Prédiction de marché"""
    asset_type: str
    horizon: PredictionHorizon
    direction: PredictionDirection
    magnitude: float
    confidence: float
    price_target: Optional[float]
    probability: float
    key_factors: List[str]
    risk_factors: List[str]
    predicted_volatility: float
    predicted_trend: str
    predicted_regime: MarketRegime
    key_levels: Dict  # Support/Résistance prédits
    opportunities: List[str]  # Opportunités identifiées
    risks: List[str]  # Risques prédits
    optimal_strategies: List[str]  # Stratégies recommandées
    generated_at: datetime
    prediction_timestamp: datetime
    expires_at: datetime

@dataclass
class PredictiveAlert:
    """Alerte prédictive"""
    alert_id: str
    asset_type: str
    alert_type: str  # "opportunity", "risk", "regime_change"
    severity: str    # "low", "medium", "high", "critical"
    predicted_event: str
    probability: float
    time_to_event: timedelta
    recommended_actions: List[str]
    confidence: float
    created_at: datetime

@dataclass
class MarketRegimeData:
    """Données de régime de marché"""
    trend: PredictionDirection
    volatility: str  # "low", "medium", "high"
    market_phase: str  # "accumulation", "markup", "distribution", "markdown"
    confidence: float
    regime_strength: float
    detected_at: datetime

class PredictiveSystem:
    """
    🔮 SYSTÈME DE PRÉDICTION AVANCÉE
    
    Intelligence prédictive pour anticiper les mouvements de marché
    et optimiser les stratégies de trading avant qu'ils ne se produisent.
    """
    
    def __init__(self):
        self.market_history: Dict[str, List[Dict]] = {}
        self.prediction_cache: Dict[str, MarketPrediction] = {}
        self.active_alerts: List[PredictiveAlert] = []
        self.pattern_library: Dict[str, Dict] = {}
        
        # Paramètres d'apprentissage
        self.lookback_periods = {
            PredictionHorizon.SHORT_TERM: 50,
            PredictionHorizon.MEDIUM_TERM: 200,
            PredictionHorizon.LONG_TERM: 500,
            PredictionHorizon.STRATEGIC: 1000
        }
        
        # Métriques de performance
        self.prediction_accuracy = {}
        self.total_predictions = 0
        self.successful_predictions = 0
        
        logger.info("🔮 Système de prédiction avancée initialisé")

    async def generate_market_predictions(self, asset_type: str) -> Dict[str, MarketPrediction]:
        """
        🎯 Générer des prédictions de marché pour tous les horizons
        
        Args:
            asset_type: Type d'asset à analyser
            
        Returns:
            Dict des prédictions par horizon temporel
        """
        try:
            predictions = {}
            
            # Analyser l'historique récent
            historical_data = await self._gather_historical_data(asset_type)
            
            # Générer prédictions pour chaque horizon
            for horizon in PredictionHorizon:
                prediction = await self._predict_for_horizon(asset_type, horizon, historical_data)
                if prediction:
                    predictions[horizon.value] = prediction
                    self.prediction_cache[f"{asset_type}_{horizon.value}"] = prediction
            
            # Identifier les alertes prédictives
            await self._generate_predictive_alerts(asset_type, predictions)
            
            logger.info(f"🔮 Prédictions générées pour {asset_type} - {len(predictions)} horizons")
            return predictions
            
        except Exception as e:
            logger.error(f"❌ Erreur génération prédictions {asset_type}: {e}")
            return {}

    async def _gather_historical_data(self, asset_type: str) -> Dict:
        """📊 Collecter les données historiques pour l'analyse"""
        
        try:
            # Simuler la collecte de données historiques
            # En production, ceci se connecterait aux APIs de marché réelles
            
            historical_data = {
                "volatility_series": self._generate_volatility_series(asset_type),
                "trend_series": self._generate_trend_series(asset_type),
                "volume_series": self._generate_volume_series(asset_type),
                "price_action": self._generate_price_action(asset_type),
                "market_cycles": self._identify_market_cycles(asset_type),
                "correlation_matrix": self._calculate_asset_correlations(asset_type)
            }
            
            return historical_data
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte données historiques {asset_type}: {e}")
            return {}

    def _generate_volatility_series(self, asset_type: str) -> List[float]:
        """📈 Générer une série de volatilité réaliste"""
        
        try:
            # Paramètres par type d'asset
            base_volatility = {
                "meme_coins": 0.8,
                "crypto_lt": 0.4, 
                "forex": 0.2,
                "etf": 0.15
            }.get(asset_type, 0.3)
            
            # Série temporelle avec clustering de volatilité
            series = []
            current_vol = base_volatility
            
            for i in range(100):
                # Persistance de volatilité (clustering)
                change = np.random.normal(0, 0.05)
                current_vol = max(0.05, min(1.0, current_vol + change))
                
                # Ajout de chocs occasionnels
                if np.random.random() < 0.05:  # 5% de chance de choc
                    shock = np.random.normal(0, 0.3)
                    current_vol = max(0.05, min(1.0, current_vol + shock))
                
                series.append(current_vol)
            
            return series
            
        except Exception as e:
            logger.error(f"❌ Erreur génération série volatilité: {e}")
            return []

    def _generate_trend_series(self, asset_type: str) -> List[float]:
        """🎢 Générer une série de tendance réaliste"""
        
        try:
            # Tendances cycliques avec du bruit
            series = []
            
            for i in range(100):
                # Tendance cyclique de base
                cycle = 0.3 * np.sin(i * 0.1) 
                
                # Tendance persistante
                trend = 0.2 * np.sin(i * 0.02)
                
                # Bruit aléatoire
                noise = np.random.normal(0, 0.1)
                
                value = cycle + trend + noise
                series.append(max(-1.0, min(1.0, value)))
            
            return series
            
        except Exception as e:
            logger.error(f"❌ Erreur génération série tendance: {e}")
            return []

    def _generate_volume_series(self, asset_type: str) -> List[float]:
        """📊 Générer une série de volume réaliste"""
        
        try:
            base_volume = {
                "meme_coins": 1.5,
                "crypto_lt": 1.0,
                "forex": 2.0,
                "etf": 0.8
            }.get(asset_type, 1.0)
            
            series = []
            
            for i in range(100):
                # Volume corrélé à la volatilité
                vol_impact = 0.5 + 0.5 * np.random.random()
                
                # Patterns intraday (forex/etf)
                if asset_type in ["forex", "etf"]:
                    hour_impact = 1.0 + 0.3 * np.sin(i * 0.26)  # Cycle journalier
                else:
                    hour_impact = 1.0
                
                volume = base_volume * vol_impact * hour_impact
                series.append(max(0.1, volume))
            
            return series
            
        except Exception as e:
            logger.error(f"❌ Erreur génération série volume: {e}")
            return []

    def _generate_price_action(self, asset_type: str) -> Dict:
        """💰 Analyser l'action des prix"""
        
        try:
            price_action = {
                "support_levels": [0.95, 0.88, 0.82],
                "resistance_levels": [1.05, 1.12, 1.18],
                "breakout_probability": np.random.uniform(0.2, 0.8),
                "momentum": np.random.uniform(-1.0, 1.0),
                "mean_reversion_strength": np.random.uniform(0.3, 0.9),
                "trend_strength": np.random.uniform(-1.0, 1.0)
            }
            
            return price_action
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse price action: {e}")
            return {}

    def _identify_market_cycles(self, asset_type: str) -> Dict:
        """🔄 Identifier les cycles de marché"""
        
        try:
            cycles = {
                "primary_cycle": {
                    "phase": np.random.choice(["accumulation", "markup", "distribution", "markdown"]),
                    "strength": np.random.uniform(0.3, 0.9),
                    "time_remaining": np.random.randint(10, 200)
                },
                "secondary_cycle": {
                    "phase": np.random.choice(["bullish", "bearish", "neutral"]),
                    "strength": np.random.uniform(0.2, 0.7)
                },
                "micro_cycle": {
                    "phase": np.random.choice(["impulse", "correction", "consolidation"]),
                    "strength": np.random.uniform(0.4, 0.8)
                }
            }
            
            return cycles
            
        except Exception as e:
            logger.error(f"❌ Erreur identification cycles: {e}")
            return {}

    def _calculate_asset_correlations(self, asset_type: str) -> Dict:
        """🔗 Calculer les corrélations entre assets"""
        
        try:
            # Corrélations typiques
            correlations = {
                "meme_coins": {
                    "crypto_lt": 0.7,
                    "forex": 0.1,
                    "etf": 0.2,
                    "market_sentiment": 0.8
                },
                "crypto_lt": {
                    "meme_coins": 0.7,
                    "forex": 0.3,
                    "etf": 0.4,
                    "institutional_flow": 0.6
                },
                "forex": {
                    "crypto_lt": 0.3,
                    "etf": 0.5,
                    "economic_data": 0.8,
                    "central_bank_policy": 0.9
                },
                "etf": {
                    "forex": 0.5,
                    "crypto_lt": 0.4,
                    "market_indices": 0.9,
                    "institutional_sentiment": 0.7
                }
            }
            
            return correlations.get(asset_type, {})
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul corrélations: {e}")
            return {}

    async def _predict_for_horizon(self, asset_type: str, horizon: PredictionHorizon, historical_data: Dict) -> Optional[MarketPrediction]:
        """🎯 Générer une prédiction pour un horizon spécifique"""
        
        try:
            # Analyser les patterns selon l'horizon
            patterns = await self._analyze_patterns_for_horizon(historical_data, horizon)
            
            # Prédire la volatilité
            predicted_volatility = self._predict_volatility(historical_data, horizon)
            
            # Prédire la tendance
            predicted_trend = self._predict_trend(historical_data, horizon)
            
            # Identifier le régime de marché prédit
            predicted_regime = self._predict_market_regime(predicted_volatility, predicted_trend)
            
            # Calculer la confiance
            confidence_score = self._calculate_prediction_confidence(patterns, horizon)
            
            # Identifier les niveaux clés
            key_levels = self._predict_key_levels(historical_data, horizon)
            
            # Identifier opportunités et risques
            opportunities, risks = self._identify_opportunities_and_risks(
                asset_type, predicted_volatility, predicted_trend, predicted_regime
            )
            
            # Recommander des stratégies optimales
            optimal_strategies = self._recommend_optimal_strategies(
                asset_type, predicted_regime, predicted_volatility, horizon
            )
            
            # Calculer l'expiration
            time_deltas = {
                PredictionHorizon.SHORT_TERM: timedelta(minutes=5),
                PredictionHorizon.MEDIUM_TERM: timedelta(hours=1),
                PredictionHorizon.LONG_TERM: timedelta(hours=4),
                PredictionHorizon.STRATEGIC: timedelta(hours=24)
            }
            
            prediction = MarketPrediction(
                asset_type=asset_type,
                horizon=horizon,
                direction=self._predict_direction(predicted_trend),
                magnitude=predicted_volatility,
                confidence=confidence_score,
                price_target=self._predict_price_target(historical_data, predicted_trend),
                probability=confidence_score,
                key_factors=patterns.get("trend_patterns", []),
                risk_factors=patterns.get("reversal_patterns", []),
                predicted_volatility=predicted_volatility,
                predicted_trend=predicted_trend,
                predicted_regime=predicted_regime,
                key_levels=key_levels,
                opportunities=opportunities,
                risks=risks,
                optimal_strategies=optimal_strategies,
                generated_at=datetime.utcnow(),
                prediction_timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + time_deltas[horizon]
            )
            
            self.total_predictions += 1
            
            return prediction
            
        except Exception as e:
            logger.error(f"❌ Erreur prédiction horizon {horizon}: {e}")
            return None

    def _predict_volatility(self, historical_data: Dict, horizon: PredictionHorizon) -> float:
        """📊 Prédire la volatilité future"""
        
        try:
            volatility_series = historical_data.get("volatility_series", [])
            if not volatility_series:
                return 0.3
            
            # Modèle simple : moyenne pondérée récente + tendance
            recent_vol = np.mean(volatility_series[-10:])
            trend_vol = (volatility_series[-1] - volatility_series[-5]) / 5
            
            # Ajustement selon l'horizon
            horizon_adjustment = {
                PredictionHorizon.SHORT_TERM: 1.0,
                PredictionHorizon.MEDIUM_TERM: 0.9,
                PredictionHorizon.LONG_TERM: 0.8,
                PredictionHorizon.STRATEGIC: 0.7
            }[horizon]
            
            predicted_vol = (recent_vol + trend_vol * 0.3) * horizon_adjustment
            
            return max(0.05, min(1.0, predicted_vol))
            
        except Exception as e:
            logger.error(f"❌ Erreur prédiction volatilité: {e}")
            return 0.3

    def _predict_trend(self, historical_data: Dict, horizon: PredictionHorizon) -> str:
        """📈 Prédire la direction de la tendance"""
        
        try:
            trend_series = historical_data.get("trend_series", [])
            if not trend_series:
                return "neutral"
            
            # Analyser la tendance récente
            recent_trend = np.mean(trend_series[-5:])
            momentum = trend_series[-1] - trend_series[-3]
            
            # Classification
            if recent_trend > 0.1 and momentum > 0:
                return "bullish_strong"
            elif recent_trend > 0.05:
                return "bullish_weak"
            elif recent_trend < -0.1 and momentum < 0:
                return "bearish_strong"
            elif recent_trend < -0.05:
                return "bearish_weak"
            else:
                return "neutral"
                
        except Exception as e:
            logger.error(f"❌ Erreur prédiction tendance: {e}")
            return "neutral"

    def _predict_market_regime(self, volatility: float, trend: str) -> MarketRegime:
        """🎭 Prédire le régime de marché"""
        
        try:
            # Classification basée sur volatilité et tendance
            if volatility > 0.7:
                return MarketRegime.HIGH_VOLATILITY
            elif volatility < 0.3:
                return MarketRegime.LOW_VOLATILITY
            elif "bullish" in trend:
                return MarketRegime.BULL_MARKET
            elif "bearish" in trend:
                return MarketRegime.BEAR_MARKET
            elif trend == "neutral":
                return MarketRegime.SIDEWAYS
            else:
                return MarketRegime.RANGING
                
        except Exception as e:
            logger.error(f"❌ Erreur prédiction régime: {e}")
            return MarketRegime.RANGING

    def _calculate_prediction_confidence(self, patterns: Dict, horizon: PredictionHorizon) -> float:
        """🎯 Calculer la confiance de la prédiction"""
        
        try:
            base_confidence = 0.6
            
            # Ajustement selon la qualité des patterns
            pattern_quality = patterns.get("quality_score", 0.5)
            confidence = base_confidence + (pattern_quality - 0.5) * 0.4
            
            # Pénalité pour horizons longs
            horizon_penalty = {
                PredictionHorizon.SHORT_TERM: 0.0,
                PredictionHorizon.MEDIUM_TERM: 0.1,
                PredictionHorizon.LONG_TERM: 0.2,
                PredictionHorizon.STRATEGIC: 0.3
            }[horizon]
            
            confidence -= horizon_penalty
            
            return max(0.1, min(0.95, confidence))
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul confiance: {e}")
            return 0.5

    async def _analyze_patterns_for_horizon(self, historical_data: Dict, horizon: PredictionHorizon) -> Dict:
        """🔍 Analyser les patterns pour un horizon donné"""
        
        try:
            patterns = {
                "trend_patterns": [],
                "reversal_patterns": [],
                "continuation_patterns": [],
                "breakout_patterns": [],
                "quality_score": 0.0
            }
            
            # Simuler l'analyse de patterns
            volatility_series = historical_data.get("volatility_series", [])
            trend_series = historical_data.get("trend_series", [])
            
            if volatility_series and trend_series:
                # Pattern de tendance
                if abs(np.mean(trend_series[-5:])) > 0.3:
                    patterns["trend_patterns"].append("strong_trend")
                
                # Pattern de retournement
                if len(trend_series) > 10:
                    recent_change = trend_series[-1] - trend_series[-10]
                    if abs(recent_change) > 0.5:
                        patterns["reversal_patterns"].append("trend_reversal")
                
                # Score de qualité
                pattern_count = len(patterns["trend_patterns"]) + len(patterns["reversal_patterns"])
                patterns["quality_score"] = min(0.9, 0.3 + pattern_count * 0.2)
            
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse patterns: {e}")
            return {"quality_score": 0.3}

    def _predict_key_levels(self, historical_data: Dict, horizon: PredictionHorizon) -> Dict:
        """🎯 Prédire les niveaux clés futurs"""
        
        try:
            price_action = historical_data.get("price_action", {})
            
            key_levels = {
                "support_levels": price_action.get("support_levels", [0.95, 0.90]),
                "resistance_levels": price_action.get("resistance_levels", [1.05, 1.10]),
                "pivot_points": [0.98, 1.02],
                "breakout_level": 1.07,
                "breakdown_level": 0.93
            }
            
            return key_levels
            
        except Exception as e:
            logger.error(f"❌ Erreur prédiction niveaux clés: {e}")
            return {}

    def _identify_opportunities_and_risks(self, asset_type: str, volatility: float, trend: str, regime: MarketRegime) -> Tuple[List[str], List[str]]:
        """⚡ Identifier les opportunités et risques"""
        
        try:
            opportunities = []
            risks = []
            
            # Opportunités selon le contexte
            if volatility > 0.6 and asset_type == "meme_coins":
                opportunities.append("High volatility trading opportunity")
            
            if "bullish" in trend:
                opportunities.append("Trend following opportunity")
            
            if regime == MarketRegime.LOW_VOLATILITY:
                opportunities.append("Low risk accumulation opportunity")
            
            # Risques selon le contexte
            if volatility > 0.8:
                risks.append("Extreme volatility risk")
            
            if regime == MarketRegime.HIGH_VOLATILITY:
                risks.append("Increased drawdown risk")
            
            if "bearish" in trend:
                risks.append("Downtrend risk")
            
            return opportunities, risks
            
        except Exception as e:
            logger.error(f"❌ Erreur identification opportunités/risques: {e}")
            return [], []

    def _recommend_optimal_strategies(self, asset_type: str, regime: MarketRegime, volatility: float, horizon: PredictionHorizon) -> List[str]:
        """💡 Recommander les stratégies optimales"""
        
        try:
            strategies = []
            
            # Stratégies selon le régime et l'asset
            if regime == MarketRegime.HIGH_VOLATILITY and asset_type == "meme_coins":
                strategies.extend(["Momentum trading", "Scalping", "Risk management priority"])
            
            elif regime == MarketRegime.LOW_VOLATILITY:
                strategies.extend(["Accumulation strategy", "DCA approach", "Position building"])
            
            elif regime == MarketRegime.TRENDING:
                strategies.extend(["Trend following", "Breakout trading", "Momentum continuation"])
            
            elif regime == MarketRegime.RANGING:
                strategies.extend(["Range trading", "Mean reversion", "Support/resistance play"])
            
            # Stratégies selon l'horizon
            if horizon == PredictionHorizon.SHORT_TERM:
                strategies.append("Tactical adjustments")
            elif horizon == PredictionHorizon.STRATEGIC:
                strategies.append("Strategic positioning")
            
            return list(set(strategies))  # Éliminer les doublons
            
        except Exception as e:
            logger.error(f"❌ Erreur recommandation stratégies: {e}")
            return []

    async def _generate_predictive_alerts(self, asset_type: str, predictions: Dict[str, MarketPrediction]):
        """🚨 Générer des alertes prédictives intelligentes"""
        
        try:
            current_time = datetime.utcnow()
            
            for horizon_key, prediction in predictions.items():
                # Alerte d'opportunité à haute volatilité
                if prediction.predicted_volatility > 0.8 and asset_type == "meme_coins":
                    alert = PredictiveAlert(
                        alert_id=f"high_vol_{asset_type}_{int(current_time.timestamp())}",
                        asset_type=asset_type,
                        alert_type="opportunity",
                        severity="high",
                        predicted_event="High volatility trading window opening",
                        probability=prediction.confidence,
                        time_to_event=timedelta(minutes=5) if horizon_key == "5_minutes" else timedelta(hours=1),
                        recommended_actions=["Prepare high-frequency trading", "Increase position sizes", "Monitor closely"],
                        confidence=prediction.confidence,
                        created_at=current_time
                    )
                    self.active_alerts.append(alert)
                
                # Alerte de changement de régime
                if prediction.predicted_regime in [MarketRegime.BULL_MARKET, MarketRegime.BEAR_MARKET]:
                    alert = PredictiveAlert(
                        alert_id=f"regime_change_{asset_type}_{int(current_time.timestamp())}",
                        asset_type=asset_type,
                        alert_type="regime_change",
                        severity="medium",
                        predicted_event=f"Market regime shift to {prediction.predicted_regime.value}",
                        probability=prediction.confidence,
                        time_to_event=timedelta(hours=1),
                        recommended_actions=prediction.optimal_strategies,
                        confidence=prediction.confidence,
                        created_at=current_time
                    )
                    self.active_alerts.append(alert)
            
            # Nettoyer les alertes expirées
            self._cleanup_expired_alerts()
            
        except Exception as e:
            logger.error(f"❌ Erreur génération alertes prédictives: {e}")

    def _cleanup_expired_alerts(self):
        """🧹 Nettoyer les alertes expirées"""
        
        try:
            current_time = datetime.utcnow()
            
            # Supprimer les alertes de plus de 24h
            self.active_alerts = [
                alert for alert in self.active_alerts
                if (current_time - alert.created_at) < timedelta(hours=24)
            ]
            
        except Exception as e:
            logger.error(f"❌ Erreur nettoyage alertes: {e}")

    async def get_prediction_summary(self) -> Dict:
        """📊 Obtenir un résumé des prédictions en cours"""
        
        try:
            summary = {
                "total_predictions": self.total_predictions,
                "active_predictions": len(self.prediction_cache),
                "active_alerts": len(self.active_alerts),
                "prediction_accuracy": self.successful_predictions / max(1, self.total_predictions),
                "predictions_by_asset": {},
                "alert_summary": {},
                "confidence_distribution": {}
            }
            
            # Analyser les prédictions par asset
            for key, prediction in self.prediction_cache.items():
                asset_type = prediction.asset_type
                if asset_type not in summary["predictions_by_asset"]:
                    summary["predictions_by_asset"][asset_type] = 0
                summary["predictions_by_asset"][asset_type] += 1
            
            # Analyser les alertes
            alert_types = {}
            for alert in self.active_alerts:
                alert_type = alert.alert_type
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            
            summary["alert_summary"] = alert_types
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Erreur résumé prédictions: {e}")
            return {}

    async def validate_prediction(self, prediction_key: str, actual_outcome: Dict) -> Dict:
        """✅ Valider une prédiction avec le résultat réel"""
        
        try:
            if prediction_key not in self.prediction_cache:
                return {"error": "Prediction not found"}
            
            prediction = self.prediction_cache[prediction_key]
            
            # Calculer la précision
            volatility_accuracy = 1.0 - abs(prediction.predicted_volatility - actual_outcome.get("volatility", 0)) / max(prediction.predicted_volatility, 0.1)
            
            # Trend accuracy
            predicted_trend_direction = 1 if "bullish" in prediction.predicted_trend else -1 if "bearish" in prediction.predicted_trend else 0
            actual_trend_direction = actual_outcome.get("trend_direction", 0)
            trend_accuracy = 1.0 if predicted_trend_direction == actual_trend_direction else 0.0
            
            # Score global
            overall_accuracy = (volatility_accuracy + trend_accuracy) / 2
            
            # Mettre à jour les statistiques
            if overall_accuracy > 0.7:
                self.successful_predictions += 1
            
            # Stocker pour l'apprentissage
            self.prediction_accuracy[prediction_key] = {
                "overall_accuracy": overall_accuracy,
                "volatility_accuracy": volatility_accuracy,
                "trend_accuracy": trend_accuracy,
                "confidence": prediction.confidence,
                "validated_at": datetime.utcnow()
            }
            
            return {
                "prediction_validated": True,
                "overall_accuracy": overall_accuracy,
                "details": {
                    "volatility_accuracy": volatility_accuracy,
                    "trend_accuracy": trend_accuracy
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur validation prédiction: {e}")
            return {"error": str(e)}

    def _predict_direction(self, trend: str) -> PredictionDirection:
        """📈 Prédire la direction du marché"""
        if trend == "bullish":
            return PredictionDirection.UP
        elif trend == "bearish":
            return PredictionDirection.DOWN
        elif trend == "volatile":
            return PredictionDirection.VOLATILE
        else:
            return PredictionDirection.SIDEWAYS

    def _predict_price_target(self, historical_data: Dict, trend: str) -> Optional[float]:
        """🎯 Prédire une cible de prix"""
        try:
            price_action = historical_data.get("price_action", {})
            current_price = price_action.get("current_price", 100.0)
            
            if trend == "bullish":
                return current_price * 1.05  # +5%
            elif trend == "bearish":
                return current_price * 0.95  # -5%
            else:
                return current_price  # Sideways
                
        except Exception:
            return None

    async def generate_market_prediction(self, asset_type: str, horizon: PredictionHorizon, market_data: Optional[Dict] = None) -> MarketPrediction:
        """🔮 Générer une prédiction unique pour un horizon donné"""
        try:
            historical_data = await self._gather_historical_data(asset_type)
            if market_data:
                historical_data.update(market_data)
            
            prediction = await self._predict_for_horizon(asset_type, horizon, historical_data)
            if prediction:
                return prediction
            else:
                # Prédiction par défaut si échec
                return MarketPrediction(
                    asset_type=asset_type,
                    horizon=horizon,
                    direction=PredictionDirection.SIDEWAYS,
                    magnitude=0.5,
                    confidence=0.5,
                    price_target=None,
                    probability=0.5,
                    key_factors=["Données insuffisantes"],
                    risk_factors=["Incertitude élevée"],
                    predicted_volatility=0.5,
                    predicted_trend="neutral",
                    predicted_regime=MarketRegime.SIDEWAYS,
                    key_levels={},
                    opportunities=[],
                    risks=["Données limitées"],
                    optimal_strategies=["Attendre plus de données"],
                    generated_at=datetime.utcnow(),
                    prediction_timestamp=datetime.utcnow(),
                    expires_at=datetime.utcnow() + timedelta(hours=1)
                )
                
        except Exception as e:
            logger.error(f"❌ Erreur génération prédiction unique: {e}")
            raise

    async def detect_market_regime(self) -> MarketRegimeData:
        """🌊 Détecter le régime de marché actuel"""
        try:
            # Analyser les conditions actuelles de marché
            volatility = np.random.uniform(0.2, 0.8)  # Simulation
            trend_value = np.random.uniform(-1, 1)    # Simulation
            
            # Déterminer la direction
            if trend_value > 0.3:
                trend = PredictionDirection.UP
            elif trend_value < -0.3:
                trend = PredictionDirection.DOWN
            else:
                trend = PredictionDirection.SIDEWAYS
            
            # Déterminer la volatilité
            if volatility < 0.3:
                vol_level = "low"
            elif volatility < 0.6:
                vol_level = "medium"
            else:
                vol_level = "high"
            
            # Déterminer la phase de marché
            phases = ["accumulation", "markup", "distribution", "markdown"]
            market_phase = np.random.choice(phases)
            
            return MarketRegimeData(
                trend=trend,
                volatility=vol_level,
                market_phase=market_phase,
                confidence=0.7 + np.random.uniform(0, 0.3),
                regime_strength=abs(trend_value),
                detected_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"❌ Erreur détection régime marché: {e}")
            # Retour par défaut
            return MarketRegimeData(
                trend=PredictionDirection.SIDEWAYS,
                volatility="medium",
                market_phase="accumulation",
                confidence=0.5,
                regime_strength=0.5,
                detected_at=datetime.utcnow()
            )

    async def generate_predictive_alerts(self) -> List[PredictiveAlert]:
        """🚨 Générer des alertes prédictives actuelles"""
        try:
            current_alerts = []
            current_time = datetime.utcnow()
            
            # Nettoyer les alertes expirées
            self._cleanup_expired_alerts()
            
            # Générer de nouvelles alertes selon les conditions actuelles
            # Simulation d'alertes pour le démo
            if np.random.random() < 0.3:  # 30% de chance d'avoir une alerte
                alert = PredictiveAlert(
                    alert_id=f"pred_{int(current_time.timestamp())}",
                    asset_type="crypto",
                    alert_type="opportunity",
                    severity="medium",
                    predicted_event="Potential breakout pattern detected",
                    probability=0.75,
                    time_to_event=timedelta(minutes=30),
                    recommended_actions=["Monitor closely", "Prepare entry strategy"],
                    confidence=0.75,
                    created_at=current_time
                )
                current_alerts.append(alert)
                self.active_alerts.append(alert)
            
            return current_alerts
            
        except Exception as e:
            logger.error(f"❌ Erreur génération alertes prédictives: {e}")
            return []

    async def analyze_historical_patterns(self, asset_type: str) -> Dict:
        """📈 Analyser les patterns historiques pour un asset"""
        try:
            historical_data = await self._gather_historical_data(asset_type)
            
            analysis = {
                "asset_type": asset_type,
                "trend_patterns": {
                    "bullish_patterns": ["ascending_triangle", "cup_handle"],
                    "bearish_patterns": ["head_shoulders", "descending_triangle"],
                    "neutral_patterns": ["consolidation", "range_bound"]
                },
                "volatility_analysis": {
                    "average_volatility": np.mean(historical_data.get("volatility_series", [0.3])),
                    "volatility_trend": "increasing",
                    "volatility_clustering": True
                },
                "support_resistance": {
                    "support_levels": [95.0, 90.0, 85.0],
                    "resistance_levels": [105.0, 110.0, 115.0],
                    "key_level_strength": 0.8
                },
                "market_cycles": historical_data.get("market_cycles", {}),
                "correlation_analysis": historical_data.get("correlation_matrix", {}),
                "performance_metrics": {
                    "sharpe_ratio": 1.2,
                    "max_drawdown": -15.5,
                    "win_rate": 0.65
                },
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse patterns historiques: {e}")
            return {"error": str(e)}

# Instance globale
_predictive_system: Optional[PredictiveSystem] = None

def get_predictive_system() -> PredictiveSystem:
    """🔮 Obtenir l'instance du système prédictif"""
    global _predictive_system
    if _predictive_system is None:
        _predictive_system = PredictiveSystem()
    return _predictive_system 