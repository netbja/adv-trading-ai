"""
🚀 TRADING AI ETF - BACKEND PRINCIPAL
FastAPI application with ETF intelligent trading system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

from app.config import settings
from app.api.v1 import router as api_v1_router
from database.session import init_db

# Métriques Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Configuration du logger
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de cycle de vie de l'application"""
    logger.info("🚀 Démarrage du Trading AI ETF Backend")
    
    # Initialisation de la base de données
    await init_db()
    logger.info("✅ Base de données initialisée")
    
    # Initialisation des services
    logger.info("✅ Services initialisés")
    
    yield
    
    logger.info("🛑 Arrêt du Trading AI ETF Backend")

# Création de l'application FastAPI
app = FastAPI(
    title="Trading AI ETF Backend",
    description="Backend intelligent pour le trading d'ETF avec IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes principales
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "🧠 Trading AI ETF Backend",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "trading-ai-etf-backend",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/metrics")
async def get_metrics():
    """Métriques Prometheus"""
    return JSONResponse(
        content=generate_latest().decode('utf-8'),
        media_type=CONTENT_TYPE_LATEST
    )

@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware pour logger les requêtes"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Métriques
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    
    REQUEST_DURATION.observe(process_time)
    
    # Logging
    logger.info(
        "HTTP request processed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )
    
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Gestionnaire global d'exceptions"""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": "Une erreur inattendue s'est produite"
        }
    )

if __name__ == "__main__":
    import uvicorn
    import time
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    ) 