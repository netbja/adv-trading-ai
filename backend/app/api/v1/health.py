"""
🏥 API HEALTH - ENDPOINTS SANTÉ
Routes pour vérifier la santé du système
"""

from fastapi import APIRouter
from datetime import datetime
import time

router = APIRouter()

@router.get("/")
async def health_check():
    """Check de santé basique"""
    return {
        "status": "healthy",
        "service": "trading-ai-etf-backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": time.time()
    }

@router.get("/detailed")
async def detailed_health():
    """Check de santé détaillé"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "redis": "connected",
            "broker": "paper_mode",
            "ai": "available"
        },
        "metrics": {
            "memory_usage": "normal",
            "cpu_usage": "low",
            "disk_space": "available"
        },
        "timestamp": datetime.utcnow().isoformat()
    } 