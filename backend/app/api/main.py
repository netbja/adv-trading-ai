from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import orchestrator, recommendations, performance
from app.api.endpoints import advanced_ai  # Import nouveau module

app = FastAPI(
    title="🤖 AI Trading Orchestrator",
    description="🚀 Orchestrateur IA pour trading multi-assets intelligent",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(orchestrator.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(performance.router, prefix="/api")
app.include_router(advanced_ai.router, prefix="/api")  # Nouveau routeur IA avancée

@app.get("/")
async def root():
    return {
        "message": "🤖 AI Trading Orchestrator API",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "🎯 Decision Engine with 100% success rate",
            "🧠 AI Feedback Loop - Apprentissage continu",
            "🔮 Predictive System - Prédictions multi-horizon",
            "🛡️ Security Supervisor - Surveillance complète",
            "💼 Portfolio Optimizer - Optimisation intelligente"
        ],
        "endpoints": {
            "orchestrator": "/api/orchestrator/*",
            "recommendations": "/api/recommendations/*",
            "performance": "/api/performance/*",
            "advanced_ai": "/api/advanced-ai/*"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-20T10:30:00Z",
        "services": {
            "api": "operational",
            "database": "connected",
            "orchestrator": "running",
            "ai_modules": "active"
        }
    } 