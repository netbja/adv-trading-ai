#!/usr/bin/env python3
"""Test spécifique de l'endpoint de login"""

import asyncio
import os
import json
from datetime import datetime

async def test_login_endpoint():
    """Test de l'endpoint de login en direct"""
    try:
        print("🧪 TEST ENDPOINT LOGIN")
        print("="*50)
        
        # Import des modules nécessaires
        from fastapi import Request
        from src.auth.secure_auth import SecureAuthManager
        
        # Variables d'environnement (exactement comme dans trading_ai_complete.py)
        DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'trader')}:{os.getenv('POSTGRES_PASSWORD', 'TradingDB2025!')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'trading_ai')}"
        
        print(f"🔗 DATABASE_URL: postgresql://trader:[MASQUÉ]@{os.getenv('POSTGRES_HOST', 'localhost')}:5432/trading_ai")
        
        # Créer le gestionnaire d'auth (comme dans trading_ai_complete.py)
        auth_manager = SecureAuthManager(DATABASE_URL)
        await auth_manager.init_db()
        print("✅ AuthManager initialisé")
        
        # Simuler la logique de l'endpoint de login
        print("🔄 Test de la logique de login...")
        
        # Simuler les données de la requête
        username = "admin"
        password = "TradingAI2025!"
        client_ip = "192.168.1.69"
        user_agent = "Mozilla/5.0 Test"
        
        print(f"📝 Données de test:")
        print(f"   Username: {username}")
        print(f"   Password: [MASQUÉ]")
        print(f"   Client IP: {client_ip}")
        print(f"   User Agent: {user_agent}")
        
        if not username or not password:
            print("❌ Username et password requis")
            return False
        
        # Test authentification
        user_data = await auth_manager.authenticate_user(username, password, client_ip, user_agent)
        
        if not user_data:
            print("❌ Identifiants invalides")
            return False
        
        print("✅ Authentification réussie!")
        print(f"📊 Données utilisateur:")
        for key, value in user_data.items():
            if key == 'session_token':
                print(f"   {key}: {value[:20]}...")
            else:
                print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans test login: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

async def test_imports():
    """Test des imports de trading_ai_complete.py"""
    try:
        print("\n🔧 TEST DES IMPORTS")
        print("="*30)
        
        # Test des imports un par un
        imports_to_test = [
            "asyncio",
            "os", 
            "logging",
            "datetime",
            "dataclasses",
            "fastapi",
            "uvicorn",
            "random",
            "src.auth.secure_auth",
            "src.workflows.live_trading_engine",
            "src.ui.workflow_pages",
            "src.ui.workflow_js",
            "smart_capital_growth_system"
        ]
        
        for module_name in imports_to_test:
            try:
                if module_name == "src.auth.secure_auth":
                    from src.auth.secure_auth import SecureAuthManager
                    print(f"✅ {module_name}")
                elif module_name == "src.workflows.live_trading_engine":
                    from src.workflows.live_trading_engine import LiveTradingOrchestrator
                    print(f"✅ {module_name}")
                elif module_name == "src.ui.workflow_pages":
                    from src.ui.workflow_pages import get_crypto_workflow_page
                    print(f"✅ {module_name}")
                elif module_name == "src.ui.workflow_js":
                    from src.ui.workflow_js import get_workflow_javascript
                    print(f"✅ {module_name}")
                elif module_name == "smart_capital_growth_system":
                    from smart_capital_growth_system import IntelligentCompoundGrowth, AutonomousTradingMaster
                    print(f"✅ {module_name}")
                elif module_name == "dataclasses":
                    from dataclasses import asdict
                    print(f"✅ {module_name}")
                elif module_name == "datetime":
                    from datetime import datetime
                    print(f"✅ {module_name}")
                elif module_name == "fastapi":
                    from fastapi import FastAPI, HTTPException, Request, Depends, Cookie
                    from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
                    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
                    print(f"✅ {module_name}")
                else:
                    __import__(module_name)
                    print(f"✅ {module_name}")
                    
            except Exception as e:
                print(f"❌ {module_name}: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Erreur test imports: {e}")
        return False

async def main():
    """Test principal"""
    # Test 1: Imports
    await test_imports()
    
    # Test 2: Login endpoint
    await test_login_endpoint()

if __name__ == "__main__":
    asyncio.run(main()) 