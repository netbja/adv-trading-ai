"""
💼 API PORTFOLIO - GESTION PORTEFEUILLE ETF
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/current")
async def get_current_portfolio():
    """Portefeuille actuel détaillé"""
    return {
        "portfolio": [
            {
                "symbol": "VTI",
                "name": "Vanguard Total Stock Market ETF",
                "allocation": 35,
                "value": 43900,
                "performance": 1.2,
                "ai_status": "HOLD",
                "shares": 185.5,
                "avg_cost": 220.50
            },
            {
                "symbol": "VTIAX",
                "name": "Vanguard Total International",
                "allocation": 25,
                "value": 31350,
                "performance": -0.5,
                "ai_status": "ACCUMULATE",
                "shares": 1250.0,
                "avg_cost": 25.08
            },
            {
                "symbol": "QQQ",
                "name": "Invesco QQQ Trust",
                "allocation": 20,
                "value": 25086,
                "performance": 2.1,
                "ai_status": "HOLD",
                "shares": 65.2,
                "avg_cost": 384.75
            },
            {
                "symbol": "BND",
                "name": "Vanguard Total Bond Market",
                "allocation": 15,
                "value": 18814,
                "performance": 0.1,
                "ai_status": "REDUCE",
                "shares": 245.8,
                "avg_cost": 76.55
            },
            {
                "symbol": "VNQ",
                "name": "Vanguard Real Estate ETF",
                "allocation": 5,
                "value": 6270,
                "performance": -1.2,
                "ai_status": "HOLD",
                "shares": 68.5,
                "avg_cost": 91.53
            }
        ],
        "total_value": 125420.0,
        "total_cost": 122850.0,
        "total_gain": 2570.0,
        "total_gain_percent": 2.09,
        "last_updated": datetime.utcnow().isoformat()
    }

@router.get("/performance")
async def get_portfolio_performance():
    """Performance historique du portefeuille"""
    return {
        "performance": {
            "1d": 2.45,
            "1w": 3.8,
            "1m": 7.2,
            "3m": 12.5,
            "6m": 18.9,
            "1y": 24.7,
            "ytd": 5.2
        },
        "benchmark_comparison": {
            "portfolio": 24.7,
            "sp500": 22.1,
            "outperformance": 2.6
        },
        "risk_metrics": {
            "sharpe_ratio": 1.45,
            "max_drawdown": -8.5,
            "volatility": 12.3,
            "beta": 0.95
        }
    } 