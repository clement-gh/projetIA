import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from const import *
import cv2
import math
def binarize_mask(mask):
    binarized_mask= mask
    for j in range(len(mask)):
        for k in range(len(mask[j])):
            if mask[j][k] :
                binarized_mask[j][k] = 255
            else:
                binarized_mask[j][k] = 0
    binarized_mask = binarized_mask.astype(np.uint8) * 255
    return binarized_mask

def binarize_list_of_masks(list_of_masks):
    LOGGER.info("binarize_list_of_masks")
    binarized_masks = []
    for i in range(len(list_of_masks)):
        binarized_masks.append( binarize_mask(list_of_masks[i]))
    LOGGER.info("binarize_list_of_masks terminé")
    return binarized_masks



def plot_masks(list_of_masks):
    for i in range(len(list_of_masks)):
        # get mask information
        mask = list_of_masks[i]
        # show the mask
        fig, ax = plt.subplots()
        ax.imshow(mask, cmap='gray')
        ax.set_axis_off()
        plt.show()

def colorize_mask(bin_mask, img):
    img_arr = np.asarray(img)
    bin_mask = np.expand_dims(bin_mask, axis=2)
    result_arr = np.bitwise_and(img_arr, bin_mask)
    # convert arr to image with opencv
    result_img = cv2.cvtColor(result_arr, cv2.COLOR_BGR2RGB)
    #convert to RGB with cv2

    return result_img

def colorize_list_of_masks(list_of_masks, img):
    LOGGER.info("colorize_list_of_masks")
    colorized_masks = []
    for i in range(len(list_of_masks)):
        colorized_masks.append(colorize_mask(list_of_masks[i], img))
    LOGGER.info("colorize_list_of_masks terminé")
    return colorized_masks

def get_bib_numbers_index(tab_labels):
    index = 0
    for label in tab_labels:
        if label == 'number':
            return index
        index += 1
    return None

def crop_bip_numbers(tab_labels,image, detections):
    LOGGER.info("crop_bip_numbers")
    index= get_bib_numbers_index(tab_labels)
    if index is not None:
        # rounding the float numbers
        x1 = math.floor(detections.xyxy[index][0])
        y1 = math.floor(detections.xyxy[index][1])
        x2 = math.floor(detections.xyxy[index][2])
        y2 = math.floor(detections.xyxy[index][3])
        
        # crop the original image with the detection box
        cropped_image = image[y1:y2, x1:x2]
        LOGGER.info("crop_bip_numbers terminé")
        return cropped_image
    else:

        LOGGER.info("any bip numbers found in the image")
        return None