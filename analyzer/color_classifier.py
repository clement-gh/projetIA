from color_detection import verif_format_hsv, calculate_centers, create_bar, weighted_hsv_mean
import cv2
import matplotlib.pyplot as plt
import numpy as np
def hue_classifier(h):
    switch = {
        0 <= h <= 15 or 345 < h <= 360: "Red",
        15 < h <= 45: "Orange",
        45 < h <= 75: "Yellow",
        75 < h <= 105: "Yellow green",
        105 < h <= 135: "Green",
        135 < h <= 165: "Blue green",
        165 < h <= 195: "Cyan",
        195 < h <= 225: "Blue",
        225 < h <= 255: "Dark blue",
        255 < h <= 285: "Purple",
        285 < h <= 315: "Magenta",
        315 < h <= 345: "Pink"
    }

    result = switch.get(True)
    if result is not None:
        return result
    else:
        raise Exception('Hue must be between 0 and 360')

def gray_classifier(v):
    if (v>0 and v<=1):
        if v <= 0.2:
            return 'Black'
        elif v > 0.2 and v <= 0.5:
            return 'Grey'
        elif v > 0.5 and v <= 0.9:
            return 'Grey'
        elif v > 0.8 and v <= 1:
            return 'White'
    else:
        raise Exception('V must be between 0 and 1')
def Curve(y, x):
    n = 0.05
    return (y - (0.1 / (x - n)) - n)

def is_color_above_curve(hsv):
    verif_format_hsv(hsv)
    x1= hsv[1]
    y1 = hsv[2]
    value = Curve(y1, x1)
    if x1<= 0.05:
      return False
    if value >= 0:
        return True
    else:
        return False

def color_or_grayscale(hsv):
    verif_format_hsv(hsv)

    if is_color_above_curve(hsv):
        return hue_classifier(hsv[0])
    else:
      return gray_classifier(hsv[2])
    #TODO detect brown


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