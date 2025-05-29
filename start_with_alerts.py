#!/usr/bin/env python3
"""
🚨 SYSTÈME D'ALERTES INTELLIGENT - LANCEMENT SIMPLIFIÉ
Surveille ta progression et t'alerte quand tu peux investir
"""

import asyncio
import os
import sys
import json
from datetime import datetime, timedelta
import time

class SimpleProgressionMonitor:
    """Moniteur de progression simplifié"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.alerts = []
        
        # Métriques clés
        self.metrics = {
            "decisions": 0,
            "win_rate": 0.0,
            "duration_days": 0,
            "max_drawdown": 0.0,
            "stability_score": 0.0
        }
        
        # Seuils pour chaque phase
        self.investment_thresholds = {
            "apis_premium": {
                "budget": 200,  # €/mois
                "conditions": {
                    "decisions": 50,
                    "win_rate": 0.80,
                    "duration_days": 14,
                    "max_drawdown": 0.10
                }
            },
            "micro_trading": {
                "budget": 300,  # € capital
                "conditions": {
                    "decisions": 100,
                    "win_rate": 0.85,
                    "duration_days": 28,
                    "stability_score": 0.95
                }
            },
            "serious_trading": {
                "budget": 3000,  # € capital  
                "conditions": {
                    "decisions": 200,
                    "win_rate": 0.75,
                    "duration_days": 60,
                    "micro_profit": 1.0
                }
            }
        }
        
        self.notifications_sent = set()
        
    def update_metrics(self, **kwargs):
        """Met à jour les métriques"""
        for key, value in kwargs.items():
            if key in self.metrics:
                old_value = self.metrics[key]
                self.metrics[key] = value
                
                # Vérifier milestone
                if self._is_significant_improvement(key, old_value, value):
                    self._send_milestone_alert(key, value)
                    
        # Mettre à jour durée
        runtime = datetime.now() - self.start_time
        self.metrics["duration_days"] = runtime.days + runtime.seconds / 86400
        
        # Vérifier préparation phases
        self._check_investment_readiness()
        
    def _is_significant_improvement(self, metric: str, old_value: float, new_value: float) -> bool:
        """Vérifie si amélioration significative"""
        improvements = {
            "win_rate": 0.05,  # +5%
            "decisions": 10,   # +10 décisions
            "stability_score": 0.1  # +10%
        }
        
        threshold = improvements.get(metric, 0)
        return new_value - old_value >= threshold
        
    def _send_milestone_alert(self, metric: str, value: float):
        """Envoie alerte milestone"""
        messages = {
            "win_rate": f"🎉 Win rate atteint {value:.1%}! Excellente progression!",
            "decisions": f"📊 {value} décisions complétées! L'algorithme se stabilise.",
            "stability_score": f"🔧 Stabilité système: {value:.1%}! Système fiable."
        }
        
        message = messages.get(metric, f"Amélioration {metric}: {value}")
        
        self._display_alert("🎯 MILESTONE", message, "INFO")
        
    def _check_investment_readiness(self):
        """Vérifie préparation investissement"""
        for phase, config in self.investment_thresholds.items():
            if phase in self.notifications_sent:
                continue
                
            conditions = config["conditions"]
            budget = config["budget"]
            
            # Vérifier toutes conditions
            ready = all(
                self.metrics.get(metric, 0) >= threshold
                for metric, threshold in conditions.items()
                if metric in self.metrics
            )
            
            if ready:
                self._send_investment_alert(phase, budget)
                self.notifications_sent.add(phase)
                
    def _send_investment_alert(self, phase: str, budget: int):
        """Envoie alerte d'investissement majeure"""
        phase_names = {
            "apis_premium": "APIs Premium",
            "micro_trading": "Micro-Trading", 
            "serious_trading": "Trading Sérieux"
        }
        
        phase_name = phase_names.get(phase, phase)
        
        print("\n" + "="*60)
        print("🚨 ALERTE INVESTISSEMENT MAJEURE! 🚨")
        print("="*60)
        print(f"🎯 PHASE PRÊTE: {phase_name}")
        print(f"💰 BUDGET REQUIS: {budget}€")
        print(f"📊 TOUTES LES CONDITIONS SONT REMPLIES!")
        print()
        
        # Détails conditions
        conditions = self.investment_thresholds[phase]["conditions"]
        print("✅ CONDITIONS REMPLIES:")
        for metric, threshold in conditions.items():
            current = self.metrics.get(metric, 0)
            if metric == "win_rate":
                print(f"   • {metric}: {current:.1%} (requis: {threshold:.1%})")
            elif metric == "max_drawdown":
                print(f"   • {metric}: {current:.1%} (max: {threshold:.1%})")
            else:
                print(f"   • {metric}: {current:.1f} (requis: {threshold})")
                
        print()
        print("🎯 ACTION REQUISE: DÉCISION D'INVESTISSEMENT")
        print("⚠️  Tu peux maintenant considérer d'investir en toute sécurité!")
        print("="*60)
        
        # Log alert
        self.alerts.append({
            "type": "INVESTMENT_READY",
            "phase": phase,
            "budget": budget,
            "timestamp": datetime.now(),
            "conditions_met": dict(conditions)
        })
        
    def _display_alert(self, title: str, message: str, level: str):
        """Affiche une alerte"""
        emoji = {"INFO": "ℹ️", "WARNING": "⚠️", "SUCCESS": "✅", "CRITICAL": "🚨"}
        
        print(f"\n{emoji.get(level, '📢')} {title}")
        print(f"   {message}")
        print(f"   Heure: {datetime.now().strftime('%H:%M:%S')}")
        
    def display_current_status(self):
        """Affiche statut actuel"""
        runtime = datetime.now() - self.start_time
        
        print("\n" + "="*50)
        print("📊 STATUT DE PROGRESSION ACTUEL")
        print("="*50)
        print(f"⏱️  Runtime: {runtime}")
        print(f"🎯 Décisions: {self.metrics['decisions']}")
        print(f"📈 Win Rate: {self.metrics['win_rate']:.1%}")
        print(f"📉 Max Drawdown: {self.metrics['max_drawdown']:.1%}")
        print(f"🔧 Stabilité: {self.metrics['stability_score']:.1%}")
        
        # Progression vers prochaine phase
        print("\n🎯 PROGRESSION VERS INVESTISSEMENT:")
        
        for phase, config in self.investment_thresholds.items():
            if phase in self.notifications_sent:
                print(f"✅ {phase}: PRÊT!")
                continue
                
            conditions = config["conditions"]
            budget = config["budget"]
            
            print(f"\n💰 {phase.upper()} ({budget}€):")
            
            ready_conditions = 0
            total_conditions = len(conditions)
            
            for metric, threshold in conditions.items():
                current = self.metrics.get(metric, 0)
                is_ready = current >= threshold
                ready_conditions += is_ready
                
                status = "✅" if is_ready else "❌"
                if metric == "win_rate":
                    print(f"   {status} {metric}: {current:.1%} / {threshold:.1%}")
                elif metric == "max_drawdown":
                    print(f"   {status} {metric}: {current:.1%} (max {threshold:.1%})")
                else:
                    print(f"   {status} {metric}: {current:.1f} / {threshold}")
                    
            completion = ready_conditions / total_conditions * 100
            print(f"   📊 Completion: {completion:.1f}%")
            
            if completion >= 100:
                print(f"   🚨 PRÊT À INVESTIR {budget}€!")
            elif completion >= 75:
                print(f"   🟡 Presque prêt! Plus que {total_conditions - ready_conditions} condition(s)")
            else:
                print(f"   🔴 Encore {total_conditions - ready_conditions} condition(s) à remplir")
                
        print("="*50)
        
    def generate_investment_decision(self) -> dict:
        """Génère une décision d'investissement claire"""
        recommendations = []
        next_budget = 0
        
        # Trouver prochaine phase prête
        for phase, config in self.investment_thresholds.items():
            if phase in self.notifications_sent:
                recommendations.append(f"✅ {phase}: Déjà validé")
                continue
                
            conditions = config["conditions"]
            budget = config["budget"]
            
            ready = all(
                self.metrics.get(metric, 0) >= threshold
                for metric, threshold in conditions.items()
                if metric in self.metrics
            )
            
            if ready and next_budget == 0:
                next_budget = budget
                recommendations.append(f"🚀 PRÊT: {phase} - {budget}€")
                break
            else:
                missing = []
                for metric, threshold in conditions.items():
                    current = self.metrics.get(metric, 0)
                    if current < threshold:
                        missing.append(f"{metric}: {current:.1f}/{threshold}")
                        
                recommendations.append(f"⏳ {phase}: Manque {', '.join(missing)}")
                if next_budget == 0:
                    next_budget = budget
                break
                
        return {
            "ready_to_invest": next_budget > 0 and any("PRÊT" in r for r in recommendations),
            "next_budget": next_budget,
            "recommendations": recommendations,
            "current_performance": {
                "win_rate": f"{self.metrics['win_rate']:.1%}",
                "decisions": self.metrics['decisions'],
                "runtime_days": f"{self.metrics['duration_days']:.1f}"
            },
            "risk_level": self._assess_risk()
        }
        
    def _assess_risk(self) -> str:
        """Évalue le niveau de risque"""
        win_rate = self.metrics['win_rate']
        decisions = self.metrics['decisions']
        
        if win_rate >= 0.85 and decisions >= 100:
            return "🟢 TRÈS FAIBLE - Performance excellente et stable"
        elif win_rate >= 0.75 and decisions >= 50:
            return "🟡 FAIBLE - Performance bonne"
        elif win_rate >= 0.6 and decisions >= 30:
            return "🟠 MODÉRÉ - Performance acceptable"
        else:
            return "🔴 ÉLEVÉ - Performance insuffisante pour investir"

