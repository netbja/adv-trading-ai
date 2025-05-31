"""
⏰ AI SCHEDULER
Planificateur intelligent qui remplace les crons traditionnels
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
import logging

from celery import Celery
from sqlalchemy.orm import Session
from redis import Redis

from .decision_engine import DecisionEngine, TaskType, Priority, TaskRecommendation

import sys
sys.path.append('/app/backend')
from database.connection import get_db
from utils.logger import get_logger
# Note: ces imports seront corrigés une fois les tâches créées
# from ..tasks.celery_app import celery_app

logger = get_logger(__name__)

@dataclass
class ScheduledTask:
    id: str
    task_type: TaskType
    priority: Priority
    next_execution: datetime
    frequency_minutes: int
    celery_task_name: str
    parameters: Dict
    last_execution: Optional[datetime] = None
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    avg_execution_time: float = 0.0
    reason: str = ""

class AIScheduler:
    """
    ⏰ Planificateur intelligent de tâches
    
    Remplace les crons traditionnels par une IA qui adapte 
    dynamiquement la planification selon les conditions.
    """
    
    def __init__(self, redis_client: Optional[Redis] = None):
        self.decision_engine = DecisionEngine()
        self.redis_client = redis_client
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.task_registry = self._build_task_registry()
        
    def _build_task_registry(self) -> Dict[TaskType, str]:
        """Mappage des types de tâches vers les tâches Celery"""
        return {
            # Workflows génériques
            TaskType.MARKET_ANALYSIS: "app.tasks.ai_tasks.ai_market_analysis",
            TaskType.SYSTEM_HEALTH: "app.tasks.monitoring_tasks.system_health_check",
            TaskType.DATA_SYNC: "app.tasks.trading_tasks.sync_market_data",
            TaskType.AI_LEARNING: "app.tasks.ai_tasks.ai_learning_update",
            TaskType.RISK_ASSESSMENT: "app.tasks.trading_tasks.risk_assessment",
            
            # 🪙 MEME COINS WORKFLOW
            TaskType.MEME_ANALYSIS: "app.tasks.meme_tasks.analyze_meme_trends",
            TaskType.MEME_TRADING: "app.tasks.meme_tasks.execute_meme_trades",
            TaskType.MEME_MONITORING: "app.tasks.meme_tasks.monitor_meme_positions",
            
            # ₿ CRYPTO LONG TERME WORKFLOW
            TaskType.CRYPTO_LT_ANALYSIS: "app.tasks.crypto_tasks.analyze_crypto_longterm",
            TaskType.CRYPTO_LT_TRADING: "app.tasks.crypto_tasks.execute_crypto_dca",
            TaskType.CRYPTO_LT_REBALANCING: "app.tasks.crypto_tasks.rebalance_crypto_portfolio",
            
            # 💱 FOREX WORKFLOW
            TaskType.FOREX_ANALYSIS: "app.tasks.forex_tasks.analyze_forex_pairs",
            TaskType.FOREX_TRADING: "app.tasks.forex_tasks.execute_forex_trades",
            TaskType.FOREX_CORRELATION: "app.tasks.forex_tasks.analyze_forex_correlations",
            
            # 📈 ETF WORKFLOW
            TaskType.ETF_ANALYSIS: "app.tasks.etf_tasks.analyze_etf_performance",
            TaskType.ETF_TRADING: "app.tasks.etf_tasks.execute_etf_trades",
            TaskType.ETF_REBALANCING: "app.tasks.etf_tasks.rebalance_etf_portfolio",
            
            # Legacy (compatibilité)
            TaskType.TRADING_EXECUTION: "app.tasks.trading_tasks.execute_trading_signal"
        }

    async def start(self):
        """Démarre l'orchestrateur AI"""
        logger.info("🚀 Démarrage de l'Orchestrateur AI")
        self.running = True
        
        # Initialisation des tâches de base
        await self._initialize_base_tasks()
        
        # Boucle principale de l'orchestrateur
        await self._main_loop()

    async def stop(self):
        """Arrête l'orchestrateur AI"""
        logger.info("🛑 Arrêt de l'Orchestrateur AI")
        self.running = False

    async def _initialize_base_tasks(self):
        """Initialise les tâches de base du système"""
        
        # Tâches critiques toujours présentes
        base_tasks = [
            ScheduledTask(
                id="system_health_monitor",
                task_type=TaskType.SYSTEM_HEALTH,
                priority=Priority.CRITICAL,
                next_execution=datetime.utcnow(),
                frequency_minutes=5,
                celery_task_name=self.task_registry[TaskType.SYSTEM_HEALTH],
                parameters={},
                reason="Tâche système critique"
            ),
            ScheduledTask(
                id="market_data_sync",
                task_type=TaskType.DATA_SYNC,
                priority=Priority.HIGH,
                next_execution=datetime.utcnow() + timedelta(minutes=1),
                frequency_minutes=5,
                celery_task_name=self.task_registry[TaskType.DATA_SYNC],
                parameters={},
                reason="Synchronisation données de base"
            )
        ]
        
        for task in base_tasks:
            self.scheduled_tasks[task.id] = task
            
        logger.info(f"📋 {len(base_tasks)} tâches de base initialisées")

    async def _main_loop(self):
        """Boucle principale de l'orchestrateur"""
        
        loop_count = 0
        
        while self.running:
            try:
                loop_count += 1
                logger.info(f"🔄 Cycle orchestrateur #{loop_count}")
                
                # 1. Analyser les conditions actuelles
                market_condition, system_status = await self.decision_engine.analyze_current_conditions()
                
                # 2. Générer les recommandations
                recommendations = await self.decision_engine.generate_recommendations(
                    market_condition, system_status
                )
                
                # 3. Mettre à jour le planning
                await self._update_schedule(recommendations)
                
                # 4. Exécuter les tâches prêtes
                await self._execute_ready_tasks()
                
                # 5. Nettoyer les tâches obsolètes
                await self._cleanup_tasks()
                
                # 6. Persister l'état
                await self._persist_state()
                
                # 7. Attendre avant le prochain cycle
                await asyncio.sleep(30)  # Cycle toutes les 30 secondes
                
            except Exception as e:
                logger.error(f"❌ Erreur dans la boucle principale: {e}")
                await asyncio.sleep(60)  # Attendre plus longtemps en cas d'erreur

    async def _update_schedule(self, recommendations: List[TaskRecommendation]):
        """Met à jour le planning selon les recommandations de l'IA"""
        
        for rec in recommendations:
            task_id = f"{rec.task_type.value}_{rec.priority.name.lower()}"
            
            if task_id in self.scheduled_tasks:
                # Mettre à jour une tâche existante
                task = self.scheduled_tasks[task_id]
                
                # Adapter la fréquence si nécessaire
                if task.frequency_minutes != rec.frequency_minutes:
                    logger.info(f"🔄 Ajustement fréquence {task_id}: "
                              f"{task.frequency_minutes} → {rec.frequency_minutes} min")
                    task.frequency_minutes = rec.frequency_minutes
                    
                # Mettre à jour les paramètres
                task.parameters.update(rec.parameters)
                task.priority = rec.priority
                task.reason = rec.reason
                
            else:
                # Créer une nouvelle tâche
                if rec.task_type in self.task_registry:
                    new_task = ScheduledTask(
                        id=task_id,
                        task_type=rec.task_type,
                        priority=rec.priority,
                        next_execution=datetime.utcnow() + timedelta(minutes=1),
                        frequency_minutes=rec.frequency_minutes,
                        celery_task_name=self.task_registry[rec.task_type],
                        parameters=rec.parameters,
                        reason=rec.reason
                    )
                    
                    self.scheduled_tasks[task_id] = new_task
                    logger.info(f"➕ Nouvelle tâche planifiée: {task_id}")

    async def _execute_ready_tasks(self):
        """Exécute les tâches prêtes à être lancées"""
        
        now = datetime.utcnow()
        ready_tasks = [
            task for task in self.scheduled_tasks.values()
            if task.next_execution <= now
        ]
        
        if not ready_tasks:
            return
            
        logger.info(f"🎯 {len(ready_tasks)} tâches prêtes à l'exécution")
        
        # Trier par priorité
        ready_tasks.sort(key=lambda t: t.priority.value)
        
        for task in ready_tasks:
            try:
                await self._execute_task(task)
            except Exception as e:
                logger.error(f"❌ Erreur exécution tâche {task.id}: {e}")
                task.failure_count += 1

    async def _execute_task(self, task: ScheduledTask):
        """Exécute une tâche spécifique"""
        
        start_time = datetime.utcnow()
        
        logger.info(f"🚀 Exécution tâche: {task.id} (priorité: {task.priority.name})")
        
        try:
            # TODO: Lancer la tâche Celery (temporairement désactivé)
            # celery_task = celery_app.send_task(
            #     task.celery_task_name,
            #     kwargs=task.parameters
            # )
            
            # Simulation d'exécution pour le moment
            logger.info(f"📋 Simulation exécution tâche: {task.celery_task_name}")
            await asyncio.sleep(0.1)  # Simulation d'une tâche rapide
            
            # Attendre le résultat (optionnel, pour tracking)
            # result = celery_task.get(timeout=300)  # 5 minutes timeout
            
            # Mise à jour des statistiques
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            task.last_execution = start_time
            task.execution_count += 1
            task.success_count += 1
            
            # Mise à jour temps d'exécution moyen
            if task.avg_execution_time == 0:
                task.avg_execution_time = execution_time
            else:
                task.avg_execution_time = (task.avg_execution_time + execution_time) / 2
            
            # Programmer la prochaine exécution
            task.next_execution = start_time + timedelta(minutes=task.frequency_minutes)
            
            logger.info(f"✅ Tâche {task.id} exécutée avec succès en {execution_time:.2f}s")
            
        except Exception as e:
            task.failure_count += 1
            logger.error(f"❌ Échec exécution tâche {task.id}: {e}")
            
            # Retarder la prochaine exécution en cas d'échec
            delay_minutes = min(task.frequency_minutes * 2, 30)  # Max 30 min de délai
            task.next_execution = datetime.utcnow() + timedelta(minutes=delay_minutes)

    async def _cleanup_tasks(self):
        """Nettoie les tâches obsolètes ou en échec"""
        
        tasks_to_remove = []
        
        for task_id, task in self.scheduled_tasks.items():
            # Supprimer les tâches avec trop d'échecs
            if task.execution_count > 0:
                failure_rate = task.failure_count / task.execution_count
                if failure_rate > 0.8 and task.execution_count > 5:
                    logger.warning(f"🗑️ Suppression tâche en échec: {task_id} "
                                 f"(taux d'échec: {failure_rate:.1%})")
                    tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.scheduled_tasks[task_id]

    async def _persist_state(self):
        """Persiste l'état de l'orchestrateur dans Redis"""
        
        if not self.redis_client:
            return
            
        try:
            state = {
                "timestamp": datetime.utcnow().isoformat(),
                "tasks_count": len(self.scheduled_tasks),
                "tasks": {
                    task_id: {
                        "task_type": task.task_type.value,
                        "priority": task.priority.name,
                        "next_execution": task.next_execution.isoformat(),
                        "frequency_minutes": task.frequency_minutes,
                        "execution_count": task.execution_count,
                        "success_count": task.success_count,
                        "failure_count": task.failure_count,
                        "avg_execution_time": task.avg_execution_time,
                        "reason": task.reason
                    }
                    for task_id, task in self.scheduled_tasks.items()
                }
            }
            
            self.redis_client.set(
                "orchestrator:state",
                json.dumps(state, default=str),
                ex=3600  # Expire dans 1 heure
            )
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde état: {e}")

    def get_status(self) -> Dict:
        """Retourne le statut actuel de l'orchestrateur"""
        
        total_tasks = len(self.scheduled_tasks)
        total_executions = sum(task.execution_count for task in self.scheduled_tasks.values())
        total_successes = sum(task.success_count for task in self.scheduled_tasks.values())
        
        success_rate = (total_successes / total_executions * 100) if total_executions > 0 else 0
        
        return {
            "running": self.running,
            "total_tasks": total_tasks,
            "total_executions": total_executions,
            "success_rate": round(success_rate, 1),
            "tasks": [
                {
                    "id": task.id,
                    "type": task.task_type.value,
                    "priority": task.priority.name,
                    "next_execution": task.next_execution.isoformat(),
                    "frequency_minutes": task.frequency_minutes,
                    "execution_count": task.execution_count,
                    "success_rate": round((task.success_count / task.execution_count * 100) if task.execution_count > 0 else 0, 1),
                    "avg_execution_time": round(task.avg_execution_time, 2),
                    "reason": task.reason
                }
                for task in sorted(self.scheduled_tasks.values(), key=lambda t: t.priority.value)
            ]
        } 