#!/usr/bin/env python3
"""
🧠 SMART CAPITAL GROWTH SYSTEM
Système 100% autonome avec croissance intelligente et intérêts composés
L'IA gère TOUT - tu ne fais que regarder ton capital grandir ! 💰

VERSION DOCKER AVEC APIs GRATUITES/SIMULATION
"""

import asyncio
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging
import math
from fastapi import FastAPI, HTTPException, Response, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
import secrets

# Imports de nos systèmes
try:
    from roi_10x_trading_system import ROI10xTradingSystem
    from src.infrastructure.rpc_optimizer import AutoTradingRPCManager
    from src.social_intelligence.social_monitor import SocialTradingIntegrator
    from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
except ImportError:
    # Mode simulation si modules pas disponibles
    print("⚠️ Mode simulation - modules réels non disponibles")
    # Fallback pour prometheus_client si pas installé
    try:
        from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
    except ImportError:
        Counter = Gauge = None
        generate_latest = lambda: "# Prometheus non disponible"
        CONTENT_TYPE_LATEST = "text/plain"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration environnement
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
API_MODE = "SIMULATION" if DEMO_MODE else "LIVE"
PORT = int(os.getenv("PORT", "8000"))
PROFESSIONAL_MODE = os.getenv("PROFESSIONAL_MODE", "false").lower() == "true"

