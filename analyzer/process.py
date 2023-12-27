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



#img = cv2.imread(img_path)

def detect_and_segment(img, text_prompt):
    
    annotated_image, detections, phrases = detect_with_dino(img, text_prompt)
    
    segmented_image, detections = segment(detections, img)

    
    return annotated_image, segmented_image, detections, phrases

def first_step(img):
    text_prompt = ['person']
    annotated_image, segmented_image, detections, phrases = detect_and_segment(img, text_prompt)

    if len(detections) == 0 or detections is None:
        raise ValueError("No detection detected")
    binarized_list_of_masks=binarize_list_of_masks(detections.mask)
    colorized_list_of_masks=colorize_list_of_masks(binarized_list_of_masks, img)
    return colorized_list_of_masks


def second_step(colorize_list_of_masks):

    for i in range(len(colorize_list_of_masks)):

        cv2.imwrite(PATH_PERSON+"p_"+id_gen()+".jpg", colorize_list_of_masks[i])
    
def third_step():
    # for each image in the folder PATH_PERSON
    text_prompt = ['cap', 'shirt', 'sunglasses', 'shoe', 'sock', 'backpack', 'sticks', 'bib', 'trousers']
    for filename in os.listdir(PATH_PERSON):
        img = cv2.imread(PATH_PERSON+filename)
        annotated_image, segmented_image, detections, phrases = detect_and_segment(img, text_prompt)
        if len(detections) == 0 or detections is None:
            LOGGER.error("No detection detected")
        else:
            binarized_list_of_masks=binarize_list_of_masks(detections.mask)
            colorized_list_of_masks=colorize_list_of_masks(binarized_list_of_masks, img)
            



