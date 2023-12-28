#creer une personne avec une image de personne, l'image originale, les detections un nom de personneen json

import time

import calendar
import random

import hashlib

def id_gen(image_name):
    # Convertir le nom de l'image en une chaîne d'octets pour le hachage
    image_name_bytes = image_name.encode('utf-8')
    # Calculer le hachage MD5 (ou un autre algorithme de hachage si préféré)
    hashed = hashlib.md5(image_name_bytes)
    # Obtenir la représentation hexadécimale du hachage
    hex_hash = hashed.hexdigest()
    # Prendre les 8 premiers caractères du hachage pour limiter la taille de l'ID
    limited_hash = hex_hash[:8]
    # Convertir la représentation hexadécimale en un nombre entier 
    numeric_id = int(limited_hash, 16)  # Convertir depuis la base 16 (hexadécimale
    return numeric_id


def create_person(name, person_image, original_image_name):
    person = {}
    person["name"] = name
    person["image"] = person_image
    person["original_image"] = original_image_name
    return person


dict = {}
dict['person'] =  None
dict['cap'] = {
    'detected': False,
    'color': None,
}
dict['shirt'] = {
    'detected': False,
    'color': None,
}
dict['sunglasses'] = {
    'detected': False,
    'color': None,
}
dict['shoe'] = {
    'detected': False,
    'color': None,
}
dict['sock'] = {
    'detected': False,
    'color': None,
}
dict['backpack'] = {
    'detected': False,
    'color': None,
}
dict['sticks'] = {
    'detected': False,
    # pas de couleur car non pertinent de l'utiliser
}
dict['bib'] = {
    'detected': False,
    'nmbers': None,
}
dict['trousers'] = {
    'detected': False,
    'color': None,
}


