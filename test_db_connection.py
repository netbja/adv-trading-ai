#!/usr/bin/env python3
"""Test de connexion DB pour diagnostiquer le problème de login"""

import asyncio
import asyncpg
import os
import sys

async def test_db_connection():
    """Test de connexion à la base de données"""
    try:
        # Variables d'environnement
        db_user = os.getenv('POSTGRES_USER', 'trader')
        db_password = os.getenv('POSTGRES_PASSWORD', 'TradingDB2025!')
        db_host = os.getenv('POSTGRES_HOST', 'localhost')
        db_port = os.getenv('POSTGRES_PORT', '5432')
        db_name = os.getenv('POSTGRES_DB', 'trading_ai')
        
        print(f"🔍 Variables d'environnement:")
        print(f"   POSTGRES_USER: {db_user}")
        print(f"   POSTGRES_PASSWORD: [MASQUÉ]")
        print(f"   POSTGRES_HOST: {db_host}")
        print(f"   POSTGRES_PORT: {db_port}")
        print(f"   POSTGRES_DB: {db_name}")
        
        # Construction URL
        DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print(f"🔗 URL de connexion: postgresql://{db_user}:[MASQUÉ]@{db_host}:{db_port}/{db_name}")
        
        # Test de connexion
        print("🔄 Test de connexion...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Test de requête
        version = await conn.fetchval('SELECT version()')
        print(f"✅ Connexion réussie!")
        print(f"📊 Version PostgreSQL: {version[:80]}...")
        
        # Test de la table users
        users_exist = await conn.fetchval("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        print(f"👥 Table 'users' existe: {users_exist}")
        
        if users_exist:
            user_count = await conn.fetchval("SELECT COUNT(*) FROM users")
            print(f"👤 Nombre d'utilisateurs: {user_count}")
            
            # Vérifier l'utilisateur admin
            admin_exists = await conn.fetchval("SELECT EXISTS (SELECT 1 FROM users WHERE username = 'admin')")
            print(f"🔐 Utilisateur 'admin' existe: {admin_exists}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")
        return False

async def test_auth_manager():
    """Test du gestionnaire d'authentification"""
    try:
        print("\n" + "="*50)
        print("🔐 Test du gestionnaire d'authentification")
        print("="*50)
        
        # Import du gestionnaire d'auth
        from src.auth.secure_auth import SecureAuthManager
        
        # Variables d'environnement
        db_user = os.getenv('POSTGRES_USER', 'trader')
        db_password = os.getenv('POSTGRES_PASSWORD', 'TradingDB2025!')
        db_host = os.getenv('POSTGRES_HOST', 'localhost')
        db_port = os.getenv('POSTGRES_PORT', '5432')
        db_name = os.getenv('POSTGRES_DB', 'trading_ai')
        
        DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Créer le gestionnaire
        auth_manager = SecureAuthManager(DATABASE_URL)
        print("✅ SecureAuthManager créé")
        
        # Initialiser la DB
        await auth_manager.init_db()
        print("✅ Base de données initialisée")
        
        # Test d'authentification
        print("🔄 Test d'authentification admin...")
        result = await auth_manager.authenticate_user("admin", "TradingAI2025!", "127.0.0.1", "test-agent")
        
        if result:
            print("✅ Authentification réussie!")
            print(f"   Session token: {result.get('session_token', 'N/A')[:20]}...")
            print(f"   Utilisateur: {result.get('username')}")
            print(f"   Rôle: {result.get('role')}")
        else:
            print("❌ Authentification échouée")
            
        return result is not None
        
    except Exception as e:
        print(f"❌ Erreur gestionnaire auth: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Test principal"""
    print("🧪 DIAGNOSTIC CONNEXION TRADING AI")
    print("="*50)
    
    # Test 1: Connexion DB
    db_ok = await test_db_connection()
    
    if db_ok:
        # Test 2: Gestionnaire d'auth
        auth_ok = await test_auth_manager()
        
        if auth_ok:
            print("\n✅ TOUS LES TESTS RÉUSSIS - Le problème est ailleurs")
        else:
            print("\n❌ PROBLÈME AVEC LE GESTIONNAIRE D'AUTHENTIFICATION")
    else:
        print("\n❌ PROBLÈME DE CONNEXION À LA BASE DE DONNÉES")

if __name__ == "__main__":
    asyncio.run(main()) 