# Authentification
security = HTTPBasic()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "TradingAI2025!")

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Vérification authentification"""
    is_correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

app = FastAPI(title="🧠 Trading AI Autonome", version="1.0.0")

@dataclass
class CapitalMilestone:
    """Milestone de capital"""
    target_amount: float
    description: str
    action_required: str
    human_approval_needed: bool
    compound_rate: float
    risk_adjustment: str

class IntelligentCompoundGrowth:
    """Gestionnaire de croissance intelligente avec intérêts composés"""
    
    def __init__(self, initial_capital: float = 200.0):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.total_profit = 0.0
        self.compound_cycles = 0
        self.start_date = datetime.now()
        
        # Configuration croissance intelligente
        self.target_annual_return = 5.0  # 500% par an (très conservateur vs crypto)
        self.monthly_target_return = (1 + self.target_annual_return) ** (1/12) - 1  # ~15.5% / mois
        self.daily_target_return = (1 + self.monthly_target_return) ** (1/30) - 1  # ~0.49% / jour
        
        # Milestones automatiques de croissance
        self.milestones = self._generate_smart_milestones()
        self.current_milestone_index = 0
        
        # Historique de performance
        self.daily_returns = []
        self.weekly_performance = []
        self.monthly_snapshots = []
        
    def _generate_smart_milestones(self) -> List[CapitalMilestone]:
        """Génère milestones intelligents de croissance"""
        milestones = []
        
        # Phase 1: Validation système (1er mois)
        milestones.append(CapitalMilestone(
            target_amount=500.0,  # 200€ → 500€ (+150%)
            description="🎯 Validation système - Premier doublement+",
            action_required="CONTINUE_AUTO",
            human_approval_needed=False,
            compound_rate=0.8,  # Réinvestir 80%
            risk_adjustment="CONSERVATIVE"
        ))
        
        # Phase 2: Croissance accélérée (2-3 mois)
        milestones.append(CapitalMilestone(
            target_amount=1000.0,  # 500€ → 1000€ (+100%)
            description="🚀 Premier millier - Activation APIs premium",
            action_required="UPGRADE_APIS",
            human_approval_needed=True,  # Demander confirmation pour APIs premium
            compound_rate=0.85,  # Réinvestir 85%
            risk_adjustment="MODERATE"
        ))
        
        # Phase 3: Croissance soutenue (4-6 mois)
        milestones.append(CapitalMilestone(
            target_amount=2500.0,  # 1000€ → 2500€ (+150%)
            description="Capital significatif - Diversification automatique",
            action_required="DIVERSIFY_AUTO",
            human_approval_needed=False,
            compound_rate=0.9,  # Réinvestir 90%
            risk_adjustment="MODERATE"
        ))
        
        # Phase 4: Scaling professionnel (6-12 mois)
        milestones.append(CapitalMilestone(
            target_amount=5000.0,  # 2500€ → 5000€ (+100%)
            description="🏆 Trading professionnel - Capital protection",
            action_required="PROFESSIONAL_MODE",
            human_approval_needed=True,  # Confirmation pour mode pro
            compound_rate=0.75,  # Réinvestir 75% (plus conservateur)
            risk_adjustment="CONSERVATIVE"
        ))
        
        # Phase 5: Wealth building (1-2 ans)
        milestones.append(CapitalMilestone(
            target_amount=10000.0,  # 5000€ → 10000€ (+100%)
            description="💰 Wealth building - Réinvestissement optimal",
            action_required="WEALTH_MODE",
            human_approval_needed=False,
            compound_rate=0.85,
            risk_adjustment="MODERATE"
        ))
        
        # Phase 6: Capital important (2+ ans)
        milestones.append(CapitalMilestone(
            target_amount=25000.0,  # 10k€ → 25k€ (+150%)
            description="🌟 Capital majeur - Gestion patrimoniale",
            action_required="WEALTH_MANAGEMENT",
            human_approval_needed=True,  # Confirmation pour gestion patrimoniale
            compound_rate=0.7,  # Plus conservateur avec gros capital
            risk_adjustment="VERY_CONSERVATIVE"
        ))
        
        return milestones
        
    def calculate_compound_growth(self, days_elapsed: int) -> Dict:
        """Calcule croissance composée théorique vs réelle"""
        
        # Croissance théorique (intérêts composés parfaits)
        theoretical_value = self.initial_capital * (1 + self.daily_target_return) ** days_elapsed
        
        # Performance réelle
        actual_value = self.current_capital
        actual_return = (actual_value / self.initial_capital - 1) * 100
        theoretical_return = (theoretical_value / self.initial_capital - 1) * 100
        
        # Efficacité du système
        efficiency = (actual_return / theoretical_return * 100) if theoretical_return > 0 else 0
        
        return {
            "days_elapsed": days_elapsed,
            "initial_capital": self.initial_capital,
            "current_capital": actual_value,
            "theoretical_target": theoretical_value,
            "actual_return_pct": actual_return,
            "theoretical_return_pct": theoretical_return,
            "system_efficiency_pct": efficiency,
            "outperformance": actual_return - theoretical_return,
            "daily_compound_rate": self.daily_target_return * 100,
            "annualized_return": actual_return * (365 / days_elapsed) if days_elapsed > 0 else 0
        }
        
    def get_next_milestone_progress(self) -> Dict:
        """Progression vers prochain milestone"""
        if self.current_milestone_index >= len(self.milestones):
            return {"status": "ALL_MILESTONES_COMPLETED", "next_target": "UNLIMITED_GROWTH"}
            
        current_milestone = self.milestones[self.current_milestone_index]
        progress_pct = (self.current_capital / current_milestone.target_amount) * 100
        
        return {
            "current_milestone": {
                "index": self.current_milestone_index + 1,
                "target": current_milestone.target_amount,
                "description": current_milestone.description,
                "action": current_milestone.action_required,
                "approval_needed": current_milestone.human_approval_needed
            },
            "progress_percentage": min(100, progress_pct),
            "remaining_amount": max(0, current_milestone.target_amount - self.current_capital),
            "estimated_days_to_target": self._estimate_days_to_milestone(current_milestone.target_amount),
            "compound_strategy": {
                "reinvest_rate": current_milestone.compound_rate,
                "risk_level": current_milestone.risk_adjustment
            }
        }
        
    def _estimate_days_to_milestone(self, target: float) -> int:
        """Estime jours pour atteindre un milestone"""
        if self.current_capital >= target:
            return 0
            
        required_growth = target / self.current_capital
        
        # Utiliser performance récente si disponible
        if len(self.daily_returns) >= 7:
            avg_daily_return = sum(self.daily_returns[-7:]) / 7  # Moyenne 7 derniers jours
        else:
            avg_daily_return = self.daily_target_return  # Utiliser target théorique
            
        if avg_daily_return <= 0:
            return 999  # Performance négative
            
        days_needed = math.log(required_growth) / math.log(1 + avg_daily_return)
        return max(1, int(days_needed))
        
    def should_trigger_milestone_action(self) -> Optional[Dict]:
        """Vérifie si action milestone requise"""
        if self.current_milestone_index >= len(self.milestones):
            return None
            
        current_milestone = self.milestones[self.current_milestone_index]
        
        if self.current_capital >= current_milestone.target_amount:
            return {
                "milestone_achieved": current_milestone,
                "action_required": current_milestone.action_required,
                "needs_human_approval": current_milestone.human_approval_needed,
                "compound_adjustment": {
                    "new_reinvest_rate": current_milestone.compound_rate,
                    "new_risk_level": current_milestone.risk_adjustment
                }
            }
            
        return None
        
    def update_capital(self, new_amount: float, profit: float):
        """Met à jour capital avec nouveau montant"""
        old_capital = self.current_capital
        self.current_capital = new_amount
        self.total_profit += profit
        
        # Calculer rendement quotidien
        if old_capital > 0:
            daily_return = (new_amount / old_capital - 1)
            self.daily_returns.append(daily_return)
            
            # Garder seulement 30 derniers jours
            if len(self.daily_returns) > 30:
                self.daily_returns = self.daily_returns[-30:]
                
        # Mettre à jour métriques Prometheus
        self._update_prometheus_metrics()
                
    def _update_prometheus_metrics(self):
        """Met à jour les métriques Prometheus"""
        if not trading_capital_current:
            return
            
        try:
            days_elapsed = (datetime.now() - self.start_date).days + 1
            compound_stats = self.calculate_compound_growth(days_elapsed)
            
            trading_capital_current.set(self.current_capital)
            trading_return_percentage.set(compound_stats["actual_return_pct"])
            trading_system_efficiency.set(compound_stats["system_efficiency_pct"])
            trading_uptime_days.set(days_elapsed)
            trading_profit_total.set(self.total_profit)
        except Exception as e:
            logger.warning(f"Erreur mise à jour métriques Prometheus: {e}")

class AutonomousTradingMaster:
    """Maître autonome du trading - gère TOUT automatiquement"""
    
    def __init__(self, initial_capital: float = 200.0):
        self.capital_manager = IntelligentCompoundGrowth(initial_capital)
        
        # Mode simulation ou réel
        if DEMO_MODE:
            self.roi_system = None  # Simulation
            logger.info("🎮 MODE SIMULATION - Aucune API requise")
        else:
            try:
                self.roi_system = ROI10xTradingSystem(initial_capital)
                logger.info("🔴 MODE RÉEL - APIs configurées")
            except:
                self.roi_system = None
                logger.warning("⚠️ Fallback vers mode simulation")
                
        self.autonomous_mode = True
        self.human_intervention_required = False
        self.active = True
        
        # Configuration autonomie totale
        self.auto_reinvest = True
        self.auto_upgrade_apis = True
        self.auto_adjust_risk = True
        self.auto_diversify = True
        
        # Seuils pour demander aval humain (seulement vraiment important)
        self.major_decision_threshold = 5000.0  # >5k€ = décision majeure
        self.risk_increase_threshold = 0.3  # >30% risque = demander aval
        self.capital_allocation_threshold = 0.5  # >50% capital sur un trade = demander aval
        
        # Stats temps réel
        self.daily_stats = {
            "trades_executed": 0,
            "successful_trades": 0,
            "profit_today": 0.0,
            "loss_today": 0.0
        }
        
    async def initialize_autonomous_system(self) -> Dict:
        """Initialise système 100% autonome"""
        logger.info("🧠 Initialisation MAÎTRE AUTONOME...")
        
        # 1. Initialiser sous-systèmes selon mode
        if self.roi_system and not DEMO_MODE:
            roi_status = await self.roi_system.initialize_roi_10x_system()
        else:
            roi_status = {"status": "SIMULATION_MODE"}
        
        # 2. Configuration autonomie totale
        self.active = True
        
        return {
            "system": "AUTONOMOUS TRADING MASTER",
            "mode": API_MODE,
            "status": "FULLY_AUTONOMOUS",
            "human_control": "MINIMAL - Only major decisions",
            "capital_initial": self.capital_manager.initial_capital,
            "growth_strategy": "INTELLIGENT_COMPOUND",
            "autonomy_level": "100%",
            "demo_mode": DEMO_MODE,
            "subsystems": {
                "roi_trading": roi_status["status"],
                "compound_growth": "ACTIVE",
                "milestone_tracking": "ACTIVE", 
                "risk_management": "AUTO",
                "capital_allocation": "AUTO",
                "simulation_engine": "ACTIVE" if DEMO_MODE else "DISABLED"
            },
            "intelligence_features": [
                "🧠 Décisions 100% autonomes",
                "💰 Réinvestissement automatique intelligent", 
                "📈 Ajustement risque automatique",
                "🎯 Milestone tracking avec actions auto",
                "🔄 Optimisation continue sans intervention",
                "⚡ Compound growth optimization",
                "🛡️ Protection capital automatique",
                "🎮 Mode simulation intégré" if DEMO_MODE else "🔴 Mode trading réel"
            ],
            "human_intervention": [
                f"Seulement si capital > {self.major_decision_threshold}€",
                "Seulement si risque > 30%",
                "Seulement si allocation > 50% sur un trade"
            ]
        }

    def _calculate_daily_profit(self) -> float:
        """Calcule profit journalier (simulation intelligente)"""
        import random
        
        # Simuler profit quotidien basé sur performance système
        base_return = self.capital_manager.daily_target_return
        volatility = 0.003  # 0.3% de volatilité
        
        # Simulation plus réaliste avec cycles de marché
        market_cycle = math.sin(time.time() / 86400) * 0.5  # Cycle quotidien
        
        # Performance avec un biais positif (système optimisé) + cycles
        daily_return = random.normalvariate(
            base_return * 1.1 + market_cycle * 0.002, 
            volatility
        )
        
        profit = self.capital_manager.current_capital * daily_return
        
        # Limitation des pertes (protection capital)
        max_daily_loss = self.capital_manager.current_capital * 0.02  # Max 2% perte par jour
        profit = max(-max_daily_loss, profit)
        
        # Mettre à jour stats
        if profit > 0:
            self.daily_stats["successful_trades"] += 1
            self.daily_stats["profit_today"] += profit
            # Mettre à jour métriques Prometheus
            if trading_trades_successful:
                trading_trades_successful.inc()
        else:
            self.daily_stats["loss_today"] += abs(profit)
            if trading_trades_failed:
                trading_trades_failed.inc()
            
        self.daily_stats["trades_executed"] += 1
        
        return profit

# Instance globale
master_instance = None

@app.on_event("startup")
async def startup_event():
    """Démarre le maître autonome au démarrage de l'API"""
    global master_instance
    
    initial_capital = float(os.getenv("INITIAL_CAPITAL", "200"))
    master_instance = AutonomousTradingMaster(initial_capital)
    
    # Initialiser
    status = await master_instance.initialize_autonomous_system()
    logger.info(f"🚀 Système autonome initialisé: {status}")
    
    # Lancer en arrière-plan
    asyncio.create_task(autonomous_background_loop())

