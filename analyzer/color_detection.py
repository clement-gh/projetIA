import math
import numpy as np
from numpy.ma.extras import average
import cv2
import colorsys
from PIL import Image
from sklearn.cluster import KMeans
import torch
from torch import Tensor

def rgb2bgr(img_rgb):
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_bgr
def bgr2rgb(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb

def rgb2hsv(r, g, b):

    r, g, b = r/255.0, g/255.0, b/255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val
    h, s, v = 0, 0.0, 0.0

    v = max_val
    v= round(v, 2)

    if max_val == 0:
        s = 0
    else:
        s = delta / max_val
        s = round(s, 2)
    if delta == 0:
        h = 0
    elif max_val == r:
        h = ((g - b) / delta) % 6
    elif max_val == g:
        h = ((b - r) / delta) + 2
    else:
        h = ((r - g) / delta) + 4
    h = h * 60
    h = round(h, 0)
    return h, s, v

def hsv2rgb (hsv):

    h,s,v = hsv[0]/360, hsv[1],hsv[2]
    r, g, b = colorsys.hsv_to_rgb(h,s,v)
    rgb = int(r*255),int(g*255),int(b*255)

    return rgb

def hsv2hexa (hsv):

    h,s,v = hsv[0]/360, hsv[1],hsv[2]
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r*255)
    g = int(g*255)
    b = int(b*255)
    return '#%02x%02x%02x' % (r, g, b)

def verif_format_hsv(hsv):
    if (hsv[0] > 360) or (hsv[1] > 1) or (hsv[2] > 1):
        raise Exception('HSV values must be between 0 and 360 for H, 0 and 1 for S and V')
def get_name_from_filename(filename):
  parts = filename.split("_")
  central_part = parts[-2]
  return central_part

def same_size(tab1, tab2):
    return len(tab1) == len(tab2)

def hsv_to_polar(hsv):
    h, s, v = hsv
    r = v
    theta = h * math.pi / 180
    return (theta,s, v)

def polar_to_hsv(polar):
    r, theta, s = polar
    h = (theta * 180 / math.pi) % 360
    return (h, s, r)

def rounding_hsv(hsv):
    hsv=round(hsv[0]),round(hsv[1],2),round(hsv[2],2)
    return hsv

def show_colors(tab_colors):
    for color in tab_colors:
        rgb = hsv2rgb(color)
        image = Image.new("RGB", (100, 100), rgb)
        image.show()

def weighted_hsv_mean(hsv_list, weights):
    # Convert HSV to polar coordinates
    polar_list = [hsv_to_polar(hsv) for hsv in hsv_list]

    # Get the theta, s, and r values from the polar coordinates
    theta_list,s_list,r_list = zip(*polar_list)

    # Calculate the weighted mean of r
    r_mean = np.average(r_list, weights=weights)

    # Calculate the weighted mean of sin(theta) and cos(theta)
    sin_theta_mean = np.average(np.sin(theta_list), weights=weights)
    cos_theta_mean = np.average(np.cos(theta_list), weights=weights)

    # Convert the weighted mean of sin(theta) and cos(theta) back to theta
    theta_mean = math.atan2(sin_theta_mean, cos_theta_mean)
    # Calculate the weighted mean of s
    s_mean = np.average(s_list, weights=weights)
    # Convert the weighted means back to HSV
    hsv_mean = polar_to_hsv((r_mean, theta_mean, s_mean))
    # Round the HSV values
    hsv_mean = rounding_hsv(hsv_mean)

    return hsv_mean

def create_bar(height, width, color):

    rgb = int(color[2]), int(color[1]), int(color[0])
    hsv = rgb2hsv(color[2],color[1],color[0])
    hsv = rounding_hsv(hsv)
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = rgb
    return bar, hsv

def calculate_centers(img, number_of_colors):
    height, width, channels = np.shape(img)

    flags = cv2.KMEANS_PP_CENTERS

    # change the image into a two-dimensional picture
    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    # kmeans algorithm to determine the main colors of the image
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    compactness, labels, centers = cv2.kmeans(data, number_of_colors, None, criteria, 10, flags)
    flat_labels = labels.flatten()
    counts = np.unique(flat_labels, return_counts=True)[1]
    return counts, centers


"""
color_classes = ['t shirt', 'shoe', 'sock', 'backpack', 'trousers']
def selected_files( color_classes = color_classes):

    tab_path = []
    for filename in os.listdir('/content/masks_color'):

        if get_name_from_filename(filename)in color_classes:
            tab_path.append(filename)
    print(tab_path)
    return tab_path
    """


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



def calculate_centers_v2(img, number_of_colors):
    height, width, channels = np.shape(img)

    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    kmeans = KMeans(n_clusters=number_of_colors, init='k-means++', random_state=42)
    kmeans.fit(data)

    centers = kmeans.cluster_centers_
    labels = kmeans.labels_

    flat_labels = labels.flatten()
    counts = np.unique(flat_labels, return_counts=True)[1]
    return counts, centers


def calculate_centers_v3(img, number_of_colors):
    height, width, channels = np.shape(img)

    # Changement de l'image en une image à deux dimensions
    data = np.reshape(img, (height * width, 3))
    data = torch.from_numpy(np.float32(data)).cuda()

    # Utilisation de l'algorithme K-Means GPU
    centers, labels = kmeans_torch_gpu(data, number_of_colors)

    # Obtention des comptages des clusters
    flat_labels = labels.cpu().numpy().flatten()
    counts = np.unique(flat_labels, return_counts=True)[1]
    
    return counts, centers.cpu().numpy()

from typing import Tuple

def kmeans_torch_gpu(data: Tensor, k: int, max_iters: int = 100) -> Tuple[Tensor, Tensor]:
    # Initialisation aléatoire des centroïdes
    centroids = data[torch.randperm(data.size(0))[:k]].clone().cuda()
    centroids_prev = centroids.clone()

    for _ in range(max_iters):
        # Assigner chaque point au centroïde le plus proche
        distances = ((data[:, None] - centroids[None]) ** 2).sum(-1)
        labels = torch.argmin(distances, dim=-1)

        # Mettre à jour les centroïdes
        for i in range(k):
            if torch.sum(labels == i) > 0:
                centroids[i] = data[labels == i].mean(0)

        # Vérifier la convergence
        if torch.all(centroids == centroids_prev):
            break
        centroids_prev = centroids.clone()

    return centroids, labels