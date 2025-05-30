"""
🧠 AI DECISION ENGINE
Moteur de décision intelligent pour l'orchestrateur
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.market import MarketData
from ..models.system import SystemHealth
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2 
    MEDIUM = 3
    LOW = 4

class TaskType(Enum):
    MARKET_ANALYSIS = "market_analysis"
    TRADING_EXECUTION = "trading_execution"
    SYSTEM_HEALTH = "system_health"
    DATA_SYNC = "data_sync"
    AI_LEARNING = "ai_learning"
    RISK_ASSESSMENT = "risk_assessment"

@dataclass
class MarketCondition:
    volatility: float
    trend_strength: float
    volume_ratio: float
    sentiment_score: float
    news_impact: float
    timestamp: datetime

@dataclass
class SystemStatus:
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int
    error_rate: float
    response_time: float

@dataclass
class TaskRecommendation:
    task_type: TaskType
    priority: Priority
    frequency_minutes: int
    reason: str
    confidence: float
    parameters: Dict

class DecisionEngine:
    """
    🧠 Moteur de décision intelligent de l'orchestrateur
    
    Analyse les conditions de marché, l'état du système et les performances
    pour décider intelligemment quand et comment exécuter les tâches.
    """
    
    def __init__(self):
        self.market_threshold_high_volatility = 0.7
        self.market_threshold_strong_trend = 0.6
        self.system_threshold_high_load = 0.8
        self.min_confidence_threshold = 0.6
        
    async def analyze_current_conditions(self) -> Tuple[MarketCondition, SystemStatus]:
        """Analyse les conditions actuelles du marché et du système"""
        
        market_condition = await self._analyze_market_conditions()
        system_status = await self._analyze_system_status()
        
        logger.info(f"🔍 Conditions analysées - Volatilité: {market_condition.volatility:.2f}, "
                   f"CPU: {system_status.cpu_usage:.1f}%")
        
        return market_condition, system_status

    async def generate_recommendations(self, 
                                     market_condition: MarketCondition, 
                                     system_status: SystemStatus) -> List[TaskRecommendation]:
        """Génère des recommandations intelligentes de tâches"""
        
        recommendations = []
        
        # 🔥 LOGIQUE DE PRIORISATION INTELLIGENTE
        
        # 1. Analyse de marché haute priorité si volatilité élevée
        if market_condition.volatility > self.market_threshold_high_volatility:
            recommendations.append(TaskRecommendation(
                task_type=TaskType.MARKET_ANALYSIS,
                priority=Priority.HIGH,
                frequency_minutes=2,  # Plus fréquent
                reason=f"Volatilité élevée détectée: {market_condition.volatility:.2f}",
                confidence=0.9,
                parameters={"deep_analysis": True, "risk_mode": "conservative"}
            ))
        else:
            recommendations.append(TaskRecommendation(
                task_type=TaskType.MARKET_ANALYSIS,
                priority=Priority.MEDIUM,
                frequency_minutes=5,  # Normal
                reason="Conditions de marché normales",
                confidence=0.7,
                parameters={"deep_analysis": False}
            ))

        # 2. Trading plus agressif si tendance forte
        if market_condition.trend_strength > self.market_threshold_strong_trend:
            recommendations.append(TaskRecommendation(
                task_type=TaskType.TRADING_EXECUTION,
                priority=Priority.HIGH,
                frequency_minutes=3,
                reason=f"Tendance forte détectée: {market_condition.trend_strength:.2f}",
                confidence=0.85,
                parameters={"position_size_multiplier": 1.2, "risk_tolerance": "medium"}
            ))

        # 3. Surveillance système renforcée si charge élevée
        if system_status.cpu_usage > self.system_threshold_high_load * 100:
            recommendations.append(TaskRecommendation(
                task_type=TaskType.SYSTEM_HEALTH,
                priority=Priority.CRITICAL,
                frequency_minutes=1,
                reason=f"Charge système élevée: {system_status.cpu_usage:.1f}%",
                confidence=0.95,
                parameters={"auto_healing": True, "resource_optimization": True}
            ))
        else:
            recommendations.append(TaskRecommendation(
                task_type=TaskType.SYSTEM_HEALTH,
                priority=Priority.LOW,
                frequency_minutes=10,
                reason="Système stable",
                confidence=0.8,
                parameters={}
            ))

        # 4. Synchronisation données adaptative
        sync_frequency = self._calculate_sync_frequency(market_condition, system_status)
        recommendations.append(TaskRecommendation(
            task_type=TaskType.DATA_SYNC,
            priority=Priority.MEDIUM,
            frequency_minutes=sync_frequency,
            reason=f"Fréquence adaptée aux conditions (vol: {market_condition.volatility:.2f})",
            confidence=0.75,
            parameters={"batch_size": "auto"}
        ))

        # 5. Apprentissage IA en période calme
        if (market_condition.volatility < 0.3 and 
            system_status.cpu_usage < 50):
            recommendations.append(TaskRecommendation(
                task_type=TaskType.AI_LEARNING,
                priority=Priority.LOW,
                frequency_minutes=30,
                reason="Période calme - optimisation des modèles",
                confidence=0.6,
                parameters={"model_types": ["technical_analysis", "sentiment"], "epochs": 10}
            ))

        # Filtrer par confiance minimale
        recommendations = [r for r in recommendations if r.confidence >= self.min_confidence_threshold]
        
        logger.info(f"📋 {len(recommendations)} recommandations générées")
        return recommendations

    async def _analyze_market_conditions(self) -> MarketCondition:
        """Analyse les conditions actuelles du marché"""
        
        # Simulation d'analyse (à remplacer par vraies données)
        # TODO: Intégrer avec les données réelles via MarketData
        
        # Calcul de volatilité basé sur les dernières données
        volatility = np.random.beta(2, 5)  # Simulation réaliste
        trend_strength = np.random.beta(3, 3)
        volume_ratio = np.random.gamma(2, 0.5)
        sentiment_score = np.random.normal(0.5, 0.2)
        news_impact = np.random.exponential(0.3)
        
        # Normalisation
        volatility = np.clip(volatility, 0, 1)
        trend_strength = np.clip(trend_strength, 0, 1)
        volume_ratio = np.clip(volume_ratio, 0.1, 3.0)
        sentiment_score = np.clip(sentiment_score, 0, 1)
        news_impact = np.clip(news_impact, 0, 1)
        
        return MarketCondition(
            volatility=volatility,
            trend_strength=trend_strength,
            volume_ratio=volume_ratio,
            sentiment_score=sentiment_score,
            news_impact=news_impact,
            timestamp=datetime.utcnow()
        )

    async def _analyze_system_status(self) -> SystemStatus:
        """Analyse l'état actuel du système"""
        
        # TODO: Intégrer avec les vraies métriques système
        import psutil
        
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Métriques simulées pour les autres
        active_connections = np.random.poisson(50)
        error_rate = np.random.exponential(0.01)
        response_time = np.random.gamma(2, 50)  # milliseconds
        
        return SystemStatus(
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            active_connections=active_connections,
            error_rate=min(error_rate, 0.1),
            response_time=response_time
        )

    def _calculate_sync_frequency(self, market: MarketCondition, system: SystemStatus) -> int:
        """Calcule la fréquence optimale de synchronisation"""
        
        base_frequency = 5  # minutes
        
        # Plus fréquent si volatilité élevée
        if market.volatility > 0.7:
            base_frequency = 2
        elif market.volatility > 0.5:
            base_frequency = 3
            
        # Moins fréquent si système surchargé
        if system.cpu_usage > 80:
            base_frequency *= 2
            
        return max(base_frequency, 1)

    async def should_execute_task(self, task_type: TaskType, last_execution: Optional[datetime] = None) -> Tuple[bool, str]:
        """Décide si une tâche doit être exécutée maintenant"""
        
        if last_execution is None:
            return True, "Première exécution"
            
        market_condition, system_status = await self.analyze_current_conditions()
        recommendations = await self.generate_recommendations(market_condition, system_status)
        
        # Trouve la recommandation pour ce type de tâche
        task_rec = next((r for r in recommendations if r.task_type == task_type), None)
        
        if not task_rec:
            return False, "Aucune recommandation pour cette tâche"
            
        time_since_last = datetime.utcnow() - last_execution
        required_interval = timedelta(minutes=task_rec.frequency_minutes)
        
        should_execute = time_since_last >= required_interval
        reason = f"Intervalle requis: {task_rec.frequency_minutes}min, écoulé: {time_since_last.total_seconds()/60:.1f}min"
        
        return should_execute, reason 