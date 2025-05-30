# 🌐 FRONTEND VUE3 - TRADING AI DASHBOARD
FROM node:18-alpine

WORKDIR /app

# Copier package.json en premier pour optimiser le cache Docker
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Exposer le port de développement
EXPOSE 3000

# Variables d'environnement par défaut
ENV NODE_ENV=development
ENV VITE_API_URL=http://localhost:8080
ENV VITE_N8N_URL=http://localhost:5678

# Commande de démarrage
CMD ["npm", "run", "dev"] 