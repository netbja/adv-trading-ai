"""
📊 API DASHBOARD - ENDPOINTS TABLEAU DE BORD
Routes pour alimenter le dashboard Vue3
"""

from fastapi import APIRouter
from datetime import datetime
import random

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats():
    """Statistiques principales du dashboard"""
    return {
        "portfolio_value": 125430.50,
        "daily_change": 2.45,
        "active_etfs": 8,
        "ai_signals": 12,
        "system_health": 98,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/ai-insights")
async def get_ai_insights():
    """Insights de l'IA pour le dashboard"""
    return {
        "insights": [
            {
                "id": 1,
                "type": "buy",
                "title": "Signal d'Achat Fort : VTI",
                "description": "L'IA détecte une opportunité d'accumulation sur l'ETF Vanguard Total Stock Market avec une probabilité de succès de 82%.",
                "timestamp": "Il y a 15 min",
                "confidence": 0.82
            },
            {
                "id": 2,
                "type": "neutral",
                "title": "Analyse Sectorielle : Tech Stable",
                "description": "Le secteur technologique (QQQ) montre des signaux neutres. Maintien de l'allocation recommandé.",
                "timestamp": "Il y a 1h",
                "confidence": 0.65
            },
            {
                "id": 3,
                "type": "warning",
                "title": "Alerte Rebalancing : VXUS",
                "description": "L'ETF international dépasse l'allocation cible de 2%. Rebalancing automatique programmé.",
                "timestamp": "Il y a 2h",
                "confidence": 0.95
            }
        ]
    }

@router.get("/portfolio-allocations")
async def get_portfolio_allocations():
    """Allocations du portefeuille ETF"""
    return {
        "allocations": [
            {
                "symbol": "VTI",
                "name": "Vanguard Total Stock Market",
                "percentage": 35,
                "change": 1.2,
                "color": "#22c55e",
                "target_allocation": 35,
                "current_allocation": 36.2
            },
            {
                "symbol": "VTIAX",
                "name": "Vanguard Total International",
                "percentage": 25,
                "change": -0.5,
                "color": "#3b82f6",
                "target_allocation": 25,
                "current_allocation": 24.8
            },
            {
                "symbol": "QQQ",
                "name": "Invesco QQQ Trust",
                "percentage": 20,
                "change": 2.1,
                "color": "#8b5cf6",
                "target_allocation": 20,
                "current_allocation": 21.1
            },
            {
                "symbol": "BND",
                "name": "Vanguard Total Bond Market",
                "percentage": 15,
                "change": 0.1,
                "color": "#f59e0b",
                "target_allocation": 15,
                "current_allocation": 14.9
            },
            {
                "symbol": "VNQ",
                "name": "Vanguard Real Estate",
                "percentage": 5,
                "change": -1.2,
                "color": "#ef4444",
                "target_allocation": 5,
                "current_allocation": 3.0
            }
        ],
        "rebalancing_needed": True,
        "last_rebalance": "2024-01-15T10:30:00Z"
    }

@router.post("/refresh")
async def refresh_dashboard_data():
    """Actualiser les données du dashboard"""
    # Simuler une actualisation
    new_portfolio_value = 125430.50 + (random.random() - 0.5) * 2000
    new_daily_change = 2.45 + (random.random() - 0.5) * 1.0
    
    return {
        "message": "Données actualisées",
        "portfolio_value": round(new_portfolio_value, 2),
        "daily_change": round(new_daily_change, 2),
        "timestamp": datetime.utcnow().isoformat()
    } 