#!/usr/bin/env python3
"""
🤖 SYSTÈME TRADING 100% AUTOMATIQUE - ZERO MINDSET
Élimine complètement les émotions et décisions humaines du trading
Tu n'as plus besoin de "mindset" - tout est automatisé !
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# Imports de nos systèmes existants
from src.infrastructure.rpc_optimizer import AutoTradingRPCManager
from src.monitoring.progression_monitor import ProgressionMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingEmotionBlocker:
    """Bloque toutes les émotions de trading"""
    
    BLOCKED_EMOTIONS = [
        "fear", "greed", "fomo", "panic", "euphoria", 
        "regret", "hope", "anxiety", "excitement", "doubt"
    ]
    
    @staticmethod
    def process_decision(decision_data: Dict) -> Dict:
        """Traite une décision en bloquant toute émotion"""
        # Supprimer toutes les considérations émotionnelles
        clean_decision = {
            "action": decision_data.get("action"),
            "amount": decision_data.get("amount"),
            "reasoning": "Décision automatique basée sur données",
            "confidence": decision_data.get("confidence", 1.0),
            "risk_level": decision_data.get("risk_level"),
            "emotional_state": "BLOCKED",
            "human_override": False
        }
        
        return clean_decision
        
    @staticmethod
    def validate_no_emotion(decision: Dict) -> bool:
        """Valide qu'aucune émotion n'interfère"""
        decision_text = json.dumps(decision).lower()
        
        for emotion in TradingEmotionBlocker.BLOCKED_EMOTIONS:
            if emotion in decision_text:
                logger.warning(f"🚫 Émotion détectée et bloquée: {emotion}")
                return False
                
        return True

class AutoInvestmentDecisionEngine:
    """Moteur de décision d'investissement automatique"""
    
    def __init__(self):
        self.progression_monitor = ProgressionMonitor()
        self.rpc_manager = AutoTradingRPCManager()
        self.emotion_blocker = TradingEmotionBlocker()
        
        # Règles d'investissement automatique strictes
        self.investment_rules = {
            "apis_premium": {
                "trigger_conditions": {
                    "min_decisions": 50,
                    "min_win_rate": 0.80,
                    "min_duration_days": 14,
                    "max_drawdown": 0.10,
                    "min_stability": 0.90
                },
                "budget": 200,  # €/mois
                "auto_execute": True,
                "confidence_threshold": 0.95
            },
            "micro_trading": {
                "trigger_conditions": {
                    "min_decisions": 100,
                    "min_win_rate": 0.85,
                    "min_duration_days": 28,
                    "max_drawdown": 0.08,
                    "api_stability": 0.95
                },
                "budget": 300,  # € capital
                "auto_execute": True,
                "confidence_threshold": 0.98
            },
            "serious_trading": {
                "trigger_conditions": {
                    "min_decisions": 200,
                    "min_win_rate": 0.75,
                    "min_duration_days": 60,
                    "consecutive_profitable_months": 3,
                    "sharpe_ratio": 1.5
                },
                "budget": 3000,  # € capital
                "auto_execute": False,  # Requires explicit confirmation
                "confidence_threshold": 0.99
            }
        }
        
    async def auto_evaluate_investment_readiness(self) -> Dict:
        """Évalue automatiquement la préparation pour investir"""
        logger.info("🤖 Évaluation automatique de préparation investissement...")
        
        # Obtenir métriques actuelles
        current_metrics = await self._get_current_performance_metrics()
        
        # Évaluer chaque phase d'investissement
        evaluations = {}
        for phase, rules in self.investment_rules.items():
            evaluation = self._evaluate_phase_readiness(phase, current_metrics, rules)
            evaluations[phase] = evaluation
            
        # Décision automatique finale
        final_decision = self._make_automatic_investment_decision(evaluations)
        
        return {
            "evaluation_timestamp": datetime.now(),
            "current_metrics": current_metrics,
            "phase_evaluations": evaluations,
            "automatic_decision": final_decision,
            "emotional_interference": "BLOCKED",
            "human_decision_required": final_decision.get("requires_human_approval", False)
        }
        
    def _evaluate_phase_readiness(self, phase: str, metrics: Dict, rules: Dict) -> Dict:
        """Évalue la préparation pour une phase spécifique"""
        conditions = rules["trigger_conditions"]
        met_conditions = []
        failed_conditions = []
        
        # Vérifier chaque condition
        for condition, threshold in conditions.items():
            current_value = metrics.get(condition, 0)
            
            if condition.startswith("min_"):
                condition_met = current_value >= threshold
            elif condition.startswith("max_"):
                condition_met = current_value <= threshold
            else:
                condition_met = current_value >= threshold
                
            if condition_met:
                met_conditions.append({
                    "condition": condition,
                    "required": threshold,
                    "current": current_value,
                    "status": "MET"
                })
            else:
                failed_conditions.append({
                    "condition": condition,
                    "required": threshold,
                    "current": current_value,
                    "status": "FAILED",
                    "gap": threshold - current_value if condition.startswith("min_") else current_value - threshold
                })
                
        all_conditions_met = len(failed_conditions) == 0
        confidence_score = len(met_conditions) / (len(met_conditions) + len(failed_conditions))
        
        return {
            "phase": phase,
            "ready": all_conditions_met,
            "confidence": confidence_score,
            "budget_required": rules["budget"],
            "auto_execute": rules["auto_execute"],
            "met_conditions": met_conditions,
            "failed_conditions": failed_conditions,
            "recommendation": self._generate_phase_recommendation(phase, all_conditions_met, rules["budget"])
        }
        
    def _generate_phase_recommendation(self, phase: str, ready: bool, budget: int) -> str:
        """Génère une recommandation automatique"""
        if ready:
            return f"🚀 AUTOMATIQUE: Prêt à investir {budget}€ pour {phase}"
        else:
            return f"⏳ AUTOMATIQUE: Continue la simulation pour {phase}"
            
    def _make_automatic_investment_decision(self, evaluations: Dict) -> Dict:
        """Prend une décision automatique d'investissement"""
        # Trouver la prochaine phase prête
        ready_phases = []
        for phase, eval_data in evaluations.items():
            if eval_data["ready"] and eval_data["confidence"] >= self.investment_rules[phase]["confidence_threshold"]:
                ready_phases.append((phase, eval_data))
                
        if ready_phases:
            # Prendre la première phase prête
            next_phase, phase_data = ready_phases[0]
            
            decision = {
                "decision": "INVEST",
                "phase": next_phase,
                "budget": phase_data["budget_required"],
                "confidence": phase_data["confidence"],
                "auto_execute": phase_data["auto_execute"],
                "requires_human_approval": not phase_data["auto_execute"],
                "reasoning": f"Toutes conditions remplies pour {next_phase}",
                "risk_assessment": self._assess_automatic_risk(phase_data),
                "recommended_action": "Procéder à l'investissement automatique" if phase_data["auto_execute"] else "Demander confirmation humaine"
            }
        else:
            decision = {
                "decision": "WAIT",
                "phase": None,
                "budget": 0,
                "confidence": 0.0,
                "auto_execute": False,
                "requires_human_approval": False,
                "reasoning": "Aucune phase prête pour investissement",
                "recommended_action": "Continuer la simulation"
            }
            
        # Nettoyer la décision de toute émotion
        clean_decision = self.emotion_blocker.process_decision(decision)
        
        return clean_decision
        
    def _assess_automatic_risk(self, phase_data: Dict) -> str:
        """Évalue automatiquement le risque"""
        confidence = phase_data["confidence"]
        
        if confidence >= 0.99:
            return "🟢 TRÈS FAIBLE - Toutes métriques excellentes"
        elif confidence >= 0.95:
            return "🟡 FAIBLE - Métriques très bonnes"
        elif confidence >= 0.90:
            return "🟠 MODÉRÉ - Métriques acceptables"
        else:
            return "🔴 ÉLEVÉ - Métriques insuffisantes"
            
    async def _get_current_performance_metrics(self) -> Dict:
        """Obtient les métriques de performance actuelles"""
        # Simuler récupération des vraies métriques
        # Dans le vrai système, ceci se connecterait aux vraies données
        
        runtime = datetime.now() - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        return {
            "min_decisions": 75,  # Simulé
            "min_win_rate": 0.82,  # 82%
            "min_duration_days": 18,
            "max_drawdown": 0.06,  # 6%
            "min_stability": 0.94,  # 94%
            "api_stability": 0.97,  # 97%
            "consecutive_profitable_months": 2,
            "sharpe_ratio": 1.2,
            "last_updated": datetime.now()
        }

