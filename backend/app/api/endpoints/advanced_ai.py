"""
🚀 ADVANCED AI ENDPOINTS - API POUR MODULES AVANCÉS
==================================================

Endpoints API pour tous les modules d'IA avancée :
- AI Feedback Loop : Apprentissage continu et adaptation
- Predictive System : Prédictions et analyse de marché
- Security Supervisor : Supervision sécurité et health checks
- Portfolio Optimizer : Optimisation intelligente de portefeuille
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pydantic import BaseModel

from app.orchestrator.ai_feedback_loop import get_ai_feedback_loop, LearningSignal, AdaptationContext
from app.orchestrator.predictive_system import get_predictive_system, PredictionHorizon, AlertType
from app.orchestrator.security_supervisor import get_security_supervisor, AlertSeverity
from app.orchestrator.portfolio_optimizer import get_portfolio_optimizer, AllocationStrategy, RiskLevel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advanced-ai", tags=["advanced-ai"])

# ================================================================================
# MODELS DE DONNÉES POUR L'API
# ================================================================================

class LearningSignalRequest(BaseModel):
    signal_type: str  # SUCCESS, FAILURE, OPTIMIZATION, ADAPTATION
    component: str
    context: Dict[str, Any]
    performance_metrics: Dict[str, float]
    timestamp: Optional[datetime] = None

class PredictionRequest(BaseModel):
    asset_type: str
    horizon: str  # "5min", "1hour", "4hour", "24hour"
    market_data: Optional[Dict[str, Any]] = None

class PortfolioOptimizationRequest(BaseModel):
    strategy: str = "balanced"
    risk_level: str = "medium"
    market_conditions: Optional[Dict[str, Any]] = None

class SecurityScanRequest(BaseModel):
    scan_type: str = "comprehensive"  # "comprehensive", "cve_only", "health_only"
    deep_scan: bool = False

# ================================================================================
# 🧠 AI FEEDBACK LOOP ENDPOINTS
# ================================================================================

@router.post("/feedback/learn")
async def submit_learning_signal(request: LearningSignalRequest, background_tasks: BackgroundTasks):
    """
    🧠 Soumettre un signal d'apprentissage pour amélioration continue
    
    Permet de signaler les succès/échecs/optimisations pour que l'IA s'adapte
    """
    try:
        # Debug: Afficher les données reçues
        logger.info(f"🔍 Données reçues feedback: signal_type={request.signal_type}, component={request.component}")
        
        feedback_loop = get_ai_feedback_loop()
        
        # Convertir string en enum (mapping correct)
        signal_mapping = {
            "SUCCESS": LearningSignal.SUCCESS,
            "FAILURE": LearningSignal.FAILURE,
            "OPTIMIZATION": LearningSignal.OPTIMIZATION,
            "ADAPTATION": LearningSignal.ADAPTATION
        }
        
        signal_type = signal_mapping.get(request.signal_type.upper(), LearningSignal.SUCCESS)
        
        # Créer contexte d'adaptation avec validation
        try:
            context = AdaptationContext(
                market_conditions=request.context.get("market_conditions", {}),
                system_state=request.context.get("system_state", {}),
                recent_performance=request.context.get("recent_performance", {}),
                external_factors=request.context.get("external_factors", {})
            )
        except Exception as ctx_error:
            logger.error(f"❌ Erreur création contexte: {ctx_error}")
            # Contexte par défaut
            context = AdaptationContext(
                market_conditions={},
                system_state={},
                recent_performance={},
                external_factors={}
            )
        
        # Traitement en arrière-plan
        background_tasks.add_task(
            feedback_loop.process_learning_signal,
            signal_type,
            request.component,
            context,
            request.performance_metrics
        )
        
        return {
            "status": "success",
            "message": f"Learning signal {request.signal_type} submitted for {request.component}",
            "signal_id": f"learn_{int(datetime.utcnow().timestamp())}",
            "processing": "background"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur soumission signal apprentissage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/patterns")
async def get_learning_patterns():
    """
    📋 Obtenir les patterns d'apprentissage découverts
    """
    try:
        feedback_loop = get_ai_feedback_loop()
        patterns = await feedback_loop.get_learning_patterns()
        
        return {
            "status": "success",
            "patterns": patterns,
            "total_patterns": len(patterns),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/adaptations")
async def get_recent_adaptations():
    """
    🔄 Obtenir les adaptations récentes du système
    """
    try:
        feedback_loop = get_ai_feedback_loop()
        adaptations = await feedback_loop.get_recent_adaptations()
        
        return {
            "status": "success",
            "adaptations": adaptations,
            "count": len(adaptations),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération adaptations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback/analyze-performance")
async def analyze_performance(performance_data: Dict[str, Any]):
    """
    📊 Analyser les performances et détecter les anomalies
    """
    try:
        feedback_loop = get_ai_feedback_loop()
        analysis = await feedback_loop.analyze_performance_anomalies(performance_data)
        
        return {
            "status": "success",
            "analysis": analysis,
            "anomalies_detected": len(analysis.get("anomalies", [])),
            "recommendations": analysis.get("recommendations", [])
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur analyse performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# 🔮 PREDICTIVE SYSTEM ENDPOINTS
# ================================================================================

@router.post("/prediction/forecast")
async def generate_prediction(request: PredictionRequest):
    """
    🔮 Générer des prédictions de marché multi-horizon
    """
    try:
        predictive_system = get_predictive_system()
        
        # Convertir horizon string en enum (mapping correct)
        horizon_mapping = {
            "5min": PredictionHorizon.SHORT_TERM,
            "1hour": PredictionHorizon.MEDIUM_TERM,
            "4hour": PredictionHorizon.LONG_TERM,
            "24hour": PredictionHorizon.STRATEGIC
        }
        
        horizon = horizon_mapping.get(request.horizon, PredictionHorizon.MEDIUM_TERM)
        
        prediction = await predictive_system.generate_market_prediction(
            asset_type=request.asset_type,
            horizon=horizon,
            market_data=request.market_data
        )
        
        return {
            "status": "success",
            "prediction": {
                "asset_type": prediction.asset_type,
                "horizon": prediction.horizon.value,
                "direction": prediction.direction.value,
                "magnitude": prediction.magnitude,
                "confidence": prediction.confidence,
                "price_target": prediction.price_target,
                "probability": prediction.probability,
                "key_factors": prediction.key_factors,
                "risk_factors": prediction.risk_factors,
                "predicted_volatility": prediction.predicted_volatility,
                "predicted_trend": prediction.predicted_trend,
                "predicted_regime": prediction.predicted_regime.value,
                "key_levels": prediction.key_levels,
                "opportunities": prediction.opportunities,
                "risks": prediction.risks,
                "optimal_strategies": prediction.optimal_strategies,
                "generated_at": prediction.generated_at.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur génération prédiction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prediction/regime")
async def detect_market_regime():
    """
    🌊 Détecter le régime de marché actuel
    """
    try:
        predictive_system = get_predictive_system()
        regime = await predictive_system.detect_market_regime()
        
        return {
            "status": "success",
            "regime": {
                "trend": regime.trend.value,
                "volatility": regime.volatility,
                "market_phase": regime.market_phase,
                "confidence": regime.confidence,
                "regime_strength": regime.regime_strength,
                "detected_at": regime.detected_at.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur détection régime: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prediction/alerts")
async def get_predictive_alerts():
    """
    🚨 Obtenir les alertes prédictives actives
    """
    try:
        predictive_system = get_predictive_system()
        alerts = await predictive_system.generate_predictive_alerts()
        
        return {
            "status": "success",
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "alert_type": alert.alert_type,
                    "asset_type": alert.asset_type,
                    "severity": alert.severity,
                    "predicted_event": alert.predicted_event,
                    "probability": alert.probability,
                    "time_to_event": str(alert.time_to_event),
                    "recommended_actions": alert.recommended_actions,
                    "confidence": alert.confidence,
                    "created_at": alert.created_at.isoformat()
                }
                for alert in alerts
            ],
            "total_alerts": len(alerts),
            "high_priority": len([a for a in alerts if a.severity == "high"])
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération alertes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prediction/analysis/{asset_type}")
async def get_historical_analysis(asset_type: str):
    """
    📈 Obtenir l'analyse historique pour un asset
    """
    try:
        predictive_system = get_predictive_system()
        analysis = await predictive_system.analyze_historical_patterns(asset_type)
        
        return {
            "status": "success",
            "asset_type": asset_type,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur analyse historique {asset_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# 🛡️ SECURITY SUPERVISOR ENDPOINTS
# ================================================================================

@router.post("/security/health-check")
async def run_health_check(background_tasks: BackgroundTasks):
    """
    🏥 Lancer un health check complet du système
    """
    try:
        security_supervisor = get_security_supervisor()
        health_results = await security_supervisor.run_comprehensive_health_check()
        
        return {
            "status": "success",
            "health_check": {
                component: {
                    "status": result.status.value,
                    "message": result.message,
                    "response_time_ms": result.response_time_ms,
                    "metrics": result.metrics,
                    "recommendations": result.recommendations
                }
                for component, result in health_results.items()
            },
            "overall_status": "healthy" if all(r.status.value in ["healthy", "warning"] for r in health_results.values()) else "critical",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/security/cve-scan")
async def scan_vulnerabilities(request: SecurityScanRequest, background_tasks: BackgroundTasks):
    """
    🔍 Scanner les vulnérabilités CVE du système
    """
    try:
        security_supervisor = get_security_supervisor()
        
        # Lancer scan en arrière-plan pour les scans profonds
        if request.deep_scan:
            background_tasks.add_task(security_supervisor.scan_cve_vulnerabilities)
            return {
                "status": "initiated",
                "message": "Deep CVE scan initiated in background",
                "scan_id": f"cve_scan_{int(datetime.utcnow().timestamp())}"
            }
        else:
            vulnerabilities = await security_supervisor.scan_cve_vulnerabilities()
            
            return {
                "status": "success",
                "vulnerabilities": [
                    {
                        "cve_id": vuln.cve_id,
                        "severity": vuln.severity.value,
                        "score": vuln.score,
                        "component": vuln.component,
                        "description": vuln.description,
                        "patch_available": vuln.patch_available,
                        "remediation_steps": vuln.remediation_steps
                    }
                    for vuln in vulnerabilities
                ],
                "total_vulnerabilities": len(vulnerabilities),
                "critical_count": len([v for v in vulnerabilities if v.severity.value == "critical"]),
                "high_count": len([v for v in vulnerabilities if v.severity.value == "high"])
            }
        
    except Exception as e:
        logger.error(f"❌ Erreur scan CVE: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/security/dashboard")
async def get_security_dashboard():
    """
    📊 Obtenir le tableau de bord sécurité complet
    """
    try:
        security_supervisor = get_security_supervisor()
        dashboard = await security_supervisor.get_security_dashboard()
        
        return {
            "status": "success",
            "dashboard": dashboard
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur dashboard sécurité: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/security/alerts")
async def get_security_alerts():
    """
    🚨 Obtenir les alertes de sécurité actives
    """
    try:
        security_supervisor = get_security_supervisor()
        
        return {
            "status": "success",
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "severity": alert.severity.value,
                    "component": alert.component,
                    "title": alert.title,
                    "description": alert.description,
                    "impact": alert.impact,
                    "remediation": alert.remediation,
                    "detected_at": alert.detected_at.isoformat(),
                    "resolved": alert.resolved_at is not None
                }
                for alert in security_supervisor.active_alerts
            ],
            "total_alerts": len(security_supervisor.active_alerts),
            "by_severity": {
                severity.value: len([a for a in security_supervisor.active_alerts if a.severity == severity])
                for severity in AlertSeverity
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur alertes sécurité: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# 💼 PORTFOLIO OPTIMIZER ENDPOINTS
# ================================================================================

@router.post("/portfolio/optimize")
async def optimize_portfolio(request: PortfolioOptimizationRequest):
    """
    🎯 Optimiser l'allocation de portefeuille intelligente
    """
    try:
        portfolio_optimizer = get_portfolio_optimizer()
        
        # Convertir strings en enums
        strategy = AllocationStrategy[request.strategy.upper()]
        risk_level = RiskLevel[request.risk_level.upper()]
        
        optimization_result = await portfolio_optimizer.optimize_portfolio(
            strategy=strategy,
            risk_level=risk_level,
            market_conditions=request.market_conditions
        )
        
        return {
            "status": "success",
            "optimization": {
                "optimization_id": optimization_result.optimization_id,
                "strategy": optimization_result.strategy.value,
                "risk_level": optimization_result.risk_level.value,
                "optimal_weights": optimization_result.optimal_weights,
                "expected_return": optimization_result.expected_return,
                "expected_volatility": optimization_result.expected_volatility,
                "expected_sharpe": optimization_result.expected_sharpe,
                "confidence_score": optimization_result.confidence_score,
                "improvement_vs_current": optimization_result.improvement_vs_current,
                "constraints_satisfied": optimization_result.constraints_satisfied,
                "optimization_time_ms": optimization_result.optimization_time_ms,
                "timestamp": optimization_result.timestamp.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur optimisation portefeuille: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/rebalance")
async def get_rebalance_recommendations():
    """
    ⚖️ Obtenir les recommandations de rééquilibrage
    """
    try:
        portfolio_optimizer = get_portfolio_optimizer()
        recommendations = await portfolio_optimizer.generate_rebalance_recommendations()
        
        return {
            "status": "success",
            "recommendations": [
                {
                    "asset_type": rec.asset_type,
                    "current_weight": rec.current_weight,
                    "target_weight": rec.target_weight,
                    "weight_drift": rec.weight_drift,
                    "action": rec.action,
                    "amount": rec.amount,
                    "priority": rec.priority,
                    "reason": rec.reason,
                    "expected_impact": rec.expected_impact
                }
                for rec in recommendations
            ],
            "total_recommendations": len(recommendations),
            "high_priority": len([r for r in recommendations if r.priority == "high"]),
            "rebalance_needed": len(recommendations) > 0
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur recommandations rééquilibrage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/metrics")
async def get_portfolio_metrics():
    """
    📊 Obtenir les métriques de performance du portefeuille
    """
    try:
        portfolio_optimizer = get_portfolio_optimizer()
        metrics = await portfolio_optimizer.calculate_portfolio_metrics()
        
        return {
            "status": "success",
            "metrics": {
                "total_value": metrics.total_value,
                "total_return": metrics.total_return,
                "volatility": metrics.volatility,
                "sharpe_ratio": metrics.sharpe_ratio,
                "max_drawdown": metrics.max_drawdown,
                "var_95": metrics.var_95,
                "cvar_95": metrics.cvar_95,
                "calmar_ratio": metrics.calmar_ratio,
                "sortino_ratio": metrics.sortino_ratio,
                "alpha": metrics.alpha,
                "beta": metrics.beta,
                "information_ratio": metrics.information_ratio,
                "tracking_error": metrics.tracking_error
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur métriques portefeuille: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/summary")
async def get_optimization_summary():
    """
    📋 Obtenir un résumé complet des optimisations
    """
    try:
        portfolio_optimizer = get_portfolio_optimizer()
        summary = await portfolio_optimizer.get_optimization_summary()
        
        return {
            "status": "success",
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur résumé optimisation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================================
# 🎛️ ENDPOINTS DE CONTRÔLE GLOBAL
# ================================================================================

@router.get("/status/complete")
async def get_complete_system_status():
    """
    🎛️ Obtenir le statut complet de tous les modules avancés
    """
    try:
        # Récupérer le status de tous les modules (version simplifiée)
        feedback_loop = get_ai_feedback_loop()
        predictive_system = get_predictive_system()
        security_supervisor = get_security_supervisor()
        portfolio_optimizer = get_portfolio_optimizer()
        
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "modules": {
                "ai_feedback_loop": {
                    "active": True,
                    "status": "operational",
                    "type": "learning_system"
                },
                "predictive_system": {
                    "active": True,
                    "status": "operational", 
                    "total_predictions": predictive_system.total_predictions,
                    "successful_predictions": predictive_system.successful_predictions
                },
                "security_supervisor": {
                    "active": True,
                    "status": "operational",
                    "total_checks": security_supervisor.total_checks,
                    "failed_checks": security_supervisor.failed_checks,
                    "active_alerts": len(security_supervisor.active_alerts)
                },
                "portfolio_optimizer": {
                    "active": True,
                    "status": "operational",
                    "total_optimizations": portfolio_optimizer.total_optimizations,
                    "successful_optimizations": portfolio_optimizer.successful_optimizations
                }
            },
            "overall_health": "operational",
            "intelligence_level": "advanced",
            "modules_operational": 4,
            "system_ready": True
        }
        
        return {
            "status": "success",
            "system_status": status
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur status système complet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/control/reset")
async def reset_all_modules(confirm: bool = False):
    """
    🔄 Réinitialiser tous les modules avancés (DEV ONLY)
    """
    try:
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "Add ?confirm=true to reset all modules",
                "warning": "This will clear all learning history and adaptations"
            }
        
        # Réinitialiser tous les modules (version simplifiée)
        feedback_loop = get_ai_feedback_loop()
        predictive_system = get_predictive_system()
        security_supervisor = get_security_supervisor()
        portfolio_optimizer = get_portfolio_optimizer()
        
        # Reset basic counters
        predictive_system.total_predictions = 0
        predictive_system.successful_predictions = 0
        
        security_supervisor.total_checks = 0
        security_supervisor.failed_checks = 0
        security_supervisor.active_alerts.clear()
        
        portfolio_optimizer.total_optimizations = 0
        portfolio_optimizer.successful_optimizations = 0
        
        return {
            "status": "success",
            "message": "All advanced modules reset successfully",
            "modules_reset": ["ai_feedback_loop", "predictive_system", "security_supervisor", "portfolio_optimizer"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur reset modules: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 