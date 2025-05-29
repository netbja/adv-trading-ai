#!/usr/bin/env python3
"""
🧠 TRADING AI COMPLET - INTERFACE PROFESSIONNELLE
Dashboard avec authentification DB, workflows live et gestion des secrets
"""

import asyncio
import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

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
            /* Variables CSS professionnelles */
            :root {{
                --primary: #2563eb;
                --primary-dark: #1e40af;
                --secondary: #64748b;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --bg-main: #f8fafc;
                --bg-card: #ffffff;
                --border: #e2e8f0;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: var(--bg-main);
                color: var(--text-primary);
                line-height: 1.6;
            }}
            
            .app-layout {{
                display: grid;
                grid-template-columns: 280px 1fr;
                min-height: 100vh;
            }}
            
            /* Sidebar navigation */
            .sidebar {{
                background: var(--bg-card);
                border-right: 1px solid var(--border);
                padding: 0;
                position: fixed;
                left: 0;
                top: 0;
                width: 280px;
                height: 100vh;
                overflow-y: auto;
                z-index: 100;
            }}
            
            .sidebar-header {{
                padding: 1.5rem;
                border-bottom: 1px solid var(--border);
                background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                color: white;
            }}
            
            .sidebar-header h1 {{
                font-size: 1.25rem;
                margin-bottom: 0.25rem;
            }}
            
            .sidebar-header .user-info {{
                font-size: 0.875rem;
                opacity: 0.9;
            }}
            
            .nav-menu {{
                padding: 1rem 0;
            }}
            
            .nav-section {{
                margin-bottom: 2rem;
            }}
            
            .nav-section-title {{
                padding: 0 1.5rem 0.5rem;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--text-secondary);
            }}
            
            .nav-item {{
                margin: 0.25rem 1rem;
            }}
            
            .nav-link {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem 1rem;
                border-radius: 0.5rem;
                color: var(--text-secondary);
                text-decoration: none;
                transition: all 0.2s;
                font-weight: 500;
                cursor: pointer;
            }}
            
            .nav-link:hover {{
                background: #f1f5f9;
                color: var(--primary);
            }}
            
            .nav-link.active {{
                background: #dbeafe;
                color: var(--primary);
                font-weight: 600;
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
            
            .status-active {{ background: var(--success); animation: pulse 2s infinite; }}
            .status-idle {{ background: var(--secondary); }}
            .status-error {{ background: var(--danger); }}
            
            /* Main content */
            .main-content {{
                margin-left: 280px;
                min-height: 100vh;
            }}
            
            .topbar {{
                background: var(--bg-card);
                border-bottom: 1px solid var(--border);
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 50;
            }}
            
            .topbar-title {{
                font-size: 1.5rem;
                font-weight: 600;
            }}
            
            .topbar-actions {{
                display: flex;
                gap: 1rem;
                align-items: center;
            }}
            
            .btn {{
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.375rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            }}
            
            .btn-primary {{ background: var(--primary); color: white; }}
            .btn-secondary {{ background: var(--bg-card); color: var(--text-secondary); border: 1px solid var(--border); }}
            .btn-danger {{ background: var(--danger); color: white; }}
            
            .btn:hover {{ transform: translateY(-1px); }}
            
            .content-area {{
                padding: 2rem;
            }}
            
            .page-content {{
                display: none;
            }}
            
            .page-content.active {{
                display: block;
                animation: fadeIn 0.3s ease;
            }}
            
            .grid {{
                display: grid;
                gap: 1.5rem;
            }}
            
            .grid-2 {{ grid-template-columns: 1fr 1fr; }}
            .grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
            .grid-4 {{ grid-template-columns: repeat(4, 1fr); }}
            
            .card {{
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 0.75rem;
                padding: 1.5rem;
                box-shadow: var(--shadow);
                transition: all 0.2s;
            }}
            
            .card:hover {{
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            
            .card-header {{
                display: flex;
                justify-content: between;
                align-items: flex-start;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid var(--border);
            }}
            
            .card-title {{
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--text-primary);
            }}
            
            .card-subtitle {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin-top: 0.25rem;
            }}
            
            .metric {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.75rem 0;
                border-bottom: 1px solid #f1f5f9;
            }}
            
            .metric:last-child {{ border-bottom: none; }}
            
            .metric-label {{
                color: var(--text-secondary);
                font-weight: 500;
            }}
            
            .metric-value {{
                font-weight: 600;
                color: var(--text-primary);
            }}
            
            .metric-value.positive {{ color: var(--success); }}
            .metric-value.negative {{ color: var(--danger); }}
            .metric-value.warning {{ color: var(--warning); }}
            
            /* Workflow status */
            .workflow-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
            }}
            
            .workflow-card {{
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 0.75rem;
                padding: 1.5rem;
                position: relative;
                overflow: hidden;
            }}
            
            .workflow-status {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--secondary);
            }}
            
            .workflow-status.scanning {{ background: var(--warning); }}
            .workflow-status.analyzing {{ background: var(--primary); }}
            .workflow-status.executing {{ background: var(--success); }}
            .workflow-status.completed {{ background: var(--success); }}
            .workflow-status.error {{ background: var(--danger); }}
            
            .workflow-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }}
            
            .workflow-title {{
                font-size: 1.125rem;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
            
            .status-badge {{
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
            }}
            
            .status-idle {{ background: #f1f5f9; color: var(--text-secondary); }}
            .status-scanning {{ background: #fef3c7; color: #92400e; }}
            .status-analyzing {{ background: #dbeafe; color: #1e40af; }}
            .status-executing {{ background: #d1fae5; color: #065f46; }}
            .status-completed {{ background: #d1fae5; color: #065f46; }}
            .status-error {{ background: #fee2e2; color: #991b1b; }}
            
            /* Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            
            .pulse {{ animation: pulse 2s infinite; }}
            
            /* Activity feed */
            .activity-feed {{
                max-height: 400px;
                overflow-y: auto;
            }}
            
            .activity-item {{
                display: flex;
                gap: 1rem;
                padding: 1rem 0;
                border-bottom: 1px solid var(--border);
            }}
            
            .activity-item:last-child {{ border-bottom: none; }}
            
            .activity-icon {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.125rem;
                flex-shrink: 0;
            }}
            
            .activity-icon.crypto {{ background: #fef3c7; color: #92400e; }}
            .activity-icon.forex {{ background: #dbeafe; color: #1e40af; }}
            .activity-icon.meme {{ background: #f3e8ff; color: #7c3aed; }}
            
            .activity-content {{
                flex: 1;
            }}
            
            .activity-title {{
                font-weight: 600;
                margin-bottom: 0.25rem;
            }}
            
            .activity-description {{
                color: var(--text-secondary);
                font-size: 0.875rem;
            }}
            
            .activity-time {{
                color: var(--text-secondary);
                font-size: 0.75rem;
                margin-top: 0.25rem;
            }}
            
            {workflow_styles}
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
                        <span id="last-update">Dernière MAJ: --:--</span>
                        <button class="btn btn-secondary" onclick="refreshData()">🔄 Actualiser</button>
                        <button class="btn btn-danger" onclick="logout()">🚪 Déconnexion</button>
                    </div>
                </header>
                
                <div class="content-area">
                    <!-- Page Vue d'ensemble -->
                    <div id="overview-page" class="page-content active">
                        <div class="grid grid-4" style="margin-bottom: 2rem;">
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <div class="card-title">Capital Total</div>
                                        <div class="card-subtitle">Simulation active</div>
                                    </div>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Actuel</span>
                                    <span class="metric-value positive" id="current-capital">200.00€</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Rendement</span>
                                    <span class="metric-value positive" id="total-return">+0.00%</span>
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <div class="card-title">Workflows Actifs</div>
                                        <div class="card-subtitle">Temps réel</div>
                                    </div>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Crypto</span>
                                    <span class="metric-value" id="crypto-status">🔄 Actif</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Forex</span>
                                    <span class="metric-value" id="forex-status">🔄 Actif</span>
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <div class="card-title">Signaux Détectés</div>
                                        <div class="card-subtitle">Dernière heure</div>
                                    </div>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Total</span>
                                    <span class="metric-value" id="signals-total">0</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Forts</span>
                                    <span class="metric-value warning" id="signals-strong">0</span>
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <div class="card-title">Performance</div>
                                        <div class="card-subtitle">Système</div>
                                    </div>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Efficacité</span>
                                    <span class="metric-value positive" id="system-efficiency">100%</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Uptime</span>
                                    <span class="metric-value" id="system-uptime">1 jour</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="grid grid-2">
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <div class="card-title">📊 Statut Workflows</div>
                                        <div class="card-subtitle">État en temps réel</div>
                                    </div>
                                </div>
                                <div class="workflow-grid" id="workflow-status" style="grid-template-columns: 1fr;">
                                    <!-- Contenu chargé dynamiquement -->
                                </div>
                            </div>
                            
                            <div class="card">
                                <div class="card-header">
                                    <div>
                                        <div class="card-title">⚡ Activité Récente</div>
                                        <div class="card-subtitle">Dernières actions</div>
                                    </div>
                                </div>
                                <div class="activity-feed" id="recent-activity">
                                    <!-- Contenu chargé dynamiquement -->
                                </div>
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
                document.getElementById(pageId + '-page').classList.add('active');
                
                // Activer le lien nav
                event.target.closest('.nav-link').classList.add('active');
                
                // Mettre à jour le titre
                const titles = {{
                    'overview': 'Vue d\'ensemble',
                    'capital': 'Capital & Performance',
                    'crypto-workflow': 'Workflow Crypto Principal',
                    'meme-workflow': 'Workflow Crypto Meme',
                    'forex-workflow': 'Workflow Forex Trading',
                    'wallets': 'Wallets & Secrets',
                    'settings': 'Paramètres',
                    'logs': 'Logs Système'
                }};
                
                document.getElementById('page-title').textContent = titles[pageId] || pageId;
                currentPage = pageId;
                
                // Charger les données de la page
                loadPageData(pageId);
            }}
            
            async function loadPageData(pageId) {{
                if (pageId === 'overview') {{
                    await loadOverviewData();
                }} else if (pageId.includes('workflow')) {{
                    const workflowType = pageId.replace('-workflow', '');
                    await loadWorkflowPage(workflowType);
                }}
            }}
            
            async function loadOverviewData() {{
                try {{
                    // Charger données dashboard
                    const dashResponse = await fetch('/api/dashboard');
                    const dashData = await dashResponse.json();
                    
                    // Mettre à jour métriques
                    document.getElementById('current-capital').textContent = 
                        dashData.capital_growth.current.toFixed(2) + '€';
                    document.getElementById('total-return').textContent = 
                        (dashData.capital_growth.total_return_pct > 0 ? '+' : '') + 
                        dashData.capital_growth.total_return_pct.toFixed(1) + '%';
                    document.getElementById('system-efficiency').textContent = 
                        dashData.capital_growth.system_efficiency_pct.toFixed(0) + '%';
                    document.getElementById('system-uptime').textContent = 
                        dashData.uptime_days + ' jour(s)';
                    
                    // Charger statut workflows
                    const workflowResponse = await fetch('/api/workflows/live-status');
                    const workflowData = await workflowResponse.json();
                    
                    updateWorkflowStatus(workflowData);
                    updateRecentActivity(workflowData);
                    
                    // Mettre à jour timestamp
                    document.getElementById('last-update').textContent = 
                        'Dernière MAJ: ' + new Date().toLocaleTimeString();
                    
                }} catch (error) {{
                    console.error('Erreur chargement données:', error);
                }}
            }}
            
            function updateWorkflowStatus(data) {{
                const statusContainer = document.getElementById('workflow-status');
                const workflows = [
                    {{ key: 'crypto', title: '₿ Crypto Principal', icon: '₿' }},
                    {{ key: 'meme', title: '🐸 Crypto Meme', icon: '🐸' }},
                    {{ key: 'forex', title: '💱 Forex', icon: '💱' }}
                ];
                
                statusContainer.innerHTML = workflows.map(workflow => {{
                    const status = data[workflow.key]?.status || 'idle';
                    const execution = data[workflow.key]?.current_execution;
                    
                    return `
                        <div class="workflow-card">
                            <div class="workflow-status ${{status}}"></div>
                            <div class="workflow-header">
                                <div class="workflow-title">
                                    ${{workflow.icon}} ${{workflow.title}}
                                </div>
                                <div class="status-badge status-${{status}}">
                                    ${{status}}
                                </div>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Statut</span>
                                <span class="metric-value">${{status === 'idle' ? '⏱️ En attente' : 
                                                           status === 'scanning' ? '🔍 Scan marché' :
                                                           status === 'analyzing' ? '📊 Analyse' :
                                                           status === 'executing' ? '⚡ Exécution' : 
                                                           '✅ Terminé'}}</span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Dernière exec</span>
                                <span class="metric-value">${{execution ? 
                                    new Date(execution.start_time).toLocaleTimeString() : 'Jamais'}}</span>
                            </div>
                        </div>
                    `;
                }}).join('');
            }}
            
            function updateRecentActivity(data) {{
                const activityContainer = document.getElementById('recent-activity');
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
            }}
            
            function logout() {{
                document.cookie = 'session_token=; path=/; max-age=0';
                window.location.reload();
            }}
            
            // Auto-refresh toutes les 30 secondes
            setInterval(refreshData, 30000);
            
            // Charger données initiales
            loadOverviewData();
            
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
    """Statut live des workflows"""
    return live_orchestrator.get_live_status()

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
        return {{
            "pairs_monitored": len(crypto_engine.target_pairs),
            "signals_today": len([s for s in crypto_engine.signal_history if s.timestamp.date() == datetime.now().date()]),
            "avg_confidence": 0.75,
            "next_scan_in_seconds": 180,
            "current_execution": asdict(current_execution) if current_execution else None,
            "pairs_data": {{
                pair: {{
                    "price": 45000.0 if "BTC" in pair else 2500.0 if "ETH" in pair else 100.0,
                    "change_24h": 2.5,
                    "volume_24h": 250000000
                }} for pair in crypto_engine.target_pairs
            }},
            "recent_signals": [asdict(s) for s in crypto_engine.signal_history[-10:]]
        }}
    except Exception as e:
        logger.error(f"Erreur crypto workflow details: {{e}}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/meme/details")
async def get_meme_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow meme"""
    try:
        meme_engine = live_orchestrator.meme_engine
        current_execution = meme_engine.current_execution
        
        return {{
            "tokens_scanned": len(meme_engine.target_tokens),
            "max_viral_score": 85,
            "total_social_mentions": 1250,
            "overall_risk_level": "MEDIUM",
            "current_execution": asdict(current_execution) if current_execution else None,
            "tokens_data": {{
                token: {{
                    "viral_score": 65,
                    "social_mentions": 250,
                    "change_24h": 15.2,
                    "whale_activity": "medium"
                }} for token in meme_engine.target_tokens
            }},
            "risk_analysis": {{
                token: {{
                    "risk_level": "MEDIUM",
                    "risk_score": 45,
                    "factors": {{
                        "volatility": 25.5,
                        "social_activity": 250,
                        "whale_activity": "medium"
                    }}
                }} for token in meme_engine.target_tokens
            }},
            "viral_alerts": []
        }}
    except Exception as e:
        logger.error(f"Erreur meme workflow details: {{e}}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/workflows/forex/details")
async def get_forex_workflow_details(user_data: dict = Depends(require_auth)):
    """Détails du workflow forex"""
    try:
        forex_engine = live_orchestrator.forex_engine
        current_execution = forex_engine.current_execution
        
        return {{
            "pairs_active": len(forex_engine.currency_pairs),
            "usd_strength_index": 102.5,
            "avg_volatility": 0.021,
            "active_signals_count": 2,
            "current_execution": asdict(current_execution) if current_execution else None,
            "pairs_data": {{
                pair: {{
                    "current_rate": 1.0850 if "EUR" in pair else 1.2650 if "GBP" in pair else 149.50,
                    "change_24h": 0.35,
                    "trend": "Haussier"
                }} for pair in forex_engine.currency_pairs
            }},
            "economic_data": {{
                "usd_strength_index": 102.5,
                "global_risk_sentiment": "risk_on",
                "central_bank_sentiment": {{
                    "fed": "hawkish",
                    "ecb": "neutral"
                }},
                "economic_calendar": {{
                    "high_impact_events_today": 2
                }}
            }},
            "correlations": {{
                "EUR/USD_vs_GBP/USD": 0.75,
                "USD/JPY_vs_risk_sentiment": -0.65,
                "AUD/USD_vs_commodities": 0.80
            }}
        }}
    except Exception as e:
        logger.error(f"Erreur forex workflow details: {{e}}")
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