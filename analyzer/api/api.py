import jwt
#pip install pyjwt
from flask import Flask, request, jsonify
#pip install python-dotenv
import hashlib
import sys
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from flask_cors import CORS
from security import hash_password, verify_user_validity
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("TOKEN_KEY") # Clé secrète pour la création de JWT



@app.route("/test" , methods=['GET'])
def hello_world():
    #curl -X GET http://localhost:5000/
    return "hello world"



# Route de login pour générer le token JWT
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"username\":\"user\",\"password\":\"password\"}" http://localhost:5000/login

    if verify_user_validity(username, password):
 
        # Créer le token en spécifiant l'expiration
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Échec de l\'authentification'}), 401


# test de la route de login
    
@app.route('/protected', methods=['GET'])
def protected():
    # curl -X GET http://localhost:5000/protected -H "Authorization: Bearer VOTRE_TOKEN"
    msg=verify_token(request.headers.get('Authorization').split()[1])
    if msg.status_code == 401:
        return msg
    else:
        return jsonify({'message': 'Authentification réussie'})




@app.route('/upload-image', methods=['POST'])
def upload_image():
    token = request.headers.get('Authorization').split()[1]
    msg = verify_token(token)
    if msg.status_code == 401:
        return msg
    else:
        uploaded_file = request.files['image']
        is_last_image = request.form.get('is_last_image') == 'True'  # Récupérer le marqueur pour savoir si c'est la dernière image
        filename = secure_filename(uploaded_file.filename)  # Récupérer le nom du fichier
        
    # Traiter l'image reçue
    # Sauvegarder, manipuler, etc.

    if is_last_image:
# Exécuter la fonction côté serveur lorsque c'est la dernière image
        return jsonify({'message': 'Dernière image reçue.'})
    else:
        return jsonify({'message': 'Image reçue.'})

@app.route('/traitement', methods=['POST'])
def traitement():
    token = request.headers.get('Authorization').split()[1]
    msg = verify_token(token)
    if msg.status_code == 401:
        return msg
    else:
        print("traitement")

def verify_token(token):
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Vérifier l'expiration du token

        return jsonify({'message': 'Authentification reussie'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Le token a expiré'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Échec de l\'authentification'}), 401

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True)