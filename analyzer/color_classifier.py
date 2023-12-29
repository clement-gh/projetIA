from color_detection import verif_format_hsv, calculate_centers, create_bar, weighted_hsv_mean
import cv2
import matplotlib.pyplot as plt
import numpy as np



def determine_color_v2(mask_images, label_list, number_of_colors=10):
    tab_average_colors = []
    tab_names = []

    for img, label in zip(mask_images, label_list):
        color_counts = {}
        bars = []
        hsv_values = []
        tab_names.append(label)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        all_counts, centers = calculate_centers(img, number_of_colors)

        valid_centers = []
        valid_counts = []

        for idx, (row, count) in enumerate(zip(centers, all_counts)):
            bar, hsv = create_bar(200, 200, row)
            if hsv[2] > 0.03:
                bars.append(bar)
                hsv_values.append(hsv)
                valid_centers.append(row)
                valid_counts.append(count)
                color_counts[tuple(hsv)] = color_counts.get(tuple(hsv), 0) + count

        if bars:
            img_bar = np.hstack(bars)
            for idx, row in enumerate(hsv_values):
                image = cv2.putText(img_bar, f'{idx + 1}', (5 + 200 * idx, 200 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

            tab_colors = list(color_counts.keys())
            tab_nb_pixels = list(color_counts.values())

            dominant_color = weighted_hsv_mean(tab_colors, tab_nb_pixels)
            tab_average_colors.append(dominant_color)
            print(dominant_color)
            # afficher le label
            print(label)

    return tab_names, tab_average_colors