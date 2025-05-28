#!/bin/bash
# Fichier: ./configs/postgres/init/01-setup-config.sh
set -e

echo "🔧 Configuration personnalisée PostgreSQL..."

# Créer la base pour N8N si elle n'existe pas
echo "🔧 Création base N8N..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE n8n;
    GRANT ALL PRIVILEGES ON DATABASE n8n TO $POSTGRES_USER;
EOSQL

echo "✅ Base N8N créée"