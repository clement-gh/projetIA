# Utilisation de l'image Node.js 14 LTS comme base
FROM node:14-alpine

# Création du répertoire de travail dans l'image Docker
WORKDIR /usr/src/app

# Installation des dépendances du projet
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copie des fichiers de l'application dans l'image Docker
COPY . .

# Compilation TypeScript (si nécessaire)
RUN npm run build

# Exposition du port sur lequel l'application va écouter
EXPOSE 3000

# Commande pour démarrer l'application lorsque le conteneur démarre
CMD ["npm", "run", "start"]
