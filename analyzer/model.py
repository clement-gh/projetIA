#creer une personne avec une image de personne, l'image originale, les detections un nom de personneen json

import time

import calendar
import random

def id_gen():
    time_stamp = calendar.timegm(time.gmtime()) + random.randint(0,1000)
    return time_stamp

def create_person(original_image_name, person_image, detections):
    person = {}
    person["name"] = id_gen()
    person["image"] = person_image
    person["original_image"] = original_image_name
    return person





