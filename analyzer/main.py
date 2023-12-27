import torch
import supervision as sv
import os
import cv2

from setup import *
from const import *
from dino_detection import detect_with_dino
from segment import segment
import logging


if __name__ == '__main__':
    
    
    print (check_available_weights())
    img_path = 'assets/61.jpg'
    text_prompt = ['cap', 'shirt', 'sunglasses', 'shoe', 'sock', 'backpack', 'sticks', 'bib', 'trousers']
    annotated_image, detections, phrases = detect_with_dino(img_path, text_prompt)

    segmented_image, detections = segment(detections, img_path)
    # enregistrer les images
    cv2.imwrite("assets/segmented_image.jpg", segmented_image)
    
    
