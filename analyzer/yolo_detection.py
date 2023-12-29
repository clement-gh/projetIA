

from const import *
import torch
import torch.backends.cudnn as cudnn

from torchvision import transforms

from yolov7.models.experimental import attempt_load

from yolov7.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh
from yolov7.utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

def detect_objects(image, weights=YOLO_CUSTOM_WEIGHTS_PATH, img_size=640, conf_thres=0.25, iou_thres=0.45, device='', view_img=False, classes=None, agnostic_nms=False, augment=False, trace=False):
    #device = select_device(device)
    model = attempt_load(weights, map_location=device)
    #model = TracedModel(model, device, img_size)

    img_transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    img = img_transforms(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        pred = model(img, augment=augment)[0]

    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

    detections = []

    for det in pred:
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image.shape).round()

            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / torch.tensor([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])).view(-1).tolist()
                detections.append({'class': int(cls), 'label': model.names[int(cls)], 'confidence': conf.item(), 'box': xyxy})

    LOGGER.info(f"Found {len(detections)} objects in image")
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
