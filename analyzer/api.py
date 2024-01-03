import time
import jwt
#pip install pyjwt
from flask import Flask, request, jsonify
#pip install python-dotenv

import threading
import sys
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from flask_cors import CORS
from security import hash_password, verify_user_validity
from werkzeug.utils import secure_filename
#from process import save_img, clear_img_brut_folder

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
    return msg
@app.route('/clearfolder', methods=['POST'])
def clearfolder():
    token  = request.headers.get('Authorization').split()[1]
    msg,status_code= verify_token(token)
    if status_code == 401:
        return msg
    else:
        from process import clear_img_brut_folder
        msg_return = clear_img_brut_folder()
        return jsonify({'message': msg_return})



@app.route('/upload-image', methods=['POST'])
def upload_image():
    token = request.headers.get('Authorization').split()[1]
    msg,status_code = verify_token(token)
    if status_code == 401:
        return msg,status_code
    else:
        uploaded_file = request.files['image']
        is_last_image = request.form.get('is_last_image') == 'True'  # Récupérer le marqueur pour savoir si c'est la dernière image
        filename = secure_filename(uploaded_file.filename)  # Récupérer le nom du fichier
        # Sauvegarder l'image dans le dossier
        from const import PATH_IMGS
        from process import save_img
        path =  PATH_IMGS+filename
        print(path)
        uploaded_file.save(path)

    if is_last_image:
# Exécuter la fonction côté serveur lorsque c'est la dernière image
        return jsonify({'message': 'Dernière image reçue.'}),200
    else:
        return jsonify({'message': 'Image reçue.'}),200

@app.route('/traitement', methods=['POST'])
def traitement():
    token = request.headers.get('Authorization')
    if token is None or len(token.split()) != 2 or token.split()[0].lower() != 'bearer':
        return "Token invalide", 401

    msg,status_code = verify_token(token.split()[1])
    if status_code == 401:
        return msg.text, 401

    # Démarrer le traitement dans un thread
    traitement_thread = threading.Thread(target=run_traitement)
    traitement_thread.start()

    # Renvoyer une réponse au client
    return "Traitement lancé"

def run_traitement():
    # parcours du dossier brut
    from const import PATH_IMGS
    for filename in os.listdir(PATH_IMGS):
        print(filename)
        if filename == '.gitkeep':
            continue
        else:
            path = PATH_IMGS+filename
            # traitement de l'image
            from process import all_steps
            print("Traitement de l'image : "+path)
            result= all_steps(path)
            print (result)
    print("Traitement terminé")



def verify_token(token) :
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Vérifier l'expiration du token
        

        return {'message': 'Authentification reussie'}, 200
    except jwt.ExpiredSignatureError:
        return {'message': 'Le token a expiré'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Echec de l\'authentification'}, 401

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            
            print("Passed argument not supported ! Supported argument : check_syntax")
            exit(1)
    app.run(debug=True) 