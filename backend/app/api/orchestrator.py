"""
🌐 API ORCHESTRATOR
Endpoints pour l'orchestrateur AI
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional
from datetime import datetime
import json

from ..orchestrator.ai_scheduler import AIScheduler
from ..orchestrator.decision_engine import DecisionEngine, TaskType
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Instance globale de l'orchestrateur (à améliorer avec un singleton pattern)
orchestrator_instance: Optional[AIScheduler] = None

router = APIRouter(prefix="/orchestrator", tags=["🤖 AI Orchestrator"])

async def get_orchestrator() -> AIScheduler:
    """Dependency pour obtenir l'instance de l'orchestrateur"""
    global orchestrator_instance
    
    if orchestrator_instance is None:
        orchestrator_instance = AIScheduler()
    
    return orchestrator_instance

@router.get("/status", summary="📊 Statut de l'Orchestrateur")
async def get_orchestrator_status(orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Retourne le statut actuel de l'orchestrateur AI
    
    - **running**: Si l'orchestrateur est en cours d'exécution
    - **total_tasks**: Nombre total de tâches planifiées
    - **total_executions**: Nombre total d'exécutions
    - **success_rate**: Taux de succès global
    - **tasks**: Liste détaillée des tâches
    """
    try:
        status = orchestrator.get_status()
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "orchestrator": status
        }
    except Exception as e:
        logger.error(f"❌ Erreur récupération statut orchestrateur: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start", summary="🚀 Démarrer l'Orchestrateur")
