

from const import *
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from pathlib import Path

from yolov7.models.experimental import attempt_load
from yolov7.utils.datasets import LoadStreams, LoadImages
from yolov7.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh
from yolov7.utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

def detect_objects(source, weights=YOLO_CUSTOM_WEIGHTS_PATH, img_size=640, conf_thres=0.25, iou_thres=0.45, device='', view_img=False, classes=None, agnostic_nms=False, augment=False, trace=False):
    device = select_device(device)
    half = device.type != 'cpu'

    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    img_size = check_img_size(img_size, s=stride)

    if trace:
        model = TracedModel(model, device, img_size)

    if half:
        model.half()

    dataset = LoadImages(source, img_size=img_size, stride=stride)
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    detections = []

    for path, img, im0s, _ in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        t1 = time_synchronized()
        with torch.no_grad():
            pred = model(img, augment=augment)[0]
        t2 = time_synchronized()

        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

        for i, det in enumerate(pred):
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)
            p = Path(p)
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "

                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                    line = (cls, *xywh, conf)
                    detections.append({'class': int(cls), 'label': names[int(cls)], 'confidence': conf.item(), 'box': xyxy})
    LOGGER.info(f"Found {len(detections)} objects in {source}")
    return detections

''' Example d'utilisation:
source_path = "./assets/tests/bib.jpg" # Remplacez cela par votre chemin d'accès à l'image ou à la vidéo

detected_objects = detect_objects(source_path)


for detection in detected_objects:
    print(f"Class: {detection['class']}, Label: {detection['label']}, Confidence: {detection['confidence']}, Box: {detection['box']}")
'''


def sort_bib_numbers(detections):
    sorted_detections = sorted(detections, key=lambda x: x['box'][0])
    return sorted_detections

# fonction pour extraire les numéros de dossard de la liste des détections
def extract_bib_numbers(detections):
    bib_numbers = []
    for detection in detections:
        bib_numbers.append(detection['label'])
    return bib_numbers

# concaténer les numéros de dossard
def concat_bib_numbers(bib_numbers):
    bib_numbers = ''.join(bib_numbers)
    return bib_numbers

# en fonction du nombre de dossards on verifie si le numéro est complet ou non
def  check_bib_numbers(bib_numbers, number_of_bibs):
    if len(bib_numbers) == number_of_bibs:
        return True
    else:
        return False
