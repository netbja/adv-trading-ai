#!/usr/bin/env python3
"""
🧠 TRADING AI COMPLET - INTERFACE PROFESSIONNELLE
Dashboard avec authentification DB, workflows live et gestion des secrets
"""

import asyncio
import os
import logging
from datetime import datetime, timedelta
from dataclasses import asdict
from fastapi import FastAPI, HTTPException, Request, Depends, Cookie, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import random
import secrets

# Imports des modules
from .auth.secure_auth import SecureAuthManager
from .workflows.live_trading_engine import LiveTradingOrchestrator
from .ui.workflow_pages import get_crypto_workflow_page, get_meme_workflow_page, get_forex_workflow_page, get_workflow_styles
from .ui.workflow_js import get_workflow_javascript
from .smart_capital_growth_system import IntelligentCompoundGrowth, AutonomousTradingMaster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'trader')}:{os.getenv('POSTGRES_PASSWORD', 'TradingDB2025!')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'trading_ai')}"
PORT = int(os.getenv("PORT", "8000"))

# Instances globales
app = FastAPI(title="🧠 Trading AI Professional", version="2.0.0")
auth_manager = SecureAuthManager(DATABASE_URL)
live_orchestrator = LiveTradingOrchestrator()
trading_master = None
security = HTTPBearer()

# Monter les fichiers statiques (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Optionnel: Configuration de Jinja2Templates si on veut rendre des templates HTML depuis le serveur
# templates = Jinja2Templates(directory="frontend")

def get_login_page_from_file():
    return FileResponse("frontend/login.html", media_type="text/html")

def get_main_dashboard_from_file():
    return FileResponse("frontend/index.html", media_type="text/html")

@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage"""
    global trading_master
    
    # Initialiser base de données
    await auth_manager.init_db()
    logger.info("✅ Base de données initialisée")
    
    # Initialiser système de trading
    trading_master = AutonomousTradingMaster(200.0)
    await trading_master.initialize_autonomous_system()
    logger.info("✅ Système de trading initialisé")
    
    # Démarrer workflows live en arrière-plan
    asyncio.create_task(live_orchestrator.start_live_workflows())
    logger.info("✅ Workflows live démarrés")

# Middleware d'authentification
async def get_current_user(request: Request, session_token: str = Cookie(None)):
    """Vérifie l'authentification via cookie de session"""
    if not session_token:
        return None
    
    user_data = await auth_manager.verify_session(session_token)
    return user_data

