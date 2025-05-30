"""
📝 LOGGER - SYSTÈME DE LOGS
Configuration et gestion des logs pour le système de trading AI
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    """
    Obtient un logger configuré pour le système de trading AI
    
    Args:
        name: Nom du module (généralement __name__)
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configuration du logger seulement s'il n'a pas déjà de handlers
        logger.setLevel(logging.INFO)
        
        # Format des logs avec émojis pour plus de lisibilité
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler pour la console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler pour fichier (optionnel)
        try:
            log_dir = Path("/app/logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / f"trading_ai_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            # Si on ne peut pas écrire dans /app/logs, on ignore
            pass
    
    return logger

def log_ai_decision(logger: logging.Logger, decision_type: str, decision: str, confidence: float, reasoning: str):
    """
    Log spécialisé pour les décisions d'IA
    """
    logger.info(f"🧠 AI_DECISION | Type: {decision_type} | Decision: {decision} | Confidence: {confidence:.2f} | Reasoning: {reasoning}")

def log_task_execution(logger: logging.Logger, task_type: str, status: str, duration: float = None):
    """
    Log spécialisé pour l'exécution des tâches
    """
    if duration:
        logger.info(f"📋 TASK_EXECUTION | Type: {task_type} | Status: {status} | Duration: {duration:.2f}s")
    else:
        logger.info(f"📋 TASK_EXECUTION | Type: {task_type} | Status: {status}")

def log_system_health(logger: logging.Logger, cpu: float, memory: float, status: str):
    """
    Log spécialisé pour la santé système
    """
    logger.info(f"💻 SYSTEM_HEALTH | CPU: {cpu:.1f}% | Memory: {memory:.1f}% | Status: {status}")

def log_market_analysis(logger: logging.Logger, symbol: str, volatility: float, trend: str):
    """
    Log spécialisé pour l'analyse de marché
    """
    logger.info(f"📈 MARKET_ANALYSIS | Symbol: {symbol} | Volatility: {volatility:.2f} | Trend: {trend}") 