#!/usr/bin/env python3
"""
📊 PROGRESSION MONITOR - SYSTÈME D'ALERTES INTELLIGENT
Surveille la progression et génère des alertes pour les moments clés d'investissement
"""

import asyncio
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
import asyncio
import threading

console = Console()

class ProgressionPhase(Enum):
    """Phases de progression"""
    SIMULATION_PURE = "simulation_pure"
    APIS_PREMIUM = "apis_premium" 
    MICRO_TRADING = "micro_trading"
    TRADING_CONSERVATEUR = "trading_conservateur"
    SCALING_PRO = "scaling_pro"

class AlertLevel(Enum):
    """Niveaux d'alerte"""
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    CRITICAL = "critical"
    MILESTONE = "milestone"

@dataclass
class ProgressionMetric:
    """Métrique de progression"""
    name: str
    current_value: float
    target_value: float
    unit: str
    phase_required: ProgressionPhase
    description: str
    
    @property
    def completion_rate(self) -> float:
        """Taux de completion"""
        if self.target_value == 0:
            return 1.0
        return min(1.0, self.current_value / self.target_value)
    
    @property
    def is_achieved(self) -> bool:
        """Objectif atteint"""
        return self.current_value >= self.target_value

@dataclass
class Alert:
    """Alerte système"""
    level: AlertLevel
    title: str
    message: str
    action_required: str
    timestamp: datetime
    phase: ProgressionPhase
    
