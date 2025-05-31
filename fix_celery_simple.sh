#!/bin/bash

echo "🔧 RÉPARATION CELERY BEAT SIMPLE"
echo "================================"

echo "🛑 Arrêt de Celery Beat..."
docker-compose stop celery_beat

echo "🗑️ Suppression du container..."
docker-compose rm -f celery_beat

echo "🔨 Rebuild avec nouvelles dépendances..."
docker-compose build celery_beat

echo "🚀 Redémarrage de Celery Beat avec Redis scheduler..."
docker-compose up -d celery_beat

echo "⏳ Attente 10 secondes..."
sleep 10

echo "📋 Vérification des logs:"
docker-compose logs --tail=15 celery_beat

echo "🎯 Statut du container:"
docker-compose ps celery_beat

echo "✅ Réparation terminée!" 