#!/usr/bin/env python3
"""
🌉 N8N BRIDGE - Interface entre Orchestrateur Python et workflows N8N
Enhanced with concepts from JavaScript workflows:
- Advanced Forex Trading Support
- Dynamic Strategy Allocation
- Technical Analysis Integration
- Sophisticated Feedback Loops
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class N8NWorkflowManager:
    """Gestionnaire des workflows N8N enhanced avec stratégies avancées"""
    
    def __init__(self):
        self.base_url = "http://n8n:5678/webhook"
        self.auth = aiohttp.BasicAuth(
            os.getenv('N8N_USER', 'admin'),
            os.getenv('N8N_PASSWORD', 'TradingN8N2025!')
        )
        
        # Enhanced workflow endpoints avec support complet
        self.workflow_endpoints = {
            # === CRYPTO WORKFLOWS (Enhanced) ===
            "SCAN_AGGRESSIVE": {
                "webhook": "crypto-aggressive-scan",
                "type": "crypto",
                "strategy": "meme_scalping",
                "description": "Scan agressif des nouvelles opportunités crypto",
                "allocation_weight": 0.4,
                "risk_level": "HIGH",
                "expected_roi": 0.15
            },
            "SCAN_NORMAL": {
                "webhook": "crypto-normal-scan", 
                "type": "crypto",
                "strategy": "meme_scalping",
                "description": "Scan normal du marché crypto",
                "allocation_weight": 0.3,
                "risk_level": "MEDIUM",
                "expected_roi": 0.08
            },
            "SCAN_LIGHT": {
                "webhook": "crypto-light-monitoring",
                "type": "crypto", 
                "strategy": "meme_scalping",
                "description": "Monitoring léger crypto",
                "allocation_weight": 0.2,
                "risk_level": "LOW",
                "expected_roi": 0.04
            },
            
            # === TECHNICAL ANALYSIS WORKFLOWS (New from JS) ===
            "TECHNICAL_SCAN": {
                "webhook": "technical-analysis-scan",
                "type": "technical",
                "strategy": "technical_analysis", 
                "description": "Analyse technique des tokens établis",
                "allocation_weight": 0.35,
                "risk_level": "MEDIUM",
                "expected_roi": 0.12,
                "indicators": ["RSI", "MACD", "Bollinger", "EMA"],
                "min_market_cap": 100000000,
                "max_market_cap": 50000000000
            },
            "TECHNICAL_DEEP": {
                "webhook": "technical-deep-analysis",
                "type": "technical",
                "strategy": "technical_analysis",
                "description": "Analyse technique approfondie multi-timeframes",
                "allocation_weight": 0.5,
                "risk_level": "MEDIUM",
                "expected_roi": 0.18,
                "timeframes": ["1h", "4h", "1d"],
                "advanced_indicators": True
            },
            
            # === FOREX WORKFLOWS (Enhanced from JS patterns) ===
            "FOREX_SCAN_LONDON": {
                "webhook": "forex-london-session",
                "type": "forex",
                "strategy": "forex_sessions",
                "description": "Trading session de Londres (7-16 UTC)",
                "allocation_weight": 0.4,
                "risk_level": "HIGH",
                "expected_roi": 0.10,
                "session_hours": "07:00-16:00",
                "major_pairs": ["EURUSD", "GBPUSD", "EURGBP"],
                "volatility_filter": "MEDIUM_TO_HIGH"
            },
            "FOREX_SCAN_NY": {
                "webhook": "forex-newyork-session",
                "type": "forex",
                "strategy": "forex_sessions",
                "description": "Trading session de New York (13-22 UTC)",
                "allocation_weight": 0.5,
                "risk_level": "HIGH", 
                "expected_roi": 0.12,
                "session_hours": "13:00-22:00",
                "major_pairs": ["EURUSD", "GBPUSD", "USDJPY", "USDCAD"],
                "volatility_filter": "HIGH",
                "overlap_with": "LONDON"
            },
            "FOREX_SCAN_ASIA": {
                "webhook": "forex-asia-session",
                "type": "forex",
                "strategy": "forex_sessions",
                "description": "Trading session asiatique (21-6 UTC)",
                "allocation_weight": 0.3,
                "risk_level": "MEDIUM",
                "expected_roi": 0.06,
                "session_hours": "21:00-06:00",
                "major_pairs": ["USDJPY", "AUDUSD", "NZDUSD"],
                "volatility_filter": "LOW_TO_MEDIUM"
            },
            
            # === DUAL STRATEGY WORKFLOWS (From JS Dual AI Sync) ===
            "DUAL_MARKET_SYNC": {
                "webhook": "dual-market-synchronization",
                "type": "hybrid",
                "strategy": "dual_market",
                "description": "Synchronisation dual crypto + forex",
                "allocation_weight": 0.6,
                "risk_level": "MEDIUM",
                "expected_roi": 0.14,
                "combines": ["crypto", "forex"]
            },
            "STRATEGY_REBALANCE": {
                "webhook": "strategy-allocation-rebalance",
                "type": "management",
                "strategy": "allocation",
                "description": "Rebalancement allocation entre stratégies",
                "allocation_weight": 1.0,
                "risk_level": "LOW",
                "expected_roi": 0.02
            },
            
            # === HEALTH & MONITORING (Enhanced) ===
            "HEALTH_CHECK": {
                "webhook": "health-monitor-check",
                "type": "system",
                "strategy": "monitoring",
                "description": "Vérification santé système complète",
                "allocation_weight": 0.0,
                "risk_level": "NONE",
                "expected_roi": 0.0,
                "checks": ["apis", "system", "network", "performance"]
            },
            "EMERGENCY_PROTOCOL": {
                "webhook": "emergency-protocol-activation",
                "type": "system",
                "strategy": "emergency",
                "description": "Protocole d'urgence - arrêt sécurisé",
                "allocation_weight": 0.0,
                "risk_level": "CRITICAL",
                "expected_roi": 0.0
            },
            
            # === ANALYSIS WORKFLOWS (Enhanced) ===
            "ANALYSIS_DEEP": {
                "webhook": "deep-market-analysis",
                "type": "analysis",
                "strategy": "market_analysis",
                "description": "Analyse approfondie multi-asset",
                "allocation_weight": 0.0,
                "risk_level": "NONE",
                "expected_roi": 0.0,
                "scope": ["crypto", "forex", "technical", "sentiment"]
            },
            "PERFORMANCE_ANALYSIS": {
                "webhook": "performance-feedback-analysis",
                "type": "analysis",
                "strategy": "performance",
                "description": "Analyse performance et feedback loops",
                "allocation_weight": 0.0,
                "risk_level": "NONE", 
                "expected_roi": 0.0,
                "metrics": ["win_rate", "roi", "risk_adjusted", "patterns"]
            }
        }
        
        # Forex trading configuration (from JS)
        self.forex_config = {
            "sessions": {
                "LONDON": {
                    "hours": "07:00-16:00",
                    "pairs": ["EURUSD", "GBPUSD", "EURGBP", "EURJPY"],
                    "volatility": "HIGH",
                    "overlap": None
                },
                "NEW_YORK": {
                    "hours": "13:00-22:00", 
                    "pairs": ["EURUSD", "GBPUSD", "USDJPY", "USDCAD"],
                    "volatility": "VERY_HIGH",
                    "overlap": "LONDON"
                },
                "ASIA": {
                    "hours": "21:00-06:00",
                    "pairs": ["USDJPY", "AUDUSD", "NZDUSD", "EURJPY"],
                    "volatility": "MEDIUM",
                    "overlap": None
                }
            },
            "risk_management": {
                "max_position_size": 0.02,  # 2% per position
                "max_total_exposure": 0.10,  # 10% total forex
                "stop_loss": 0.008,  # 0.8% stop loss
                "take_profit": [0.012, 0.02, 0.035]  # 1.2%, 2%, 3.5%
            }
        }
        
    async def trigger_workflow(self, action: str, parameters: Dict[str, Any] = None) -> Dict:
        """Déclenche un workflow N8N via webhook (enhanced)"""
        if action not in self.workflow_endpoints:
            logger.warning(f"⚠️  Unknown workflow action: {action}")
            return {"success": False, "error": f"Unknown action: {action}"}
            
        workflow = self.workflow_endpoints[action]
        webhook_url = f"{self.base_url}/{workflow['webhook']}"
        
        # Enhanced payload avec métadonnées complètes
        payload = {
            "trigger_source": "ai_orchestrator_enhanced",
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "workflow_type": workflow["type"],
            "strategy": workflow["strategy"],
            "parameters": self._enrich_parameters(parameters or {}, workflow),
            "metadata": {
                "description": workflow["description"],
                "triggered_by": "intelligent_orchestrator",
                "allocation_weight": workflow.get("allocation_weight", 0),
                "risk_level": workflow.get("risk_level", "MEDIUM"),
                "expected_roi": workflow.get("expected_roi", 0),
                "workflow_version": "enhanced-v2.0"
            },
            "risk_management": self._get_risk_parameters(workflow),
            "market_context": parameters.get("market_context", {}) if parameters else {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                logger.info(f"🚀 Triggering N8N workflow: {action}")
                logger.info(f"📡 Strategy: {workflow['strategy']} | Risk: {workflow.get('risk_level', 'MEDIUM')}")
                
                async with session.post(
                    webhook_url,
                    json=payload,
                    auth=self.auth,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Workflow {action} triggered successfully")
                        return {
                            "success": True,
                            "workflow": action,
                            "strategy": workflow["strategy"],
                            "response": result,
                            "expected_roi": workflow.get("expected_roi", 0),
                            "risk_level": workflow.get("risk_level", "MEDIUM"),
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Workflow {action} failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "workflow": action,
                            "error": f"HTTP {response.status}: {error_text}",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        
        except asyncio.TimeoutError:
            logger.error(f"⏰ Timeout triggering workflow {action}")
            return {"success": False, "error": "Timeout", "workflow": action}
            
        except Exception as e:
            logger.error(f"❌ Error triggering workflow {action}: {str(e)}")
            return {"success": False, "error": str(e), "workflow": action}
            
    def _enrich_parameters(self, parameters: Dict, workflow: Dict) -> Dict:
        """Enrichit les paramètres avec des données contextuelles"""
        enriched = parameters.copy()
        
        # Ajouter configuration spécifique au workflow
        if workflow["type"] == "forex":
            session = workflow.get("session_hours", "")
            enriched.update({
                "session_config": self.forex_config["sessions"].get(
                    enriched.get("forex_session", "LONDON"), {}
                ),
                "risk_config": self.forex_config["risk_management"],
                "major_pairs": workflow.get("major_pairs", []),
                "volatility_filter": workflow.get("volatility_filter", "MEDIUM")
            })
        elif workflow["type"] == "technical":
            enriched.update({
                "indicators": workflow.get("indicators", []),
                "timeframes": workflow.get("timeframes", ["1h"]),
                "min_market_cap": workflow.get("min_market_cap", 0),
                "max_market_cap": workflow.get("max_market_cap", float('inf')),
                "advanced_mode": workflow.get("advanced_indicators", False)
            })
        elif workflow["type"] == "crypto":
            enriched.update({
                "scan_intensity": workflow.get("allocation_weight", 0.3),
                "risk_tolerance": workflow.get("risk_level", "MEDIUM"),
                "platforms": ["pump_fun", "dexscreener", "birdeye"]
            })
            
        return enriched
        
    def _get_risk_parameters(self, workflow: Dict) -> Dict:
        """Calcule les paramètres de risque pour le workflow"""
        risk_level = workflow.get("risk_level", "MEDIUM")
        expected_roi = workflow.get("expected_roi", 0.05)
        
        risk_params = {
            "position_size_multiplier": 1.0,
            "stop_loss_multiplier": 1.0,
            "take_profit_multiplier": 1.0,
            "max_positions": 3
        }
        
        if risk_level == "LOW":
            risk_params.update({
                "position_size_multiplier": 0.5,
                "stop_loss_multiplier": 0.7,
                "take_profit_multiplier": 0.8,
                "max_positions": 2
            })
        elif risk_level == "HIGH":
            risk_params.update({
                "position_size_multiplier": 1.5,
                "stop_loss_multiplier": 1.3,
                "take_profit_multiplier": 1.4,
                "max_positions": 5
            })
        elif risk_level == "CRITICAL":
            risk_params.update({
                "position_size_multiplier": 0.1,
                "stop_loss_multiplier": 0.5,
                "take_profit_multiplier": 0.5,
                "max_positions": 1
            })
            
        return risk_params
        
    async def trigger_crypto_workflow(self, intensity: str = "normal", focus_areas: List[str] = None, allocation: float = 0.33) -> Dict:
        """Déclenche les workflows crypto selon l'intensité (enhanced)"""
        parameters = {
            "focus_areas": focus_areas or ["pump_fun", "dexscreener"],
            "allocation_percentage": allocation,
            "market_context": {
                "intensity": intensity,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        if intensity == "aggressive":
            parameters.update({
                "scan_depth": "deep",
                "risk_tolerance": "high",
                "min_volume": 100000,
                "max_age_hours": 1
            })
            return await self.trigger_workflow("SCAN_AGGRESSIVE", parameters)
        elif intensity == "light":
            parameters.update({
                "scan_depth": "surface", 
                "risk_tolerance": "conservative",
                "min_volume": 500000,
                "max_age_hours": 24
            })
            return await self.trigger_workflow("SCAN_LIGHT", parameters)
        else:
            parameters.update({
                "scan_depth": "medium",
                "risk_tolerance": "medium",
                "min_volume": 250000,
                "max_age_hours": 6
            })
            return await self.trigger_workflow("SCAN_NORMAL", parameters)
            
    async def trigger_technical_workflow(self, complexity: str = "standard", allocation: float = 0.33) -> Dict:
        """Déclenche les workflows d'analyse technique (new from JS)"""
        parameters = {
            "allocation_percentage": allocation,
            "analysis_complexity": complexity,
            "market_context": {
                "timestamp": datetime.utcnow().isoformat(),
                "requested_complexity": complexity
            }
        }
        
        if complexity == "deep":
            parameters.update({
                "include_advanced_indicators": True,
                "multi_timeframe": True,
                "sentiment_analysis": True,
                "pattern_recognition": True
            })
            return await self.trigger_workflow("TECHNICAL_DEEP", parameters)
        else:
            parameters.update({
                "include_advanced_indicators": False,
                "multi_timeframe": False,
                "focus_indicators": ["RSI", "MACD", "Bollinger"]
            })
            return await self.trigger_workflow("TECHNICAL_SCAN", parameters)
            
    async def trigger_forex_workflow(self, session: str, pairs: List[str] = None, allocation: float = 0.33) -> Dict:
        """Déclenche les workflows forex selon la session active (enhanced)"""
        session_config = self.forex_config["sessions"].get(session, {})
        
        parameters = {
            "session": session.lower(),
            "pairs": pairs or session_config.get("pairs", []),
            "allocation_percentage": allocation,
            "session_config": session_config,
            "risk_config": self.forex_config["risk_management"],
            "market_context": {
                "session": session,
                "volatility": session_config.get("volatility", "MEDIUM"),
                "overlap": session_config.get("overlap"),
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        if session == "LONDON":
            parameters.update({
                "volatility_filter": "medium_to_high",
                "focus_pairs": ["EURUSD", "GBPUSD", "EURGBP"],
                "session_strength": "high"
            })
            return await self.trigger_workflow("FOREX_SCAN_LONDON", parameters)
        elif session == "NEW_YORK":
            parameters.update({
                "volatility_filter": "high",
                "focus_pairs": ["EURUSD", "GBPUSD", "USDJPY", "USDCAD"],
                "session_strength": "very_high",
                "london_overlap": True
            })
            return await self.trigger_workflow("FOREX_SCAN_NY", parameters)
        elif session == "ASIA":
            parameters.update({
                "volatility_filter": "low_to_medium",
                "focus_pairs": ["USDJPY", "AUDUSD", "NZDUSD"],
                "session_strength": "medium"
            })
            return await self.trigger_workflow("FOREX_SCAN_ASIA", parameters)
        else:
            logger.info("🌙 Quiet forex session - minimal activity")
            return {"success": True, "message": "Quiet session, minimal forex activity"}
            
    async def trigger_dual_market_sync(self, allocation_data: Dict) -> Dict:
        """Déclenche la synchronisation dual market (from JS Dual AI Sync)"""
        parameters = {
            "allocation_data": allocation_data,
            "sync_type": "dual_market",
            "strategies": ["meme_scalping", "technical_analysis", "forex_sessions"],
            "market_context": {
                "sync_timestamp": datetime.utcnow().isoformat(),
                "total_allocation": sum(allocation_data.values()),
                "rebalancing": True
            }
        }
        
        return await self.trigger_workflow("DUAL_MARKET_SYNC", parameters)
        
    async def trigger_strategy_rebalance(self, old_allocation: Dict, new_allocation: Dict, reasoning: str) -> Dict:
        """Déclenche le rebalancement de stratégies"""
        parameters = {
            "old_allocation": old_allocation,
            "new_allocation": new_allocation,
            "rebalance_reasoning": reasoning,
            "allocation_changes": {
                strategy: new_allocation.get(strategy, 0) - old_allocation.get(strategy, 0)
                for strategy in set(list(old_allocation.keys()) + list(new_allocation.keys()))
            },
            "market_context": {
                "rebalance_timestamp": datetime.utcnow().isoformat(),
                "trigger": "ai_orchestrator"
            }
        }
        
        return await self.trigger_workflow("STRATEGY_REBALANCE", parameters)
        
    async def trigger_health_check(self, check_type: str = "comprehensive") -> Dict:
        """Déclenche une vérification de santé complète (enhanced)"""
        parameters = {
            "check_type": check_type,
            "include_apis": True,
            "include_system": True,
            "include_network": True,
            "include_performance": True,
            "health_scope": ["pump_fun", "dexscreener", "tradermade", "coingecko", "birdeye"],
            "market_context": {
                "health_check_timestamp": datetime.utcnow().isoformat(),
                "requested_scope": check_type
            }
        }
        
        return await self.trigger_workflow("HEALTH_CHECK", parameters)
        
    async def trigger_emergency_protocol(self, emergency_type: str, severity: str = "HIGH") -> Dict:
        """Déclenche le protocole d'urgence"""
        parameters = {
            "emergency_type": emergency_type,
            "severity": severity,
            "immediate_actions": [
                "stop_new_positions",
                "secure_existing_positions", 
                "enable_emergency_monitoring"
            ],
            "market_context": {
                "emergency_timestamp": datetime.utcnow().isoformat(),
                "trigger_reason": emergency_type,
                "auto_triggered": True
            }
        }
        
        return await self.trigger_workflow("EMERGENCY_PROTOCOL", parameters)
        
    async def trigger_performance_analysis(self, analysis_scope: str = "all_strategies") -> Dict:
        """Déclenche l'analyse de performance et feedback"""
        parameters = {
            "analysis_scope": analysis_scope,
            "include_patterns": True,
            "include_feedback_loops": True,
            "performance_metrics": ["win_rate", "avg_roi", "risk_adjusted_return", "sharpe_ratio"],
            "market_context": {
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "scope": analysis_scope
            }
        }
        
        return await self.trigger_workflow("PERFORMANCE_ANALYSIS", parameters)
        
    async def get_workflow_status(self, workflow_id: str) -> Dict:
        """Vérifie le statut d'un workflow en cours"""
        # Cette méthode nécessiterait l'API N8N pour récupérer le statut
        # Pour l'instant, simulation enrichie
        return {
            "workflow_id": workflow_id,
            "status": "running",
            "progress": "65%",
            "estimated_completion": "1.5 minutes",
            "current_step": "market_analysis",
            "performance_metrics": {
                "api_calls": 45,
                "data_points": 230,
                "success_rate": 0.96
            }
        }
        
    def get_available_workflows(self) -> Dict[str, Dict]:
        """Retourne la liste des workflows disponibles (enhanced)"""
        return self.workflow_endpoints
        
    def get_forex_sessions_config(self) -> Dict:
        """Retourne la configuration des sessions Forex"""
        return self.forex_config
        
    def calculate_optimal_allocation(self, strategy_performances: Dict) -> Dict:
        """Calcule l'allocation optimale basée sur les performances"""
        total_performance = sum(perf.get("win_rate", 0) for perf in strategy_performances.values())
        
        if total_performance == 0:
            # Allocation égale si pas de données
            return {"meme": 0.33, "technical": 0.33, "forex": 0.34}
            
        optimal_allocation = {}
        for strategy, perf in strategy_performances.items():
            win_rate = perf.get("win_rate", 0)
            # Allocation basée sur performance avec limites
            allocation = min(0.6, max(0.15, win_rate / total_performance))
            optimal_allocation[strategy] = allocation
            
        # Normaliser pour que la somme soit 1.0
        total_allocation = sum(optimal_allocation.values())
        if total_allocation > 0:
            optimal_allocation = {k: v/total_allocation for k, v in optimal_allocation.items()}
            
        return optimal_allocation

class WorkflowOrchestrator:
    """Orchestrateur spécialisé pour la gestion des workflows (enhanced)"""
    
    def __init__(self):
        self.n8n = N8NWorkflowManager()
        self.active_workflows: Dict[str, Dict] = {}
        self.performance_tracker = {
            "total_executions": 0,
            "successful_executions": 0,
            "strategy_performance": {
                "meme_scalping": {"executions": 0, "successes": 0},
                "technical_analysis": {"executions": 0, "successes": 0}, 
                "forex_sessions": {"executions": 0, "successes": 0}
            }
        }
        
    async def execute_ai_decision(self, decision_action: str, mode: str, parameters: Dict) -> Dict:
        """Exécute une décision de l'IA en déclenchant les bons workflows (enhanced)"""
        results = []
        strategy = parameters.get("strategy", "unknown")
        allocation = parameters.get("allocation_changes", {})
        
        logger.info(f"🎯 Executing AI decision: {decision_action} | Mode: {mode} | Strategy: {strategy}")
        
        # Track execution
        self.performance_tracker["total_executions"] += 1
        if strategy in self.performance_tracker["strategy_performance"]:
            self.performance_tracker["strategy_performance"][strategy]["executions"] += 1
        
        try:
            if mode == "crypto":
                result = await self._execute_crypto_strategy(decision_action, parameters)
                results.append(result)
                
            elif mode == "forex":
                result = await self._execute_forex_strategy(decision_action, parameters)
                results.append(result)
                
            elif mode == "hybrid":
                # Exécuter stratégies multiples selon allocation
                crypto_result = await self._execute_crypto_strategy("SCAN_NORMAL", parameters)
                forex_result = await self._execute_forex_strategy(
                    parameters.get("forex_session", "LONDON"), parameters
                )
                results.extend([crypto_result, forex_result])
                
                # Trigger dual market sync si allocation change
                if allocation:
                    sync_result = await self.n8n.trigger_dual_market_sync(allocation)
                    results.append(sync_result)
                    
            # Actions spéciales
            if decision_action == "HEALTH_CHECK":
                health_result = await self.n8n.trigger_health_check("comprehensive")
                results.append(health_result)
                
            elif decision_action == "ANALYSIS_DEEP":
                analysis_result = await self.n8n.trigger_performance_analysis("all_strategies")
                results.append(analysis_result)
                
            elif decision_action == "REBALANCE_ALLOCATION" and allocation:
                old_allocation = parameters.get("old_allocation", {})
                reasoning = parameters.get("reasoning", "AI-driven rebalancing")
                rebalance_result = await self.n8n.trigger_strategy_rebalance(
                    old_allocation, allocation, reasoning
                )
                results.append(rebalance_result)
                
            # Marquer succès
            successful_results = [r for r in results if r.get("success", False)]
            if successful_results:
                self.performance_tracker["successful_executions"] += 1
                if strategy in self.performance_tracker["strategy_performance"]:
                    self.performance_tracker["strategy_performance"][strategy]["successes"] += 1
                    
            return {
                "executed_workflows": len(successful_results),
                "total_workflows": len(results),
                "results": results,
                "strategy": strategy,
                "mode": mode,
                "success_rate": len(successful_results) / len(results) if results else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error executing AI decision: {e}")
            return {
                "executed_workflows": 0,
                "total_workflows": 0,
                "results": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
    async def _execute_crypto_strategy(self, action: str, parameters: Dict) -> Dict:
        """Exécute une stratégie crypto spécifique"""
        allocation = parameters.get("allocation_changes", {}).get("meme", 0.33)
        focus_areas = parameters.get("focus_areas", [])
        
        if action == "SCAN_AGGRESSIVE":
            return await self.n8n.trigger_crypto_workflow("aggressive", focus_areas, allocation)
        elif action == "SCAN_LIGHT":
            return await self.n8n.trigger_crypto_workflow("light", focus_areas, allocation)
        else:
            return await self.n8n.trigger_crypto_workflow("normal", focus_areas, allocation)
            
    async def _execute_forex_strategy(self, action: str, parameters: Dict) -> Dict:
        """Exécute une stratégie forex spécifique"""
        allocation = parameters.get("allocation_changes", {}).get("forex", 0.33)
        session = parameters.get("forex_session", "LONDON")
        
        if action.startswith("FOREX_SCAN_"):
            session = action.split("_")[-1]
            
        return await self.n8n.trigger_forex_workflow(session, None, allocation)
        
    async def emergency_stop_all(self) -> Dict:
        """Arrêt d'urgence de tous les workflows (enhanced)"""
        logger.warning("🚨 Emergency stop requested for all workflows")
        
        emergency_result = await self.n8n.trigger_emergency_protocol(
            "manual_stop", "CRITICAL"
        )
        
        return {
            "success": True,
            "emergency_protocol": emergency_result,
            "message": "Emergency stop protocol activated",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    def get_performance_metrics(self) -> Dict:
        """Retourne les métriques de performance des workflows"""
        total_exec = self.performance_tracker["total_executions"]
        success_exec = self.performance_tracker["successful_executions"]
        
        metrics = {
            "overall_success_rate": success_exec / total_exec if total_exec > 0 else 0,
            "total_executions": total_exec,
            "successful_executions": success_exec,
            "strategy_breakdown": {}
        }
        
        for strategy, data in self.performance_tracker["strategy_performance"].items():
            executions = data["executions"]
            successes = data["successes"]
            metrics["strategy_breakdown"][strategy] = {
                "executions": executions,
                "successes": successes,
                "success_rate": successes / executions if executions > 0 else 0
            }
            
        return metrics

# Test enhanced de la bridge
async def test_enhanced_n8n_bridge():
    """Test de la bridge N8N enhanced"""
    bridge = N8NWorkflowManager()
    
    print("🧪 Testing Enhanced N8N Bridge...")
    
    # Test forex workflow
    forex_result = await bridge.trigger_forex_workflow("LONDON", ["EURUSD", "GBPUSD"], 0.4)
    print(f"Forex test: {forex_result.get('success', False)}")
    
    # Test technical workflow
    tech_result = await bridge.trigger_technical_workflow("deep", 0.35)
    print(f"Technical test: {tech_result.get('success', False)}")
    
    # Test dual market sync
    allocation = {"meme": 0.3, "technical": 0.4, "forex": 0.3}
    sync_result = await bridge.trigger_dual_market_sync(allocation)
    print(f"Dual sync test: {sync_result.get('success', False)}")
    
if __name__ == "__main__":
    asyncio.run(test_enhanced_n8n_bridge()) 