async def start_orchestrator(background_tasks: BackgroundTasks, 
                           orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Démarre l'orchestrateur AI en arrière-plan
    
    L'orchestrateur commencera à analyser les conditions et à planifier
    les tâches automatiquement selon son intelligence.
    """
    try:
        if orchestrator.running:
            return {
                "success": True,
                "message": "L'orchestrateur est déjà en cours d'exécution",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Démarrer en arrière-plan
        background_tasks.add_task(orchestrator.start)
        
        logger.info("🚀 Démarrage de l'orchestrateur AI demandé")
        
        return {
            "success": True,
            "message": "Orchestrateur AI démarré avec succès",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Erreur démarrage orchestrateur: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop", summary="🛑 Arrêter l'Orchestrateur")
async def stop_orchestrator(orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Arrête l'orchestrateur AI
    
    Toutes les tâches en cours continueront, mais aucune nouvelle
    tâche ne sera planifiée.
    """
    try:
        if not orchestrator.running:
            return {
                "success": True,
                "message": "L'orchestrateur n'est pas en cours d'exécution",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        await orchestrator.stop()
        
        logger.info("🛑 Arrêt de l'orchestrateur AI demandé")
        
        return {
            "success": True,
            "message": "Orchestrateur AI arrêté avec succès",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Erreur arrêt orchestrateur: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations", summary="💡 Recommandations IA")
async def get_current_recommendations(orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Retourne les recommandations actuelles de l'IA
    
    Analyse les conditions de marché et système en temps réel
    pour donner les recommandations de planification.
    """
    try:
        decision_engine = DecisionEngine()
        
        # Analyser les conditions actuelles
        market_condition, system_status = await decision_engine.analyze_current_conditions()
        
        # Générer les recommandations
        recommendations = await decision_engine.generate_recommendations(
            market_condition, system_status
        )
        
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "market_conditions": {
                "volatility": round(market_condition.volatility, 3),
                "trend_strength": round(market_condition.trend_strength, 3),
                "volume_ratio": round(market_condition.volume_ratio, 3),
                "sentiment_score": round(market_condition.sentiment_score, 3),
                "news_impact": round(market_condition.news_impact, 3)
            },
            "system_status": {
                "cpu_usage": round(system_status.cpu_usage, 1),
                "memory_usage": round(system_status.memory_usage, 1),
                "disk_usage": round(system_status.disk_usage, 1),
                "active_connections": system_status.active_connections,
                "error_rate": round(system_status.error_rate, 4),
                "response_time": round(system_status.response_time, 1)
            },
            "recommendations": [
                {
                    "task_type": rec.task_type.value,
                    "priority": rec.priority.name,
                    "frequency_minutes": rec.frequency_minutes,
                    "reason": rec.reason,
                    "confidence": round(rec.confidence, 2),
                    "parameters": rec.parameters
                }
                for rec in recommendations
            ]
        }
    except Exception as e:
        logger.error(f"❌ Erreur génération recommandations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks", summary="📋 Liste des Tâches")
async def get_scheduled_tasks(task_type: Optional[str] = None,
                            orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Retourne la liste des tâches actuellement planifiées
    
    - **task_type**: Filtrer par type de tâche (optionnel)
    """
    try:
        status = orchestrator.get_status()
        tasks = status.get("tasks", [])
        
        # Filtrer par type si spécifié
        if task_type:
            tasks = [task for task in tasks if task["type"] == task_type]
        
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "total_tasks": len(tasks),
            "tasks": tasks
        }
    except Exception as e:
        logger.error(f"❌ Erreur récupération tâches: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", summary="📈 Métriques de Performance")
async def get_orchestrator_metrics(orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Retourne les métriques de performance de l'orchestrateur
    
    Statistiques détaillées sur l'efficacité et les performances
    de l'orchestrateur AI.
    """
    try:
        status = orchestrator.get_status()
        tasks = status.get("tasks", [])
        
        # Calculs de métriques avancées
        if tasks:
            avg_success_rate = sum(task["success_rate"] for task in tasks) / len(tasks)
            avg_execution_time = sum(task["avg_execution_time"] for task in tasks) / len(tasks)
            
            # Répartition par priorité
            priority_counts = {}
            for task in tasks:
                priority = task["priority"]
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Répartition par type
            type_counts = {}
            for task in tasks:
                task_type = task["type"]
                type_counts[task_type] = type_counts.get(task_type, 0) + 1
        else:
            avg_success_rate = 0
            avg_execution_time = 0
            priority_counts = {}
            type_counts = {}
        
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "orchestrator_running": status.get("running", False),
                "total_tasks": status.get("total_tasks", 0),
                "total_executions": status.get("total_executions", 0),
                "global_success_rate": status.get("success_rate", 0),
                "average_task_success_rate": round(avg_success_rate, 1),
                "average_execution_time": round(avg_execution_time, 2),
                "tasks_by_priority": priority_counts,
                "tasks_by_type": type_counts
            }
        }
    except Exception as e:
        logger.error(f"❌ Erreur récupération métriques: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", summary="🏥 Santé de l'Orchestrateur")
async def get_orchestrator_health(orchestrator: AIScheduler = Depends(get_orchestrator)):
    """
    Endpoint de santé pour l'orchestrateur AI
    
    Vérifie que l'orchestrateur fonctionne correctement et 
    retourne son état de santé global.
    """
    try:
        status = orchestrator.get_status()
        
        # Critères de santé
        is_running = status.get("running", False)
        success_rate = status.get("success_rate", 0)
        total_tasks = status.get("total_tasks", 0)
        
        # Déterminer l'état de santé
        if not is_running:
            health_status = "stopped"
        elif success_rate >= 80 and total_tasks > 0:
            health_status = "healthy"
        elif success_rate >= 60:
            health_status = "warning"
        else:
            health_status = "critical"
        
        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "health": {
                "status": health_status,
                "running": is_running,
                "success_rate": success_rate,
                "total_tasks": total_tasks,
                "message": {
                    "healthy": "Orchestrateur fonctionne parfaitement",
                    "warning": "Orchestrateur fonctionne mais avec des avertissements",
                    "critical": "Orchestrateur a des problèmes critiques",
                    "stopped": "Orchestrateur n'est pas en cours d'exécution"
                }.get(health_status, "État inconnu")
            }
        }
    except Exception as e:
        logger.error(f"❌ Erreur vérification santé: {e}")
        return {
            "success": False,
            "timestamp": datetime.utcnow().isoformat(),
            "health": {
                "status": "error",
                "message": f"Erreur lors de la vérification: {str(e)}"
            }
        } 