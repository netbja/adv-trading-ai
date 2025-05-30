"""
🌐 API V1 - ROUTES PRINCIPALES
Router principal pour l'API v1 du backend
"""

from fastapi import APIRouter
from app.api.v1 import portfolio, etf, health, dashboard, ai_system

# Router principal de l'API v1
router = APIRouter()

# Inclure les sous-routers
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
router.include_router(etf.router, prefix="/etf", tags=["etf"])
router.include_router(ai_system.router, prefix="/ai-system", tags=["ai-system"]) 