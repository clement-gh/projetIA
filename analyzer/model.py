#creer une personne avec une image de personne, l'image originale, les detections un nom de personneen json


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


def generate_json_person (text_prompt):
    # ajouter le nom de la personne
    dict={}
    dict['person'] =  None
    dict['imgName'] = None
    for text in text_prompt:
        dict[text] = {
            'detected': False,
        }
        if text in ['cap', 'shirt', 'trousers']:
            dict[text]['color'] = None
        elif text == 'number':
            dict[text]['numbers'] = None
    return dict

