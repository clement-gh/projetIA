import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from const import *
import cv2
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
    binarized_masks = list_of_masks
    for i in range(len(list_of_masks)):
        binarized_masks[i] = binarize_mask(list_of_masks[i])
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
    result_img = Image.fromarray(result_arr)
    #convert to RGB with cv2
    result_img = cv2.cvtColor(np.array(result_img), cv2.COLOR_BGR2RGB)
    return result_img

def colorize_list_of_masks(list_of_masks, img):
    LOGGER.info("colorize_list_of_masks")
    colorized_masks = []
    for i in range(len(list_of_masks)):
        colorized_masks.append(colorize_mask(list_of_masks[i], img))
    LOGGER.info("colorize_list_of_masks terminé")
    return colorized_masks