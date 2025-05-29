#!/usr/bin/env python3
"""
🔐 SYSTÈME AUTHENTIFICATION SÉCURISÉ
Gestion comptes cryptés avec master password pour wallets et secrets
"""

import hashlib
import secrets
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import asyncpg
import asyncio
from dataclasses import dataclass

@dataclass
class User:
    """Modèle utilisateur sécurisé"""
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    master_password_hash: Optional[str]
    encrypted_secrets: Optional[str]

class CryptoManager:
    """Gestionnaire de cryptographie pour secrets sensibles"""
    
    def __init__(self):
        self.salt = None
        self.key = None
    
    def derive_key_from_password(self, master_password: str, salt: bytes = None) -> bytes:
        """Dérive une clé de chiffrement depuis le master password"""
        if salt is None:
            salt = os.urandom(16)
        self.salt = salt
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.key = key
        return key
    
    def encrypt_secret(self, secret: str, master_password: str) -> Dict[str, str]:
        """Chiffre un secret avec le master password"""
        key = self.derive_key_from_password(master_password)
        fernet = Fernet(key)
        
        encrypted_data = fernet.encrypt(secret.encode())
        
        return {
            "encrypted_data": base64.urlsafe_b64encode(encrypted_data).decode(),
            "salt": base64.urlsafe_b64encode(self.salt).decode()
        }
    
    def decrypt_secret(self, encrypted_data: str, salt: str, master_password: str) -> str:
        """Déchiffre un secret avec le master password"""
        salt_bytes = base64.urlsafe_b64decode(salt.encode())
        key = self.derive_key_from_password(master_password, salt_bytes)
        fernet = Fernet(key)
        
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = fernet.decrypt(encrypted_bytes)
        
        return decrypted_data.decode()