class ZeroMindsetTradingSystem:
    """Système de trading qui élimine complètement le besoin de mindset"""
    
    def __init__(self):
        self.investment_engine = AutoInvestmentDecisionEngine()
        self.rpc_manager = AutoTradingRPCManager()
        self.emotion_blocker = TradingEmotionBlocker()
        self.active = False
        
    async def initialize_anti_mindset_system(self) -> Dict:
        """Initialise le système anti-mindset"""
        logger.info("🤖 Initialisation du système ZERO MINDSET...")
        
        # 1. Optimiser automatiquement les RPC
        rpc_optimization = await self.rpc_manager.setup_for_zero_mindset_trading()
        
        # 2. Évaluer préparation investissement
        investment_readiness = await self.investment_engine.auto_evaluate_investment_readiness()
        
        # 3. Activer le système
        self.active = True
        
        system_status = {
            "system": "ZERO MINDSET TRADING",
            "status": "ACTIVE",
            "mindset_required": False,
            "emotional_decisions": "BLOCKED",
            "human_intervention": "MINIMIZED",
            "automation_level": "100%",
            "rpc_optimization": rpc_optimization,
            "investment_readiness": investment_readiness,
            "advantages": [
                "🚫 Aucune émotion ne peut interférer",
                "🤖 Décisions purement basées sur données",
                "⚡ Exécution automatique instantanée",
                "🛡️ Protection contre FOMO/Panic/Greed",
                "📊 Optimisation RPC automatique",
                "💰 Alertes d'investissement intelligentes",
                "🔄 Auto-ajustement continu"
            ]
        }
        
        return system_status
        
    async def run_automated_trading_loop(self):
        """Boucle de trading automatique sans intervention humaine"""
        logger.info("🔄 Démarrage boucle trading automatique...")
        
        if not self.active:
            await self.initialize_anti_mindset_system()
            
        cycle = 0
        while self.active:
            try:
                cycle += 1
                logger.info(f"🔄 Cycle automatique #{cycle}")
                
                # 1. Évaluer situation automatiquement
                evaluation = await self.investment_engine.auto_evaluate_investment_readiness()
                
                # 2. Prendre décision automatique
                decision = evaluation["automatic_decision"]
                
                # 3. Valider absence d'émotion
                if not self.emotion_blocker.validate_no_emotion(decision):
                    logger.warning("🚫 Décision rejetée - émotion détectée")
                    continue
                    
                # 4. Exécuter si approprié
                if decision["decision"] == "INVEST" and decision["auto_execute"]:
                    await self._execute_automatic_investment(decision)
                elif decision["decision"] == "INVEST" and decision["requires_human_approval"]:
                    await self._request_human_approval(decision)
                    
                # 5. Générer rapport de cycle
                await self._generate_cycle_report(cycle, evaluation, decision)
                
                # 6. Attendre avant prochain cycle
                await asyncio.sleep(30)  # 30 secondes entre cycles
                
            except Exception as e:
                logger.error(f"❌ Erreur dans cycle automatique: {e}")
                await asyncio.sleep(60)  # Wait longer on error
                
    async def _execute_automatic_investment(self, decision: Dict):
        """Exécute automatiquement un investissement"""
        logger.info(f"💰 Exécution automatique investissement: {decision['budget']}€ pour {decision['phase']}")
        
        # Dans un vrai système, ceci déclencherait l'achat d'APIs premium, etc.
        execution_result = {
            "executed": True,
            "phase": decision["phase"],
            "budget": decision["budget"],
            "timestamp": datetime.now(),
            "method": "automatic",
            "confidence": decision["confidence"]
        }
        
        logger.info(f"✅ Investissement automatique exécuté: {execution_result}")
        return execution_result
        
    async def _request_human_approval(self, decision: Dict):
        """Demande approbation humaine pour gros investissements"""
        logger.warning(f"👤 Approbation humaine requise pour {decision['budget']}€")
        
        print("\n" + "="*60)
        print("🚨 APPROBATION HUMAINE REQUISE")
        print("="*60)
        print(f"💰 Budget: {decision['budget']}€")
        print(f"📊 Phase: {decision['phase']}")
        print(f"🎯 Confiance: {decision['confidence']:.1%}")
        print(f"⚖️ Risque: {decision['risk_assessment']}")
        print(f"💡 Recommandation: {decision['recommended_action']}")
        print("="*60)
        
        # Attendre approbation (dans un vrai système, ceci serait via UI/notification)
        print("⏳ En attente d'approbation humaine...")
        
    async def _generate_cycle_report(self, cycle: int, evaluation: Dict, decision: Dict):
        """Génère un rapport de cycle"""
        metrics = evaluation["current_metrics"]
        
        if cycle % 10 == 0:  # Rapport détaillé tous les 10 cycles
            print(f"\n📊 RAPPORT AUTOMATIQUE - CYCLE #{cycle}")
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
            print(f"🎯 Décisions: {metrics['min_decisions']}")
            print(f"📈 Win Rate: {metrics['min_win_rate']:.1%}")
            print(f"⚖️ Risque: {decision.get('risk_assessment', 'N/A')}")
            print(f"🤖 Décision: {decision['decision']}")
            print(f"💰 Budget prêt: {decision.get('budget', 0)}€")
            
    def emergency_stop(self):
        """Arrêt d'urgence du système"""
        logger.warning("🛑 ARRÊT D'URGENCE ACTIVÉ")
        self.active = False
        
    def get_system_status(self) -> Dict:
        """Obtient le statut du système"""
        return {
            "active": self.active,
            "mindset_eliminated": True,
            "emotional_trading": "BLOCKED",
            "automation_level": "100%",
            "human_intervention_required": False,
            "last_check": datetime.now()
        }

