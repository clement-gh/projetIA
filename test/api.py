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



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_TOKEN") # Clé secrète pour la création de JWT

def hash_password(user,password):
    return hashlib.sha256((user+password).encode()).hexdigest()

def verify_user_validity(user,password):
    hash_password_user = hash_password(user,password)

    pwd=os.getenv("PASSWORD_HASHED")
    user=os.getenv("USER")
    return  (hash_password_user == pwd and user == user)

@app.route("/test" , methods=['GET'])
def hello_world():
    #curl -X GET http://localhost:5000/
    return "hello world"



# Route de login pour générer le token JWT
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Vérifiez l'authentification de l'utilisateur ici (ex : vérification du nom d'utilisateur et du mot de passe)
    # curl -X POST -H "Content-Type: application/json; charset=utf-8" --data "{\"username\":\"user\",\"password\":\"password\"}" http://localhost:5000/login

    # Si l'authentification réussit, générez un token JWT
    if verify_user_validity(username, password):
 
        # Créer le token en spécifiant l'expiration
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Échec de l\'authentification'}), 401


# test de la route de login
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Vérifier l'expiration du token
        if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
            return jsonify({'message': 'Le token a expiré'}), 401

        return jsonify({'message': 'Authentification réussie'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Le token a expiré'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Échec de l\'authentification'}), 401

@app.route('/upload-image', methods=['POST'])
def upload_image():
    token = request.headers.get('Authorization').split()[1]
    request.files['image']

    msg=verify_token(token)
    if msg.status_code == 401:
        return msg
    else:
        #save image
        request.files['image'].save("image.png")
        return jsonify({'message': 'Image traitée avec succès'})




def verify_token(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Vérifier l'expiration du token
        if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
            return jsonify({'message': 'Le token a expiré'}), 401

        return jsonify({'message': 'Authentification réussie'})
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