class ProgressionMonitor:
    """Moniteur de progression intelligent"""
    
    def __init__(self):
        self.current_phase = ProgressionPhase.SIMULATION_PURE
        self.start_time = datetime.now()
        self.alerts: List[Alert] = []
        self.performance_history: List[Dict] = []
        self.live_display = None
        
        # Métriques de progression
        self.metrics = {
            # Phase 1: Simulation Pure
            "simulation_decisions": ProgressionMetric(
                "Décisions simulation", 0, 50, "décisions",
                ProgressionPhase.SIMULATION_PURE,
                "Minimum 50 décisions pour valider l'algorithme"
            ),
            "simulation_win_rate": ProgressionMetric(
                "Win rate simulation", 0.0, 0.8, "%",
                ProgressionPhase.SIMULATION_PURE,
                "80% de réussite pour passer aux APIs premium"
            ),
            "simulation_max_drawdown": ProgressionMetric(
                "Max drawdown", 0.0, 0.1, "%",
                ProgressionPhase.SIMULATION_PURE,
                "Maximum 10% de perte en simulation"
            ),
            "simulation_duration": ProgressionMetric(
                "Durée simulation", 0, 14, "jours",
                ProgressionPhase.SIMULATION_PURE,
                "Minimum 2 semaines de test"
            ),
            
            # Phase 2: APIs Premium
            "premium_performance": ProgressionMetric(
                "Performance APIs premium", 0.0, 0.85, "%",
                ProgressionPhase.APIS_PREMIUM,
                "85% de réussite avec données premium"
            ),
            "api_stability": ProgressionMetric(
                "Stabilité APIs", 0.0, 0.95, "%",
                ProgressionPhase.APIS_PREMIUM,
                "95% de disponibilité des APIs"
            ),
            
            # Phase 3: Micro Trading
            "micro_trades": ProgressionMetric(
                "Micro-trades", 0, 30, "trades",
                ProgressionPhase.MICRO_TRADING,
                "Minimum 30 micro-trades profitables"
            ),
            "micro_profit": ProgressionMetric(
                "Profit micro-trading", 0.0, 1.0, "%",
                ProgressionPhase.MICRO_TRADING,
                "Performance positive sur 1 mois"
            ),
            
            # Phase 4: Trading Conservateur
            "conservative_months": ProgressionMetric(
                "Mois profitables", 0, 3, "mois",
                ProgressionPhase.TRADING_CONSERVATEUR,
                "3 mois consécutifs profitables"
            ),
            "sharpe_ratio": ProgressionMetric(
                "Sharpe Ratio", 0.0, 1.5, "ratio",
                ProgressionPhase.TRADING_CONSERVATEUR,
                "Ratio risque/rendement optimal"
            )
        }
        
        # Seuils d'alerte
        self.phase_requirements = {
            ProgressionPhase.APIS_PREMIUM: {
                "budget_required": 200,  # €/mois
                "metrics": ["simulation_decisions", "simulation_win_rate", "simulation_duration"]
            },
            ProgressionPhase.MICRO_TRADING: {
                "budget_required": 300,  # € capital
                "metrics": ["premium_performance", "api_stability"]
            },
            ProgressionPhase.TRADING_CONSERVATEUR: {
                "budget_required": 3000,  # € capital
                "metrics": ["micro_trades", "micro_profit"]
            },
            ProgressionPhase.SCALING_PRO: {
                "budget_required": 10000,  # € capital
                "metrics": ["conservative_months", "sharpe_ratio"]
            }
        }
        
    def update_metric(self, metric_name: str, value: float):
        """Met à jour une métrique"""
        if metric_name in self.metrics:
            old_value = self.metrics[metric_name].current_value
            self.metrics[metric_name].current_value = value
            
            # Vérifier si nouveau milestone
            if not self.metrics[metric_name].was_achieved and self.metrics[metric_name].is_achieved:
                self._trigger_milestone_alert(metric_name)
                
        # Mettre à jour durée simulation
        if metric_name == "simulation_duration":
            runtime = datetime.now() - self.start_time
            self.metrics["simulation_duration"].current_value = runtime.days
            
    def _trigger_milestone_alert(self, metric_name: str):
        """Déclenche une alerte de milestone"""
        metric = self.metrics[metric_name]
        
        alert = Alert(
            level=AlertLevel.MILESTONE,
            title=f"🎉 MILESTONE ATTEINT!",
            message=f"{metric.name}: {metric.current_value}{metric.unit} (objectif: {metric.target_value}{metric.unit})",
            action_required="Vérifier si prêt pour phase suivante",
            timestamp=datetime.now(),
            phase=self.current_phase
        )
        
        self.alerts.append(alert)
        self._check_phase_readiness()
        
    def _check_phase_readiness(self):
        """Vérifie si prêt pour phase suivante"""
        next_phases = {
            ProgressionPhase.SIMULATION_PURE: ProgressionPhase.APIS_PREMIUM,
            ProgressionPhase.APIS_PREMIUM: ProgressionPhase.MICRO_TRADING,
            ProgressionPhase.MICRO_TRADING: ProgressionPhase.TRADING_CONSERVATEUR,
            ProgressionPhase.TRADING_CONSERVATEUR: ProgressionPhase.SCALING_PRO
        }
        
        if self.current_phase in next_phases:
            next_phase = next_phases[self.current_phase]
            requirements = self.phase_requirements.get(next_phase, {})
            required_metrics = requirements.get("metrics", [])
            
            # Vérifier toutes les métriques requises
            all_ready = all(
                self.metrics[metric].is_achieved 
                for metric in required_metrics 
                if metric in self.metrics
            )
            
            if all_ready:
                budget = requirements.get("budget_required", 0)
                self._trigger_phase_ready_alert(next_phase, budget)
                
    def _trigger_phase_ready_alert(self, next_phase: ProgressionPhase, budget: int):
        """Alerte de phase prête"""
        phase_names = {
            ProgressionPhase.APIS_PREMIUM: "APIs Premium",
            ProgressionPhase.MICRO_TRADING: "Micro-Trading", 
            ProgressionPhase.TRADING_CONSERVATEUR: "Trading Conservateur",
            ProgressionPhase.SCALING_PRO: "Scaling Professionnel"
        }
        
        phase_name = phase_names.get(next_phase, str(next_phase))
        
        alert = Alert(
            level=AlertLevel.SUCCESS,
            title=f"🚀 PRÊT POUR {phase_name.upper()}!",
            message=f"Toutes les conditions sont remplies pour passer à la phase {phase_name}",
            action_required=f"Budget requis: {budget}€ - Décision d'investissement nécessaire",
            timestamp=datetime.now(),
            phase=next_phase
        )
        
        self.alerts.append(alert)
        
    def generate_progression_chart(self) -> str:
        """Génère un graphique de progression"""
        # Créer données pour graphique
        phases = ["Simulation", "APIs Premium", "Micro-Trading", "Conservateur", "Pro"]
        phase_values = [0, 1, 2, 3, 4]
        
        current_phase_idx = list(ProgressionPhase).index(self.current_phase)
        progress_values = [1 if i < current_phase_idx else 0.5 if i == current_phase_idx else 0 
                          for i in range(len(phases))]
        
        # Graphique ASCII simple
        chart = "\n📊 PROGRESSION DES PHASES:\n"
        chart += "="*50 + "\n"
        
        for i, (phase, progress) in enumerate(zip(phases, progress_values)):
            bar_length = 20
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            status = "✅" if progress == 1 else "🔄" if progress > 0 else "⏳"
            chart += f"{status} {phase:15} |{bar}| {progress*100:3.0f}%\n"
            
        return chart
        
    def generate_metrics_table(self) -> Table:
        """Génère tableau des métriques"""
        table = Table(title="📊 Métriques de Progression")
        table.add_column("Métrique", style="cyan")
        table.add_column("Actuel", style="magenta") 
        table.add_column("Objectif", style="green")
        table.add_column("Progression", style="yellow")
        table.add_column("Status", style="bold")
        
        for metric in self.metrics.values():
            if metric.phase_required == self.current_phase or metric.is_achieved:
                completion = metric.completion_rate * 100
                status = "✅" if metric.is_achieved else "🔄" if completion > 50 else "⏳"
                
                table.add_row(
                    metric.name,
                    f"{metric.current_value:.1f}{metric.unit}",
                    f"{metric.target_value:.1f}{metric.unit}",
                    f"{completion:.1f}%",
                    status
                )
                
        return table
        
    def generate_alerts_panel(self) -> Panel:
        """Génère panneau d'alertes"""
        if not self.alerts:
            return Panel("Aucune alerte", title="🔔 Alertes")
            
        # Dernières 5 alertes
        recent_alerts = sorted(self.alerts, key=lambda x: x.timestamp, reverse=True)[:5]
        
        alert_text = ""
        for alert in recent_alerts:
            emoji = {
                AlertLevel.INFO: "ℹ️",
                AlertLevel.WARNING: "⚠️", 
                AlertLevel.SUCCESS: "✅",
                AlertLevel.CRITICAL: "🚨",
                AlertLevel.MILESTONE: "🎉"
            }.get(alert.level, "📢")
            
            time_str = alert.timestamp.strftime("%H:%M")
            alert_text += f"{emoji} {time_str} - {alert.title}\n"
            alert_text += f"   {alert.message}\n"
            if alert.action_required:
                alert_text += f"   ⚡ Action: {alert.action_required}\n"
            alert_text += "\n"
            
        return Panel(alert_text, title="🔔 Alertes Récentes")
        
    def create_live_dashboard(self) -> Layout:
        """Crée dashboard temps réel"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=5)
        )
        
        layout["main"].split_row(
            Layout(name="metrics"),
            Layout(name="alerts")
        )
        
        # Header
        runtime = datetime.now() - self.start_time
        phase_name = self.current_phase.value.replace("_", " ").title()
        
        header_text = Text()
        header_text.append("🚀 TRADING AI - MONITEUR DE PROGRESSION\n", style="bold magenta")
        header_text.append(f"Phase actuelle: {phase_name} | Runtime: {runtime}", style="cyan")
        
        layout["header"].update(Panel(header_text, title="Dashboard"))
        
        # Métriques
        layout["metrics"].update(self.generate_metrics_table())
        
        # Alertes
        layout["alerts"].update(self.generate_alerts_panel())
        
        # Footer - Progression
        layout["footer"].update(Panel(self.generate_progression_chart(), title="📈 Progression"))
        
        return layout
        
    async def start_monitoring(self):
        """Démarre le monitoring temps réel"""
        console.print("🔄 Démarrage du moniteur de progression...", style="cyan")
        
        try:
            with Live(self.create_live_dashboard(), refresh_per_second=1) as live:
                self.live_display = live
                
                while True:
                    # Simuler mise à jour des métriques
                    await self._simulate_progression()
                    
                    # Mettre à jour dashboard
                    live.update(self.create_live_dashboard())
                    
                    await asyncio.sleep(5)  # Update every 5 seconds
                    
        except KeyboardInterrupt:
            console.print("\n🛑 Monitoring arrêté", style="red")
            
    async def _simulate_progression(self):
        """Simule la progression (remplacer par vraies données)"""
        # Simulation de données en temps réel
        import random
        
        # Augmenter graduellement les métriques
        if self.current_phase == ProgressionPhase.SIMULATION_PURE:
            # Simulation decisions
            current_decisions = self.metrics["simulation_decisions"].current_value
            if current_decisions < 50:
                self.update_metric("simulation_decisions", current_decisions + random.uniform(0.1, 0.5))
                
            # Win rate simulation
            target_win_rate = 0.75 + random.uniform(-0.05, 0.1)
            current_wr = self.metrics["simulation_win_rate"].current_value
            new_wr = current_wr + (target_win_rate - current_wr) * 0.01
            self.update_metric("simulation_win_rate", min(new_wr, 1.0))
            
            # Durée simulation 
            runtime = datetime.now() - self.start_time
            self.update_metric("simulation_duration", runtime.days + runtime.seconds / 86400)
            
        # Déclencher alertes aléatoires pour demo
        if random.random() < 0.05:  # 5% chance
            self._trigger_random_alert()
            
    def _trigger_random_alert(self):
        """Déclenche alerte aléatoire pour demo"""
        import random
        
        sample_alerts = [
            ("Performance excellente!", "Win rate dépasse 75% - APIs premium recommandées", AlertLevel.SUCCESS),
            ("Système stable", "Aucun crash détecté depuis 24h", AlertLevel.INFO),
            ("Objectif proche", "Plus que 5 décisions pour atteindre l'objectif", AlertLevel.WARNING),
            ("Nouvelle opportunité", "Session Forex optimale détectée", AlertLevel.INFO)
        ]
        
        title, message, level = random.choice(sample_alerts)
        
        alert = Alert(
            level=level,
            title=title,
            message=message,
            action_required="Continuer la surveillance",
            timestamp=datetime.now(),
            phase=self.current_phase
        )
        
        self.alerts.append(alert)
        
    def generate_investment_decision_report(self) -> Dict:
        """Génère rapport de décision d'investissement"""
        next_phase_map = {
            ProgressionPhase.SIMULATION_PURE: (ProgressionPhase.APIS_PREMIUM, 200),
            ProgressionPhase.APIS_PREMIUM: (ProgressionPhase.MICRO_TRADING, 300),
            ProgressionPhase.MICRO_TRADING: (ProgressionPhase.TRADING_CONSERVATEUR, 3000),
            ProgressionPhase.TRADING_CONSERVATEUR: (ProgressionPhase.SCALING_PRO, 10000)
        }
        
        if self.current_phase in next_phase_map:
            next_phase, budget = next_phase_map[self.current_phase]
            requirements = self.phase_requirements.get(next_phase, {})
            required_metrics = requirements.get("metrics", [])
            
            metrics_status = {}
            for metric_name in required_metrics:
                if metric_name in self.metrics:
                    metric = self.metrics[metric_name]
                    metrics_status[metric_name] = {
                        "achieved": metric.is_achieved,
                        "completion": metric.completion_rate,
                        "current": metric.current_value,
                        "target": metric.target_value
                    }
                    
            all_ready = all(status["achieved"] for status in metrics_status.values())
            
            return {
                "current_phase": self.current_phase.value,
                "next_phase": next_phase.value,
                "budget_required": budget,
                "ready_to_invest": all_ready,
                "metrics_status": metrics_status,
                "completion_rate": sum(s["completion"] for s in metrics_status.values()) / len(metrics_status) if metrics_status else 0,
                "recommendation": self._get_investment_recommendation(all_ready, budget),
                "timeline": self._estimate_timeline(metrics_status),
                "risk_assessment": self._assess_investment_risk()
            }
        
        return {"status": "max_phase_reached"}
        
    def _get_investment_recommendation(self, ready: bool, budget: int) -> str:
        """Recommandation d'investissement"""
        if ready:
            return f"🟢 RECOMMANDATION: Prêt à investir {budget}€ pour la phase suivante"
        else:
            return f"🟡 RECOMMANDATION: Continue la phase actuelle, pas encore prêt pour {budget}€"
            
    def _estimate_timeline(self, metrics_status: Dict) -> str:
        """Estime timeline"""
        if not metrics_status:
            return "Timeline indéterminée"
            
        avg_completion = sum(s["completion"] for s in metrics_status.values()) / len(metrics_status)
        
        if avg_completion > 0.9:
            return "Prêt maintenant"
        elif avg_completion > 0.7:
            return "1-2 semaines"
        elif avg_completion > 0.5:
            return "2-4 semaines"
        else:
            return "1-2 mois"
            
    def _assess_investment_risk(self) -> str:
        """Évalue risque investissement"""
        win_rate = self.metrics.get("simulation_win_rate", type('obj', (object,), {'current_value': 0})).current_value
        
        if win_rate > 0.85:
            return "🟢 RISQUE FAIBLE - Performance excellente"
        elif win_rate > 0.75:
            return "🟡 RISQUE MODÉRÉ - Performance bonne"
        elif win_rate > 0.6:
            return "🟠 RISQUE ÉLEVÉ - Performance moyenne"
        else:
            return "🔴 RISQUE TRÈS ÉLEVÉ - Performance insuffisante"