# Interface de lancement simple
async def launch_zero_mindset_system():
    """Lance le système de trading sans mindset"""
    print("🤖 LANCEMENT SYSTÈME TRADING ZERO MINDSET")
    print("="*50)
    print("✅ Plus besoin de mindset - tout est automatisé!")
    print("🚫 Émotions bloquées automatiquement")
    print("💡 Décisions basées uniquement sur données")
    print("⚡ Exécution automatique optimale")
    print("="*50)
    
    system = ZeroMindsetTradingSystem()
    
    # Initialisation
    status = await system.initialize_anti_mindset_system()
    print("\n🚀 INITIALISATION TERMINÉE:")
    print(json.dumps(status, indent=2, default=str))
    
    # Lancer la boucle automatique
    try:
        await system.run_automated_trading_loop()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
        system.emergency_stop()
        
        final_status = system.get_system_status()
        print("\n📊 STATUT FINAL:")
        print(json.dumps(final_status, indent=2, default=str))

# Point d'entrée principal
def main():
    """Point d'entrée"""
    print("🎯 Choix du mode:")
    print("1. 🤖 Système Zero Mindset (recommandé)")
    print("2. 📊 Test évaluation seule")
    print("3. 🔧 Test optimisation RPC")
    
    choice = input("\nTon choix (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(launch_zero_mindset_system())
    elif choice == "2":
        async def test_evaluation():
            engine = AutoInvestmentDecisionEngine()
            result = await engine.auto_evaluate_investment_readiness()
            print(json.dumps(result, indent=2, default=str))
        asyncio.run(test_evaluation())
    elif choice == "3":
        from src.infrastructure.rpc_optimizer import test_rpc_optimization
        asyncio.run(test_rpc_optimization())
    else:
        print("❌ Choix invalide")

if __name__ == "__main__":
    main() 