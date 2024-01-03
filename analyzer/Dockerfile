# Utilisation d'une image de base avec Python
FROM python:3.7

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie du contenu de 'analyser' dans le conteneur
COPY . /app
# Installation des dépendances
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update 
RUN apt-get install -y libgl1-mesa-glx
# Exécution de setup.py lors de la construction de l'image
#RUN python setup.py

# Exposer le port sur lequel votre API s'exécute


ENV FLASK_APP=api.py
ENV FLASK_DEBUG=1

EXPOSE 5000
CMD [ "flask","run", "-h", "0.0.0.0"]
