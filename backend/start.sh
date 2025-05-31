#!/bin/bash

# Script de démarrage conditionnel pour dev/prod

if [ "$ENVIRONMENT" = "production" ]; then
    echo "🚀 Démarrage en mode PRODUCTION"
    exec gunicorn app.main:app \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --max-requests 1000 \
        --max-requests-jitter 50 \
        --timeout 30 \
        --keep-alive 2 \
        --access-logfile - \
        --error-logfile -
else
    echo "🛠️ Démarrage en mode DÉVELOPPEMENT"
    exec uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload
fi 