# Simulation avec alertes intelligentes
async def run_simulation_with_alerts():
    """Lance simulation avec système d'alertes"""
    monitor = SimpleProgressionMonitor()
    
    print("🚀 DÉMARRAGE SIMULATION AVEC ALERTES INTELLIGENTES")
    print("🔔 Tu seras alerté automatiquement des moments clés d'investissement")
    print("⏳ Démarrage...")
    
    try:
        cycle = 0
        while True:
            cycle += 1
            
            # Simuler progression réaliste
            import random
            
            # Augmentation graduelle des métriques
            decisions_increment = random.uniform(0.2, 1.0)
            current_decisions = monitor.metrics["decisions"] + decisions_increment
            
            # Win rate qui s'améliore avec le temps mais avec variabilité
            target_win_rate = 0.78 + random.uniform(-0.1, 0.15)
            current_wr = monitor.metrics["win_rate"]
            new_wr = current_wr + (target_win_rate - current_wr) * 0.02
            
            # Stabilité qui augmente
            stability_increment = random.uniform(0.005, 0.02)
            new_stability = min(1.0, monitor.metrics["stability_score"] + stability_increment)
            
            # Drawdown variable
            new_drawdown = random.uniform(0.02, 0.12)
            
            # Mettre à jour
            monitor.update_metrics(
                decisions=current_decisions,
                win_rate=min(new_wr, 1.0),
                stability_score=new_stability,
                max_drawdown=new_drawdown
            )
            
            # Afficher statut périodiquement
            if cycle % 10 == 0:  # Toutes les 10 itérations
                monitor.display_current_status()
                
                # Générer décision d'investissement
                decision = monitor.generate_investment_decision()
                
                print(f"\n💡 RECOMMANDATION ACTUELLE:")
                print(f"   💰 Prêt à investir: {'OUI' if decision['ready_to_invest'] else 'NON'}")
                print(f"   💶 Prochain budget: {decision['next_budget']}€")
                print(f"   ⚖️  Niveau de risque: {decision['risk_level']}")
                
            # Pause entre cycles
            await asyncio.sleep(3)  # 3 secondes entre updates
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation arrêtée")
        
        # Rapport final
        print("\n📋 RAPPORT FINAL:")
        decision = monitor.generate_investment_decision()
        
        print(json.dumps(decision, indent=2, ensure_ascii=False))
        
        # Sauvegarder alertes
        with open(f"alerts_history_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "w") as f:
            json.dump(monitor.alerts, f, indent=2, default=str, ensure_ascii=False)
            
        print(f"\n💾 Historique des alertes sauvegardé")
        print(f"📊 Total alertes: {len(monitor.alerts)}")

def main():
    """Point d'entrée principal"""
    print("🔔 SYSTÈME D'ALERTES INTELLIGENT POUR TRADING AI")
    print("=" * 60)
    print("🎯 Objectif: Te dire EXACTEMENT quand tu peux investir")
    print("💡 Le système t'alertera automatiquement à chaque milestone")
    print("🚨 Alertes spéciales pour les moments d'investissement")
    print("=" * 60)
    
    response = input("\n🚀 Démarrer avec alertes intelligentes ? (y/N): ")
    if response.lower() != 'y':
        print("👋 Annulé")
        return
        
    try:
        asyncio.run(run_simulation_with_alerts())
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main() 