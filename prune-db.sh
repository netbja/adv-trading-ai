#!/bin/bash
# 🗑️ SUPPRIMER LE VOLUME DOCKER POSTGRESQL

echo "🗑️ SUPPRESSION VOLUME DOCKER POSTGRESQL"
echo "======================================="

# 1. Arrêter PostgreSQL
echo "⏹️ Arrêt PostgreSQL..."
docker-compose stop postgres
docker-compose rm -f postgres

# 2. Lister les volumes pour identifier le bon
echo "📋 Volumes Docker existants:"
docker volume ls

# 3. Identifier le volume PostgreSQL du projet
PROJECT_NAME=$(basename $(pwd) | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')
POSSIBLE_NAMES=(
    "${PROJECT_NAME}_postgres_data"
    "adv-trading-ai_postgres_data"
    "advtradingai_postgres_data"
    "postgres_data"
)

echo "🔍 Recherche du volume PostgreSQL..."
VOLUME_TO_DELETE=""

for volume_name in "${POSSIBLE_NAMES[@]}"; do
    if docker volume ls -q | grep -q "^${volume_name}$"; then
        VOLUME_TO_DELETE="$volume_name"
        echo "✅ Volume trouvé: $volume_name"
        break
    fi
done

if [ -z "$VOLUME_TO_DELETE" ]; then
    echo "🔍 Recherche par pattern..."
    VOLUME_TO_DELETE=$(docker volume ls -q | grep -E "(postgres|trading)" | head -1)
fi

if [ -n "$VOLUME_TO_DELETE" ]; then
    echo "🗑️ Suppression du volume: $VOLUME_TO_DELETE"
    docker volume rm "$VOLUME_TO_DELETE"
    echo "✅ Volume $VOLUME_TO_DELETE supprimé!"
else
    echo "⚠️ Aucun volume PostgreSQL trouvé"
    echo "📋 Tous les volumes:"
    docker volume ls
    echo ""
    echo "💡 Supprimer manuellement avec:"
    echo "   docker volume rm [NOM_DU_VOLUME]"
fi

# 4. Vérification
echo "📋 Volumes restants:"
docker volume ls

# 5. Test démarrage PostgreSQL
echo "🚀 Test démarrage PostgreSQL..."
docker-compose up -d postgres

# 6. Attendre et vérifier
echo "⏳ Attente initialisation (15 secondes)..."
sleep 15

echo "📋 Status PostgreSQL:"
docker-compose ps postgres

echo "📋 Logs PostgreSQL (dernières lignes):"
docker-compose logs postgres --tail=10

if docker-compose ps postgres | grep -q "Up"; then
    echo "✅ SUCCÈS! PostgreSQL fonctionne!"
    echo "🔌 Test de connexion..."
    docker-compose exec postgres psql -U trader -d trading_ai -c "SELECT version();" 2>/dev/null && echo "✅ Connexion OK!" || echo "⏳ Attendre encore un peu..."
else
    echo "❌ PostgreSQL toujours en erreur"
    echo "📋 Logs complets:"
    docker-compose logs postgres
fi

echo ""
echo "🚀 Si PostgreSQL fonctionne, démarrer N8N:"
echo "   docker-compose up -d n8n"
