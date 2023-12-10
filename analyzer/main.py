import torch
import supervision as sv
import os

from setup import *
from const import *
from dino_detection import detect_with_dino
from segment import segment


if __name__ == '__main__':
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(message)s')
    logging.debug('This message should go to the log file')
    print (check_available_weights())
    img_path = 'assets/61.jpg'
    text_prompt = ['cap', 'shirt', 'sunglasses', 'shoe', 'sock', 'backpack', 'sticks', 'bib', 'trousers']
    annotated_image, detections, phrases = detect_with_dino(img_path, text_prompt)
    logging.warning("test")
    segmented_image, detections = segment(detections, img_path)