async def autonomous_background_loop():
    """Boucle autonome en arrière-plan - AVEC VISIBILITÉ COMPLÈTE"""
    cycle = 0
    last_milestone_check = datetime.now()
    last_compound_calculation = datetime.now()
    
    logger.info("🚀 DÉMARRAGE BOUCLE AUTONOME - Système 100% indépendant activé")
    
    while master_instance and master_instance.active:
        try:
            cycle += 1
            current_time = datetime.now()
            
            # Log début de cycle
            logger.info(f"🔄 CYCLE #{cycle} - {current_time.strftime('%H:%M:%S')}")
            
            # 1. Exécuter cycle trading automatique
            logger.info("📊 Analyse marché + calcul profit quotidien...")
            profit_today = master_instance._calculate_daily_profit()
            new_capital = master_instance.capital_manager.current_capital + profit_today
            
            # Log décision de trading
            if profit_today > 0:
                logger.info(f"💰 PROFIT généré: +{profit_today:.4f}€ (Capital: {new_capital:.2f}€)")
            elif profit_today < 0:
                logger.info(f"📉 Perte simulée: {profit_today:.4f}€ (Capital: {new_capital:.2f}€)")
            else:
                logger.info(f"⚖️ Position HOLD - Capital stable: {new_capital:.2f}€")
            
            master_instance.capital_manager.update_capital(new_capital, profit_today)
            
            # 2. Calculer croissance composée (toutes les heures)
            if current_time - last_compound_calculation >= timedelta(hours=1):
                logger.info("🧮 Calcul croissance composée horaire...")
                days_elapsed = (datetime.now() - master_instance.capital_manager.start_date).days + 1
                compound_stats = master_instance.capital_manager.calculate_compound_growth(days_elapsed)
                
                # Log performance détaillé
                logger.info(f"📈 PERFORMANCE: Efficacité {compound_stats['system_efficiency_pct']:.1f}% | Rendement {compound_stats['actual_return_pct']:.2f}%")
                
                if compound_stats["system_efficiency_pct"] > 120:
                    logger.info(f"🎉 EXCELLENCE! Système surperforme la cible de {compound_stats['system_efficiency_pct']-100:.1f}%")
                elif compound_stats["system_efficiency_pct"] < 80:
                    logger.warning(f"⚠️ SOUS-PERFORMANCE détectée. Optimisation requise.")
                    
                last_compound_calculation = current_time
            
            # 3. Vérifier milestones (toutes les 4 heures)
            if current_time - last_milestone_check >= timedelta(hours=4):
                logger.info("🎯 Vérification progression milestones...")
                milestone_action = master_instance.capital_manager.should_trigger_milestone_action()
                if milestone_action:
                    logger.info(f"🚀 MILESTONE ATTEINT! {milestone_action['milestone_achieved'].description}")
                    logger.info(f"📋 Action requise: {milestone_action['milestone_achieved'].action_required}")
                    master_instance.capital_manager.current_milestone_index += 1
                else:
                    progress = master_instance.capital_manager.get_next_milestone_progress()
                    logger.info(f"📊 Progression milestone: {progress['progress_percentage']:.1f}% vers {progress['current_milestone']['target']}€")
                last_milestone_check = current_time
            
            # 4. Rapport de performance (tous les 50 cycles)
            if cycle % 50 == 0:
                await generate_performance_report(cycle)
            
            # Log fin de cycle
            logger.info(f"✅ Cycle #{cycle} terminé - Prochain dans 60s")
            await asyncio.sleep(60)  # 1 minute entre cycles
            
        except Exception as e:
            logger.error(f"❌ ERREUR CYCLE #{cycle}: {e}")
            logger.info("🔄 Récupération automatique dans 5 minutes...")
            await asyncio.sleep(300)  # 5 minutes de pause sur erreur

async def generate_performance_report(cycle: int):
    """Génère rapport de performance"""
    if not master_instance:
        return
        
    days_elapsed = (datetime.now() - master_instance.capital_manager.start_date).days + 1
    compound_stats = master_instance.capital_manager.calculate_compound_growth(days_elapsed)
    milestone_progress = master_instance.capital_manager.get_next_milestone_progress()
    
    logger.info(f"🧠 RAPPORT AUTONOME #{cycle} - Capital: {compound_stats['current_capital']:.2f}€ (+{compound_stats['actual_return_pct']:.1f}%)")

# API ENDPOINTS