# Interface de notification
class NotificationSystem:
    """Système de notifications intelligentes"""
    
    def __init__(self, monitor: ProgressionMonitor):
        self.monitor = monitor
        self.notification_history = []
        
    async def send_investment_alert(self, phase: ProgressionPhase, budget: int):
        """Envoie alerte d'investissement"""
        phase_names = {
            ProgressionPhase.APIS_PREMIUM: "APIs Premium",
            ProgressionPhase.MICRO_TRADING: "Micro-Trading",
            ProgressionPhase.TRADING_CONSERVATEUR: "Trading Conservateur",  
            ProgressionPhase.SCALING_PRO: "Scaling Professionnel"
        }
        
        phase_name = phase_names.get(phase, str(phase))
        
        console.print(Panel(
            f"🚨 ALERTE INVESTISSEMENT!\n\n"
            f"Phase: {phase_name}\n"
            f"Budget requis: {budget}€\n"
            f"Toutes les conditions sont remplies!\n\n"
            f"Action requise: Décision d'investissement",
            title="💰 Prêt à Investir",
            border_style="green"
        ))
        
        # Log notification
        self.notification_history.append({
            "type": "investment_alert",
            "phase": phase.value,
            "budget": budget,
            "timestamp": datetime.now()
        })

# Fonction principale de lancement
async def main():
    """Démarre le système de monitoring"""
    monitor = ProgressionMonitor()
    notifications = NotificationSystem(monitor)
    
    console.print("🚀 Démarrage du système de monitoring intelligent...", style="bold green")
    
    try:
        await monitor.start_monitoring()
    except KeyboardInterrupt:
        console.print("\n📋 Génération du rapport final...", style="cyan")
        
        # Rapport final
        report = monitor.generate_investment_decision_report()
        console.print(Panel(
            json.dumps(report, indent=2, default=str),
            title="📊 Rapport de Décision d'Investissement"
        ))

if __name__ == "__main__":
    asyncio.run(main()) 