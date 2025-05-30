"""
🔄 TASKS MODULE - TÂCHES ASYNCHRONES CELERY
Module pour les tâches d'arrière-plan du système de trading IA
"""

from .celery_app import celery_app

__all__ = ["celery_app"] 