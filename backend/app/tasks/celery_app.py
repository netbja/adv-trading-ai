"""
🔄 CELERY APPLICATION - CONFIGURATION ULTRA-AVANCÉE
Application Celery pour les tâches asynchrones du système de trading IA
"""

from celery import Celery
from app.config import settings
import os

# Création de l'instance Celery
celery_app = Celery(
    "trading_ai",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.trading_tasks",
        "app.tasks.ai_tasks", 
        "app.tasks.monitoring_tasks"
    ]
)

# Configuration Celery ultra-optimisée
celery_app.conf.update(
    # Timezone et schedules
    timezone="Europe/Paris",
    enable_utc=True,
    
    # Performance optimization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    result_expires=3600,  # 1 heure
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    
    # Monitoring
    task_send_sent_event=True,
    task_track_started=True,
    
    # Error handling
    task_reject_on_worker_lost=True,
    task_ignore_result=False,
    
    # Security
    worker_hijack_root_logger=False,
    worker_log_color=False,
)

# Configuration des tâches périodiques (remplace les crons !)
# Note: Ces tâches seront gérées par l'Orchestrateur IA à terme
celery_app.conf.beat_schedule = {
    "health-check": {
        "task": "app.tasks.monitoring_tasks.system_health_check",
        "schedule": 60.0,  # Toutes les minutes
    },
    "market-data-sync": {
        "task": "app.tasks.trading_tasks.sync_market_data",
        "schedule": 300.0,  # Toutes les 5 minutes
    },
}

# Auto-discovery des tâches
celery_app.autodiscover_tasks()

if __name__ == "__main__":
    celery_app.start() 