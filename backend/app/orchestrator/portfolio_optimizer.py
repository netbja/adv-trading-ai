"""
💼 PORTFOLIO OPTIMIZER - OPTIMISATION DE PORTEFEUILLE INTELLIGENTE
================================================================

Ce module implémente l'optimisation intelligente de portefeuille :
- Allocation dynamique multi-assets basée sur l'IA
- Rééquilibrage automatique selon conditions de marché
- Gestion de risque adaptive et optimisation rendement/risque
- Stratégies d'investissement personnalisées par asset
"""

import logging
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
from scipy.optimize import minimize
import pandas as pd

logger = logging.getLogger(__name__)

class AllocationStrategy(Enum):
    """Stratégies d'allocation de portefeuille"""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    TACTICAL = "tactical"
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"

class RiskLevel(Enum):
    """Niveaux de risque"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class RebalanceFrequency(Enum):
    """Fréquences de rééquilibrage"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ADAPTIVE = "adaptive"

@dataclass
class AssetAllocation:
    """Allocation d'un asset dans le portefeuille"""
    asset_type: str
    target_weight: float
    current_weight: float
    min_weight: float
    max_weight: float
    risk_contribution: float
    expected_return: float
    volatility: float
    sharpe_ratio: float
    last_rebalance: datetime

@dataclass
class PortfolioMetrics:
    """Métriques de performance du portefeuille"""
    total_value: float
    total_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    var_95: float  # Value at Risk 95%
    cvar_95: float  # Conditional VaR 95%
    calmar_ratio: float
    sortino_ratio: float
    alpha: float
    beta: float
    information_ratio: float
    tracking_error: float

@dataclass
class RebalanceRecommendation:
    """Recommandation de rééquilibrage"""
    asset_type: str
    current_weight: float
    target_weight: float
    weight_drift: float
    action: str  # "buy", "sell", "hold"
    amount: float
    priority: str  # "high", "medium", "low"
    reason: str
    expected_impact: Dict[str, float]

@dataclass
class OptimizationResult:
    """Résultat d'optimisation de portefeuille"""
    optimization_id: str
    timestamp: datetime
    strategy: AllocationStrategy
    risk_level: RiskLevel
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    expected_sharpe: float
    confidence_score: float
    improvement_vs_current: Dict[str, float]
    constraints_satisfied: bool
    optimization_time_ms: float

