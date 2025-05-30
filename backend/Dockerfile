# 🐍 BACKEND PYTHON ETF - TRADING AI ULTRA-PERFORMANT
FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système optimisées
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Installer setuptools compatible Python 3.12 + wheel
RUN pip install --no-cache-dir --upgrade pip setuptools>=68.0.0 wheel

# Installer numpy et pandas avec wheels pré-compilés AVANT les autres
RUN pip install --no-cache-dir --only-binary=all numpy==1.26.2 pandas==2.1.4

# Copier et installer les requirements Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Variables d'environnement par défaut
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Exposer le port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Script de démarrage conditionnel
COPY start.sh .
RUN chmod +x start.sh

# Commande par défaut
CMD ["./start.sh"] 