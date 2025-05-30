"""
🏥 SYSTEM HEALTH MODEL - MODÈLE SANTÉ SYSTÈME
Surveillance et métriques système
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from backend.database.connection import Base

class SystemHealth(Base):
    """
    💻 Modèle pour la santé du système
    """
    __tablename__ = "system_health"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Métriques système
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    disk_usage = Column(Float, nullable=False)
    
    # Métriques réseau/connexions
    active_connections = Column(Integer, default=0)
    response_time = Column(Float)  # en millisecondes
    error_rate = Column(Float, default=0.0)
    
    # Métriques application
    active_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    
    # Status global
    health_score = Column(Float)  # 0.0 à 1.0
    status = Column(String(20), default="healthy")  # healthy, warning, critical
    
    # Métadonnées
    node_name = Column(String(50), default="backend")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<SystemHealth(cpu={self.cpu_usage}%, memory={self.memory_usage}%, status={self.status})>"

class TaskExecution(Base):
    """
    📋 Modèle pour le suivi des tâches de l'orchestrateur
    """
    __tablename__ = "task_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations tâche
    task_type = Column(String(50), nullable=False)
    task_name = Column(String(100), nullable=False)
    priority = Column(String(20), nullable=False)
    
    # Exécution
    status = Column(String(20), nullable=False)  # pending, running, completed, failed
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    
    # Résultats
    success = Column(Boolean)
    error_message = Column(Text)
    result_data = Column(Text)  # JSON des résultats
    
    # IA Decision
    ai_confidence = Column(Float)
    ai_reasoning = Column(Text)
    
    # Métadonnées
    orchestrator_id = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<TaskExecution(type={self.task_type}, status={self.status}, success={self.success})>"

class AIDecision(Base):
    """
    🧠 Modèle pour tracer les décisions de l'IA
    """
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Contexte de décision
    decision_type = Column(String(50), nullable=False)  # task_scheduling, trading_signal, etc.
    context_data = Column(Text)  # JSON du contexte (market conditions, system status)
    
    # Décision prise
    decision = Column(Text, nullable=False)  # JSON de la décision
    confidence = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=False)
    
    # Résultat
    executed = Column(Boolean, default=False)
    execution_result = Column(Text)  # JSON du résultat
    success_rate = Column(Float)  # Taux de succès historique pour ce type de décision
    
    # Métadonnées
    ai_model = Column(String(50))  # Quel AI a pris la décision
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<AIDecision(type={self.decision_type}, confidence={self.confidence}, executed={self.executed})>" 