import requests
import jwt
#pip install pyjwt
#pip install python-dotenv
import hashlib
import sys
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

URL= "http://localhost:5000"
load_dotenv()
MY_TOKEN = os.getenv("TOKEN_API")



# Remplacez ceci par le chemin d'accès à votre image

def authentification():
    url = URL + "/login"
    username= os.getenv("USER")
    password= os.getenv("PASSWORD")
    donnees = {"username": username, "password": password}
    try:
        reponse = requests.post(url, json=donnees)
        if reponse.status_code == 200:
            token = reponse.json()["token"]
            return token
        else:
            print(f"Erreur lors de la requête : {reponse.status_code}")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")


def trigger_new_request():
    server_url = URL + '/protected' 
    global MY_TOKEN
    headers = {'Authorization': f'Bearer {MY_TOKEN}'}
    response = requests.get(server_url, headers=headers)
    if response.status_code == 200:
        print(f"Requête envoyée avec succès.")
        print(response.text)
    else:
        print(f"Échec de l'envoi de la requête.")
        print(response.text)


def upload_img(img_paths):
    server_url = URL + '/upload-image'  # Remplacez par l'adresse de votre serveur
    global MY_TOKEN
    headers = {'Authorization': f'Bearer {MY_TOKEN}'}

    for index, img_path in enumerate(img_paths):
        filename = os.path.basename(img_path)
        with open(img_path, 'rb') as file:
            files = {'image': file, 'filename': filename}

            # Vérifier si c'est la dernière image
            is_last_image = index == len(img_paths) - 1

            response = requests.post(server_url, headers=headers, files=files, data={'is_last_image': is_last_image})

            if response.status_code == 200:
                print(f"Image {img_path} envoyée avec succès.")
                print(response.json())
                if is_last_image:
                    trigger_new_request()  # Appel d'une nouvelle fonction après avoir reçu la confirmation du serveur
            else:
                print(f"Échec de l'envoi de l'image {img_path}.")
                print(response.text)


# Liste des chemins vers les images que vous souhaitez envoyer
                
image_paths = ['./DSC1223.jpg', './demo7.jpg', './61.jpg']
#upload_img(image_paths)

trigger_new_request()
