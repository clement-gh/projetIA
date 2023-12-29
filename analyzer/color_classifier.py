from color_detection import  calculate_centers, create_bar, weighted_hsv_mean, calculate_centers_v3
import matplotlib.pyplot as plt
import numpy as np

import cv2
import torch


def determine_color(mask_images, label_list, number_of_colors=10):
    tab_average_colors = []
    tab_names = []

    for index, img in enumerate(mask_images):
        color_counts = {}
        bars = []
        hsv_values = []
        tab_names.append(label_list[index])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        all_counts, centers = calculate_centers(img, number_of_colors)

        counts = []
        for idx, row in enumerate(centers):
            bar, hsv = create_bar(200, 200, row)
            if hsv[2] > 0.03:
                bars.append(bar)
                hsv_values.append(hsv)
                counts.append(all_counts[idx])

        for count, color in zip(counts, hsv_values):
            color_counts[color] = count if color not in color_counts else color_counts[color] + count

        if bars:
            img_bar = np.hstack(bars)
            
            for idx, row in enumerate(hsv_values):
                image = cv2.putText(img_bar, f'{idx + 1}', (5 + 200 * idx, 200 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            '''
            plt.imshow(image)
            plt.axis('off')
            plt.show()
            '''
            for count, color in zip(counts, hsv_values):
                color_counts[color] = count if color not in color_counts else color_counts[color] + count

            tab_colors = []
            tab_nb_pixels = []
            for key, value in color_counts.items():
                tab_colors.append(key)
                tab_nb_pixels.append(value)

            dominant_color = weighted_hsv_mean(tab_colors, tab_nb_pixels)
            tab_average_colors.append(dominant_color)
            print(dominant_color)
            # afficher le label
            print(label_list[index])

    return tab_names, tab_average_colors

import time


def determine_color_v2(mask_images, label_list, number_of_colors=10):
    
    tab_average_colors = []
    tab_names = []

    for img, label in zip(mask_images, label_list):
        color_counts = {}
        bars = []
        hsv_values = []
        tab_names.append(label)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #start_time = time.time()
        #all_counts, centers = calculate_centers_v2(img, number_of_colors

        if torch.cuda.is_available():
            all_counts, centers = calculate_centers_v3(img, number_of_colors)
        else:
            all_counts, centers = calculate_centers(img, number_of_colors)
        '''
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Temps d'exécution : {execution_time} secondes")
        '''
        valid_centers = []
        valid_counts = []

        for idx, (row, count) in enumerate(zip(centers, all_counts)):
            bar, hsv = create_bar(200, 200, row)
            if hsv[2] > 0.03:# si la valeur de v est supérieur à 0.03 on considère que c'est une couleur valide
                bars.append(bar)
                hsv_values.append(hsv)
                valid_centers.append(row)
                valid_counts.append(count)
                color_counts[tuple(hsv)] = color_counts.get(tuple(hsv), 0) + count

        if bars:
            tab_colors = list(color_counts.keys())
            tab_nb_pixels = list(color_counts.values())

            dominant_color = weighted_hsv_mean(tab_colors, tab_nb_pixels)
            tab_average_colors.append(dominant_color)

    return tab_names, tab_average_colors
