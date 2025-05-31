"""
📊 PERFORMANCE TRACKER - SUIVI DE PERFORMANCE
=============================================

Ce module implémente le suivi des performances de l'orchestrateur :
- Collecte des métriques en temps réel
- Analyse des tendances de performance
- Alertes sur dégradation
- Optimisation automatique
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import json

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types de métriques"""
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    RESOURCE_USAGE = "resource_usage"

@dataclass
class PerformanceMetric:
    """Métrique de performance"""
    timestamp: datetime
    metric_type: MetricType
    value: float
    unit: str
    component: str
    metadata: Dict[str, Any]

@dataclass
class PerformanceReport:
    """Rapport de performance"""
    period_start: datetime
    period_end: datetime
    total_operations: int
    successful_operations: int
    failed_operations: int
    average_execution_time: float
    min_execution_time: float
    max_execution_time: float
    throughput_per_second: float
    success_rate: float
    error_rate: float
    trends: Dict[str, str]
    recommendations: List[str]

class PerformanceTracker:
    """
    📊 SUIVI DE PERFORMANCE SYSTÈME
    
    Collecte et analyse les métriques de performance :
    - Temps d'exécution des opérations
    - Taux de succès/échec
    - Throughput et latence
    - Détection de dégradation
    """
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.operations_log: List[Dict] = []
        
        # Configuration
        self.max_metrics_history = 10000
        self.alert_thresholds = {
            "max_execution_time": 5.0,  # secondes
            "min_success_rate": 95.0,   # pourcentage
            "max_error_rate": 5.0       # pourcentage
        }
        
        # État actuel
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.last_cleanup = datetime.utcnow()
        
        logger.info("📊 Performance Tracker initialisé")

    async def record_operation(self, 
                             component: str,
                             operation: str,
                             execution_time: float,
                             success: bool,
                             metadata: Optional[Dict] = None) -> None:
        """
        📝 Enregistrer une opération
        
        Args:
            component: Nom du composant
            operation: Type d'opération
            execution_time: Temps d'exécution en secondes
            success: Si l'opération a réussi
            metadata: Métadonnées additionnelles
        """
        try:
            timestamp = datetime.utcnow()
            
            # Enregistrer l'opération
            operation_record = {
                "timestamp": timestamp,
                "component": component,
                "operation": operation,
                "execution_time": execution_time,
                "success": success,
                "metadata": metadata or {}
            }
            self.operations_log.append(operation_record)
            
            # Créer les métriques
            await self._create_metrics(timestamp, component, execution_time, success)
            
            # Mettre à jour les compteurs
            self.total_operations += 1
            if success:
                self.successful_operations += 1
            else:
                self.failed_operations += 1
            
            # Nettoyer l'historique si nécessaire
            await self._cleanup_old_data()
            
        except Exception as e:
            logger.error(f"❌ Erreur enregistrement opération: {e}")

    async def _create_metrics(self, timestamp: datetime, component: str, 
                            execution_time: float, success: bool) -> None:
        """📊 Créer les métriques à partir d'une opération"""
        
        try:
            # Métrique temps d'exécution
            self.metrics.append(PerformanceMetric(
                timestamp=timestamp,
                metric_type=MetricType.EXECUTION_TIME,
                value=execution_time,
                unit="seconds",
                component=component,
                metadata={"success": success}
            ))
            
            # Métrique taux de succès/échec
            if success:
                self.metrics.append(PerformanceMetric(
                    timestamp=timestamp,
                    metric_type=MetricType.SUCCESS_RATE,
                    value=1.0,
                    unit="percentage",
                    component=component,
                    metadata={}
                ))
            else:
                self.metrics.append(PerformanceMetric(
                    timestamp=timestamp,
                    metric_type=MetricType.ERROR_RATE,
                    value=1.0,
                    unit="percentage",
                    component=component,
                    metadata={}
                ))
                
        except Exception as e:
            logger.error(f"❌ Erreur création métriques: {e}")

    async def get_recent_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """
        📈 Obtenir les métriques récentes
        
        Args:
            hours: Nombre d'heures à analyser
            
        Returns:
            Dict avec les métriques récentes
        """
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            recent_operations = [
                op for op in self.operations_log 
                if op["timestamp"] >= cutoff_time
            ]
            
            if not recent_operations:
                return {
                    "total_operations": 0,
                    "success_rate": 0,
                    "error_rate": 0,
                    "average_execution_time": 0,
                    "last_activity": "no_activity"
                }
            
            # Calculs de base
            total_ops = len(recent_operations)
            successful_ops = sum(1 for op in recent_operations if op["success"])
            success_rate = (successful_ops / total_ops) * 100 if total_ops > 0 else 0
            error_rate = ((total_ops - successful_ops) / total_ops) * 100 if total_ops > 0 else 0
            
            # Temps d'exécution
            execution_times = [op["execution_time"] for op in recent_operations]
            avg_execution_time = statistics.mean(execution_times) if execution_times else 0
            
            # Dernière activité
            last_operation = max(recent_operations, key=lambda x: x["timestamp"])
            last_activity = last_operation["timestamp"].isoformat()
            
            return {
                "total_operations": total_ops,
                "successful_operations": successful_ops,
                "failed_operations": total_ops - successful_ops,
                "success_rate": round(success_rate, 2),
                "error_rate": round(error_rate, 2),
                "average_execution_time": round(avg_execution_time, 3),
                "min_execution_time": round(min(execution_times) if execution_times else 0, 3),
                "max_execution_time": round(max(execution_times) if execution_times else 0, 3),
                "last_activity": last_activity,
                "throughput_per_hour": total_ops
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul métriques récentes: {e}")
            return {}

    async def generate_performance_report(self, hours: int = 24) -> PerformanceReport:
        """
        📋 Générer un rapport de performance
        
        Args:
            hours: Période d'analyse en heures
            
        Returns:
            Rapport de performance complet
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            # Filtrer les opérations de la période
            period_operations = [
                op for op in self.operations_log 
                if start_time <= op["timestamp"] <= end_time
            ]
            
            if not period_operations:
                return PerformanceReport(
                    period_start=start_time,
                    period_end=end_time,
                    total_operations=0,
                    successful_operations=0,
                    failed_operations=0,
                    average_execution_time=0.0,
                    min_execution_time=0.0,
                    max_execution_time=0.0,
                    throughput_per_second=0.0,
                    success_rate=0.0,
                    error_rate=0.0,
                    trends={},
                    recommendations=[]
                )
            
            # Calculs statistiques
            total_ops = len(period_operations)
            successful_ops = sum(1 for op in period_operations if op["success"])
            failed_ops = total_ops - successful_ops
            
            execution_times = [op["execution_time"] for op in period_operations]
            avg_execution_time = statistics.mean(execution_times)
            min_execution_time = min(execution_times)
            max_execution_time = max(execution_times)
            
            # Throughput (opérations par seconde)
            period_seconds = (end_time - start_time).total_seconds()
            throughput_per_second = total_ops / period_seconds if period_seconds > 0 else 0
            
            # Taux
            success_rate = (successful_ops / total_ops) * 100
            error_rate = (failed_ops / total_ops) * 100
            
            # Analyse des tendances
            trends = await self._analyze_trends(period_operations)
            
            # Recommandations
            recommendations = await self._generate_recommendations(
                success_rate, error_rate, avg_execution_time, max_execution_time
            )
            
            return PerformanceReport(
                period_start=start_time,
                period_end=end_time,
                total_operations=total_ops,
                successful_operations=successful_ops,
                failed_operations=failed_ops,
                average_execution_time=round(avg_execution_time, 3),
                min_execution_time=round(min_execution_time, 3),
                max_execution_time=round(max_execution_time, 3),
                throughput_per_second=round(throughput_per_second, 2),
                success_rate=round(success_rate, 2),
                error_rate=round(error_rate, 2),
                trends=trends,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport: {e}")
            return PerformanceReport(
                period_start=datetime.utcnow(),
                period_end=datetime.utcnow(),
                total_operations=0,
                successful_operations=0,
                failed_operations=0,
                average_execution_time=0.0,
                min_execution_time=0.0,
                max_execution_time=0.0,
                throughput_per_second=0.0,
                success_rate=0.0,
                error_rate=0.0,
                trends={},
                recommendations=[]
            )

    async def _analyze_trends(self, operations: List[Dict]) -> Dict[str, str]:
        """📈 Analyser les tendances de performance"""
        
        trends = {}
        
        try:
            if len(operations) < 2:
                return trends
            
            # Diviser en deux moitiés pour analyser la tendance
            mid_point = len(operations) // 2
            first_half = operations[:mid_point]
            second_half = operations[mid_point:]
            
            # Tendance du taux de succès
            first_success_rate = sum(1 for op in first_half if op["success"]) / len(first_half) * 100
            second_success_rate = sum(1 for op in second_half if op["success"]) / len(second_half) * 100
            
            if second_success_rate > first_success_rate + 5:
                trends["success_rate"] = "improving"
            elif second_success_rate < first_success_rate - 5:
                trends["success_rate"] = "degrading"
            else:
                trends["success_rate"] = "stable"
            
            # Tendance du temps d'exécution
            first_avg_time = statistics.mean([op["execution_time"] for op in first_half])
            second_avg_time = statistics.mean([op["execution_time"] for op in second_half])
            
            if second_avg_time < first_avg_time * 0.9:
                trends["execution_time"] = "improving"
            elif second_avg_time > first_avg_time * 1.1:
                trends["execution_time"] = "degrading"
            else:
                trends["execution_time"] = "stable"
                
        except Exception as e:
            logger.error(f"❌ Erreur analyse tendances: {e}")
            
        return trends

    async def _generate_recommendations(self, success_rate: float, error_rate: float,
                                      avg_execution_time: float, max_execution_time: float) -> List[str]:
        """💡 Générer des recommandations d'optimisation"""
        
        recommendations = []
        
        try:
            # Recommandations basées sur le taux de succès
            if success_rate < 90:
                recommendations.append("Taux de succès bas - investiguer les causes d'échec")
            elif success_rate < 95:
                recommendations.append("Taux de succès modéré - optimiser la robustesse")
            
            # Recommandations basées sur les temps d'exécution
            if avg_execution_time > 2.0:
                recommendations.append("Temps d'exécution élevé - optimiser les performances")
            
            if max_execution_time > 10.0:
                recommendations.append("Pics de latence détectés - investiguer les goulots d'étranglement")
            
            # Recommandations basées sur le taux d'erreur
            if error_rate > 10:
                recommendations.append("Taux d'erreur élevé - renforcer la gestion d'erreurs")
            elif error_rate > 5:
                recommendations.append("Taux d'erreur modéré - améliorer la stabilité")
            
            # Recommandations générales
            if not recommendations:
                recommendations.append("Performance satisfaisante - maintenir le niveau actuel")
                
        except Exception as e:
            logger.error(f"❌ Erreur génération recommandations: {e}")
            
        return recommendations

    async def _cleanup_old_data(self) -> None:
        """🧹 Nettoyer les anciennes données"""
        
        try:
            now = datetime.utcnow()
            
            # Nettoyer toutes les heures
            if (now - self.last_cleanup).total_seconds() < 3600:
                return
            
            # Garder seulement les données des 7 derniers jours
            cutoff_time = now - timedelta(days=7)
            
            # Nettoyer les métriques
            self.metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]
            
            # Nettoyer les opérations
            self.operations_log = [op for op in self.operations_log if op["timestamp"] >= cutoff_time]
            
            self.last_cleanup = now
            
            logger.debug(f"🧹 Nettoyage terminé - {len(self.metrics)} métriques, {len(self.operations_log)} opérations conservées")
            
        except Exception as e:
            logger.error(f"❌ Erreur nettoyage données: {e}")

    async def get_component_performance(self, component: str, hours: int = 24) -> Dict[str, Any]:
        """📊 Obtenir les performances d'un composant spécifique"""
        
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            component_operations = [
                op for op in self.operations_log 
                if op["component"] == component and op["timestamp"] >= cutoff_time
            ]
            
            if not component_operations:
                return {"component": component, "operations": 0}
            
            total_ops = len(component_operations)
            successful_ops = sum(1 for op in component_operations if op["success"])
            execution_times = [op["execution_time"] for op in component_operations]
            
            return {
                "component": component,
                "operations": total_ops,
                "success_rate": round((successful_ops / total_ops) * 100, 2),
                "average_execution_time": round(statistics.mean(execution_times), 3),
                "min_execution_time": round(min(execution_times), 3),
                "max_execution_time": round(max(execution_times), 3)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur performance composant {component}: {e}")
            return {"component": component, "error": str(e)}

    async def get_performance_summary(self) -> Dict[str, Any]:
        """📋 Obtenir un résumé de performance global"""
        
        try:
            recent_metrics = await self.get_recent_metrics(24)
            
            # Statut global
            success_rate = recent_metrics.get("success_rate", 0)
            avg_time = recent_metrics.get("average_execution_time", 0)
            
            if success_rate >= 95 and avg_time <= 1.0:
                status = "excellent"
            elif success_rate >= 90 and avg_time <= 2.0:
                status = "good"
            elif success_rate >= 80 and avg_time <= 5.0:
                status = "acceptable"
            else:
                status = "needs_attention"
            
            return {
                "status": status,
                "recent_metrics": recent_metrics,
                "total_lifetime_operations": self.total_operations,
                "lifetime_success_rate": round((self.successful_operations / max(1, self.total_operations)) * 100, 2),
                "metrics_count": len(self.metrics),
                "operations_logged": len(self.operations_log)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur résumé performance: {e}")
            return {"status": "error", "error": str(e)}

# Instance globale
_performance_tracker: Optional[PerformanceTracker] = None

def get_performance_tracker() -> PerformanceTracker:
    """📊 Obtenir l'instance du tracker de performance"""
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceTracker()
    return _performance_tracker 