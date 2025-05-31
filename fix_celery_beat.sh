#!/bin/bash

echo "🔧 NETTOYAGE CELERY BEAT - Réparation du scheduler"
echo "================================================="

# Arrêter seulement celery_beat
echo "🛑 Arrêt de Celery Beat..."
docker-compose stop celery_beat

# Supprimer le container celery_beat
echo "🗑️ Suppression du container Celery Beat..."
docker-compose rm -f celery_beat

# Supprimer le volume corrompu
echo "🧹 Nettoyage du volume corrompu..."
docker volume rm trading_celery_beat_data 2>/dev/null || echo "Volume déjà supprimé"

# Recreer le volume
echo "📦 Création d'un nouveau volume..."
docker volume create trading_celery_beat_data

# Redémarrer celery_beat
echo "🚀 Redémarrage de Celery Beat..."
docker-compose up -d celery_beat

# Attendre et vérifier
echo "⏳ Attente du démarrage..."
sleep 5

echo "📊 Vérification du statut..."
docker-compose ps celery_beat

echo "📝 Logs de Celery Beat:"
docker-compose logs --tail=10 celery_beat

echo "✅ Réparation terminée!" 