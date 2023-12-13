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
MY_TOKEN = ""
load_dotenv()


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



def upload_img(img_path):
    server_url = URL + '/upload-image'  # Remplacez par l'adresse de votre serveur
    global MY_TOKEN
    if MY_TOKEN == "":
        MY_TOKEN = authentification()
    headers = {'Authorization': f'Bearer {MY_TOKEN}'}

    with open(img_path, 'rb') as file:
        files = {'image': file}
        response = requests.post(server_url, headers=headers, files=files)

        if response.status_code == 200:
            print(response.json())
        # Si on a une erreur 401, on réessaie une fois car le token a peut-être expiré
        elif response.status_code == 401:
            MY_TOKEN = authentification()
            headers = {'Authorization': f'Bearer {MY_TOKEN}'}
            response = requests.post(server_url, headers=headers, files=files)
            # si on a toujours une erreur, on affiche l'erreur
            if response.status_code == 401:
                print("Erreur lors de l'authentification")
            elif response.status_code == 200:
                print(response.json())
            
        else:
            print(response.text)


image_path = './DSC1223.jpg'
upload_img(image_path)