class SecureAuthManager:
    """Gestionnaire d'authentification sécurisé avec DB"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.crypto_manager = CryptoManager()
        self.active_sessions = {}  # user_id: session_data
    
    async def init_db(self):
        """Initialise les tables de base de données"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            # Table utilisateurs
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(128) NOT NULL,
                    role VARCHAR(20) DEFAULT 'user',
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT NOW(),
                    last_login TIMESTAMP,
                    master_password_hash VARCHAR(128),
                    encrypted_secrets TEXT
                )
            """)
            
            # Table sessions
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    session_token VARCHAR(64) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    expires_at TIMESTAMP NOT NULL,
                    ip_address INET,
                    user_agent TEXT
                )
            """)
            
            # Table secrets/wallets
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_secrets (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    secret_name VARCHAR(50) NOT NULL,
                    encrypted_value TEXT NOT NULL,
                    salt VARCHAR(32) NOT NULL,
                    secret_type VARCHAR(20) NOT NULL,  -- 'wallet', 'api_key', 'private_key'
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Créer utilisateur admin par défaut
            await self.create_default_admin(conn)
            
        finally:
            await conn.close()
    
    async def create_default_admin(self, conn):
        """Crée un utilisateur admin par défaut"""
        try:
            # Vérifier si admin existe déjà
            existing = await conn.fetchrow("SELECT id FROM users WHERE username = 'admin'")
            if existing:
                return
            
            # Créer admin
            password_hash = bcrypt.hashpw("TradingAI2025!".encode(), bcrypt.gensalt()).decode()
            
            await conn.execute("""
                INSERT INTO users (username, email, password_hash, role, master_password_hash)
                VALUES ($1, $2, $3, $4, $5)
            """, "admin", "admin@trading-ai.local", password_hash, "admin", password_hash)
            
            print("✅ Utilisateur admin créé: admin / TradingAI2025!")
            
        except Exception as e:
            print(f"⚠️ Erreur création admin: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash un mot de passe avec bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Vérifie un mot de passe"""
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def generate_session_token(self) -> str:
        """Génère un token de session sécurisé"""
        return secrets.token_urlsafe(32)
    
    async def authenticate_user(self, username: str, password: str, ip_address: str = None, user_agent: str = None) -> Optional[Dict]:
        """Authentifie un utilisateur et crée une session"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            # Récupérer utilisateur
            user_data = await conn.fetchrow("""
                SELECT id, username, email, password_hash, role, is_active, 
                       master_password_hash, encrypted_secrets
                FROM users 
                WHERE username = $1 AND is_active = true
            """, username)
            
            if not user_data:
                return None
            
            # Vérifier mot de passe
            if not self.verify_password(password, user_data['password_hash']):
                return None
            
            # Mettre à jour last_login
            await conn.execute("UPDATE users SET last_login = NOW() WHERE id = $1", user_data['id'])
            
            # Créer session
            session_token = self.generate_session_token()
            expires_at = datetime.now() + timedelta(hours=24)
            
            await conn.execute("""
                INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address, user_agent)
                VALUES ($1, $2, $3, $4, $5)
            """, user_data['id'], session_token, expires_at, ip_address, user_agent)
            
            # Ajouter à sessions actives
            self.active_sessions[user_data['id']] = {
                "username": user_data['username'],
                "role": user_data['role'],
                "session_token": session_token,
                "expires_at": expires_at
            }
            
            return {
                "user_id": user_data['id'],
                "username": user_data['username'],
                "email": user_data['email'],
                "role": user_data['role'],
                "session_token": session_token,
                "has_master_password": user_data['master_password_hash'] is not None
            }
            
        finally:
            await conn.close()
    
    async def verify_session(self, session_token: str) -> Optional[Dict]:
        """Vérifie une session existante"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            session_data = await conn.fetchrow("""
                SELECT s.user_id, s.expires_at, u.username, u.role, u.is_active
                FROM user_sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_token = $1 AND s.expires_at > NOW() AND u.is_active = true
            """, session_token)
            
            if not session_data:
                return None
            
            return {
                "user_id": session_data['user_id'],
                "username": session_data['username'],
                "role": session_data['role']
            }
            
        finally:
            await conn.close()
    
    async def set_master_password(self, user_id: int, master_password: str) -> bool:
        """Définit le master password pour un utilisateur"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            master_hash = self.hash_password(master_password)
            
            await conn.execute("""
                UPDATE users SET master_password_hash = $1 WHERE id = $2
            """, master_hash, user_id)
            
            return True
            
        except Exception as e:
            print(f"Erreur set master password: {e}")
            return False
        finally:
            await conn.close()
    
    async def store_encrypted_secret(self, user_id: int, secret_name: str, secret_value: str, 
                                   secret_type: str, master_password: str) -> bool:
        """Stocke un secret chiffré (wallet, clé API, etc.)"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            # Chiffrer le secret
            encrypted_data = self.crypto_manager.encrypt_secret(secret_value, master_password)
            
            # Supprimer ancien secret s'il existe
            await conn.execute("""
                DELETE FROM user_secrets WHERE user_id = $1 AND secret_name = $2
            """, user_id, secret_name)
            
            # Insérer nouveau secret
            await conn.execute("""
                INSERT INTO user_secrets (user_id, secret_name, encrypted_value, salt, secret_type)
                VALUES ($1, $2, $3, $4, $5)
            """, user_id, secret_name, encrypted_data['encrypted_data'], 
                encrypted_data['salt'], secret_type)
            
            return True
            
        except Exception as e:
            print(f"Erreur store secret: {e}")
            return False
        finally:
            await conn.close()
    
    async def retrieve_decrypted_secret(self, user_id: int, secret_name: str, master_password: str) -> Optional[str]:
        """Récupère et déchiffre un secret"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            secret_data = await conn.fetchrow("""
                SELECT encrypted_value, salt FROM user_secrets 
                WHERE user_id = $1 AND secret_name = $2
            """, user_id, secret_name)
            
            if not secret_data:
                return None
            
            # Déchiffrer
            decrypted = self.crypto_manager.decrypt_secret(
                secret_data['encrypted_value'],
                secret_data['salt'],
                master_password
            )
            
            return decrypted
            
        except Exception as e:
            print(f"Erreur retrieve secret: {e}")
            return None
        finally:
            await conn.close()
    
    async def list_user_secrets(self, user_id: int) -> list:
        """Liste les secrets d'un utilisateur (sans les valeurs)"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            secrets = await conn.fetch("""
                SELECT secret_name, secret_type, created_at, updated_at
                FROM user_secrets WHERE user_id = $1
                ORDER BY secret_name
            """, user_id)
            
            return [dict(secret) for secret in secrets]
            
        finally:
            await conn.close()
    
    async def logout_user(self, session_token: str):
        """Déconnecte un utilisateur"""
        conn = await asyncpg.connect(self.db_url)
        
        try:
            await conn.execute("DELETE FROM user_sessions WHERE session_token = $1", session_token)
            
            # Supprimer des sessions actives
            for user_id, session_data in list(self.active_sessions.items()):
                if session_data.get("session_token") == session_token:
                    del self.active_sessions[user_id]
                    break
            
        finally:
            await conn.close() 