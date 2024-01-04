# Utilisation d'une image de base compatible avec le GPU
FROM nvidia/cuda:11.0-runtime

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie du contenu de 'analyser' dans le conteneur
COPY . /app

# Installation des dépendances
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx

# Installation de Python et des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py
RUN pip install -e ./GroundingDINO

# Exposer le port sur lequel votre API s'exécute
ENV FLASK_APP=api.py
ENV FLASK_DEBUG=1
EXPOSE 5000

# Commande pour démarrer votre application Flask
CMD ["flask", "run", "-h", "0.0.0.0"]
