#!/usr/bin/env python3
"""
🚀 SCRIPT DE DÉMARRAGE TRADING AI COMPLET
Lance l'interface professionnelle avec authentification DB et workflows live
"""

import os
import sys
import subprocess
import time

def check_requirements():
    """Vérifie les dépendances nécessaires"""
    required_packages = [
        'fastapi', 'uvicorn', 'asyncpg', 'bcrypt', 
        'cryptography', 'python-multipart'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Packages manquants: {', '.join(missing)}")
        print("💡 Installation automatique...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("✅ Packages installés")

def check_database():
    """Vérifie la connexion à la base de données"""
    print("🔍 Vérification de la base de données...")
    
    # Variables d'environnement par défaut
    db_vars = {
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432', 
        'POSTGRES_DB': 'trading_ai',
        'POSTGRES_USER': 'trader',
        'POSTGRES_PASSWORD': 'TradingDB2025!'
    }
    
    for var, default in db_vars.items():
        if var not in os.environ:
            os.environ[var] = default
            print(f"📝 Variable {var} définie par défaut: {default}")
    
    print("✅ Configuration base de données OK")

def start_application():
    """Démarre l'application Trading AI"""
    print("\n🧠 DÉMARRAGE TRADING AI PROFESSIONNEL")
    print("="*60)
    print("🔐 Authentification DB sécurisée")
    print("🔄 Workflows crypto, meme et forex live")
    print("💼 Interface professionnelle temps réel")
    print("🌐 Port: 8000")
    print("="*60)
    print("\n📱 Interface disponible sur: http://localhost:8000")
    print("👤 Compte par défaut: admin / TradingAI2025!")
    print("\n🚀 Démarrage en cours...\n")
    
    # Lancer l'application
    os.system("python3 trading_ai_complete.py")

if __name__ == "__main__":
    try:
        print("🔧 Vérification de l'environnement...")
        check_requirements()
        check_database()
        start_application()
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du Trading AI")
    except Exception as e:
        print(f"\n❌ Erreur de démarrage: {e}")
        print("💡 Vérifiez que PostgreSQL est installé et démarré") 