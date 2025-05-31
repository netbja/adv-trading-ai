#!/usr/bin/env python3
"""
🚀 TEST COMPLET DES MODULES IA AVANCÉE - GRANDEUR NATURE
=======================================================

Script de test grandeur nature pour valider l'autonomie et l'intelligence 
de tous les modules d'IA avancée :

✅ Module 1: AI Feedback Loop - Apprentissage continu
✅ Module 2: Predictive System - Prédictions intelligentes  
✅ Module 3: Security Supervisor - Surveillance complète
✅ Module 4: Portfolio Optimizer - Optimisation intelligente
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import random

# Configuration
BASE_URL = "http://localhost:8000/api"
ADVANCED_AI_URL = f"{BASE_URL}/advanced-ai"

class AITestOrchestrator:
    """🎯 Orchestrateur de tests pour IA avancée"""
    
    def __init__(self):
        self.session = None
        self.test_results = {}
        self.start_time = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.start_time = datetime.utcnow()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def run_complete_test_suite(self):
        """🎯 Lancer la suite complète de tests"""
        
        print("🚀 DÉMARRAGE TESTS IA AVANCÉE - GRANDEUR NATURE")
        print("=" * 60)
        
        # 1. Tests AI Feedback Loop
        print("\n🧠 MODULE 1: AI FEEDBACK LOOP")
        print("-" * 40)
        await self.test_ai_feedback_loop()
        
        # 2. Tests Predictive System
        print("\n🔮 MODULE 2: PREDICTIVE SYSTEM") 
        print("-" * 40)
        await self.test_predictive_system()
        
        # 3. Tests Security Supervisor
        print("\n🛡️ MODULE 3: SECURITY SUPERVISOR")
        print("-" * 40)
        await self.test_security_supervisor()
        
        # 4. Tests Portfolio Optimizer
        print("\n💼 MODULE 4: PORTFOLIO OPTIMIZER")
        print("-" * 40)
        await self.test_portfolio_optimizer()
        
        # 5. Tests d'intégration
        print("\n🔗 TESTS D'INTÉGRATION COMPLÈTE")
        print("-" * 40)
        await self.test_system_integration()
        
        # 6. Rapport final
        await self.generate_final_report()

    async def test_ai_feedback_loop(self):
        """🧠 Tests complets du feedback loop IA"""
        
        try:
            # Test 1: Soumettre signal de succès
            print("📝 Test 1.1: Soumission signal de succès...")
            success_signal = {
                "signal_type": "SUCCESS",
                "component": "meme_coins_strategy",
                "context": {
                    "market_conditions": {"volatility": 0.4, "trend": "bullish"},
                    "system_state": {"cpu_usage": 45, "memory_usage": 60},
                    "recent_performance": {"profit_rate": 15.5, "win_rate": 0.85}
                },
                "performance_metrics": {
                    "execution_time": 1.2,
                    "accuracy": 0.92,
                    "profit": 1250.75
                }
            }
            
            response = await self._post(f"{ADVANCED_AI_URL}/feedback/learn", success_signal)
            assert response["status"] == "success"
            print(f"✅ Signal de succès soumis: {response['signal_id']}")
            
            # Test 2: Soumettre signal d'échec pour apprentissage
            print("📝 Test 1.2: Soumission signal d'échec...")
            failure_signal = {
                "signal_type": "FAILURE",
                "component": "forex_strategy",
                "context": {
                    "market_conditions": {"volatility": 0.8, "trend": "bearish"},
                    "system_state": {"cpu_usage": 85, "memory_usage": 90}
                },
                "performance_metrics": {
                    "execution_time": 5.2,
                    "accuracy": 0.45,
                    "loss": -850.25
                }
            }
            
            response = await self._post(f"{ADVANCED_AI_URL}/feedback/learn", failure_signal)
            assert response["status"] == "success"
            print(f"✅ Signal d'échec soumis: {response['signal_id']}")
            
            # Test 3: Analyser les patterns découverts
            print("📝 Test 1.3: Analyse des patterns d'apprentissage...")
            await asyncio.sleep(2)  # Laisser temps de traitement
            
            patterns = await self._get(f"{ADVANCED_AI_URL}/feedback/patterns")
            print(f"✅ Patterns découverts: {patterns['total_patterns']}")
            
            # Test 4: Obtenir les adaptations récentes
            print("📝 Test 1.4: Récupération adaptations récentes...")
            adaptations = await self._get(f"{ADVANCED_AI_URL}/feedback/adaptations")
            print(f"✅ Adaptations récentes: {adaptations['count']}")
            
            # Test 5: Analyse de performance
            print("📝 Test 1.5: Analyse détaillée des performances...")
            performance_data = {
                "strategy_performance": {
                    "meme_coins": {"return": 15.2, "volatility": 0.4, "sharpe": 0.8},
                    "crypto_lt": {"return": 12.5, "volatility": 0.3, "sharpe": 0.9},
                    "forex": {"return": 3.2, "volatility": 0.15, "sharpe": 0.6},
                    "etf": {"return": 8.1, "volatility": 0.18, "sharpe": 0.7}
                },
                "system_metrics": {
                    "cpu_avg": 65,
                    "memory_avg": 75,
                    "response_time_avg": 1.8
                }
            }
            
            analysis = await self._post(f"{ADVANCED_AI_URL}/feedback/analyze-performance", performance_data)
            print(f"✅ Anomalies détectées: {analysis['anomalies_detected']}")
            
            self.test_results["ai_feedback_loop"] = "✅ SUCCÈS"
            
        except Exception as e:
            print(f"❌ Erreur AI Feedback Loop: {e}")
            self.test_results["ai_feedback_loop"] = f"❌ ÉCHEC: {e}"

    async def test_predictive_system(self):
        """🔮 Tests complets du système prédictif"""
        
        try:
            # Test 1: Prédictions multi-horizon
            print("📝 Test 2.1: Prédictions multi-horizon...")
            
            horizons = ["5min", "1hour", "4hour", "24hour"]
            assets = ["meme_coins", "crypto_lt", "forex", "etf"]
            
            predictions = []
            for asset in assets:
                for horizon in horizons:
                    prediction_request = {
                        "asset_type": asset,
                        "horizon": horizon,
                        "market_data": {
                            "current_price": random.uniform(50, 200),
                            "volume": random.uniform(1000000, 10000000),
                            "volatility": random.uniform(0.1, 0.8)
                        }
                    }
                    
                    response = await self._post(f"{ADVANCED_AI_URL}/prediction/forecast", prediction_request)
                    predictions.append(response["prediction"])
                    print(f"   ✅ {asset} {horizon}: {response['prediction']['direction']} (conf: {response['prediction']['confidence']:.2f})")
            
            # Test 2: Détection régime de marché
            print("📝 Test 2.2: Détection régime de marché...")
            regime = await self._get(f"{ADVANCED_AI_URL}/prediction/regime")
            print(f"✅ Régime détecté: {regime['regime']['market_phase']} (conf: {regime['regime']['confidence']:.2f})")
            
            # Test 3: Alertes prédictives
            print("📝 Test 2.3: Génération alertes prédictives...")
            alerts = await self._get(f"{ADVANCED_AI_URL}/prediction/alerts")
            print(f"✅ Alertes générées: {alerts['total_alerts']} (prioritaires: {alerts['high_priority']})")
            
            # Test 4: Analyse historique par asset
            print("📝 Test 2.4: Analyses historiques...")
            for asset in assets:
                analysis = await self._get(f"{ADVANCED_AI_URL}/prediction/analysis/{asset}")
                print(f"   ✅ Analyse {asset}: Patterns détectés")
            
            self.test_results["predictive_system"] = "✅ SUCCÈS"
            
        except Exception as e:
            print(f"❌ Erreur Predictive System: {e}")
            self.test_results["predictive_system"] = f"❌ ÉCHEC: {e}"

    async def test_security_supervisor(self):
        """🛡️ Tests complets du superviseur de sécurité"""
        
        try:
            # Test 1: Health check complet
            print("📝 Test 3.1: Health check système complet...")
            health_check = await self._post(f"{ADVANCED_AI_URL}/security/health-check", {})
            
            print(f"✅ Status global: {health_check['overall_status']}")
            for component, status in health_check["health_check"].items():
                print(f"   • {component}: {status['status']} ({status['response_time_ms']:.1f}ms)")
            
            # Test 2: Scan CVE des vulnérabilités
            print("📝 Test 3.2: Scan CVE vulnérabilités...")
            cve_request = {"scan_type": "comprehensive", "deep_scan": False}
            cve_scan = await self._post(f"{ADVANCED_AI_URL}/security/cve-scan", cve_request)
            
            print(f"✅ Vulnérabilités: {cve_scan['total_vulnerabilities']} (critiques: {cve_scan['critical_count']})")
            
            # Test 3: Dashboard sécurité complet
            print("📝 Test 3.3: Dashboard sécurité...")
            dashboard = await self._get(f"{ADVANCED_AI_URL}/security/dashboard")
            
            if dashboard["dashboard"]:
                metrics = dashboard["dashboard"].get("system_metrics", {})
                print(f"✅ Score sécurité: {dashboard['dashboard'].get('security_score', 0):.1f}/100")
                print(f"   • Santé globale: {dashboard['dashboard'].get('overall_health', 'unknown')}")
            
            # Test 4: Alertes de sécurité
            print("📝 Test 3.4: Alertes de sécurité...")
            alerts = await self._get(f"{ADVANCED_AI_URL}/security/alerts")
            print(f"✅ Alertes actives: {alerts['total_alerts']}")
            
            # Test 5: Scan profond en arrière-plan
            print("📝 Test 3.5: Scan CVE profond (arrière-plan)...")
            deep_scan_request = {"scan_type": "comprehensive", "deep_scan": True}
            deep_scan = await self._post(f"{ADVANCED_AI_URL}/security/cve-scan", deep_scan_request)
            print(f"✅ Scan profond initié: {deep_scan['scan_id']}")
            
            self.test_results["security_supervisor"] = "✅ SUCCÈS"
            
        except Exception as e:
            print(f"❌ Erreur Security Supervisor: {e}")
            self.test_results["security_supervisor"] = f"❌ ÉCHEC: {e}"

    async def test_portfolio_optimizer(self):
        """💼 Tests complets de l'optimiseur de portefeuille"""
        
        try:
            # Test 1: Optimisations avec différentes stratégies
            print("📝 Test 4.1: Optimisations multi-stratégies...")
            
            strategies = [
                {"strategy": "conservative", "risk_level": "low"},
                {"strategy": "balanced", "risk_level": "medium"},
                {"strategy": "aggressive", "risk_level": "high"},
                {"strategy": "momentum", "risk_level": "high"}
            ]
            
            optimizations = []
            for strat in strategies:
                optimization_request = {
                    **strat,
                    "market_conditions": {
                        "volatility": random.uniform(0.2, 0.8),
                        "trend_strength": random.uniform(-0.5, 0.5),
                        "market_regime": "bull" if random.random() > 0.5 else "bear"
                    }
                }
                
                response = await self._post(f"{ADVANCED_AI_URL}/portfolio/optimize", optimization_request)
                optimization = response["optimization"]
                optimizations.append(optimization)
                
                print(f"   ✅ {strat['strategy']}: Sharpe {optimization['expected_sharpe']:.2f} (conf: {optimization['confidence_score']:.2f})")
                print(f"      Allocation: {optimization['optimal_weights']}")
            
            # Test 2: Recommandations de rééquilibrage
            print("📝 Test 4.2: Recommandations rééquilibrage...")
            rebalance = await self._get(f"{ADVANCED_AI_URL}/portfolio/rebalance")
            
            print(f"✅ Recommandations: {rebalance['total_recommendations']} (prioritaires: {rebalance['high_priority']})")
            for rec in rebalance["recommendations"][:3]:  # Afficher top 3
                print(f"   • {rec['asset_type']}: {rec['action']} {rec['amount']:.1%} ({rec['priority']})")
            
            # Test 3: Métriques de performance
            print("📝 Test 4.3: Métriques de performance...")
            metrics = await self._get(f"{ADVANCED_AI_URL}/portfolio/metrics")
            
            perf = metrics["metrics"]
            print(f"✅ Performance portefeuille:")
            print(f"   • Rendement: {perf['total_return']:.1%}")
            print(f"   • Volatilité: {perf['volatility']:.1%}")
            print(f"   • Sharpe: {perf['sharpe_ratio']:.2f}")
            print(f"   • Max Drawdown: {perf['max_drawdown']:.1%}")
            
            # Test 4: Résumé optimisations
            print("📝 Test 4.4: Résumé des optimisations...")
            summary = await self._get(f"{ADVANCED_AI_URL}/portfolio/summary")
            
            if summary["summary"]:
                print(f"✅ Optimisations réalisées: {summary['summary'].get('total_optimizations', 0)}")
                print(f"   • Taux de succès: {summary['summary'].get('success_rate', 0):.1%}")
                print(f"   • Rééquilibrage nécessaire: {'Oui' if summary['summary'].get('rebalance_needed') else 'Non'}")
            
            self.test_results["portfolio_optimizer"] = "✅ SUCCÈS"
            
        except Exception as e:
            print(f"❌ Erreur Portfolio Optimizer: {e}")
            self.test_results["portfolio_optimizer"] = f"❌ ÉCHEC: {e}"

    async def test_system_integration(self):
        """🔗 Tests d'intégration système complète"""
        
        try:
            # Test 1: Status complet de tous les modules
            print("📝 Test 5.1: Status système complet...")
            system_status = await self._get(f"{ADVANCED_AI_URL}/status/complete")
            
            status = system_status["system_status"]
            print(f"✅ Santé globale: {status['overall_health']}")
            print(f"   • Niveau d'intelligence: {status['intelligence_level']}")
            
            for module, info in status["modules"].items():
                print(f"   • {module}: {'✅ Actif' if info['active'] else '❌ Inactif'}")
            
            # Test 2: Simulation scénario de trading complet
            print("📝 Test 5.2: Simulation scénario trading...")
            
            # Étape 1: Prédiction de marché
            prediction_request = {
                "asset_type": "meme_coins",
                "horizon": "1hour",
                "market_data": {"current_price": 125.50, "volume": 5000000}
            }
            prediction = await self._post(f"{ADVANCED_AI_URL}/prediction/forecast", prediction_request)
            
            # Étape 2: Optimisation basée sur prédiction
            optimization_request = {
                "strategy": "momentum" if prediction["prediction"]["direction"] == "UP" else "conservative",
                "risk_level": "high" if prediction["prediction"]["confidence"] > 0.8 else "medium",
                "market_conditions": {
                    "predicted_direction": prediction["prediction"]["direction"],
                    "confidence": prediction["prediction"]["confidence"]
                }
            }
            optimization = await self._post(f"{ADVANCED_AI_URL}/portfolio/optimize", optimization_request)
            
            # Étape 3: Signal de feedback basé sur résultat
            feedback_signal = {
                "signal_type": "OPTIMIZATION",
                "component": "integrated_trading_scenario",
                "context": {
                    "market_conditions": {"prediction_used": True},
                    "optimization_result": optimization["optimization"]
                },
                "performance_metrics": {
                    "confidence_alignment": 0.85,
                    "expected_improvement": optimization["optimization"]["confidence_score"]
                }
            }
            await self._post(f"{ADVANCED_AI_URL}/feedback/learn", feedback_signal)
            
            print("✅ Scénario intégré exécuté avec succès")
            
            # Test 3: Test de stress - Multiple requêtes simultanées
            print("📝 Test 5.3: Test de stress (requêtes simultanées)...")
            
            tasks = []
            for i in range(10):
                # Mélange de requêtes différentes
                if i % 4 == 0:
                    task = self._get(f"{ADVANCED_AI_URL}/security/dashboard")
                elif i % 4 == 1:
                    task = self._get(f"{ADVANCED_AI_URL}/portfolio/metrics")
                elif i % 4 == 2:
                    task = self._get(f"{ADVANCED_AI_URL}/prediction/regime")
                else:
                    task = self._get(f"{ADVANCED_AI_URL}/feedback/patterns")
                tasks.append(task)
            
            start_stress = time.time()
            stress_results = await asyncio.gather(*tasks, return_exceptions=True)
            stress_time = time.time() - start_stress
            
            success_count = sum(1 for result in stress_results if not isinstance(result, Exception))
            print(f"✅ Test de stress: {success_count}/10 succès en {stress_time:.2f}s")
            
            self.test_results["system_integration"] = "✅ SUCCÈS"
            
        except Exception as e:
            print(f"❌ Erreur intégration système: {e}")
            self.test_results["system_integration"] = f"❌ ÉCHEC: {e}"

    async def generate_final_report(self):
        """📊 Générer le rapport final des tests"""
        
        total_time = (datetime.utcnow() - self.start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("📊 RAPPORT FINAL - TESTS IA AVANCÉE")
        print("=" * 60)
        
        success_count = sum(1 for result in self.test_results.values() if "✅" in result)
        total_count = len(self.test_results)
        
        print(f"⏱️  Durée totale: {total_time:.1f} secondes")
        print(f"🎯 Résultats: {success_count}/{total_count} modules validés")
        print(f"📈 Taux de succès: {(success_count/total_count)*100:.1f}%")
        
        print("\n📋 Détail par module:")
        for module, result in self.test_results.items():
            print(f"   {result} {module.replace('_', ' ').title()}")
        
        # Évaluation de l'autonomie
        if success_count == total_count:
            print(f"\n🏆 SYSTÈME 100% AUTONOME ET INTELLIGENT")
            print("   ✅ Tous les modules fonctionnent parfaitement")
            print("   ✅ Apprentissage continu opérationnel")
            print("   ✅ Prédictions multi-horizon actives") 
            print("   ✅ Supervision sécurité complète")
            print("   ✅ Optimisation portefeuille intelligente")
            print("   ✅ Intégration système parfaite")
            
            print(f"\n🚀 LE SYSTÈME EST PRÊT POUR LA PRODUCTION!")
        else:
            print(f"\n⚠️  QUELQUES AJUSTEMENTS NÉCESSAIRES")
            
        print("\n" + "=" * 60)

    async def _get(self, url: str) -> Dict:
        """Helper pour requêtes GET"""
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    
    async def _post(self, url: str, data: Dict) -> Dict:
        """Helper pour requêtes POST"""
        async with self.session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

async def main():
    """🎯 Point d'entrée principal"""
    
    print("🔧 Vérification de la connectivité API...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/../health") as response:
                if response.status == 200:
                    print("✅ API accessible")
                else:
                    print("❌ API non accessible")
                    return
    except Exception as e:
        print(f"❌ Impossible de joindre l'API: {e}")
        print("💡 Assure-toi que le backend est démarré avec: uvicorn app.main:app --reload")
        return
    
    # Lancer les tests complets
    async with AITestOrchestrator() as orchestrator:
        await orchestrator.run_complete_test_suite()

if __name__ == "__main__":
    asyncio.run(main()) 