#!/usr/bin/env python3
"""
🧠 TRADING AI COMPLET - INTERFACE PROFESSIONNELLE
Dashboard avec authentification DB, workflows live et gestion des secrets
"""

import asyncio
import os
import logging
from datetime import datetime
from dataclasses import asdict
from fastapi import FastAPI, HTTPException, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import random

# Imports des modules
from src.auth.secure_auth import SecureAuthManager
from src.workflows.live_trading_engine import LiveTradingOrchestrator
from src.ui.workflow_pages import get_crypto_workflow_page, get_meme_workflow_page, get_forex_workflow_page, get_workflow_styles
from src.ui.workflow_js import get_workflow_javascript
from smart_capital_growth_system import IntelligentCompoundGrowth, AutonomousTradingMaster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'trader')}:{os.getenv('POSTGRES_PASSWORD', 'TradingDB2025!')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'trading_ai')}"
PORT = int(os.getenv("PORT", "8000"))

# Instances globales
app = FastAPI(title="🧠 Trading AI Professional", version="2.0.0")
auth_manager = SecureAuthManager(DATABASE_URL)
live_orchestrator = LiveTradingOrchestrator()
trading_master = None
security = HTTPBearer()

@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage"""
    global trading_master
    
    # Initialiser base de données
    await auth_manager.init_db()
    logger.info("✅ Base de données initialisée")
    
    # Initialiser système de trading
    trading_master = AutonomousTradingMaster(200.0)
    await trading_master.initialize_autonomous_system()
    logger.info("✅ Système de trading initialisé")
    
    # Démarrer workflows live en arrière-plan
    asyncio.create_task(live_orchestrator.start_live_workflows())
    logger.info("✅ Workflows live démarrés")

# Middleware d'authentification
async def get_current_user(request: Request, session_token: str = Cookie(None)):
    """Vérifie l'authentification via cookie de session"""
    if not session_token:
        return None
    
    user_data = await auth_manager.verify_session(session_token)
    return user_data

async def require_auth(request: Request, session_token: str = Cookie(None)):
    """Requiert une authentification valide"""
    user_data = await get_current_user(request, session_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Non authentifié")
    return user_data

@app.get("/", response_class=HTMLResponse)
async def dashboard_or_login(request: Request, session_token: str = Cookie(None)):
    """Page principale - dashboard ou login selon l'authentification"""
    user_data = await get_current_user(request, session_token)
    
    if not user_data:
        return get_login_page()
    else:
        return get_main_dashboard(user_data)

def get_login_page() -> HTMLResponse:
    """Page de connexion sécurisée"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading AI • Connexion Sécurisée</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .login-container {
                background: white;
                padding: 3rem;
                border-radius: 1rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 400px;
            }
            
            .logo {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .logo h1 {
                font-size: 2rem;
                color: #2563eb;
                margin-bottom: 0.5rem;
            }
            
            .logo p {
                color: #64748b;
                font-size: 0.9rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-label {
                display: block;
                font-weight: 600;
                color: #374151;
                margin-bottom: 0.5rem;
            }
            
            .form-input {
                width: 100%;
                padding: 0.75rem;
                border: 2px solid #e5e7eb;
                border-radius: 0.5rem;
                font-size: 1rem;
                transition: border-color 0.2s;
            }
            
            .form-input:focus {
                outline: none;
                border-color: #2563eb;
            }
            
            .btn-login {
                width: 100%;
                background: #2563eb;
                color: white;
                padding: 0.75rem;
                border: none;
                border-radius: 0.5rem;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }
            
            .btn-login:hover {
                background: #1d4ed8;
            }
            
            .error-message {
                background: #fef2f2;
                color: #dc2626;
                padding: 0.75rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                display: none;
            }
            
            .features {
                margin-top: 2rem;
                text-align: center;
                color: #64748b;
                font-size: 0.875rem;
            }
            
            .features ul {
                list-style: none;
                margin-top: 1rem;
            }
            
            .features li {
                margin: 0.5rem 0;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <h1>🧠 Trading AI</h1>
                <p>Interface Professionnelle Sécurisée</p>
            </div>
            
            <div class="error-message" id="error-message"></div>
            
            <form id="login-form">
                <div class="form-group">
                    <label class="form-label">Nom d'utilisateur</label>
                    <input type="text" class="form-input" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Mot de passe</label>
                    <input type="password" class="form-input" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn-login">Se connecter</button>
            </form>
            
            <div class="features">
                <strong>Fonctionnalités disponibles :</strong>
                <ul>
                    <li>🔐 Authentification sécurisée</li>
                    <li>💰 Gestion des wallets cryptés</li>
                    <li>📊 Workflows crypto & forex live</li>
                    <li>🤖 Trading autonome intelligent</li>
                    <li>⚡ Interface temps réel</li>
                </ul>
            </div>
        </div>
        
        <script>
            document.getElementById('login-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const errorDiv = document.getElementById('error-message');
                
                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        document.cookie = `session_token=${result.session_token}; path=/; max-age=86400`;
                        window.location.reload();
                    } else {
                        errorDiv.textContent = result.detail || 'Erreur de connexion';
                        errorDiv.style.display = 'block';
                    }
                } catch (error) {
                    errorDiv.textContent = 'Erreur de connexion au serveur';
                    errorDiv.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """)