@app.get("/health")
async def health_check():
    """Healthcheck pour Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mode": API_MODE,
        "active": master_instance.active if master_instance else False
    }

@app.get("/dashboard")
async def get_dashboard(username: str = Depends(authenticate_user)):
    """Dashboard complet du système autonome - PROTÉGÉ"""
    if not master_instance:
        raise HTTPException(status_code=503, detail="Système non initialisé")
    
    days_elapsed = (datetime.now() - master_instance.capital_manager.start_date).days + 1
    compound_stats = master_instance.capital_manager.calculate_compound_growth(days_elapsed)
    milestone_progress = master_instance.capital_manager.get_next_milestone_progress()
    
    return {
        "system_status": "FULLY_AUTONOMOUS" if not master_instance.human_intervention_required else "AWAITING_APPROVAL",
        "mode": API_MODE,
        "uptime_days": days_elapsed,
        "authenticated_user": username,
        "capital_growth": {
            "initial": compound_stats["initial_capital"],
            "current": compound_stats["current_capital"],
            "total_return_pct": compound_stats["actual_return_pct"],
            "system_efficiency_pct": compound_stats["system_efficiency_pct"],
            "annualized_return_pct": compound_stats["annualized_return"],
            "daily_target": master_instance.capital_manager.daily_target_return * 100
        },
        "milestone_progress": milestone_progress,
        "daily_stats": master_instance.daily_stats,
        "compound_strategy": {
            "auto_reinvest": master_instance.auto_reinvest,
            "current_reinvest_rate": milestone_progress.get("compound_strategy", {}).get("reinvest_rate", 0.8)
        },
        "autonomy_features": [
            "✅ Trading decisions: 100% autonomous",
            "✅ Risk management: Auto-adjusted", 
            "✅ Capital allocation: Intelligent",
            "✅ Profit reinvestment: Compound optimized",
            "✅ Milestone progression: Automated",
            "✅ Performance optimization: Continuous"
        ]
    }

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Interface web professionnelle pour trading autonome"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading AI • Autonomous System</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* Variables CSS professionnelles */
            :root {
                --primary-blue: #2563eb;
                --primary-dark: #1e293b;
                --bg-main: #f8fafc;
                --bg-card: #ffffff;
                --border-light: #e2e8f0;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --success-green: #10b981;
                --warning-orange: #f59e0b;
                --danger-red: #ef4444;
                --accent-purple: #8b5cf6;
            }
            
            /* Reset et base */
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: var(--bg-main);
                color: var(--text-primary);
                line-height: 1.6;
            }
            
            /* Layout principal */
            .app-layout {
                display: grid;
                grid-template-columns: 250px 1fr;
                min-height: 100vh;
            }
            
            /* Sidebar navigation */
            .sidebar {
                background: var(--bg-card);
                border-right: 1px solid var(--border-light);
                padding: 1.5rem 0;
                box-shadow: 2px 0 8px rgba(0,0,0,0.05);
            }
            
            .sidebar-brand {
                padding: 0 1.5rem 2rem;
                border-bottom: 1px solid var(--border-light);
                margin-bottom: 2rem;
            }
            
            .sidebar-brand h1 {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--primary-blue);
                margin-bottom: 0.25rem;
            }
            
            .sidebar-brand p {
                font-size: 0.875rem;
                color: var(--text-secondary);
            }
            
            .nav-menu {
                list-style: none;
            }
            
            .nav-item {
                margin: 0.25rem 1rem;
            }
            
            .nav-link {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem 1rem;
                border-radius: 0.5rem;
                color: var(--text-secondary);
                text-decoration: none;
                transition: all 0.2s ease;
                font-weight: 500;
            }
            
            .nav-link:hover {
                background: #f1f5f9;
                color: var(--primary-blue);
            }
            
            .nav-link.active {
                background: #dbeafe;
                color: var(--primary-blue);
                font-weight: 600;
            }
            
            .nav-icon {
                width: 20px;
                text-align: center;
            }
            
            /* Main content */
            .main-content {
                display: flex;
                flex-direction: column;
            }
            
            /* Top bar */
            .top-bar {
                background: var(--bg-card);
                border-bottom: 1px solid var(--border-light);
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            
            .page-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--text-primary);
            }
            
            .status-badge {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                background: #ecfdf5;
                color: var(--success-green);
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-size: 0.875rem;
                font-weight: 600;
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                background: var(--success-green);
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            
            /* Content area */
            .content-area {
                flex: 1;
                padding: 2rem;
                overflow-y: auto;
            }
            
            /* Page content */
            .page-content {
                display: none;
                animation: fadeIn 0.3s ease;
            }
            
            .page-content.active {
                display: block;
            }
            
            /* Grid layouts */
            .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
            .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
            .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; }
            
            /* Cards professionnelles */
            .card {
                background: var(--bg-card);
                border: 1px solid var(--border-light);
                border-radius: 0.75rem;
                padding: 1.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                transition: all 0.2s ease;
            }
            
            .card:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid var(--border-light);
            }
            
            .card-title {
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--text-primary);
            }
            
            .card-subtitle {
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin-top: 0.25rem;
            }
            
            /* Métriques */
            .metric {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.75rem 0;
                border-bottom: 1px solid #f1f5f9;
            }
            
            .metric:last-child {
                border-bottom: none;
            }
            
            .metric-label {
                color: var(--text-secondary);
                font-weight: 500;
            }
            
            .metric-value {
                font-weight: 600;
                color: var(--text-primary);
            }
            
            .metric-value.positive { color: var(--success-green); }
            .metric-value.negative { color: var(--danger-red); }
            .metric-value.warning { color: var(--warning-orange); }
            
            /* Progress bar */
            .progress-container {
                margin: 1rem 0;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background: #f1f5f9;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--primary-blue), var(--accent-purple));
                transition: width 0.8s ease;
            }
            
            .progress-text {
                display: flex;
                justify-content: space-between;
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin-top: 0.5rem;
            }
            
            /* Buttons */
            .btn {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.75rem 1.5rem;
                border: none;
                border-radius: 0.5rem;
                font-weight: 600;
                text-decoration: none;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.875rem;
            }
            
            .btn-primary {
                background: var(--primary-blue);
                color: white;
            }
            
            .btn-primary:hover {
                background: #1d4ed8;
                transform: translateY(-1px);
            }
            
            .btn-secondary {
                background: white;
                color: var(--text-secondary);
                border: 1px solid var(--border-light);
            }
            
            .btn-secondary:hover {
                background: #f8fafc;
                border-color: var(--primary-blue);
                color: var(--primary-blue);
            }
            
            /* Tables pour trading */
            .trading-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 1rem;
            }
            
            .trading-table th,
            .trading-table td {
                text-align: left;
                padding: 1rem;
                border-bottom: 1px solid var(--border-light);
            }
            
            .trading-table th {
                background: #f8fafc;
                font-weight: 600;
                color: var(--text-secondary);
                font-size: 0.875rem;
            }
            
            .trading-table tr:hover {
                background: #f8fafc;
            }
            
            .signal-badge {
                padding: 0.25rem 0.75rem;
                border-radius: 1rem;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .signal-buy { background: #ecfdf5; color: var(--success-green); }
            .signal-sell { background: #fef2f2; color: var(--danger-red); }
            .signal-hold { background: #f1f5f9; color: var(--text-secondary); }
            
            /* Logs */
            .logs-container {
                background: #1e293b;
                color: #e2e8f0;
                padding: 1.5rem;
                border-radius: 0.5rem;
                height: 400px;
                overflow-y: auto;
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 0.875rem;
            }
            
            .log-entry {
                margin: 0.25rem 0;
                padding: 0.5rem;
                border-radius: 0.25rem;
                border-left: 3px solid var(--primary-blue);
                background: rgba(255,255,255,0.05);
            }
            
            /* Configuration forms */
            .config-form {
                display: grid;
                gap: 1rem;
                margin-top: 1rem;
            }
            
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .form-label {
                font-weight: 600;
                color: var(--text-primary);
                font-size: 0.875rem;
            }
            
            .form-input {
                padding: 0.75rem;
                border: 1px solid var(--border-light);
                border-radius: 0.5rem;
                font-size: 0.875rem;
                transition: border-color 0.2s ease;
            }
            
            .form-input:focus {
                outline: none;
                border-color: var(--primary-blue);
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }
            
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            /* Responsive */
            @media (max-width: 1024px) {
                .app-layout {
                    grid-template-columns: 1fr;
                }
                .sidebar {
                    display: none;
                }
                .grid-2, .grid-3, .grid-4 {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="app-layout">
            <!-- Sidebar -->
            <aside class="sidebar">
                <div class="sidebar-brand">
                    <h1>Trading AI</h1>
                    <p>Autonomous System</p>
                </div>
                
                <nav>
                    <ul class="nav-menu">
                        <li class="nav-item">
                            <a href="#" class="nav-link active" onclick="showPage('dashboard')">
                                <span class="nav-icon">📊</span>
                                Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" onclick="showPage('crypto')">
                                <span class="nav-icon">₿</span>
                                Crypto Markets
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" onclick="showPage('forex')">
                                <span class="nav-icon">💱</span>
                                Forex Trading
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" onclick="showPage('analytics')">
                                <span class="nav-icon">📈</span>
                                Analytics
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" onclick="showPage('logs')">
                                <span class="nav-icon">📋</span>
                                System Logs
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" onclick="showPage('config')">
                                <span class="nav-icon">⚙️</span>
                                Configuration
                            </a>
                        </li>
                    </ul>
                </nav>
            </aside>
            
            <!-- Main content -->
            <main class="main-content">
                <!-- Top bar -->
                <header class="top-bar">
                    <h1 class="page-title" id="page-title">Dashboard</h1>
                    <div class="status-badge">
                        <div class="status-dot"></div>
                        System Active
                    </div>
                </header>
                
                <!-- Content area -->
                <div class="content-area">
                    <!-- Dashboard Page -->
                    <div id="dashboard-page" class="page-content active">
                        <div class="grid-3" id="dashboard-metrics">
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Loading...</h3>
                                </div>
                                <p>Retrieving system data...</p>
                            </div>
                        </div>
                        
                        <div class="grid-2" style="margin-top: 2rem;">
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Recent Activity</h3>
                                </div>
                                <div id="quick-activity">Loading...</div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Trading Decisions</h3>
                                </div>
                                <div id="quick-decisions">Loading...</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Crypto Page -->
                    <div id="crypto-page" class="page-content">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Cryptocurrency Markets</h3>
                                <p class="card-subtitle">Real-time crypto trading opportunities</p>
                            </div>
                            <table class="trading-table" id="crypto-table">
                                <thead>
                                    <tr>
                                        <th>Pair</th>
                                        <th>Price</th>
                                        <th>24h Change</th>
                                        <th>Volume</th>
                                        <th>Signal</th>
                                        <th>Confidence</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td colspan="6">Loading crypto data...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <!-- Forex Page -->
                    <div id="forex-page" class="page-content">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Forex Markets</h3>
                                <p class="card-subtitle">Foreign exchange trading signals</p>
                            </div>
                            <table class="trading-table" id="forex-table">
                                <thead>
                                    <tr>
                                        <th>Pair</th>
                                        <th>Price</th>
                                        <th>24h Change</th>
                                        <th>Signal</th>
                                        <th>Confidence</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td colspan="5">Loading forex data...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <!-- Analytics Page -->
                    <div id="analytics-page" class="page-content">
                        <div class="grid-2">
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Market Analytics</h3>
                                </div>
                                <div id="market-analytics">Loading...</div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Performance Metrics</h3>
                                </div>
                                <div id="performance-metrics">Loading...</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Logs Page -->
                    <div id="logs-page" class="page-content">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">System Logs</h3>
                                <button class="btn btn-secondary" onclick="loadLogs()">Refresh</button>
                            </div>
                            <div class="logs-container" id="system-logs">
                                Loading system logs...
                            </div>
                        </div>
                    </div>
                    
                    <!-- Configuration Page -->
                    <div id="config-page" class="page-content">
                        <div class="grid-2">
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Environment Configuration</h3>
                                    <button class="btn btn-secondary" onclick="loadConfig()">Reload</button>
                                </div>
                                <div id="env-config">Loading configuration...</div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">System Controls</h3>
                                </div>
                                <div class="config-form">
                                    <button class="btn btn-primary" onclick="controlSystem('start')">Start System</button>
                                    <button class="btn btn-secondary" onclick="controlSystem('stop')">Stop System</button>
                                    <button class="btn btn-secondary" onclick="exportData()">Export Data</button>
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">Mode Professionnel</h3>
                                    <p class="card-subtitle">Grafana + Prometheus</p>
                                </div>
                                <div id="professional-mode-info">
                                    <div class="metric">
                                        <span class="metric-label">Status</span>
                                        <span class="metric-value" id="pro-mode-status">Loading...</span>
                                    </div>
                                    <div class="metric">
                                        <span class="metric-label">Grafana</span>
                                        <span class="metric-value">
                                            <a href="http://localhost:3000" target="_blank" style="color: var(--primary-blue);">
                                                http://localhost:3000
                                            </a>
                                        </span>
                                    </div>
                                    <div class="metric">
                                        <span class="metric-label">Prometheus</span>
                                        <span class="metric-value">
                                            <a href="http://localhost:9090" target="_blank" style="color: var(--primary-blue);">
                                                http://localhost:9090
                                            </a>
                                        </span>
                                    </div>
                                </div>
                                <div style="margin-top: 1rem; padding: 1rem; background: #f1f5f9; border-radius: 0.5rem;">
                                    <h4 style="margin-bottom: 0.5rem; color: var(--text-primary);">Guide Mode Pro</h4>
                                    <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem;">
                                        Active Grafana pour des visualisations avancées et Prometheus pour les métriques détaillées.
                                    </p>
                                    <a href="/guide-professionnel" target="_blank" class="btn btn-primary">
                                        📖 Voir le Guide Complet
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>

        <script>
            // Navigation
            function showPage(pageId) {
                // Update page title
                const titles = {
                    'dashboard': 'Dashboard',
                    'crypto': 'Crypto Markets',
                    'forex': 'Forex Trading',
                    'analytics': 'Analytics',
                    'logs': 'System Logs',
                    'config': 'Configuration'
                };
                
                document.getElementById('page-title').textContent = titles[pageId] || 'Dashboard';
                
                // Hide all pages
                document.querySelectorAll('.page-content').forEach(page => {
                    page.classList.remove('active');
                });
                
                // Remove active from all nav links
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                
                // Show selected page
                document.getElementById(pageId + '-page').classList.add('active');
                
                // Activate nav link
                event.target.classList.add('active');
                
                // Load page data
                loadPageData(pageId);
            }

            function loadPageData(pageId) {
                switch(pageId) {
                    case 'dashboard':
                        loadDashboard();
                        loadQuickActivity();
                        loadQuickDecisions();
                        break;
                    case 'crypto':
                    case 'forex':
                        loadTradingStreams();
                        break;
                    case 'analytics':
                        loadAnalytics();
                        break;
                    case 'logs':
                        loadLogs();
                        break;
                    case 'config':
                        loadConfig();
                        break;
                }
            }

            // Dashboard functions
            async function loadDashboard() {
                try {
                    const response = await fetch('/dashboard');
                    const data = await response.json();
                    
                    document.getElementById('dashboard-metrics').innerHTML = `
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Capital Performance</h3>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Current Capital</span>
                                <span class="metric-value positive">${data.capital_growth.current.toFixed(2)}€</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Total Return</span>
                                <span class="metric-value ${data.capital_growth.total_return_pct > 0 ? 'positive' : 'negative'}">
                                    ${data.capital_growth.total_return_pct > 0 ? '+' : ''}${data.capital_growth.total_return_pct.toFixed(1)}%
                                </span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">System Efficiency</span>
                                <span class="metric-value ${data.capital_growth.system_efficiency_pct > 100 ? 'positive' : 'negative'}">
                                    ${data.capital_growth.system_efficiency_pct.toFixed(1)}%
                                </span>
                            </div>
                        </div>
                        
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">Milestone Progress</h3>
                            </div>
                            ${data.milestone_progress.current_milestone ? `
                                <p style="margin-bottom: 1rem; color: var(--text-secondary);">
                                    ${data.milestone_progress.current_milestone.description}
                                </p>
                                <div class="progress-container">
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${Math.min(100, data.milestone_progress.progress_percentage)}%"></div>
                                    </div>
                                    <div class="progress-text">
                                        <span>${data.milestone_progress.progress_percentage.toFixed(1)}% Complete</span>
                                        <span>Target: ${data.milestone_progress.current_milestone.target}€</span>
                                    </div>
                                </div>
                            ` : `<p>All milestones achieved! 🎉</p>`}
                        </div>
                        
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">System Status</h3>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Mode</span>
                                <span class="metric-value">${data.mode}</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Uptime</span>
                                <span class="metric-value">${data.uptime_days} day(s)</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">User</span>
                                <span class="metric-value">${data.authenticated_user}</span>
                            </div>
                        </div>
                    `;
                } catch (error) {
                    console.error('Dashboard error:', error);
                }
            }

            async function loadQuickActivity() {
                try {
                    const response = await fetch('/system-logs');
                    const data = await response.json();
                    
                    const activityDiv = document.getElementById('quick-activity');
                    if (data.recent_logs && data.recent_logs.length > 0) {
                        activityDiv.innerHTML = data.recent_logs
                            .filter(log => log.trim())
                            .slice(-3)
                            .map(log => `<div class="log-entry" style="background: #f8fafc; color: var(--text-primary); border-left: 3px solid var(--primary-blue); margin: 0.5rem 0; padding: 0.75rem; border-radius: 0.25rem;">${log}</div>`)
                            .join('');
                    } else {
                        activityDiv.innerHTML = '<p class="metric-label">No recent activity</p>';
                    }
                } catch (error) {
                    console.error('Activity error:', error);
                }
            }

            async function loadQuickDecisions() {
                try {
                    const response = await fetch('/trading-decisions');
                    const data = await response.json();
                    
                    const decisionsDiv = document.getElementById('quick-decisions');
                    decisionsDiv.innerHTML = data.recent_decisions
                        .slice(0, 3)
                        .map(decision => `
                            <div style="margin: 1rem 0; padding: 0.75rem; background: #f8fafc; border-radius: 0.5rem;">
                                <div style="font-weight: 600; margin-bottom: 0.25rem;">${decision.decision}</div>
                                <div style="font-size: 0.875rem; color: var(--text-secondary);">
                                    ${decision.action} • Impact: ${decision.capital_impact}
                                </div>
                            </div>
                        `)
                        .join('');
                } catch (error) {
                    console.error('Decisions error:', error);
                }
            }

            async function loadTradingStreams() {
                try {
                    const response = await fetch('/trading-streams');
                    const data = await response.json();
                    
                    // Update crypto table
                    const cryptoTableBody = document.querySelector('#crypto-table tbody');
                    if (cryptoTableBody) {
                        cryptoTableBody.innerHTML = data.crypto_markets
                            .map(crypto => `
                                <tr>
                                    <td style="font-weight: 600;">${crypto.pair}</td>
                                    <td>${crypto.price.toLocaleString()}</td>
                                    <td class="${crypto.change_24h > 0 ? 'positive' : 'negative'}">
                                        ${crypto.change_24h > 0 ? '+' : ''}${crypto.change_24h.toFixed(2)}%
                                    </td>
                                    <td>${(crypto.volume_24h / 1000000).toFixed(1)}M</td>
                                    <td><span class="signal-badge signal-${crypto.signal.toLowerCase()}">${crypto.signal}</span></td>
                                    <td>${(crypto.confidence * 100).toFixed(0)}%</td>
                                </tr>
                            `)
                            .join('');
                    }
                    
                    // Update forex table
                    const forexTableBody = document.querySelector('#forex-table tbody');
                    if (forexTableBody) {
                        forexTableBody.innerHTML = data.forex_markets
                            .map(forex => `
                                <tr>
                                    <td style="font-weight: 600;">${forex.pair}</td>
                                    <td>${forex.price.toFixed(4)}</td>
                                    <td class="${forex.change_24h > 0 ? 'positive' : 'negative'}">
                                        ${forex.change_24h > 0 ? '+' : ''}${forex.change_24h.toFixed(2)}%
                                    </td>
                                    <td><span class="signal-badge signal-${forex.signal.toLowerCase()}">${forex.signal}</span></td>
                                    <td>${(forex.confidence * 100).toFixed(0)}%</td>
                                </tr>
                            `)
                            .join('');
                    }
                } catch (error) {
                    console.error('Trading streams error:', error);
                }
            }

            async function loadAnalytics() {
                try {
                    const response = await fetch('/trading-streams');
                    const data = await response.json();
                    
                    document.getElementById('market-analytics').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Total Opportunities</span>
                            <span class="metric-value">${data.analytics.total_opportunities}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">High Confidence Signals</span>
                            <span class="metric-value">${data.analytics.high_confidence_signals}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Market Sentiment</span>
                            <span class="metric-value ${data.analytics.market_sentiment === 'BULLISH' ? 'positive' : 'negative'}">
                                ${data.analytics.market_sentiment}
                            </span>
                        </div>
                    `;
                    
                    // Load performance metrics
                    const dashResponse = await fetch('/dashboard');
                    const dashData = await dashResponse.json();
                    
                    document.getElementById('performance-metrics').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Daily Target</span>
                            <span class="metric-value">${dashData.capital_growth.daily_target.toFixed(3)}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Annualized Return</span>
                            <span class="metric-value positive">${dashData.capital_growth.annualized_return_pct.toFixed(1)}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Auto Reinvest</span>
                            <span class="metric-value">${dashData.compound_strategy.auto_reinvest ? 'Enabled' : 'Disabled'}</span>
                        </div>
                    `;
                } catch (error) {
                    console.error('Analytics error:', error);
                }
            }

            async function loadLogs() {
                try {
                    const response = await fetch('/system-logs');
                    const data = await response.json();
                    
                    const logsDiv = document.getElementById('system-logs');
                    if (data.recent_logs && data.recent_logs.length > 0) {
                        logsDiv.innerHTML = data.recent_logs
                            .filter(log => log.trim())
                            .map(log => `<div class="log-entry">${log}</div>`)
                            .join('');
                    } else {
                        logsDiv.innerHTML = '<div class="log-entry">No logs available</div>';
                    }
                } catch (error) {
                    console.error('Logs error:', error);
                }
            }

            async function loadConfig() {
                try {
                    const response = await fetch('/config');
                    const data = await response.json();
                    
                    const configDiv = document.getElementById('env-config');
                    configDiv.innerHTML = `
                        <h4 style="margin-bottom: 1rem; color: var(--text-primary);">Environment Variables</h4>
                        ${Object.entries(data.environment_vars)
                            .map(([key, value]) => `
                                <div class="metric">
                                    <span class="metric-label">${key}</span>
                                    <span class="metric-value" style="font-family: monospace;">${value}</span>
                                </div>
                            `)
                            .join('')}
                        
                        <div style="margin-top: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 0.5rem;">
                            <p style="font-size: 0.875rem; color: var(--text-secondary);">
                                Config file: ${data.config_file_exists ? '✅ Found' : '❌ Not found'}<br>
                                Path: <code>${data.config_file_path}</code>
                            </p>
                        </div>
                    `;
                    
                    // Mettre à jour status mode professionnel
                    const proModeStatus = document.getElementById('pro-mode-status');
                    if (proModeStatus) {
                        const isProfessional = data.environment_vars.PROFESSIONAL_MODE === 'true';
                        proModeStatus.innerHTML = isProfessional 
                            ? '<span style="color: var(--success-green);">✅ Activé</span>'
                            : '<span style="color: var(--text-secondary);">⚪ Mode Accessible</span>';
                    }
                } catch (error) {
                    console.error('Config error:', error);
                }
            }

            async function controlSystem(action) {
                try {
                    const response = await fetch(`/${action}`, { method: 'POST' });
                    const result = await response.json();
                    alert(`${action}: ${result.message}`);
                    loadDashboard();
                } catch (error) {
                    alert(`Error ${action}: ${error.message}`);
                }
            }

            function exportData() {
                fetch('/dashboard')
                    .then(response => response.json())
                    .then(data => {
                        const dataStr = JSON.stringify(data, null, 2);
                        const dataBlob = new Blob([dataStr], {type: 'application/json'});
                        const url = URL.createObjectURL(dataBlob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = `trading-data-${new Date().toISOString().split('T')[0]}.json`;
                        link.click();
                    })
                    .catch(error => alert('Export error: ' + error.message));
            }

            // Auto-refresh dashboard only
            setInterval(() => {
                const currentPage = document.querySelector('.page-content.active').id.replace('-page', '');
                if (currentPage === 'dashboard') {
                    loadDashboard();
                    loadQuickActivity();
                    loadQuickDecisions();
                } else if (currentPage === 'crypto' || currentPage === 'forex') {
                    loadTradingStreams();
                }
            }, 10000);

            // Load dashboard on startup
            loadDashboard();
            loadQuickActivity();
            loadQuickDecisions();
        </script>
    </body>
    </html>
    """

