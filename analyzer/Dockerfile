# Utilisation d'une image de base avec Python
FROM python:3.7

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie du contenu de 'analyser' dans le conteneur
COPY . /app
# Installation des dépendances

RUN pip install --no-cache-dir -r requirements.txt

# Exécution de setup.py lors de la construction de l'image
RUN python setup.py

# Exposer le port sur lequel votre API s'exécute
EXPOSE 8085

# Commande pour démarrer votre application
CMD ["python", "api.py"]
#dckr_pat_MM875ruHDaVWvRQtTV3YG1qC1sU