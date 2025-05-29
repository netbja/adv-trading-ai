#!/usr/bin/env python3
"""
🌐 API SERVER - Interface REST pour l'Orchestrateur AI
Permet de monitorer et contrôler l'orchestrateur depuis Grafana ou autres outils
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, Optional
import aiohttp
from aiohttp import web, web_request
import aiohttp_cors

from .ai_orchestrator import IntelligentOrchestrator

logger = logging.getLogger(__name__)

class OrchestratorAPI:
    """API REST pour l'orchestrateur intelligent"""
    
    def __init__(self, orchestrator: IntelligentOrchestrator):
        self.orchestrator = orchestrator
        self.app = web.Application()
        self.setup_routes()
        self.setup_cors()
        
    def setup_routes(self):
        """Configure les routes de l'API"""
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/status', self.get_status)
        self.app.router.add_get('/metrics', self.get_metrics)
        self.app.router.add_get('/decisions', self.get_decisions_history)
        self.app.router.add_post('/control/start', self.start_orchestrator)
        self.app.router.add_post('/control/stop', self.stop_orchestrator)
        self.app.router.add_post('/control/force-decision', self.force_decision)
        self.app.router.add_get('/workflows/available', self.get_available_workflows)
        
    def setup_cors(self):
        """Configure CORS pour Grafana"""
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Add CORS to all routes
        for route in list(self.app.router.routes()):
            cors.add(route)
            
    async def health_check(self, request: web_request.Request) -> web.Response:
        """Health check endpoint"""
        return web.json_response({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "ai_orchestrator",
            "version": "1.0.0"
        })
        
    async def get_status(self, request: web_request.Request) -> web.Response:
        """Retourne le statut complet de l'orchestrateur"""
        try:
            status = self.orchestrator.get_status()
            
            # Ajouter des infos supplémentaires
            status.update({
                "timestamp": datetime.utcnow().isoformat(),
                "uptime_seconds": int(time.time() - getattr(self.orchestrator, 'start_time', time.time())),
                "api_version": "1.0.0"
            })
            
            return web.json_response(status)
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return web.json_response({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, status=500)
            
    async def get_metrics(self, request: web_request.Request) -> web.Response:
        """Métriques Prometheus pour Grafana"""
        try:
            status = self.orchestrator.get_status()
            
            # Format Prometheus
            metrics = f"""# HELP orchestrator_decisions_total Total number of decisions made
# TYPE orchestrator_decisions_total counter
orchestrator_decisions_total {status['performance_metrics']['total_decisions']}

# HELP orchestrator_successful_decisions_total Total number of successful decisions
# TYPE orchestrator_successful_decisions_total counter
orchestrator_successful_decisions_total {status['performance_metrics']['successful_decisions']}

# HELP orchestrator_success_rate Current success rate
# TYPE orchestrator_success_rate gauge
orchestrator_success_rate {status['success_rate']}

# HELP orchestrator_mode_switches_total Total number of mode switches
# TYPE orchestrator_mode_switches_total counter
orchestrator_mode_switches_total {status['performance_metrics']['mode_switches']}

# HELP orchestrator_system_load Current system load
# TYPE orchestrator_system_load gauge
orchestrator_system_load {status['environment_health']['system_load']}

# HELP orchestrator_market_volatility Current market volatility
# TYPE orchestrator_market_volatility gauge
orchestrator_market_volatility {status['environment_health']['volatility']}

# HELP orchestrator_running Is orchestrator running
# TYPE orchestrator_running gauge
orchestrator_running {1 if status['is_running'] else 0}
"""

            # Ajouter métriques API health
            for api_name, health_score in status['environment_health']['api_health'].items():
                metrics += f"""
# HELP api_health_{api_name} Health score for {api_name}
# TYPE api_health_{api_name} gauge
api_health_{api_name} {health_score}
"""

            return web.Response(text=metrics, content_type='text/plain')
            
        except Exception as e:
            logger.error(f"Error generating metrics: {e}")
            return web.Response(text=f"# Error generating metrics: {e}", 
                              content_type='text/plain', status=500)
            
    async def get_decisions_history(self, request: web_request.Request) -> web.Response:
        """Retourne l'historique des décisions"""
        try:
            # Limiter aux 100 dernières décisions
            limit = int(request.query.get('limit', 100))
            
            decisions = []
            for decision in self.orchestrator.decision_history[-limit:]:
                decisions.append({
                    "action": decision.action,
                    "mode": decision.mode.value,
                    "urgency": decision.urgency.value,
                    "confidence": decision.confidence,
                    "reasoning": decision.reasoning,
                    "timestamp": decision.timestamp,
                    "parameters": decision.parameters
                })
                
            return web.json_response({
                "decisions": decisions,
                "total_count": len(decisions),
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error getting decisions history: {e}")
            return web.json_response({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, status=500)
            
    async def start_orchestrator(self, request: web_request.Request) -> web.Response:
        """Démarre l'orchestrateur"""
        try:
            if self.orchestrator.is_running:
                return web.json_response({
                    "status": "already_running",
                    "message": "Orchestrator is already running"
                })
                
            # Démarrer en arrière-plan
            asyncio.create_task(self.orchestrator.start())
            
            return web.json_response({
                "status": "starting",
                "message": "Orchestrator start command sent",
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error starting orchestrator: {e}")
            return web.json_response({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, status=500)
            
    async def stop_orchestrator(self, request: web_request.Request) -> web.Response:
        """Arrête l'orchestrateur"""
        try:
            await self.orchestrator.stop()
            
            return web.json_response({
                "status": "stopped",
                "message": "Orchestrator stopped successfully",
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error stopping orchestrator: {e}")
            return web.json_response({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, status=500)
            
    async def force_decision(self, request: web_request.Request) -> web.Response:
        """Force une nouvelle décision immédiatement"""
        try:
            # Cette fonctionnalité nécessiterait une modification de l'orchestrateur
            # Pour l'instant, on retourne un message
            return web.json_response({
                "status": "not_implemented",
                "message": "Force decision feature will be implemented",
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error forcing decision: {e}")
            return web.json_response({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, status=500)
            
    async def get_available_workflows(self, request: web_request.Request) -> web.Response:
        """Retourne la liste des workflows disponibles"""
        try:
            workflows = self.orchestrator.workflow_orchestrator.n8n.get_available_workflows()
            
            return web.json_response({
                "workflows": workflows,
                "count": len(workflows),
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error getting workflows: {e}")
            return web.json_response({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }, status=500)

async def create_app(orchestrator: IntelligentOrchestrator) -> web.Application:
    """Crée l'application web"""
    api = OrchestratorAPI(orchestrator)
    return api.app

async def run_api_server(orchestrator: IntelligentOrchestrator, host: str = "0.0.0.0", port: int = 8080):
    """Lance le serveur API"""
    app = await create_app(orchestrator)
    
    logger.info(f"🌐 Starting API server on {host}:{port}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    logger.info(f"✅ API server running on http://{host}:{port}")
    
    # Endpoints disponibles
    logger.info("📡 Available endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  GET  /status - Full status")
    logger.info("  GET  /metrics - Prometheus metrics")
    logger.info("  GET  /decisions - Decisions history")
    logger.info("  POST /control/start - Start orchestrator")
    logger.info("  POST /control/stop - Stop orchestrator")
    logger.info("  GET  /workflows/available - Available workflows")
    
    return runner

# Test du serveur API
async def test_api():
    """Test du serveur API"""
    from .ai_orchestrator import IntelligentOrchestrator
    
    orchestrator = IntelligentOrchestrator()
    runner = await run_api_server(orchestrator)
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping API server...")
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(test_api()) 