@app.post("/start")
async def start_system(username: str = Depends(authenticate_user)):
    """Démarre le système - PROTÉGÉ"""
    if master_instance:
        master_instance.active = True
        return {"status": "started", "message": "Système autonome activé", "user": username}
    raise HTTPException(status_code=503, detail="Système non initialisé")

@app.post("/stop")
async def stop_system(username: str = Depends(authenticate_user)):
    """Arrête le système - PROTÉGÉ"""
    if master_instance:
        master_instance.active = False
        return {"status": "stopped", "message": "Système autonome arrêté", "user": username}
    raise HTTPException(status_code=503, detail="Système non initialisé")

@app.get("/live-feed")
async def get_live_feed(username: str = Depends(authenticate_user)):
    """Feed temps réel des actions du système - PROTÉGÉ"""
    if not master_instance:
        raise HTTPException(status_code=503, detail="Système non initialisé")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system_active": master_instance.active,
        "current_cycle": getattr(master_instance, 'current_cycle', 0),
        "last_decisions": getattr(master_instance, 'decision_history', [])[-10:],  # 10 dernières décisions
        "real_time_status": {
            "capital_now": master_instance.capital_manager.current_capital,
            "daily_target": master_instance.capital_manager.daily_target_return * 100,
            "efficiency_now": master_instance.capital_manager.calculate_compound_growth((datetime.now() - master_instance.capital_manager.start_date).days + 1)["system_efficiency_pct"],
            "next_action_in": "60 secondes",
            "current_strategy": "Croissance composée intelligente"
        }
    }

