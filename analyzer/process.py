import torch
import supervision as sv
import os
import cv2

from setup import *
from const import *
from dino_detection import detect_with_dino
from segment import segment
from image_treatment import *
from model import id_gen
from color_classifier import *
from yolo_detection import detect_objects, sort_bib_numbers, extract_bib_numbers, concat_bib_numbers
from model import dict



#img = cv2.imread(img_path)

def detect_and_segment(img, text_prompt,b_t_dino=0.3, t_t_dino=0.3):
    
    annotated_image, detections, phrases = detect_with_dino(img, text_prompt,b_t_dino, t_t_dino)
    
    segmented_image, detections = segment(detections, img)

    # si il y a a une phrase dans la detection qui n'est pas  exactement dans le text_prompt
    # on print un warning
    for phrase in phrases:
        if phrase not in text_prompt:
            LOGGER.warning("La phrase : "+phrase+" n'est pas dans le text_prompt")
            print("La phrase : "+phrase+" n'est pas dans le text_prompt")
    
    return annotated_image, segmented_image, detections, phrases

def first_step(img):
    text_prompt = ['person']
    annotated_image, segmented_image, detections, phrases = detect_and_segment(img, text_prompt,b_t_dino=0.4, t_t_dino=0.3)# 0.4, 0.3 pour les personnes pour limiter les faux positifs

    if len(detections) == 0 or detections is None:
        raise ValueError("No detection detected")
    
    binarized_list_of_masks=binarize_list_of_masks(detections.mask)
    colorized_list_of_masks=colorize_list_of_masks(binarized_list_of_masks, img)
    return colorized_list_of_masks


def second_step(colorize_list_of_masks, image_path):
    # clear the folder 
    folder = PATH_PERSON
    for filename in os.listdir(folder):
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

    
    text_prompt = ['cap', 'shirt', 'sunglasses', 'shoe', 'sock', 'backpack', 'sticks', 'bib', 'trousers']
    annotated_image, segmented_image, detections, phrases = detect_and_segment(img, text_prompt)

    
    colorized_masks =colorize_list_of_masks(binarize_list_of_masks(detections.mask), img)
    filtered_masks = []
    filtered_phrases = []
    for i in range(len(detections.mask)):
        if phrases not in ['bib', 'sticks']:
            filtered_masks.append(colorized_masks[i])
            filtered_phrases.append(phrases[i])
    #tab_names , average_colors_hexa=determine_color_v2(colorized_masks,phrases)
    tab_names , average_colors_hexa=determine_color_v2(filtered_masks,filtered_phrases)
    return tab_names , average_colors_hexa,detections, phrases,colorized_masks

def step4(tab_names , average_colors_hexa,detections, phrases ,colorized_masks):
    # recuperer le mask du bib 
    # si on detecte le bib
    if 'bib' in phrases:
        for  mask , label in zip (colorized_masks , phrases):
            if label == 'bib':
                mask_bib = mask
                croped_bib = crop_bip_numbers(phrases, mask_bib, detections)
    else:
        croped_bib = None
    return croped_bib

def step5 (tab_names , average_colors_hexa,detections, phrases ,colorized_masks,croped_bib):
    dict_color = {}
    for name , color in zip (tab_names , average_colors_hexa ):
        detected_color = color_or_grayscale(color)
    #print(name ,": ", color_or_grayscale(color),color)
        dict_color[name] = detected_color
    # si on detecte le bib


    if croped_bib is not None:
        detected_objects = detect_objects(croped_bib, device=DEVICE)
        bibs= concat_bib_numbers(extract_bib_numbers(sort_bib_numbers(detected_objects)))
    for detection in dict_color :
        if detection in dict:
            dict[detection]['detected'] = True
            if detection != 'bib':
                dict[detection]['color'] = dict_color[detection]
            else:
                dict[detection]['numbers'] = bibs
        else:
            dict[detection]['detected'] = False
    return dict

def part2():
    # for each image in the folder PATH_PERSON
    for filename in os.listdir(PATH_PERSON):
        img = cv2.imread(PATH_PERSON+filename)
        tab_names , average_colors_hexa,detections, phrases,colorized_masks = step3(img)
        croped_bib = step4(tab_names , average_colors_hexa,detections, phrases ,colorized_masks)
        dict = step5(tab_names , average_colors_hexa,detections, phrases ,colorized_masks,croped_bib)
        print(dict)

part2()