def get_main_dashboard(user_data: dict) -> HTMLResponse:
    """Dashboard principal sécurisé"""
    # Récupérer les pages de workflows
    crypto_page = get_crypto_workflow_page()
    meme_page = get_meme_workflow_page()
    forex_page = get_forex_workflow_page()
    workflow_styles = get_workflow_styles()
    workflow_js = get_workflow_javascript()
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading AI • Dashboard Pro</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            /* === INTERFACE MODERNE - TRADING AI === */
            :root {{
                --primary: #3b82f6;
                --primary-dark: #1e40af;
                --secondary: #64748b;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --bg-main: #f8fafc;
                --bg-card: #ffffff;
                --bg-hero: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --border: #e2e8f0;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --text-muted: #94a3b8;
                --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
                --shadow: 0 4px 6px rgba(0,0,0,0.07);
                --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
                --shadow-xl: 0 20px 25px rgba(0,0,0,0.1);
                --sidebar-width: 280px;
                --border-radius: 12px;
                --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
                background: var(--bg-main);
                color: var(--text-primary);
                line-height: 1.6;
                font-size: 14px;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}
            
            .app-layout {{
                display: grid;
                grid-template-columns: var(--sidebar-width) 1fr;
                min-height: 100vh;
            }}
            
            /* === SIDEBAR MODERNE === */
            .sidebar {{
                background: var(--bg-card);
                border-right: 1px solid var(--border);
                position: fixed;
                left: 0;
                top: 0;
                width: var(--sidebar-width);
                height: 100vh;
                overflow-y: auto;
                z-index: 100;
                box-shadow: var(--shadow);
            }}
            
            .sidebar-header {{
                padding: 2rem 1.5rem;
                background: var(--bg-hero);
                color: white;
            }}
            
            .sidebar-header h1 {{
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}
            
            .user-info {{
                font-size: 0.875rem;
                opacity: 0.9;
                font-weight: 500;
            }}
            
            .nav-menu {{
                padding: 1.5rem 0;
            }}
            
            .nav-section {{
                margin-bottom: 2rem;
            }}
            
            .nav-section-title {{
                padding: 0 1.5rem 0.75rem;
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: var(--text-muted);
            }}
            
            .nav-item {{
                margin: 0.25rem 1rem;
            }}
            
            .nav-link {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.875rem 1rem;
                border-radius: 8px;
                color: var(--text-secondary);
                text-decoration: none;
                transition: var(--transition);
                font-weight: 500;
                cursor: pointer;
                font-size: 0.875rem;
            }}
            
            .nav-link:hover {{
                background: #f1f5f9;
                color: var(--primary);
                transform: translateX(2px);
            }}
            
            .nav-link.active {{
                background: #dbeafe;
                color: var(--primary);
                font-weight: 600;
                box-shadow: var(--shadow-sm);
            }}
            
            .nav-icon {{
                font-size: 1.125rem;
                width: 20px;
                text-align: center;
            }}
            
            .status-indicator {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-left: auto;
            }}
            
            .status-active {{ background: var(--success); }}
            .status-scanning {{ background: var(--warning); animation: pulse 2s infinite; }}
            .status-idle {{ background: var(--secondary); }}
            
            /* === MAIN CONTENT === */
            .main-content {{
                margin-left: var(--sidebar-width);
                min-height: 100vh;
            }}
            
            .topbar {{
                background: var(--bg-card);
                border-bottom: 1px solid var(--border);
                padding: 1.25rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 50;
                backdrop-filter: blur(10px);
                background: rgba(255, 255, 255, 0.9);
            }}
            
            .topbar-title {{
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-primary);
            }}
            
            .topbar-actions {{
                display: flex;
                gap: 1rem;
                align-items: center;
            }}
            
            .btn {{
                padding: 0.625rem 1.25rem;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: var(--transition);
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.875rem;
                white-space: nowrap;
            }}
            
            .btn-primary {{ 
                background: var(--primary); 
                color: white; 
                box-shadow: var(--shadow-sm);
            }}
            
            .btn-danger {{ 
                background: var(--danger); 
                color: white; 
            }}
            
            .btn:hover {{ 
                transform: translateY(-1px); 
                box-shadow: var(--shadow);
            }}
            
            .btn-icon {{
                font-size: 1rem;
            }}
            
            .content-area {{
                padding: 2rem;
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            .page-content {{
                display: none;
            }}
            
            .page-content.active {{
                display: block;
                animation: fadeIn 0.3s ease;
            }}
            
            /* === HERO SECTION === */
            .overview-hero {{
                background: var(--bg-card);
                border-radius: var(--border-radius);
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: var(--shadow);
                border: 1px solid var(--border);
            }}
            
            .hero-content {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 2rem;
            }}
            
            .hero-main {{
                flex: 1;
            }}
            
            .hero-title {{
                font-size: 1.875rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 1.5rem;
            }}
            
            .hero-metrics {{
                display: flex;
                gap: 3rem;
                align-items: center;
            }}
            
            .metric-primary {{
                text-align: center;
            }}
            
            .metric-label {{
                display: block;
                font-size: 0.875rem;
                color: var(--text-secondary);
                font-weight: 600;
                margin-bottom: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            
            .metric-value {{
                display: block;
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--text-primary);
                line-height: 1;
                margin-bottom: 0.25rem;
            }}
            
            .metric-change {{
                font-size: 1rem;
                font-weight: 600;
            }}
            
            .metric-change.positive {{ color: var(--success); }}
            .metric-change.negative {{ color: var(--danger); }}
            
            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1.5rem;
            }}
            
            .metric-item {{
                text-align: center;
                padding: 1rem;
                background: #f8fafc;
                border-radius: 8px;
                border: 1px solid var(--border);
            }}
            
            .metric-number {{
                display: block;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.25rem;
            }}
            
            .metric-text {{
                font-size: 0.75rem;
                color: var(--text-secondary);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            
            .hero-actions {{
                display: flex;
                flex-direction: column;
                gap: 1rem;
                align-items: flex-end;
            }}
            
            .status-info {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.875rem;
                color: var(--text-secondary);
            }}
            
            /* === WORKFLOWS CARDS === */
            .workflows-section {{
                margin-bottom: 2rem;
            }}
            
            .section-header {{
                margin-bottom: 1.5rem;
            }}
            
            .section-header h3 {{
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.25rem;
            }}
            
            .section-header p {{
                color: var(--text-secondary);
                font-size: 0.875rem;
            }}
            
            .workflow-cards-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 1.5rem;
            }}
            
            .workflow-card {{
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                cursor: pointer;
                transition: var(--transition);
                box-shadow: var(--shadow-sm);
                position: relative;
                overflow: hidden;
            }}
            
            .workflow-card:hover {{
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
                border-color: var(--primary);
            }}
            
            .workflow-card.crypto {{
                border-top: 3px solid #f59e0b;
            }}
            
            .workflow-card.meme {{
                border-top: 3px solid #8b5cf6;
            }}
            
            .workflow-card.forex {{
                border-top: 3px solid #3b82f6;
            }}
            
            .card-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }}
            
            .card-icon {{
                font-size: 2rem;
                width: 48px;
                height: 48px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            }}
            
            .card-status {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
            
            .status-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
            }}
            
            .status-text {{
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            
            .card-content h4 {{
                font-size: 1.125rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
            }}
            
            .card-content p {{
                color: var(--text-secondary);
                font-size: 0.875rem;
                margin-bottom: 1rem;
            }}
            
            .card-metrics {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }}
            
            .card-metric {{
                text-align: center;
            }}
            
            .card-metric .value {{
                display: block;
                font-size: 1.125rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.25rem;
            }}
            
            .card-metric .value.positive {{ color: var(--success); }}
            .card-metric .value.warning {{ color: var(--warning); }}
            
            .card-metric .label {{
                font-size: 0.75rem;
                color: var(--text-secondary);
                font-weight: 500;
            }}
            
            .card-footer {{
                margin-top: 1rem;
                padding-top: 1rem;
                border-top: 1px solid var(--border);
                text-align: center;
            }}
            
            .view-details {{
                color: var(--primary);
                font-weight: 600;
                font-size: 0.875rem;
            }}
            
            /* === ACTIVITY TIMELINE === */
            .activity-section {{
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: var(--border-radius);
                padding: 1.5rem;
                box-shadow: var(--shadow-sm);
            }}
            
            .activity-timeline {{
                max-height: 300px;
                overflow-y: auto;
            }}
            
            /* === ANIMATIONS === */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            
            /* === RESPONSIVE === */
            @media (max-width: 1024px) {{
                :root {{
                    --sidebar-width: 260px;
                }}
                
                .hero-content {{
                    flex-direction: column;
                    gap: 1.5rem;
                }}
                
                .hero-metrics {{
                    flex-direction: column;
                    gap: 2rem;
                    align-items: stretch;
                }}
                
                .metric-grid {{
                    grid-template-columns: repeat(3, 1fr);
                }}
            }}
            
            @media (max-width: 768px) {{
                .app-layout {{
                    grid-template-columns: 1fr;
                }}
                
                .sidebar {{
                    transform: translateX(-100%);
                    transition: transform 0.3s ease;
                }}
                
                .main-content {{
                    margin-left: 0;
                }}
                
                .content-area {{
                    padding: 1rem;
                }}
                
                .workflow-cards-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .metric-grid {{
                    grid-template-columns: 1fr;
                    gap: 1rem;
                }}
                
                .hero-metrics {{
                    gap: 1.5rem;
                }}
                
                .card-metrics {{
                    grid-template-columns: 1fr;
                }}
            }}
            
            /* === UTILITIES === */
            .positive {{ color: var(--success) !important; }}
            .negative {{ color: var(--danger) !important; }}
            .warning {{ color: var(--warning) !important; }}
            
            /* Suppression des anciens styles non utilisés */
        </style>
    </head>
    <body>
        <div class="app-layout">
            <!-- Sidebar -->
            <aside class="sidebar">
                <div class="sidebar-header">
                    <h1>🧠 Trading AI Pro</h1>
                    <div class="user-info">
                        Connecté: {user_data['username']} ({user_data['role']})
                    </div>
                </div>
                
                <nav class="nav-menu">
                    <div class="nav-section">
                        <div class="nav-section-title">Dashboard</div>
                        <div class="nav-item">
                            <a class="nav-link active" onclick="showPage('overview')">
                                <span class="nav-icon">📊</span>
                                Vue d'ensemble
                                <div class="status-indicator status-active"></div>
                            </a>
                        </div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('capital')">
                                <span class="nav-icon">💰</span>
                                Capital & Performance
                            </a>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <div class="nav-section-title">Workflows Live</div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('crypto-workflow')">
                                <span class="nav-icon">₿</span>
                                Crypto Principal
                                <div class="status-indicator status-active pulse"></div>
                            </a>
                        </div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('meme-workflow')">
                                <span class="nav-icon">🐸</span>
                                Crypto Meme
                                <div class="status-indicator status-active pulse"></div>
                            </a>
                        </div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('forex-workflow')">
                                <span class="nav-icon">💱</span>
                                Forex Trading
                                <div class="status-indicator status-active pulse"></div>
                            </a>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <div class="nav-section-title">Gestion</div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('wallets')">
                                <span class="nav-icon">🔐</span>
                                Wallets & Secrets
                            </a>
                        </div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('settings')">
                                <span class="nav-icon">⚙️</span>
                                Paramètres
                            </a>
                        </div>
                        <div class="nav-item">
                            <a class="nav-link" onclick="showPage('logs')">
                                <span class="nav-icon">📋</span>
                                Logs Système
                            </a>
                        </div>
                    </div>
                </nav>
            </aside>
            
            <!-- Main content -->
            <main class="main-content">
                <header class="topbar">
                    <h1 class="topbar-title" id="page-title">Vue d'ensemble</h1>
                    <div class="topbar-actions">
                        <button class="btn btn-danger" onclick="logout()">🚪 Déconnexion</button>
                    </div>
                </header>
                
                <div class="content-area">
                    <!-- Page Vue d'ensemble - Interface moderne -->
                    <div id="overview-page" class="page-content active">
                        <!-- Header avec métriques principales -->
                        <div class="overview-hero">
                            <div class="hero-content">
                                <div class="hero-main">
                                    <h2 class="hero-title">Portfolio Trading AI</h2>
                                    <div class="hero-metrics">
                                        <div class="metric-primary">
                                            <span class="metric-label">Capital Total</span>
                                            <span class="metric-value" id="current-capital">200.00€</span>
                                            <span class="metric-change positive" id="total-return">+0.00%</span>
                                        </div>
                                        <div class="metric-grid">
                                            <div class="metric-item">
                                                <span class="metric-number" id="system-efficiency">100%</span>
                                                <span class="metric-text">Efficacité</span>
                                            </div>
                                            <div class="metric-item">
                                                <span class="metric-number">3</span>
                                                <span class="metric-text">Workflows Actifs</span>
                                            </div>
                                            <div class="metric-item">
                                                <span class="metric-number" id="system-uptime">1</span>
                                                <span class="metric-text">Jour(s) Uptime</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="hero-actions">
                                    <button class="btn btn-primary" onclick="refreshData()">
                                        <span class="btn-icon">🔄</span>
                                        Actualiser
                                    </button>
                                    <div class="status-info">
                                        <div class="status-indicator status-active"></div>
                                        <span id="last-update">Dernière MAJ: --:--</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Cartes Workflows avec navigation -->
                        <div class="workflows-section">
                            <div class="section-header">
                                <h3>🚀 Workflows de Trading</h3>
                                <p>Cliquez sur un workflow pour voir les détails</p>
                            </div>
                            
                            <div class="workflow-cards-grid">
                                <div class="workflow-card crypto" onclick="showPage('crypto-workflow')">
                                    <div class="card-header">
                                        <div class="card-icon">₿</div>
                                        <div class="card-status">
                                            <span class="status-dot status-active"></span>
                                            <span class="status-text">Actif</span>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <h4>Crypto Principal</h4>
                                        <p>BTC, ETH, principales altcoins</p>
                                        <div class="card-metrics">
                                            <div class="card-metric">
                                                <span class="value">0</span>
                                                <span class="label">Signaux aujourd'hui</span>
                                            </div>
                                            <div class="card-metric">
                                                <span class="value positive">+0.0%</span>
                                                <span class="label">Performance 7j</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card-footer">
                                        <span class="view-details">Voir détails →</span>
                                    </div>
                                </div>
                                
                                <div class="workflow-card meme" onclick="showPage('meme-workflow')">
                                    <div class="card-header">
                                        <div class="card-icon">🐸</div>
                                        <div class="card-status">
                                            <span class="status-dot status-scanning"></span>
                                            <span class="status-text">Scan en cours</span>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <h4>Crypto Meme</h4>
                                        <p>Tokens viraux, analyse sentiment</p>
                                        <div class="card-metrics">
                                            <div class="card-metric">
                                                <span class="value">0</span>
                                                <span class="label">Tokens scannés</span>
                                            </div>
                                            <div class="card-metric">
                                                <span class="value warning">MEDIUM</span>
                                                <span class="label">Niveau de risque</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card-footer">
                                        <span class="view-details">Voir détails →</span>
                                    </div>
                                </div>
                                
                                <div class="workflow-card forex" onclick="showPage('forex-workflow')">
                                    <div class="card-header">
                                        <div class="card-icon">💱</div>
                                        <div class="card-status">
                                            <span class="status-dot status-active"></span>
                                            <span class="status-text">Actif</span>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <h4>Forex Trading</h4>
                                        <p>EUR/USD, GBP/USD, USD/JPY</p>
                                        <div class="card-metrics">
                                            <div class="card-metric">
                                                <span class="value">102.5</span>
                                                <span class="label">USD Strength Index</span>
                                            </div>
                                            <div class="card-metric">
                                                <span class="value positive">+0.35%</span>
                                                <span class="label">Performance 24h</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card-footer">
                                        <span class="view-details">Voir détails →</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Activité récente compacte -->
                        <div class="activity-section">
                            <div class="section-header">
                                <h3>⚡ Activité Récente</h3>
                            </div>
                            <div class="activity-timeline" id="recent-activity">
                                <!-- Contenu chargé dynamiquement -->
                            </div>
                        </div>
                    </div>
                    
                    <!-- Pages Workflows complètes -->
                    <div id="crypto-workflow-page" class="page-content">
                        {crypto_page}
                    </div>
                    
                    <div id="meme-workflow-page" class="page-content">
                        {meme_page}
                    </div>
                    
                    <div id="forex-workflow-page" class="page-content">
                        {forex_page}
                    </div>
                    
                    <!-- Autres pages (en développement) -->
                    <div id="capital-page" class="page-content">
                        <h2>Capital & Performance - En développement</h2>
                    </div>
                    
                    <div id="wallets-page" class="page-content">
                        <h2>Wallets & Secrets - En développement</h2>
                    </div>
                    
                    <div id="settings-page" class="page-content">
                        <h2>Paramètres - En développement</h2>
                    </div>
                    
                    <div id="logs-page" class="page-content">
                        <h2>Logs Système - En développement</h2>
                    </div>
                </div>
            </main>
        </div>
        
        <script>
            let currentPage = 'overview';
            
            function showPage(pageId) {{
                // Nettoyer les anciens workflows
                if (currentPage.includes('workflow')) {{
                    cleanupWorkflowPage(currentPage.replace('-page', ''));
                }}
                
                // Cacher toutes les pages
                document.querySelectorAll('.page-content').forEach(page => {{
                    page.classList.remove('active');
                }});
                
                // Désactiver tous les liens nav
                document.querySelectorAll('.nav-link').forEach(link => {{
                    link.classList.remove('active');
                }});
                
                // Afficher la page sélectionnée
                const targetPage = document.getElementById(pageId + '-page');
                if (targetPage) {{
                    targetPage.classList.add('active');
                }}
                
                // Activer le lien nav correspondant
                const navLinks = document.querySelectorAll('.nav-link');
                navLinks.forEach(link => {{
                    if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(pageId)) {{
                        link.classList.add('active');
                    }}
                }});
                
                // Mettre à jour le titre
                const titles = {{
                    'overview': 'Vue d\\'ensemble',
                    'capital': 'Capital & Performance',
                    'crypto-workflow': 'Workflow Crypto Principal',
                    'meme-workflow': 'Workflow Crypto Meme',
                    'forex-workflow': 'Workflow Forex Trading',
                    'wallets': 'Wallets & Secrets',
                    'settings': 'Paramètres',
                    'logs': 'Logs Système'
                }};
                
                const titleElement = document.getElementById('page-title');
                if (titleElement) {{
                    titleElement.textContent = titles[pageId] || pageId;
                }}
                
                currentPage = pageId;
                
                // Charger les données de la page
                loadPageData(pageId);
                
                // Scroll vers le haut
                window.scrollTo(0, 0);
            }}
            
            // Améliorer la gestion des clics sur les liens de navigation
            document.addEventListener('DOMContentLoaded', function() {{
                // Ajouter les event listeners pour tous les liens de navigation
                const navLinks = document.querySelectorAll('.nav-link[onclick]');
                navLinks.forEach(link => {{
                    link.addEventListener('click', function(e) {{
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Extraire le pageId de l'attribut onclick
                        const onclickAttr = this.getAttribute('onclick');
                        const match = onclickAttr.match(/showPage\\('([^']+)'\\)/);
                        
                        if (match) {{
                            const pageId = match[1];
                            showPage(pageId);
                        }}
                    }});
                    
                    // Améliorer l'accessibilité
                    link.setAttribute('role', 'button');
                    link.setAttribute('tabindex', '0');
                    
                    // Support du clavier
                    link.addEventListener('keydown', function(e) {{
                        if (e.key === 'Enter' || e.key === ' ') {{
                            e.preventDefault();
                            this.click();
                        }}
                    }});
                }});
                
                // Charger les données initiales
                loadOverviewData();
                
                // Auto-refresh amélioré
                startAutoRefresh();
            }});
            
            function startAutoRefresh() {{
                // Refresh toutes les 30 secondes pour la vue d'ensemble
                setInterval(() => {{
                    if (currentPage === 'overview') {{
                        loadOverviewData();
                    }}
                }}, 30000);
            }}
            
            async function loadPageData(pageId) {{
                try {{
                    if (pageId === 'overview') {{
                        await loadOverviewData();
                    }} else if (pageId.includes('workflow')) {{
                        const workflowType = pageId.replace('-workflow', '');
                        await loadWorkflowPage(workflowType);
                    }}
                }} catch (error) {{
                    console.error('Erreur chargement page:', error);
                    showNotification('Erreur de chargement des données', 'error');
                }}
            }}
            
            async function loadOverviewData() {{
                try {{
                    // Ajouter indicateur de chargement
                    const lastUpdateElement = document.getElementById('last-update');
                    if (lastUpdateElement) {{
                        lastUpdateElement.textContent = 'Chargement...';
                    }}
                    
                    // Charger données dashboard
                    const dashResponse = await fetch('/api/dashboard');
                    if (!dashResponse.ok) {{
                        throw new Error('Erreur API dashboard');
                    }}
                    const dashData = await dashResponse.json();
                    
                    // Mettre à jour métriques avec animation
                    updateMetricWithAnimation('current-capital', dashData.capital_growth.current.toFixed(2) + '€');
                    updateMetricWithAnimation('total-return', 
                        (dashData.capital_growth.total_return_pct > 0 ? '+' : '') + 
                        dashData.capital_growth.total_return_pct.toFixed(1) + '%');
                    updateMetricWithAnimation('system-efficiency', 
                        dashData.capital_growth.system_efficiency_pct.toFixed(0) + '%');
                    updateMetricWithAnimation('system-uptime', 
                        dashData.uptime_days + ' jour(s)');
                    
                    // Charger statut workflows
                    const workflowResponse = await fetch('/api/workflows/live-status');
                    if (workflowResponse.ok) {{
                        const workflowData = await workflowResponse.json();
                        updateWorkflowPerformance(workflowData);
                        updateRecentActivity(workflowData);
                    }}
                    
                    // Mettre à jour timestamp
                    if (lastUpdateElement) {{
                        lastUpdateElement.textContent = 'Dernière MAJ: ' + new Date().toLocaleTimeString();
                    }}
                    
                }} catch (error) {{
                    console.error('Erreur chargement données:', error);
                    showNotification('Erreur de connexion aux données', 'error');
                    
                    // Afficher état offline
                    const lastUpdateElement = document.getElementById('last-update');
                    if (lastUpdateElement) {{
                        lastUpdateElement.textContent = 'Erreur de connexion';
                    }}
                }}
            }}
            
            function updateMetricWithAnimation(elementId, value) {{
                const element = document.getElementById(elementId);
                if (element && element.textContent !== value) {{
                    element.style.transform = 'scale(1.1)';
                    element.style.transition = 'transform 0.2s ease';
                    
                    setTimeout(() => {{
                        element.textContent = value;
                        element.style.transform = 'scale(1)';
                    }}, 100);
                }}
            }}
            
            function updateWorkflowPerformance(data) {{
                const performanceContainer = document.getElementById('workflow-performance');
                if (!performanceContainer) return;
                
                const workflows = [
                    {{ 
                        key: 'crypto', 
                        title: 'Crypto Principal', 
                        icon: '₿',
                        color: 'crypto'
                    }},
                    {{ 
                        key: 'meme', 
                        title: 'Crypto Meme', 
                        icon: '🐸',
                        color: 'meme'
                    }},
                    {{ 
                        key: 'forex', 
                        title: 'Forex Trading', 
                        icon: '💱',
                        color: 'forex'
                    }}
                ];
                
                performanceContainer.innerHTML = workflows.map(workflow => {{
                    const workflowData = data[workflow.key] || {{}};
                    const performance = workflowData.performance || {{}};
                    
                    // Simulation de données de performance sur 7 jours
                    const weekPerformance = performance.weekly_gains || [
                        0.5, -0.2, 1.2, 0.8, -0.1, 1.5, 0.9
                    ];
                    
                    const totalGain = performance.total_gain || 0;
                    const gainPercentage = performance.gain_percentage || 0;
                    const trades = performance.total_trades || 0;
                    const winRate = performance.win_rate || 0;
                    const avgGain = performance.avg_gain_per_trade || 0;
                    
                    // Créer les barres du graphique
                    const chartBars = weekPerformance.map((gain, index) => {{
                        const height = Math.max(Math.abs(gain) * 30, 4); // Min 4px
                        const gainClass = gain >= 0 ? 'positive' : 'negative';
                        return `<div class="chart-bar ${{gainClass}}" style="height: ${{height}}px" title="Jour ${{index + 1}}: ${{gain > 0 ? '+' : ''}}${{gain}}%"></div>`;
                    }}).join('');
                    
                    const gainClass = totalGain >= 0 ? 'positive' : 'negative';
                    const gainSign = totalGain >= 0 ? '+' : '';
                    const percentageSign = gainPercentage >= 0 ? '+' : '';
                    
                    return `
                        <div class="performance-card ${{workflow.color}}">
                            <div class="performance-header">
                                <div class="performance-title">
                                    <div class="performance-icon">${{workflow.icon}}</div>
                                    <span>${{workflow.title}}</span>
                                </div>
                                <div class="performance-gain">
                                    <div class="gain-amount ${{gainClass}}">
                                        ${{gainSign}}${{totalGain.toFixed(2)}}€
                                    </div>
                                    <div class="gain-percentage ${{gainClass}}">
                                        ${{percentageSign}}${{gainPercentage.toFixed(1)}}%
                                    </div>
                                </div>
                            </div>
                            
                            <div class="performance-chart">
                                <div class="mini-chart">
                                    ${{chartBars}}
                                </div>
                            </div>
                            
                            <div class="performance-stats">
                                <div class="stat-item">
                                    <div class="stat-value">${{trades}}</div>
                                    <div class="stat-label">Trades</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-value">${{winRate.toFixed(0)}}%</div>
                                    <div class="stat-label">Win Rate</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-value">${{avgGain > 0 ? '+' : ''}}${{avgGain.toFixed(2)}}€</div>
                                    <div class="stat-label">Moy/Trade</div>
                                </div>
                            </div>
                        </div>
                    `;
                }}).join('');
                
                // Animation des barres après insertion
                setTimeout(() => {{
                    document.querySelectorAll('.chart-bar').forEach((bar, index) => {{
                        bar.style.animationDelay = `${{index * 0.1}}s`;
                    }});
                }}, 100);
            }}
            
            function updateRecentActivity(data) {{
                const activityContainer = document.getElementById('recent-activity');
                if (!activityContainer) return;
                
                const systemHealth = data.system_health || {{}};
                
                // Simuler activité récente basée sur les données système
                const activities = [
                    {{
                        type: 'crypto',
                        title: 'Scan crypto terminé',
                        description: `${{systemHealth.total_executions || 0}} exécutions totales`,
                        time: '2 min'
                    }},
                    {{
                        type: 'forex',
                        title: 'Analyse forex',
                        description: 'EUR/USD signal détecté',
                        time: '5 min'
                    }},
                    {{
                        type: 'meme',
                        title: 'Tokens meme scannés',
                        description: 'Aucun signal fort',
                        time: '8 min'
                    }}
                ];
                
                activityContainer.innerHTML = activities.map(activity => `
                    <div class="activity-item">
                        <div class="activity-icon ${{activity.type}}">
                            ${{activity.type === 'crypto' ? '₿' : 
                               activity.type === 'forex' ? '💱' : '🐸'}}
                        </div>
                        <div class="activity-content">
                            <div class="activity-title">${{activity.title}}</div>
                            <div class="activity-description">${{activity.description}}</div>
                            <div class="activity-time">il y a ${{activity.time}}</div>
                        </div>
                    </div>
                `).join('');
            }}
            
            async function refreshData() {{
                await loadPageData(currentPage);
                showNotification('Données actualisées', 'success');
            }}
            
            function logout() {{
                if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {{
                    document.cookie = 'session_token=; path=/; max-age=0';
                    window.location.reload();
                }}
            }}
            
            // Système de notifications
            function showNotification(message, type = 'info') {{
                const notification = document.createElement('div');
                notification.className = `notification notification-${{type}}`;
                notification.textContent = message;
                
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 1rem 1.5rem;
                    border-radius: 0.5rem;
                    color: white;
                    font-weight: 600;
                    z-index: 1000;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                `;
                
                if (type === 'success') {{
                    notification.style.background = '#10b981';
                }} else if (type === 'error') {{
                    notification.style.background = '#ef4444';
                }} else {{
                    notification.style.background = '#3b82f6';
                }}
                
                document.body.appendChild(notification);
                
                // Animation d'entrée
                setTimeout(() => {{
                    notification.style.transform = 'translateX(0)';
                }}, 100);
                
                // Suppression automatique
                setTimeout(() => {{
                    notification.style.transform = 'translateX(100%)';
                    setTimeout(() => {{
                        if (notification.parentNode) {{
                            notification.parentNode.removeChild(notification);
                        }}
                    }}, 300);
                }}, 3000);
            }}
            
            {workflow_js}
        </script>
    </body>
    </html>
    """)

# API ENDPOINTS
@app.post("/api/login")
async def login(request: Request):
    """Endpoint de connexion"""
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username et password requis")
        
        # Obtenir IP et User-Agent
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Authentifier
        user_data = await auth_manager.authenticate_user(username, password, client_ip, user_agent)
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Identifiants invalides")
        
        return user_data
        
    except Exception as e:
        logger.error(f"Erreur login: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/dashboard")
async def get_dashboard_data(user_data: dict = Depends(require_auth)):
    """Données du dashboard principal"""
    if not trading_master:
        raise HTTPException(status_code=503, detail="Système non initialisé")
    
    days_elapsed = (datetime.now() - trading_master.capital_manager.start_date).days + 1
    compound_stats = trading_master.capital_manager.calculate_compound_growth(days_elapsed)
    milestone_progress = trading_master.capital_manager.get_next_milestone_progress()
    
    return {
        "user": user_data,
        "capital_growth": {
            "initial": compound_stats["initial_capital"],
            "current": compound_stats["current_capital"],
            "total_return_pct": compound_stats["actual_return_pct"],
            "system_efficiency_pct": compound_stats["system_efficiency_pct"],
            "annualized_return_pct": compound_stats["annualized_return"]
        },
        "milestone_progress": milestone_progress,
        "uptime_days": days_elapsed,
        "system_active": trading_master.active
    }

@app.get("/api/workflows/live-status")
async def get_live_workflows_status(user_data: dict = Depends(require_auth)):
    """Statut live des workflows avec données de performance"""
    # Simulation de données de performance pour chaque workflow
    def generate_performance_data(base_performance=1.0):
        # Générer 7 jours de données
        weekly_gains = []
        total_gain = 0
        
        for i in range(7):
            # Simulation d'un gain/perte journalier
            daily_gain = random.uniform(-2, 3) * base_performance
            weekly_gains.append(round(daily_gain, 1))
            total_gain += daily_gain * 5  # Multiplié par capital fictif
        
        win_rate = random.uniform(60, 85)
        total_trades = random.randint(15, 45)
        
        return {
            "weekly_gains": weekly_gains,
            "total_gain": round(total_gain, 2),
            "gain_percentage": round(sum(weekly_gains), 1),
            "total_trades": total_trades,
            "win_rate": round(win_rate, 1),
            "avg_gain_per_trade": round(total_gain / total_trades if total_trades > 0 else 0, 2)
        }
    
    return {
        "crypto": {
            "status": "idle",
            "current_execution": None,
            "performance": generate_performance_data(1.2)  # Crypto plus performant
        },
        "meme": {
            "status": "scanning", 
            "current_execution": {
                "start_time": datetime.now().isoformat(),
                "status": "scanning"
            },
            "performance": generate_performance_data(0.8)  # Meme plus risqué
        },
        "forex": {
            "status": "idle",
            "current_execution": None,
            "performance": generate_performance_data(1.0)  # Forex stable
        },
        "system_health": {
            "total_executions": random.randint(150, 300),
            "uptime_hours": 24 * 7,  # 7 jours
            "error_rate": round(random.uniform(0.1, 2.5), 1)
        }
    }

@app.post("/api/logout")
async def logout(request: Request, session_token: str = Cookie(None)):
    """Déconnexion"""
    if session_token:
        await auth_manager.logout_user(session_token)
    
    response = JSONResponse({"message": "Déconnecté"})
    response.delete_cookie("session_token")
    return response

# Nouveaux API ENDPOINTS pour workflows détaillés

@app.get("/api/workflows/crypto/details")
async def get_crypto_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow crypto"""
    try:
        crypto_engine = live_orchestrator.crypto_engine
        current_execution = crypto_engine.current_execution
        
        # Simuler données réalistes
        return {
            "pairs_monitored": len(crypto_engine.target_pairs),
            "signals_today": len([s for s in crypto_engine.signal_history if s.timestamp.date() == datetime.now().date()]),
            "avg_confidence": 0.75,
            "next_scan_in_seconds": 180,
            "current_execution": asdict(current_execution) if current_execution else None,
            "pairs_data": {
                pair: {
                    "price": 45000.0 if "BTC" in pair else 2500.0 if "ETH" in pair else 100.0,
                    "change_24h": 2.5,
                    "volume_24h": 250000000
                } for pair in crypto_engine.target_pairs
            },
            "recent_signals": [asdict(s) for s in crypto_engine.signal_history[-10:]]
        }
    except Exception as e:
        logger.error(f"Erreur crypto workflow details: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/meme/details")
async def get_meme_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow meme"""
    try:
        meme_engine = live_orchestrator.meme_engine
        current_execution = meme_engine.current_execution
        
        return {
            "tokens_scanned": len(meme_engine.target_tokens),
            "max_viral_score": 85,
            "total_social_mentions": 1250,
            "overall_risk_level": "MEDIUM",
            "current_execution": asdict(current_execution) if current_execution else None,
            "tokens_data": {
                token: {
                    "viral_score": 65,
                    "social_mentions": 250,
                    "change_24h": 15.2,
                    "whale_activity": "medium"
                } for token in meme_engine.target_tokens
            },
            "risk_analysis": {
                token: {
                    "risk_level": "MEDIUM",
                    "risk_score": 45,
                    "factors": {
                        "volatility": 25.5,
                        "social_activity": 250,
                        "whale_activity": "medium"
                    }
                } for token in meme_engine.target_tokens
            },
            "viral_alerts": []
        }
    except Exception as e:
        logger.error(f"Erreur meme workflow details: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/forex/details")
async def get_forex_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow forex"""
    try:
        forex_engine = live_orchestrator.forex_engine
        current_execution = forex_engine.current_execution
        
        return {
            "pairs_active": len(forex_engine.currency_pairs),
            "usd_strength_index": 102.5,
            "avg_volatility": 0.021,
            "active_signals_count": 2,
            "current_execution": asdict(current_execution) if current_execution else None,
            "pairs_data": {
                pair: {
                    "current_rate": 1.0850 if "EUR" in pair else 1.2650 if "GBP" in pair else 149.50,
                    "change_24h": 0.35,
                    "trend": "Haussier"
                } for pair in forex_engine.currency_pairs
            },
            "economic_data": {
                "usd_strength_index": 102.5,
                "global_risk_sentiment": "risk_on",
                "central_bank_sentiment": {
                    "fed": "hawkish",
                    "ecb": "neutral"
                },
                "economic_calendar": {
                    "high_impact_events_today": 2
                }
            },
            "correlations": {
                "EUR/USD_vs_GBP/USD": 0.75,
                "USD/JPY_vs_risk_sentiment": -0.65,
                "AUD/USD_vs_commodities": 0.80
            }
        }
    except Exception as e:
        logger.error(f"Erreur forex workflow details: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.post("/api/workflows/{{workflow_type}}/force-execute")
async def force_workflow_execution(workflow_type: str, user_data: dict = Depends(require_auth)):
    """Force l'exécution d'un workflow"""
    try:
        if workflow_type == "crypto":
            asyncio.create_task(live_orchestrator.crypto_engine.execute_workflow())
        elif workflow_type == "meme":
            asyncio.create_task(live_orchestrator.meme_engine.execute_workflow())
        elif workflow_type == "forex":
            asyncio.create_task(live_orchestrator.forex_engine.execute_workflow())
        else:
            raise HTTPException(status_code=400, detail="Type de workflow invalide")
        
        return {{"message": f"Exécution forcée du workflow {{workflow_type}} démarrée"}}
    except Exception as e:
        logger.error(f"Erreur force execution {{workflow_type}}: {{e}}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/{{workflow_type}}/export")
async def export_workflow_data(workflow_type: str, user_data: dict = Depends(require_auth)):
    """Exporte les données d'un workflow"""
    try:
        if workflow_type == "crypto":
            data = live_orchestrator.crypto_engine.signal_history
        elif workflow_type == "meme":
            data = []  # TODO: Implémenter historique meme
        elif workflow_type == "forex":
            data = []  # TODO: Implémenter historique forex
        else:
            raise HTTPException(status_code=400, detail="Type de workflow invalide")
        
        export_data = {{
            "workflow_type": workflow_type,
            "export_date": datetime.now().isoformat(),
            "data": [asdict(item) for item in data]
        }}
        
        from fastapi.responses import JSONResponse
        import json
        
        response = JSONResponse(export_data)
        response.headers["Content-Disposition"] = f"attachment; filename={{workflow_type}}_export.json"
        return response
        
    except Exception as e:
        logger.error(f"Erreur export {{workflow_type}}: {{e}}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

if __name__ == "__main__":
    print("🧠 DÉMARRAGE TRADING AI PROFESSIONNEL")
    print("="*50)
    print(f"🔐 Authentification DB sécurisée")
    print(f"🔄 Workflows live actifs")
    print(f"💼 Interface professionnelle")
    print(f"🌐 Port: {PORT}")
    print("="*50)
    
    uvicorn.run(app, host="0.0.0.0", port=PORT) 