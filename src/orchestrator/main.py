#!/usr/bin/env python3
"""
🚀 MAIN ENTRY POINT - Intelligent AI Trading Orchestrator
Lance l'orchestrateur IA et l'API serveur en parallèle
"""

import asyncio
import logging
import os
import signal
import time
from typing import Optional

from .ai_orchestrator import IntelligentOrchestrator
from .api_server import run_api_server

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/orchestrator.log')
    ]
)
logger = logging.getLogger(__name__)

class OrchestrationSystem:
    """Système complet d'orchestration avec API"""
    
    def __init__(self):
        self.orchestrator = IntelligentOrchestrator()
        self.api_runner: Optional[object] = None
        self.is_running = False
        self.start_time = time.time()
        
        # Ajouter timestamp de démarrage à l'orchestrateur
        self.orchestrator.start_time = self.start_time
        
    async def start(self):
        """Démarre le système complet"""
        logger.info("🚀 Starting AI Trading Orchestration System...")
        
        # Vérifier les variables d'environnement critiques
        if not self._check_environment():
            logger.error("❌ Critical environment variables missing")
            return
            
        self.is_running = True
        
        try:
            # Démarrer l'API serveur
            logger.info("🌐 Starting API server...")
            self.api_runner = await run_api_server(
                self.orchestrator,
                host="0.0.0.0",
                port=int(os.getenv('ORCHESTRATOR_PORT', 8080))
            )
            
            # Attendre un peu que l'API soit prête
            await asyncio.sleep(2)
            
            # Démarrer l'orchestrateur principal
            logger.info("🧠 Starting AI Orchestrator...")
            orchestrator_task = asyncio.create_task(self.orchestrator.start())
            
            logger.info("✅ System fully operational!")
            logger.info(f"📊 API available at: http://localhost:{os.getenv('ORCHESTRATOR_PORT', 8080)}")
            logger.info("🔗 Key endpoints:")
            logger.info("   - /health - Health check")
            logger.info("   - /status - Full system status")
            logger.info("   - /metrics - Prometheus metrics for Grafana")
            
            # Attendre que l'orchestrateur se termine
            await orchestrator_task
            
        except Exception as e:
            logger.error(f"❌ Error in orchestration system: {e}")
            await self.stop()
            
    async def stop(self):
        """Arrête le système complet"""
        logger.info("🛑 Stopping AI Trading Orchestration System...")
        
        self.is_running = False
        
        # Arrêter l'orchestrateur
        if self.orchestrator.is_running:
            await self.orchestrator.stop()
            
        # Arrêter l'API serveur
        if self.api_runner:
            await self.api_runner.cleanup()
            
        logger.info("✅ System stopped successfully")
        
    def _check_environment(self) -> bool:
        """Vérifie que les variables d'environnement critiques sont présentes"""
        critical_vars = [
            'GROQ_API_KEY',
        ]
        
        missing_vars = []
        for var in critical_vars:
            if not os.getenv(var):
                missing_vars.append(var)
                
        if missing_vars:
            logger.error(f"❌ Missing environment variables: {missing_vars}")
            logger.error("💡 Please check your .env file or environment configuration")
            return False
            
        # Vérifications optionnelles avec avertissements
        optional_vars = {
            'N8N_USER': 'admin',
            'N8N_PASSWORD': 'TradingN8N2025!',
            'POSTGRES_USER': 'trader',
            'POSTGRES_PASSWORD': 'TradingDB2025!',
            'TELEGRAM_BOT_TOKEN': None
        }
        
        for var, default in optional_vars.items():
            if not os.getenv(var):
                if default:
                    logger.warning(f"⚠️  {var} not set, using default: {default}")
                else:
                    logger.warning(f"⚠️  {var} not set, some features may be disabled")
                    
        logger.info("✅ Environment check passed")
        return True
        
    def setup_signal_handlers(self):
        """Configure les gestionnaires de signaux pour arrêt propre"""
        def signal_handler(signum, frame):
            logger.info(f"📡 Received signal {signum}, initiating shutdown...")
            asyncio.create_task(self.stop())
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Point d'entrée principal"""
    
    print("""
🧠 AI TRADING ORCHESTRATOR
==========================
🤖 Intelligent CRON replacement powered by Groq AI
🔄 Dual-market support: Crypto + Forex
🌐 REST API for monitoring and control
📊 Grafana/Prometheus integration ready
    """)
    
    system = OrchestrationSystem()
    system.setup_signal_handlers()
    
    try:
        await system.start()
    except KeyboardInterrupt:
        logger.info("👋 Received interrupt signal")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        await system.stop()

if __name__ == "__main__":
    # Vérifier Python version
    import sys
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
        
    asyncio.run(main()) 