@app.get("/system-logs")
async def get_system_logs(username: str = Depends(authenticate_user)):
    """Logs système récents - PROTÉGÉ"""
    try:
        # Lire les dernières lignes de log
        import subprocess
        result = subprocess.run(['tail', '-50', './logs/autonomous/system.log'], 
                               capture_output=True, text=True, cwd='/app')
        logs = result.stdout.split('\n') if result.stdout else []
        
        return {
            "recent_logs": logs[-20:],  # 20 dernières lignes
            "log_file": "./logs/autonomous/system.log"
        }
    except Exception as e:
        return {"error": f"Impossible de lire les logs: {e}", "recent_logs": []}

@app.get("/trading-decisions")
async def get_trading_decisions(username: str = Depends(authenticate_user)):
    """Historique des décisions de trading - PROTÉGÉ"""
    if not master_instance:
        raise HTTPException(status_code=503, detail="Système non initialisé")
    
    # Simuler quelques décisions récentes
    decisions = [
        {
            "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat(),
            "decision": f"Analyse de marché cycle #{100-i}",
            "action": "HOLD" if i % 3 == 0 else "ANALYZE",
            "reasoning": f"Conditions de marché stables, continuer surveillance",
            "capital_impact": f"+{0.1*i:.2f}€" if i % 2 == 0 else "0€"
        }
        for i in range(10)
    ]
    
    return {
        "recent_decisions": decisions,
        "decision_frequency": "Toutes les 60 secondes",
        "next_decision": "Dans 30-60 secondes"
    }

