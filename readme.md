### Pour lancé l'app, 

Lancer dans 3 terminal différent

#### Pour lancer le Front
ng serve

#### Pour Lancer le backend
npm run build 
et 
npm run start

#### Pour lancer l'analyser
lancer le script setup.py dans le dossier analyzer si c'est la prmeière fois

Lancer api.py pour lancer l'analyser

### Connexion
Penser à generer un token d valide pour permettre au backend de comuniquer avce l'api
Pour cela, lancer le fichier main.py, il vous sera demander de rentrer un mot de passe et un nom d'utilisateur, un hash vous sera renvoyé qu'il faudra rentrer dans la variable: HASHED_USER=
La valeur TOKEN_KEY peut être une chaine de caratère quelconque.
Il est possible de changer BACKEND_URL si besoin 

#### Syntaxe du .env de l'analyzer:
HASHED_USER= 
TOKEN_KEY=
BACKEND_URL=http://localhost:3000

#### Optention du token:
Lancer api.py et  via un curl:
curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"username\":\"u\",\"password\":\"p\"}" http://localhost:5000/login

en remplacant u et p par respectivement l'username rentré précedement et p le mot de passe hashé.


#### Syntaxe du .env du backend (a placer dans le dossier backend)
Placer le token entre guillemets simples

TOKEN_API = 

FRONTEND_URL = 'http://localhost:4200'
