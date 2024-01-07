import torch
import supervision as sv
import os
import cv2

#from setup import *
from const import  DEVICE, PATH_IMGS, PATH_PERSON,LOGGER
from dino_detection import detect_with_dino
from segment import segment
from image_treatment import binarize_mask, colorize_mask, binarize_list_of_masks, colorize_list_of_masks, crop_bip_numbers
from model import id_gen
from yolo_detection import detect_objects, sort_bib_numbers, extract_bib_numbers, concat_bib_numbers
from model import  generate_json_person
from color_detection import color_or_grayscale
from color_classifier import  determine_color_v2
import json




#img = cv2.imread(img_path)

def detect_and_segment(img, text_prompt,b_t_dino=0.3, t_t_dino=0.3):
    
    annotated_image, detections, phrases = detect_with_dino(img, text_prompt,b_t_dino, t_t_dino)
    
    segmented_image, detections = segment(detections, img)

    # si il y a a une phrase dans la detection qui n'est pas  exactement dans le text_prompt
    # on print un warning
    for phrase in phrases:
        if phrase not in text_prompt:
            LOGGER.warning("La phrase : "+phrase+" n'est pas dans le text_prompt")
    
    return annotated_image, segmented_image, detections, phrases

def save_img (name, img):
    cv2.imwrite(name, img)
    
def clear_img_brut_folder():
    folderp = PATH_PERSON
    for filename in os.listdir(folderp):
        if filename == '.gitkeep':
            continue  # Skip deleting .gitkeep file
        file_path = os.path.join(folderp, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    folder = PATH_IMGS
    for filename in os.listdir(folder):
        if filename == '.gitkeep':
            continue  # Skip deleting .gitkeep file
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

        except Exception as e:
            return e
    return "Folder"+PATH_IMGS+" cleared"


def first_step(img):
    text_prompt = ['person']
    annotated_image, segmented_image, detections, phrases = detect_and_segment(img, text_prompt,b_t_dino=0.45, t_t_dino=0.3)# 0.4, 0.3 pour les personnes pour limiter les faux positifs

    #cv2.imwrite('./assets/'+'_annotated.jpg', annotated_image)
    if len(detections) == 0 or detections is None:
        raise ValueError("No detection detected")
    
    binarized_list_of_masks=binarize_list_of_masks(detections.mask)
    colorized_list_of_masks=colorize_list_of_masks(binarized_list_of_masks, img)
    return colorized_list_of_masks


def second_step(colorize_list_of_masks, image_path):
    # clear the folder 
    folder = PATH_PERSON
    for filename in os.listdir(folder):
        if filename == '.gitkeep':
            continue  # Skip deleting .gitkeep file
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    for i in range(len(colorize_list_of_masks)):
        image_path = image_path.split('.')[0]
        image_path = image_path.split('/')[-1]

        name=PATH_PERSON+"p_"+str(i)+'_'+str(id_gen(image_path))+'.jpg'
        img = colorize_list_of_masks[i]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(name, img)



def step3(img):
    text_prompt = ['cap', 'shirt', 'sunglasses', 'shoe', 'sock', 'backpack', 'sticks', 'number', 'trousers']
    annotated_image, segmented_image, detections, phrases = detect_and_segment(img, text_prompt)
    #colorized_masks =colorize_list_of_masks(binarize_list_of_masks(detections.mask), img)
    filtered_masks = []
    filtered_phrases = []
    for i in range(len(detections.mask)):
        
        if  phrases[i] == 'cap' or phrases[i] == 'shirt' or phrases[i] == 'trousers':
            filtered_masks.append(colorize_mask(binarize_mask(detections.mask[i]), img))
            filtered_phrases.append(phrases[i])
    #tab_names , average_colors_hexa=determine_color_v2(colorized_masks,phrases)
    tab_names , average_colors_hexa=determine_color_v2(filtered_masks,filtered_phrases)
    if 'number' in phrases:
                mask_bib = colorize_mask(binarize_mask(detections.mask[phrases.index('number')]), img)
                croped_bib = crop_bip_numbers(phrases, mask_bib, detections)
    else:
        croped_bib = None
    return tab_names , average_colors_hexa,detections, phrases, annotated_image, segmented_image, croped_bib,text_prompt



def step5 (tab_names , average_colors_hexa, phrases ,croped_bib, text_prompt, p_name):
    dict_color = {}
    for name , color in zip (tab_names , average_colors_hexa ):
        detected_color = color_or_grayscale(color)
        #print(name ,": ", color_or_grayscale(color),color)
        dict_color[name] = detected_color
    if croped_bib is not None:
        detected_objects = detect_objects(croped_bib, device=DEVICE)
        bibs= concat_bib_numbers(extract_bib_numbers(sort_bib_numbers(detected_objects)))

        # parcourir les phrases et le dictionnaire
    result_dict = generate_json_person(text_prompt)
    result_dict['person'] = p_name
    print("pharses",phrases)
    print (" dico result",result_dict)
    print ("dico color",dict_color)
    for phrase in phrases:
        

        if phrase in result_dict:
            if phrase in ['cap', 'shirt', 'trousers']:
                #print(dict_color[phrase])
                # ne pas faire si le dico de couleur est vide
                if dict_color != {}:
                    result_dict[phrase]['color'] = dict_color[phrase]
                result_dict[phrase]['detected'] = True
            elif phrase == 'number':
                result_dict[phrase]['detected'] = True
                result_dict[phrase]['numbers'] = bibs
            else:
                result_dict[phrase]['detected'] = True

    return result_dict

def part1(img_path):
    img = cv2.imread(img_path)
    colorized_list_of_masks = first_step(img)
    second_step(colorized_list_of_masks, img_path)

def part2(img_original_name :str):
    # for each image in the folder PATH_PERSON
    dicts = []
    for filename in os.listdir(PATH_PERSON):
        # verifier le format de nommage de l'image 
        if filename.startswith('p_'):
            img = cv2.imread(PATH_PERSON+filename)
            p_name = filename.split('.')[0]
            tab_names , average_colors_hexa,detections, phrases, annotated_image,segmented_image,croped_bib , text_prompt= step3(img)
            n_dict = step5(tab_names , average_colors_hexa, phrases ,croped_bib, text_prompt, p_name)
            # save the annotated image
            
            n_dict["imgName"] = img_original_name
            print(n_dict)
            # ne pas 
            dicts.append(n_dict)
    json_result = []
    for d in dicts:
        json_result.append(json.dumps(d))
    return json_result


def all_steps(img_path):
    img = cv2.imread(img_path)
    colorized_list_of_masks = first_step(img)
    second_step(colorized_list_of_masks, img_path)
    img_original_name = img_path.split('/')[-1]
    json_result = part2(img_original_name)
    return json_result