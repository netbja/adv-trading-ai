#!/bin/bash
# 🧹 NETTOYAGE COMPLET POSTGRESQL

echo "🧹 NETTOYAGE COMPLET POSTGRESQL"
echo "==============================="

# 1. Arrêter TOUT
echo "⏹️ Arrêt complet de Docker Compose..."
docker-compose down
docker-compose rm -f postgres

# 2. Vérifier les processus Docker PostgreSQL
echo "🔍 Vérification processus PostgreSQL..."
docker ps -a | grep postgres || echo "✅ Aucun container PostgreSQL actif"

# 3. Nettoyer les volumes Docker (optionnel mais efficace)
echo "🧹 Nettoyage volumes Docker PostgreSQL..."
docker volume ls | grep postgres && docker volume prune -f || echo "✅ Pas de volumes PostgreSQL orphelins"

# 4. Nettoyage BRUTAL du répertoire data/postgres
echo "💣 Nettoyage BRUTAL du répertoire..."
sudo rm -rf data/postgres/
sudo rm -rf data/postgres/.*  # Supprimer fichiers cachés
sudo rm -rf data/postgres/..?* # Supprimer autres fichiers cachés

# 5. Vérification
echo "🔍 Vérification suppression..."
ls -la data/ | grep postgres || echo "✅ Répertoire postgres supprimé"

# 6. Recréation propre
echo "📁 Recréation répertoire postgres..."
mkdir -p data/postgres
sudo chmod 755 data/postgres
sudo chown $(whoami):$(whoami) data/postgres

# 7. Vérification que le répertoire est vide
echo "📋 Contenu du répertoire data/postgres:"
ls -la data/postgres/ || echo "✅ Répertoire vide"

# 8. Démarrage PostgreSQL seul pour test
echo "🚀 Test démarrage PostgreSQL..."
docker-compose up -d postgres

# 9. Attendre et vérifier les logs
echo "⏳ Attente initialisation (15 secondes)..."
sleep 15

echo "📋 Logs PostgreSQL:"
docker-compose logs postgres --tail=20

# 10. Test de connexion
echo "🔌 Test de connexion..."
docker-compose exec postgres psql -U trader -d trading_ai -c "SELECT version();" 2>/dev/null && echo "✅ PostgreSQL fonctionne!" || echo "❌ Problème de connexion"

echo ""
echo "✅ Nettoyage terminé!"
echo ""
echo "🔍 Si PostgreSQL démarre correctement:"
echo "   docker-compose logs postgres"
echo ""
echo "🚀 Puis démarrer N8N:"
echo "   docker-compose up -d n8n"
echo "   docker-compose logs n8n"