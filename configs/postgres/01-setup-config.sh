#!/bin/bash
# Fichier: ./configs/postgres/init/01-setup-config.sh
set -e

echo "🔧 Configuration personnalisée PostgreSQL..."

# Attendre que PostgreSQL soit prêt
until pg_isready -h localhost -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "⏳ Attente de PostgreSQL..."
  sleep 2
done

# Copier la configuration personnalisée si elle existe
if [ -f /backup/pg_hba.conf ]; then
    echo "📋 Application de pg_hba.conf personnalisé..."
    cp /backup/pg_hba.conf "$PGDATA/pg_hba.conf"
    chmod 600 "$PGDATA/pg_hba.conf"
    chown postgres:postgres "$PGDATA/pg_hba.conf"
    
    # Recharger la configuration
    pg_ctl reload -D "$PGDATA"
    echo "✅ Configuration pg_hba.conf appliquée"
else
    echo "ℹ️  Utilisation de la configuration par défaut"
fi

# Créer la base pour N8N si elle n'existe pas
echo "🔧 Création base N8N si nécessaire..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE IF NOT EXISTS ${N8N_DB:-n8n};
    GRANT ALL PRIVILEGES ON DATABASE ${N8N_DB:-n8n} TO $POSTGRES_USER;
EOSQL

echo "✅ Initialisation PostgreSQL terminée"