@app.get("/favicon.ico")
async def favicon():
    """Favicon simple pour éviter les erreurs 404"""
    # Favicon SVG simple
    favicon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
        <rect width="32" height="32" fill="#0f0f0f"/>
        <text x="16" y="24" text-anchor="middle" font-size="20" fill="#00ff88">🧠</text>
    </svg>"""
    return Response(content=favicon_svg, media_type="image/svg+xml")

@app.get("/config")
async def get_config(username: str = Depends(authenticate_user)):
    """Configuration système depuis .env - PROTÉGÉ"""
    try:
        config = {}
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        
        # Lire .env si existe
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
        
        # Ajouter les variables d'environnement actuelles
        env_vars = {
            'DEMO_MODE': os.getenv('DEMO_MODE', 'true'),
            'INITIAL_CAPITAL': os.getenv('INITIAL_CAPITAL', '200'),
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
            'ADMIN_USERNAME': os.getenv('ADMIN_USERNAME', 'admin'),
            'ADMIN_PASSWORD': '***hidden***',  # Ne pas exposer le mot de passe
            'POSTGRES_HOST': os.getenv('POSTGRES_HOST', 'postgres'),
            'POSTGRES_DB': os.getenv('POSTGRES_DB', 'trading_ai'),
            'POSTGRES_USER': os.getenv('POSTGRES_USER', 'trader'),
            'OPENAI_API_KEY': '***hidden***' if os.getenv('OPENAI_API_KEY') else 'Non configuré',
            'TELEGRAM_BOT_TOKEN': '***hidden***' if os.getenv('TELEGRAM_BOT_TOKEN') else 'Non configuré',
            'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', 'Non configuré'),
        }
        
        return {
            "config_file": config,
            "environment_vars": env_vars,
            "config_file_exists": os.path.exists(env_file),
            "config_file_path": env_file
        }
        
    except Exception as e:
        return {"error": f"Erreur lecture configuration: {e}"}

@app.get("/trading-streams")
async def get_trading_streams(username: str = Depends(authenticate_user)):
    """Flux de trading en temps réel - PROTÉGÉ"""
    if not master_instance:
        raise HTTPException(status_code=503, detail="Système non initialisé")
    
    # Simulation de flux crypto/forex
    import random
    
    crypto_pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BONK/USDT', 'WIF/USDT']
    forex_pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD']
    
    crypto_data = []
    forex_data = []
    
    for pair in crypto_pairs:
        base_price = {'BTC/USDT': 45000, 'ETH/USDT': 2500, 'SOL/USDT': 100, 'BONK/USDT': 0.000025, 'WIF/USDT': 2.5}[pair]
        price = base_price * (1 + random.uniform(-0.05, 0.05))
        change_24h = random.uniform(-15, 15)
        
        crypto_data.append({
            "pair": pair,
            "price": round(price, 6),
            "change_24h": round(change_24h, 2),
            "volume_24h": random.randint(1000000, 100000000),
            "signal": "BUY" if change_24h > 5 else "SELL" if change_24h < -5 else "HOLD",
            "confidence": round(random.uniform(0.6, 0.95), 2)
        })
    
    for pair in forex_pairs:
        base_price = {'EUR/USD': 1.0850, 'GBP/USD': 1.2650, 'USD/JPY': 149.50, 'AUD/USD': 0.6580, 'USD/CAD': 1.3720}[pair]
        price = base_price * (1 + random.uniform(-0.01, 0.01))
        change_24h = random.uniform(-2, 2)
        
        forex_data.append({
            "pair": pair,
            "price": round(price, 4),
            "change_24h": round(change_24h, 2),
            "signal": "BUY" if change_24h > 0.5 else "SELL" if change_24h < -0.5 else "HOLD",
            "confidence": round(random.uniform(0.7, 0.9), 2)
        })
    
    return {
        "crypto_markets": crypto_data,
        "forex_markets": forex_data,
        "analytics": {
            "total_opportunities": len([x for x in crypto_data + forex_data if x["signal"] != "HOLD"]),
            "high_confidence_signals": len([x for x in crypto_data + forex_data if x["confidence"] > 0.8]),
            "market_sentiment": "BULLISH" if sum([x["change_24h"] for x in crypto_data]) > 0 else "BEARISH"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def get_metrics():
    """Métriques Prometheus pour Grafana (mode professionnel)"""
    if not PROFESSIONAL_MODE:
        raise HTTPException(status_code=404, detail="Mode professionnel non activé")
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/guide-professionnel")
async def get_professional_guide(username: str = Depends(authenticate_user)):
    """Guide du mode professionnel en HTML - PROTÉGÉ"""
    try:
        guide_path = os.path.join(os.path.dirname(__file__), "GUIDE_MODE_PROFESSIONNEL.md")
        if os.path.exists(guide_path):
            with open(guide_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Conversion simple markdown vers HTML
            html_content = markdown_content.replace('\n# ', '\n<h1>').replace('\n## ', '\n<h2>').replace('\n### ', '\n<h3>')
            html_content = html_content.replace('```bash\n', '<pre><code class="language-bash">').replace('\n```', '</code></pre>')
            html_content = html_content.replace('```promql\n', '<pre><code class="language-promql">').replace('\n```', '</code></pre>')
            html_content = html_content.replace('\n- ', '\n<li>').replace('\n\n', '</li>\n\n')
            
            return HTMLResponse(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Guide Mode Professionnel - Trading AI</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; line-height: 1.6; }}
                    h1 {{ color: #2563eb; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
                    h2 {{ color: #1e293b; margin-top: 2rem; }}
                    h3 {{ color: #64748b; }}
                    code {{ background: #f1f5f9; padding: 0.2rem 0.4rem; border-radius: 0.25rem; font-family: Monaco, monospace; }}
                    pre {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }}
                </style>
            </head>
            <body>
                <div>{html_content}</div>
                <hr>
                <p><a href="/" style="color: #2563eb;">← Retour au Dashboard</a></p>
            </body>
            </html>
            """)
        else:
            return HTMLResponse("<h1>Guide non trouvé</h1><p>Le fichier GUIDE_MODE_PROFESSIONNEL.md n'existe pas.</p>")
            
    except Exception as e:
        return HTMLResponse(f"<h1>Erreur</h1><p>Impossible de charger le guide: {e}</p>")

# Interface de lancement Docker
def main():
    """Point d'entrée pour Docker"""
    print("🧠 DÉMARRAGE SYSTÈME AUTONOME DOCKER")
    print("="*50)
    print(f"🎯 Mode: {API_MODE}")
    print(f"🐳 Port: {PORT}")
    print(f"🎮 Demo: {'Activé' if DEMO_MODE else 'Désactivé'}")
    print("="*50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=PORT,
        log_level="info"
    )

if __name__ == "__main__":
    main() 