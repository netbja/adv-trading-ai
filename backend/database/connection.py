"""
🔗 DATABASE CONNECTION - CONNEXION BASE DE DONNÉES
Configuration SQLAlchemy pour PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from contextlib import contextmanager
from typing import Generator

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/trading_ai")

# Créer l'engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Pour éviter les problèmes de pool en dev
    echo=False  # Set to True pour debug SQL
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

def get_db() -> Generator:
    """
    Générateur de session de base de données
    Usage dans FastAPI: db = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager pour la base de données
    Usage: with get_db_context() as db:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialiser les tables de base de données"""
    try:
        # Importer tous les modèles ici pour que SQLAlchemy les connaisse
        from backend.models.market import MarketData
        from backend.models.system import SystemHealth
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables de base de données créées")
        return True
    except Exception as e:
        print(f"❌ Erreur création tables: {e}")
        return False 