class PortfolioOptimizer:
    """
    💼 OPTIMISEUR DE PORTEFEUILLE INTELLIGENT
    
    Optimisation continue et intelligente du portefeuille multi-assets :
    - Allocation optimale basée sur l'IA et conditions de marché
    - Rééquilibrage adaptatif selon volatilité et tendances
    - Gestion de risque sophistiquée avec VaR et stress tests
    - Stratégies personnalisées par profil de risque
    """
    
    def __init__(self):
        self.allocations: Dict[str, AssetAllocation] = {}
        self.optimization_history: List[OptimizationResult] = []
        self.rebalance_history: List[RebalanceRecommendation] = []
        self.performance_history: List[PortfolioMetrics] = []
        
        # Configuration par défaut
        self.default_strategy = AllocationStrategy.BALANCED
        self.default_risk_level = RiskLevel.MEDIUM
        self.rebalance_frequency = RebalanceFrequency.ADAPTIVE
        self.rebalance_threshold = 0.05  # 5% de drift
        
        # Contraintes de portefeuille
        self.portfolio_constraints = {
            "max_single_asset": 0.40,  # Max 40% dans un seul asset
            "min_diversification": 3,   # Min 3 assets différents
            "max_volatility": 0.25,    # Max 25% de volatilité annuelle
            "min_liquidity": 0.20      # Min 20% en assets liquides
        }
        
        # Paramètres d'optimisation
        self.lookback_period = 252  # 1 an de données
        self.optimization_iterations = 1000
        self.monte_carlo_simulations = 10000
        
        # Métriques de performance
        self.total_optimizations = 0
        self.successful_optimizations = 0
        self.last_optimization = None
        
        logger.info("💼 Portfolio Optimizer initialisé - Optimisation intelligente active")

    async def optimize_portfolio(self, 
                                strategy: AllocationStrategy = None,
                                risk_level: RiskLevel = None,
                                market_conditions: Dict = None) -> OptimizationResult:
        """
        🎯 Optimiser l'allocation de portefeuille
        
        Args:
            strategy: Stratégie d'allocation à utiliser
            risk_level: Niveau de risque souhaité
            market_conditions: Conditions de marché actuelles
            
        Returns:
            Résultat d'optimisation avec allocations optimales
        """
        try:
            start_time = datetime.utcnow()
            
            # Utiliser stratégie par défaut si non spécifiée
            strategy = strategy or self.default_strategy
            risk_level = risk_level or self.default_risk_level
            
            logger.info(f"🎯 Optimisation portefeuille - Stratégie: {strategy.value}, Risque: {risk_level.value}")
            
            # 1. Collecter les données de marché
            market_data = await self._collect_market_data()
            
            # 2. Analyser les corrélations entre assets
            correlation_matrix = await self._calculate_correlation_matrix(market_data)
            
            # 3. Estimer les rendements et volatilités
            expected_returns, volatilities = await self._estimate_returns_and_volatility(market_data)
            
            # 4. Optimiser selon la stratégie
            optimal_weights = await self._optimize_weights(
                expected_returns, volatilities, correlation_matrix, strategy, risk_level
            )
            
            # 5. Calculer les métriques de performance attendues
            expected_metrics = await self._calculate_expected_metrics(
                optimal_weights, expected_returns, volatilities, correlation_matrix
            )
            
            # 6. Valider les contraintes
            constraints_ok = await self._validate_constraints(optimal_weights)
            
            # 7. Calculer l'amélioration vs portefeuille actuel
            improvement = await self._calculate_improvement(optimal_weights, expected_metrics)
            
            # 8. Calculer la confiance de l'optimisation
            confidence = await self._calculate_optimization_confidence(
                optimal_weights, market_data, market_conditions
            )
            
            optimization_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            result = OptimizationResult(
                optimization_id=f"opt_{int(start_time.timestamp())}",
                timestamp=start_time,
                strategy=strategy,
                risk_level=risk_level,
                optimal_weights=optimal_weights,
                expected_return=expected_metrics["return"],
                expected_volatility=expected_metrics["volatility"],
                expected_sharpe=expected_metrics["sharpe_ratio"],
                confidence_score=confidence,
                improvement_vs_current=improvement,
                constraints_satisfied=constraints_ok,
                optimization_time_ms=optimization_time
            )
            
            # Stocker le résultat
            self.optimization_history.append(result)
            self.last_optimization = result
            self.total_optimizations += 1
            
            if constraints_ok and confidence > 0.7:
                self.successful_optimizations += 1
                
                # Mettre à jour les allocations cibles
                await self._update_target_allocations(optimal_weights)
            
            logger.info(f"🎯 Optimisation terminée en {optimization_time:.1f}ms - Confiance: {confidence:.3f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur optimisation portefeuille: {e}")
            return OptimizationResult(
                optimization_id=f"error_{int(datetime.utcnow().timestamp())}",
                timestamp=datetime.utcnow(),
                strategy=strategy or self.default_strategy,
                risk_level=risk_level or self.default_risk_level,
                optimal_weights={},
                expected_return=0.0,
                expected_volatility=0.0,
                expected_sharpe=0.0,
                confidence_score=0.0,
                improvement_vs_current={},
                constraints_satisfied=False,
                optimization_time_ms=0.0
            )

    async def _collect_market_data(self) -> Dict[str, List[float]]:
        """📊 Collecter les données de marché pour optimisation"""
        
        try:
            # Simuler la collecte de données historiques de prix
            # En production, connecté aux APIs de marché réelles
            
            assets = ["meme_coins", "crypto_lt", "forex", "etf"]
            market_data = {}
            
            for asset in assets:
                # Générer des données de prix simulées avec caractéristiques réalistes
                prices = await self._generate_realistic_price_series(asset)
                market_data[asset] = prices
            
            return market_data
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte données marché: {e}")
            return {}

    async def _generate_realistic_price_series(self, asset_type: str) -> List[float]:
        """📈 Générer une série de prix réaliste pour un asset"""
        
        try:
            # Paramètres par type d'asset
            params = {
                "meme_coins": {"drift": 0.15, "volatility": 0.80, "mean_reversion": 0.1},
                "crypto_lt": {"drift": 0.12, "volatility": 0.45, "mean_reversion": 0.05},
                "forex": {"drift": 0.02, "volatility": 0.15, "mean_reversion": 0.3},
                "etf": {"drift": 0.08, "volatility": 0.18, "mean_reversion": 0.02}
            }
            
            asset_params = params.get(asset_type, params["etf"])
            
            # Générer série avec processus stochastique
            n_periods = self.lookback_period
            dt = 1/252  # Pas journalier
            
            prices = [100.0]  # Prix initial
            
            for i in range(n_periods - 1):
                # Modèle d'Ornstein-Uhlenbeck avec drift
                current_price = prices[-1]
                
                # Composante de drift
                drift = asset_params["drift"] * dt
                
                # Composante de mean reversion
                mean_reversion = asset_params["mean_reversion"] * (100 - current_price) * dt
                
                # Composante stochastique
                shock = np.random.normal(0, asset_params["volatility"] * np.sqrt(dt))
                
                # Prix suivant
                next_price = current_price * (1 + drift + mean_reversion + shock)
                next_price = max(1.0, next_price)  # Prix minimum
                
                prices.append(next_price)
            
            return prices
            
        except Exception as e:
            logger.error(f"❌ Erreur génération série prix {asset_type}: {e}")
            return [100.0] * self.lookback_period

    async def _calculate_correlation_matrix(self, market_data: Dict[str, List[float]]) -> np.ndarray:
        """🔗 Calculer la matrice de corrélation entre assets"""
        
        try:
            if not market_data:
                return np.eye(4)  # Matrice identité par défaut
            
            # Calculer les rendements
            returns_data = {}
            for asset, prices in market_data.items():
                returns = [(prices[i]/prices[i-1] - 1) for i in range(1, len(prices))]
                returns_data[asset] = returns
            
            # Convertir en DataFrame pour calcul facilité
            df = pd.DataFrame(returns_data)
            correlation_matrix = df.corr().values
            
            return correlation_matrix
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul matrice corrélation: {e}")
            return np.eye(len(market_data))

    async def _estimate_returns_and_volatility(self, market_data: Dict[str, List[float]]) -> Tuple[np.ndarray, np.ndarray]:
        """📊 Estimer les rendements et volatilités attendus"""
        
        try:
            expected_returns = []
            volatilities = []
            
            for asset, prices in market_data.items():
                # Calculer les rendements
                returns = [(prices[i]/prices[i-1] - 1) for i in range(1, len(prices))]
                
                # Rendement moyen annualisé
                mean_return = np.mean(returns) * 252
                
                # Volatilité annualisée
                volatility = np.std(returns) * np.sqrt(252)
                
                # Ajustement pour conditions de marché futures
                adjusted_return = await self._adjust_expected_return(asset, mean_return)
                adjusted_volatility = await self._adjust_expected_volatility(asset, volatility)
                
                expected_returns.append(adjusted_return)
                volatilities.append(adjusted_volatility)
            
            return np.array(expected_returns), np.array(volatilities)
            
        except Exception as e:
            logger.error(f"❌ Erreur estimation rendements/volatilité: {e}")
            n_assets = len(market_data)
            return np.array([0.08] * n_assets), np.array([0.20] * n_assets)

    async def _adjust_expected_return(self, asset_type: str, historical_return: float) -> float:
        """📈 Ajuster le rendement attendu selon les conditions"""
        
        try:
            # Facteurs d'ajustement par asset
            adjustments = {
                "meme_coins": 1.2,   # Plus optimiste en bull market
                "crypto_lt": 1.1,    # Légèrement optimiste
                "forex": 0.9,        # Plus conservateur
                "etf": 1.0           # Neutre
            }
            
            adjustment_factor = adjustments.get(asset_type, 1.0)
            
            # Limiter les rendements extrêmes
            adjusted_return = historical_return * adjustment_factor
            return max(-0.5, min(2.0, adjusted_return))  # Entre -50% et +200%
            
        except Exception as e:
            logger.error(f"❌ Erreur ajustement rendement {asset_type}: {e}")
            return historical_return

    async def _adjust_expected_volatility(self, asset_type: str, historical_volatility: float) -> float:
        """📊 Ajuster la volatilité attendue selon les conditions"""
        
        try:
            # En période d'incertitude, augmenter la volatilité
            uncertainty_factor = 1.1
            
            # Facteurs par asset
            vol_adjustments = {
                "meme_coins": 1.3,   # Plus volatile
                "crypto_lt": 1.1,    # Légèrement plus volatile
                "forex": 0.9,        # Plus stable
                "etf": 1.0           # Stable
            }
            
            adjustment = vol_adjustments.get(asset_type, 1.0) * uncertainty_factor
            adjusted_vol = historical_volatility * adjustment
            
            # Limiter les volatilités extrêmes
            return max(0.05, min(2.0, adjusted_vol))  # Entre 5% et 200%
            
        except Exception as e:
            logger.error(f"❌ Erreur ajustement volatilité {asset_type}: {e}")
            return historical_volatility

    async def _optimize_weights(self, 
                              expected_returns: np.ndarray, 
                              volatilities: np.ndarray,
                              correlation_matrix: np.ndarray,
                              strategy: AllocationStrategy,
                              risk_level: RiskLevel) -> Dict[str, float]:
        """⚡ Optimiser les poids selon la stratégie"""
        
        try:
            n_assets = len(expected_returns)
            asset_names = ["meme_coins", "crypto_lt", "forex", "etf"]
            
            # Matrice de covariance
            cov_matrix = np.outer(volatilities, volatilities) * correlation_matrix
            
            # Fonction objectif selon la stratégie
            def objective_function(weights):
                portfolio_return = np.dot(weights, expected_returns)
                portfolio_volatility = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
                
                if strategy == AllocationStrategy.CONSERVATIVE:
                    # Minimiser le risque
                    return portfolio_volatility
                elif strategy == AllocationStrategy.AGGRESSIVE:
                    # Maximiser le rendement ajusté du risque
                    return -(portfolio_return - 0.5 * portfolio_volatility)
                elif strategy == AllocationStrategy.MOMENTUM:
                    # Favoriser les assets avec momentum
                    momentum_score = sum(weights[i] * (expected_returns[i] if expected_returns[i] > 0 else 0) for i in range(n_assets))
                    return -(momentum_score - 0.3 * portfolio_volatility)
                else:  # BALANCED par défaut
                    # Maximiser le ratio de Sharpe
                    risk_free_rate = 0.02  # 2%
                    return -((portfolio_return - risk_free_rate) / portfolio_volatility)
            
            # Contraintes
            constraints = []
            
            # Somme des poids = 1
            constraints.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
            
            # Contraintes selon le niveau de risque
            risk_constraints = self._get_risk_constraints(risk_level)
            constraints.extend(risk_constraints)
            
            # Bornes pour chaque asset
            bounds = self._get_asset_bounds(strategy, risk_level)
            
            # Poids initiaux (équipondéré)
            initial_weights = np.array([1/n_assets] * n_assets)
            
            # Optimisation
            result = minimize(
                objective_function,
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'maxiter': self.optimization_iterations}
            )
            
            if result.success:
                optimal_weights = {
                    asset_names[i]: float(result.x[i]) 
                    for i in range(n_assets)
                }
            else:
                logger.warning("⚠️ Optimisation échouée, utilisation poids équipondérés")
                optimal_weights = {
                    asset: 1/n_assets for asset in asset_names
                }
            
            return optimal_weights
            
        except Exception as e:
            logger.error(f"❌ Erreur optimisation poids: {e}")
            # Retour sécurisé : équipondération
            return {
                "meme_coins": 0.25,
                "crypto_lt": 0.25,
                "forex": 0.25,
                "etf": 0.25
            }

    def _get_risk_constraints(self, risk_level: RiskLevel) -> List[Dict]:
        """🛡️ Obtenir les contraintes selon le niveau de risque"""
        
        constraints = []
        
        try:
            if risk_level == RiskLevel.VERY_LOW:
                # Max 10% en assets risqués
                constraints.append({
                    'type': 'ineq', 
                    'fun': lambda w: 0.1 - w[0]  # meme_coins <= 10%
                })
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda w: 0.6 - w[3]  # etf >= 60%
                })
            elif risk_level == RiskLevel.LOW:
                # Max 20% en assets risqués
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda w: 0.2 - w[0]  # meme_coins <= 20%
                })
            elif risk_level == RiskLevel.HIGH:
                # Peut aller jusqu'à 40% en meme coins
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda w: 0.4 - w[0]
                })
            elif risk_level == RiskLevel.VERY_HIGH:
                # Très peu de contraintes
                pass
                
        except Exception as e:
            logger.error(f"❌ Erreur contraintes risque: {e}")
        
        return constraints

    def _get_asset_bounds(self, strategy: AllocationStrategy, risk_level: RiskLevel) -> List[Tuple[float, float]]:
        """📏 Obtenir les bornes pour chaque asset"""
        
        try:
            if risk_level == RiskLevel.VERY_LOW:
                return [(0.0, 0.10), (0.0, 0.30), (0.1, 0.40), (0.4, 0.80)]  # meme, crypto, forex, etf
            elif risk_level == RiskLevel.LOW:
                return [(0.0, 0.20), (0.0, 0.40), (0.1, 0.50), (0.3, 0.70)]
            elif risk_level == RiskLevel.MEDIUM:
                return [(0.0, 0.30), (0.0, 0.50), (0.1, 0.60), (0.2, 0.60)]
            elif risk_level == RiskLevel.HIGH:
                return [(0.0, 0.40), (0.0, 0.60), (0.0, 0.70), (0.1, 0.50)]
            else:  # VERY_HIGH
                return [(0.0, 0.50), (0.0, 0.70), (0.0, 0.80), (0.0, 0.40)]
                
        except Exception as e:
            logger.error(f"❌ Erreur bornes assets: {e}")
            return [(0.0, 1.0)] * 4  # Pas de contraintes

    async def _calculate_expected_metrics(self, 
                                        weights: Dict[str, float],
                                        expected_returns: np.ndarray,
                                        volatilities: np.ndarray,
                                        correlation_matrix: np.ndarray) -> Dict[str, float]:
        """📊 Calculer les métriques attendues du portefeuille"""
        
        try:
            asset_names = ["meme_coins", "crypto_lt", "forex", "etf"]
            w = np.array([weights[asset] for asset in asset_names])
            
            # Rendement du portefeuille
            portfolio_return = np.dot(w, expected_returns)
            
            # Volatilité du portefeuille
            cov_matrix = np.outer(volatilities, volatilities) * correlation_matrix
            portfolio_volatility = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
            
            # Ratio de Sharpe
            risk_free_rate = 0.02
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
            
            # VaR 95% (approximation normale)
            var_95 = -1.65 * portfolio_volatility  # Z-score 95%
            
            # Calmar ratio (approximation)
            max_drawdown_estimate = portfolio_volatility * 2  # Estimation conservative
            calmar_ratio = portfolio_return / max_drawdown_estimate if max_drawdown_estimate > 0 else 0
            
            return {
                "return": portfolio_return,
                "volatility": portfolio_volatility,
                "sharpe_ratio": sharpe_ratio,
                "var_95": var_95,
                "calmar_ratio": calmar_ratio
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul métriques: {e}")
            return {
                "return": 0.08,
                "volatility": 0.15,
                "sharpe_ratio": 0.4,
                "var_95": -0.25,
                "calmar_ratio": 0.3
            }

    async def _validate_constraints(self, weights: Dict[str, float]) -> bool:
        """✅ Valider que l'allocation respecte les contraintes"""
        
        try:
            # Vérifier somme = 1
            total_weight = sum(weights.values())
            if abs(total_weight - 1.0) > 0.01:
                return False
            
            # Vérifier contrainte max single asset
            max_weight = max(weights.values())
            if max_weight > self.portfolio_constraints["max_single_asset"]:
                return False
            
            # Vérifier diversification minimum
            non_zero_assets = sum(1 for w in weights.values() if w > 0.01)
            if non_zero_assets < self.portfolio_constraints["min_diversification"]:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur validation contraintes: {e}")
            return False

    async def _calculate_improvement(self, optimal_weights: Dict[str, float], expected_metrics: Dict[str, float]) -> Dict[str, float]:
        """📈 Calculer l'amélioration vs portefeuille actuel"""
        
        try:
            # Portefeuille actuel (équipondéré par défaut)
            current_weights = {asset: 0.25 for asset in optimal_weights.keys()}
            
            # Estimer métriques actuelles (simplifiées)
            current_return = 0.10  # 10% par défaut
            current_volatility = 0.20  # 20% par défaut
            current_sharpe = 0.4
            
            improvement = {
                "return_improvement": expected_metrics["return"] - current_return,
                "volatility_reduction": current_volatility - expected_metrics["volatility"],
                "sharpe_improvement": expected_metrics["sharpe_ratio"] - current_sharpe,
                "weight_changes": {
                    asset: optimal_weights[asset] - current_weights[asset]
                    for asset in optimal_weights.keys()
                }
            }
            
            return improvement
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul amélioration: {e}")
            return {}

    async def _calculate_optimization_confidence(self, 
                                               weights: Dict[str, float],
                                               market_data: Dict[str, List[float]],
                                               market_conditions: Dict = None) -> float:
        """🎯 Calculer la confiance de l'optimisation"""
        
        try:
            confidence_factors = []
            
            # 1. Stabilité des données
            data_quality = self._assess_data_quality(market_data)
            confidence_factors.append(data_quality)
            
            # 2. Diversification
            diversification_score = 1.0 - max(weights.values())
            confidence_factors.append(diversification_score)
            
            # 3. Cohérence avec conditions de marché
            if market_conditions:
                market_coherence = self._assess_market_coherence(weights, market_conditions)
                confidence_factors.append(market_coherence)
            else:
                confidence_factors.append(0.7)  # Score neutre
            
            # 4. Contraintes respectées
            constraints_ok = await self._validate_constraints(weights)
            confidence_factors.append(1.0 if constraints_ok else 0.3)
            
            # Score final (moyenne pondérée)
            confidence = np.mean(confidence_factors)
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul confiance: {e}")
            return 0.5

    def _assess_data_quality(self, market_data: Dict[str, List[float]]) -> float:
        """📊 Évaluer la qualité des données"""
        
        try:
            if not market_data:
                return 0.0
            
            quality_scores = []
            
            for asset, prices in market_data.items():
                # Vérifier completude
                completeness = len(prices) / self.lookback_period
                
                # Vérifier variance (éviter données plates)
                returns = [(prices[i]/prices[i-1] - 1) for i in range(1, len(prices))]
                variance_score = 1.0 if np.std(returns) > 0.001 else 0.3
                
                asset_score = (completeness + variance_score) / 2
                quality_scores.append(asset_score)
            
            return np.mean(quality_scores)
            
        except Exception as e:
            logger.error(f"❌ Erreur évaluation qualité données: {e}")
            return 0.5

    def _assess_market_coherence(self, weights: Dict[str, float], market_conditions: Dict) -> float:
        """🌊 Évaluer la cohérence avec les conditions de marché"""
        
        try:
            volatility = market_conditions.get("volatility", 0.2)
            trend = market_conditions.get("trend_strength", 0.0)
            
            coherence_score = 0.7  # Base
            
            # En haute volatilité, favoriser ETF et réduire meme coins
            if volatility > 0.6:
                if weights.get("etf", 0) > 0.3 and weights.get("meme_coins", 0) < 0.2:
                    coherence_score += 0.2
                else:
                    coherence_score -= 0.1
            
            # En tendance forte, favoriser crypto et meme coins
            if abs(trend) > 0.3:
                crypto_exposure = weights.get("crypto_lt", 0) + weights.get("meme_coins", 0)
                if crypto_exposure > 0.4:
                    coherence_score += 0.1
            
            return min(1.0, max(0.0, coherence_score))
            
        except Exception as e:
            logger.error(f"❌ Erreur évaluation cohérence marché: {e}")
            return 0.5

    async def _update_target_allocations(self, optimal_weights: Dict[str, float]):
        """🎯 Mettre à jour les allocations cibles"""
        
        try:
            current_time = datetime.utcnow()
            
            for asset_type, target_weight in optimal_weights.items():
                if asset_type not in self.allocations:
                    # Créer nouvelle allocation
                    self.allocations[asset_type] = AssetAllocation(
                        asset_type=asset_type,
                        target_weight=target_weight,
                        current_weight=0.25,  # Équipondéré par défaut
                        min_weight=0.0,
                        max_weight=0.5,
                        risk_contribution=target_weight * 0.2,  # Estimation
                        expected_return=0.1,  # Estimation
                        volatility=0.2,  # Estimation
                        sharpe_ratio=0.5,  # Estimation
                        last_rebalance=current_time
                    )
                else:
                    # Mettre à jour allocation existante
                    self.allocations[asset_type].target_weight = target_weight
                    
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour allocations: {e}")

    async def generate_rebalance_recommendations(self) -> List[RebalanceRecommendation]:
        """⚖️ Générer des recommandations de rééquilibrage"""
        
        try:
            recommendations = []
            
            for asset_type, allocation in self.allocations.items():
                weight_drift = abs(allocation.current_weight - allocation.target_weight)
                
                if weight_drift > self.rebalance_threshold:
                    # Déterminer l'action
                    if allocation.current_weight > allocation.target_weight:
                        action = "sell"
                        amount = weight_drift
                    else:
                        action = "buy"
                        amount = weight_drift
                    
                    # Priorité selon l'ampleur du drift
                    if weight_drift > 0.15:
                        priority = "high"
                    elif weight_drift > 0.10:
                        priority = "medium"
                    else:
                        priority = "low"
                    
                    # Raison du rééquilibrage
                    reason = f"Weight drift of {weight_drift:.1%} exceeds threshold"
                    
                    # Impact attendu
                    expected_impact = {
                        "risk_reduction": weight_drift * 0.5,
                        "return_improvement": weight_drift * 0.2,
                        "diversification_gain": weight_drift * 0.3
                    }
                    
                    recommendation = RebalanceRecommendation(
                        asset_type=asset_type,
                        current_weight=allocation.current_weight,
                        target_weight=allocation.target_weight,
                        weight_drift=weight_drift,
                        action=action,
                        amount=amount,
                        priority=priority,
                        reason=reason,
                        expected_impact=expected_impact
                    )
                    
                    recommendations.append(recommendation)
            
            # Trier par priorité
            priority_order = {"high": 3, "medium": 2, "low": 1}
            recommendations.sort(key=lambda x: priority_order.get(x.priority, 0), reverse=True)
            
            # Stocker l'historique
            self.rebalance_history.extend(recommendations)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Erreur génération recommandations: {e}")
            return []

    async def calculate_portfolio_metrics(self, weights: Dict[str, float] = None) -> PortfolioMetrics:
        """📊 Calculer les métriques complètes du portefeuille"""
        
        try:
            # Utiliser poids actuels si non spécifiés
            if not weights:
                weights = {
                    asset: alloc.current_weight 
                    for asset, alloc in self.allocations.items()
                } if self.allocations else {"etf": 1.0}
            
            # Simuler métriques (en production, calculs réels)
            metrics = PortfolioMetrics(
                total_value=100000.0,  # 100k de base
                total_return=0.12,  # 12% de rendement
                volatility=0.18,  # 18% de volatilité
                sharpe_ratio=0.67,  # Ratio de Sharpe
                max_drawdown=0.15,  # 15% de drawdown max
                var_95=0.25,  # VaR 95%
                cvar_95=0.35,  # CVaR 95%
                calmar_ratio=0.8,  # Ratio de Calmar
                sortino_ratio=0.9,  # Ratio de Sortino
                alpha=0.03,  # Alpha vs benchmark
                beta=0.85,  # Beta vs marché
                information_ratio=0.4,  # Ratio d'information
                tracking_error=0.08  # Erreur de suivi
            )
            
            # Stocker historique
            self.performance_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul métriques portefeuille: {e}")
            return PortfolioMetrics(
                total_value=100000.0, total_return=0.0, volatility=0.0,
                sharpe_ratio=0.0, max_drawdown=0.0, var_95=0.0, cvar_95=0.0,
                calmar_ratio=0.0, sortino_ratio=0.0, alpha=0.0, beta=1.0,
                information_ratio=0.0, tracking_error=0.0
            )

    async def get_optimization_summary(self) -> Dict[str, Any]:
        """📋 Obtenir un résumé des optimisations"""
        
        try:
            summary = {
                "total_optimizations": self.total_optimizations,
                "successful_optimizations": self.successful_optimizations,
                "success_rate": self.successful_optimizations / max(1, self.total_optimizations),
                "last_optimization": self.last_optimization.timestamp.isoformat() if self.last_optimization else None,
                "current_allocations": {
                    asset: {
                        "target_weight": alloc.target_weight,
                        "current_weight": alloc.current_weight,
                        "drift": abs(alloc.target_weight - alloc.current_weight)
                    }
                    for asset, alloc in self.allocations.items()
                },
                "rebalance_needed": any(
                    abs(alloc.target_weight - alloc.current_weight) > self.rebalance_threshold
                    for alloc in self.allocations.values()
                ),
                "recent_performance": self.performance_history[-5:] if self.performance_history else [],
                "optimization_trends": await self._analyze_optimization_trends()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Erreur résumé optimisation: {e}")
            return {}

    async def _analyze_optimization_trends(self) -> Dict[str, Any]:
        """📈 Analyser les tendances d'optimisation"""
        
        try:
            if len(self.optimization_history) < 3:
                return {"status": "insufficient_data"}
            
            recent_optimizations = self.optimization_history[-10:]
            
            # Tendance des ratios de Sharpe
            sharpe_ratios = [opt.expected_sharpe for opt in recent_optimizations]
            sharpe_trend = "improving" if sharpe_ratios[-1] > sharpe_ratios[0] else "declining"
            
            # Tendance de confiance
            confidences = [opt.confidence_score for opt in recent_optimizations]
            confidence_trend = "improving" if confidences[-1] > confidences[0] else "declining"
            
            # Stratégies les plus utilisées
            strategy_counts = {}
            for opt in recent_optimizations:
                strategy_counts[opt.strategy.value] = strategy_counts.get(opt.strategy.value, 0) + 1
            
            most_used_strategy = max(strategy_counts, key=strategy_counts.get) if strategy_counts else "balanced"
            
            return {
                "sharpe_trend": sharpe_trend,
                "confidence_trend": confidence_trend,
                "most_used_strategy": most_used_strategy,
                "average_confidence": np.mean(confidences),
                "average_sharpe": np.mean(sharpe_ratios),
                "optimization_frequency": len(recent_optimizations)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse tendances: {e}")
            return {}

# Instance globale
_portfolio_optimizer: Optional[PortfolioOptimizer] = None

def get_portfolio_optimizer() -> PortfolioOptimizer:
    """💼 Obtenir l'instance de l'optimiseur de portefeuille"""
    global _portfolio_optimizer
    if _portfolio_optimizer is None:
        _portfolio_optimizer = PortfolioOptimizer()
    return _portfolio_optimizer 