async def require_auth(request: Request, session_token: str = Cookie(None)):
    """Requiert une authentification valide"""
    user_data = await get_current_user(request, session_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Non authentifié")
    return user_data


@app.get("/", response_class=HTMLResponse)
async def dashboard_or_login(request: Request, session_token: str = Cookie(None)):
    """Page principale - dashboard ou login selon l'authentification"""
    user_data = await get_current_user(request, session_token)
    
    if not user_data:
        return get_login_page_from_file()
    else:
        return get_main_dashboard_from_file()

# API ENDPOINTS
@app.post("/api/login")
async def login(request: Request):
    """Endpoint de connexion"""
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username et password requis")
        
        # Obtenir IP et User-Agent
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Authentifier
        user_data = await auth_manager.authenticate_user(username, password, client_ip, user_agent)
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Identifiants invalides")
        
        return user_data
        
    except Exception as e:
        logger.error(f"Erreur login: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/dashboard")
async def get_dashboard_data(user_data: dict = Depends(require_auth)):
    """Données du dashboard principal"""
    if not trading_master:
        raise HTTPException(status_code=503, detail="Système non initialisé")
    
    days_elapsed = (datetime.now() - trading_master.capital_manager.start_date).days + 1
    compound_stats = trading_master.capital_manager.calculate_compound_growth(days_elapsed)
    milestone_progress = trading_master.capital_manager.get_next_milestone_progress()
    
    return {
        "user": user_data,
        "capital_growth": {
            "initial": compound_stats["initial_capital"],
            "current": compound_stats["current_capital"],
            "total_return_pct": compound_stats["actual_return_pct"],
            "system_efficiency_pct": compound_stats["system_efficiency_pct"],
            "annualized_return_pct": compound_stats["annualized_return"]
        },
        "milestone_progress": milestone_progress,
        "uptime_days": days_elapsed,
        "system_active": trading_master.active
    }

@app.get("/api/workflows/live-status")
async def get_live_workflows_status(user_data: dict = Depends(require_auth)):
    """Statut live des workflows avec données de performance"""
    # Simulation de données de performance pour chaque workflow
    def generate_performance_data(base_performance=1.0):
        # Générer 7 jours de données
        weekly_gains = []
        total_gain = 0
        
        for i in range(7):
            # Simulation d'un gain/perte journalier
            daily_gain = random.uniform(-2, 3) * base_performance
            weekly_gains.append(round(daily_gain, 1))
            total_gain += daily_gain * 5  # Multiplié par capital fictif
        
        win_rate = random.uniform(60, 85)
        total_trades = random.randint(15, 45)
        
        return {
            "weekly_gains": weekly_gains,
            "total_gain": round(total_gain, 2),
            "gain_percentage": round(sum(weekly_gains), 1),
            "total_trades": total_trades,
            "win_rate": round(win_rate, 1),
            "avg_gain_per_trade": round(total_gain / total_trades if total_trades > 0 else 0, 2)
        }
    
    return {
        "crypto": {
            "status": "idle",
            "current_execution": None,
            "performance": generate_performance_data(1.2)  # Crypto plus performant
        },
        "meme": {
            "status": "scanning", 
            "current_execution": {
                "start_time": datetime.now().isoformat(),
                "status": "scanning"
            },
            "performance": generate_performance_data(0.8)  # Meme plus risqué
        },
        "forex": {
            "status": "idle",
            "current_execution": None,
            "performance": generate_performance_data(1.0)  # Forex stable
        },
        "system_health": {
            "total_executions": random.randint(150, 300),
            "uptime_hours": 24 * 7,  # 7 jours
            "error_rate": round(random.uniform(0.1, 2.5), 1)
        }
    }

@app.post("/api/logout")
async def logout(request: Request, session_token: str = Cookie(None)):
    """Déconnexion"""
    if session_token:
        await auth_manager.logout_user(session_token)
    
    response = JSONResponse({"message": "Déconnecté"})
    response.delete_cookie("session_token")
    return response

# Nouveaux API ENDPOINTS pour workflows détaillés

@app.get("/api/workflows/crypto/details")
async def get_crypto_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow crypto"""
    try:
        crypto_engine = live_orchestrator.crypto_engine
        current_execution = crypto_engine.current_execution
        
        # Simuler données réalistes
        return {
            "pairs_monitored": len(crypto_engine.target_pairs),
            "signals_today": len([s for s in crypto_engine.signal_history if s.timestamp.date() == datetime.now().date()]),
            "avg_confidence": 0.75,
            "next_scan_in_seconds": 180,
            "current_execution": asdict(current_execution) if current_execution else None,
            "pairs_data": {
                pair: {
                    "price": 45000.0 if "BTC" in pair else 2500.0 if "ETH" in pair else 100.0,
                    "change_24h": 2.5,
                    "volume_24h": 250000000
                } for pair in crypto_engine.target_pairs
            },
            "recent_signals": [asdict(s) for s in crypto_engine.signal_history[-10:]]
        }
    except Exception as e:
        logger.error(f"Erreur crypto workflow details: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/meme/details")
async def get_meme_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow meme"""
    try:
        meme_engine = live_orchestrator.meme_engine
        current_execution = meme_engine.current_execution
        
        return {
            "tokens_scanned": len(meme_engine.target_tokens),
            "max_viral_score": 85,
            "total_social_mentions": 1250,
            "overall_risk_level": "MEDIUM",
            "current_execution": asdict(current_execution) if current_execution else None,
            "tokens_data": {
                token: {
                    "viral_score": 65,
                    "social_mentions": 250,
                    "change_24h": 15.2,
                    "whale_activity": "medium"
                } for token in meme_engine.target_tokens
            },
            "risk_analysis": {
                token: {
                    "risk_level": "MEDIUM",
                    "risk_score": 45,
                    "factors": {
                        "volatility": 25.5,
                        "social_activity": 250,
                        "whale_activity": "medium"
                    }
                } for token in meme_engine.target_tokens
            },
            "viral_alerts": []
        }
    except Exception as e:
        logger.error(f"Erreur meme workflow details: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/forex/details")
async def get_forex_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow forex"""
    try:
        forex_engine = live_orchestrator.forex_engine
        current_execution = forex_engine.current_execution
        
        return {
            "pairs_active": len(forex_engine.currency_pairs),
            "usd_strength_index": 102.5,
            "avg_volatility": 0.021,
            "active_signals_count": 2,
            "current_execution": asdict(current_execution) if current_execution else None,
            "pairs_data": {
                pair: {
                    "current_rate": 1.0850 if "EUR" in pair else 1.2650 if "GBP" in pair else 149.50,
                    "change_24h": 0.35,
                    "trend": "Haussier"
                } for pair in forex_engine.currency_pairs
            },
            "economic_data": {
                "usd_strength_index": 102.5,
                "global_risk_sentiment": "risk_on",
                "central_bank_sentiment": {
                    "fed": "hawkish",
                    "ecb": "neutral"
                },
                "economic_calendar": {
                    "high_impact_events_today": 2
                }
            },
            "correlations": {
                "EUR/USD_vs_GBP/USD": 0.75,
                "USD/JPY_vs_risk_sentiment": -0.65,
                "AUD/USD_vs_commodities": 0.80
            }
        }
    except Exception as e:
        logger.error(f"Erreur forex workflow details: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.post("/api/workflows/{workflow_type}/force-execute")
async def force_workflow_execution(workflow_type: str, user_data: dict = Depends(require_auth)):
    """Force l'exécution d'un workflow"""
    try:
        if workflow_type == "crypto":
            asyncio.create_task(live_orchestrator.crypto_engine.execute_workflow())
        elif workflow_type == "meme":
            asyncio.create_task(live_orchestrator.meme_engine.execute_workflow())
        elif workflow_type == "forex":
            asyncio.create_task(live_orchestrator.forex_engine.execute_workflow())
        else:
            raise HTTPException(status_code=400, detail="Type de workflow invalide")
        
        return {"message": f"Exécution forcée du workflow {workflow_type} démarrée"}
    except Exception as e:
        logger.error(f"Erreur force execution {workflow_type}: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/{workflow_type}/export")
async def export_workflow_data(workflow_type: str, user_data: dict = Depends(require_auth)):
    """Exporte les données d'un workflow"""
    try:
        if workflow_type == "crypto":
            data = live_orchestrator.crypto_engine.signal_history
        elif workflow_type == "meme":
            data = []  # TODO: Implémenter historique meme
        elif workflow_type == "forex":
            data = []  # TODO: Implémenter historique forex
        else:
            raise HTTPException(status_code=400, detail="Type de workflow invalide")
        
        export_data = {
            "workflow_type": workflow_type,
            "export_date": datetime.now().isoformat(),
            "data": [asdict(item) for item in data]
        }
        
        from fastapi.responses import JSONResponse
        import json
        
        response = JSONResponse(export_data)
        response.headers["Content-Disposition"] = f"attachment; filename={workflow_type}_export.json"
        return response
        
    except Exception as e:
        logger.error(f"Erreur export {workflow_type}: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

# Nouvel Endpoint pour Capital & Performance
@app.get("/api/capital/performance/details")
async def get_capital_performance_details(user_data: dict = Depends(require_auth)):
    """Fournit des données détaillées pour la page Capital & Performance."""
    if not trading_master or not trading_master.capital_manager:
        raise HTTPException(status_code=503, detail="Système de gestion du capital non initialisé.")

    capital_manager = trading_master.capital_manager
    days_elapsed = (datetime.now() - capital_manager.start_date).days + 1
    compound_stats = capital_manager.calculate_compound_growth(days_elapsed)
    milestone = capital_manager.get_next_milestone_progress()

    # Simuler des données pour les graphiques et KPIs avancés
    # Évolution du capital (pour un graphique linéaire) - ex: 30 derniers jours
    capital_history = [
        {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), "value": round(compound_stats["current_capital"] * random.uniform(0.95 - i*0.002, 1.0 - i*0.001), 2)}
        for i in range(30)
    ]
    capital_history.reverse() # Pour avoir les dates dans l'ordre chronologique

    # Distribution des trades (pour un diagramme circulaire ou à barres)
    trade_distribution = {
        "winning_trades": random.randint(60, 100),
        "losing_trades": random.randint(20, 40),
        "breakeven_trades": random.randint(5, 15)
    }
    total_trades_simulated = sum(trade_distribution.values())

    # Performance mensuelle (pour un graphique à barres)
    monthly_performance = [
        {"month": "Jan", "pnl_pct": round(random.uniform(-2, 5), 2)},
        {"month": "Feb", "pnl_pct": round(random.uniform(1, 8), 2)},
        {"month": "Mar", "pnl_pct": round(random.uniform(-1, 3), 2)},
        {"month": "Apr", "pnl_pct": round(random.uniform(2, 6), 2)},
        # Ajouter d'autres mois si nécessaire
    ]

    # KPIs avancés (simulés)
    kpis = {
        "sharpe_ratio": round(random.uniform(0.5, 2.5), 2),
        "max_drawdown_pct": round(random.uniform(5, 15), 2),
        "average_win_pct": round(random.uniform(1, 3), 2),
        "average_loss_pct": round(random.uniform(0.5, 1.5), 2),
        "profit_factor": round(random.uniform(1.2, 3.0), 2)
    }

    return {
        "user": user_data,
        "summary": {
            "initial_capital": compound_stats["initial_capital"],
            "current_capital": compound_stats["current_capital"],
            "total_profit": round(compound_stats["current_capital"] - compound_stats["initial_capital"], 2),
            "total_return_pct": compound_stats["actual_return_pct"],
            "system_efficiency_pct": compound_stats["system_efficiency_pct"],
            "annualized_return_pct": compound_stats["annualized_return"]
        },
        "milestone": {
            "next_target": milestone["target_capital"],
            "progress_pct": milestone["progress_percentage"],
            "remaining_to_target": milestone["remaining_to_target"]
        },
        "charts_data": {
            "capital_evolution": capital_history,
            "trade_distribution": trade_distribution,
            "monthly_performance": monthly_performance
        },
        "key_performance_indicators": kpis,
        "operational_stats": {
            "uptime_days": days_elapsed,
            "total_trades_simulated": total_trades_simulated, # Basé sur la simulation ci-dessus
            "system_active": trading_master.active
        }
    }

if __name__ == "__main__":
    print("🧠 DÉMARRAGE TRADING AI PROFESSIONNEL")
    print("="*50)
    print(f"🔐 Authentification DB sécurisée")
    print(f"🔄 Workflows live actifs")
    print(f"💼 Interface professionnelle")
    print(f"🌐 Port: {PORT}")
    print("="*50)
    
    uvicorn.run(app, host="0.0.0.0", port=PORT) 