from dino_detection import detect_with_dino
from const import *
import numpy as np
from segment_anything import SamPredictor
import supervision as sv
from GroundingDINO.groundingdino.util import box_ops
from groundingdino.util.inference import load_model, load_image, predict, annotate, Model
from PIL import Image
import cv2
from segment_anything import sam_model_registry, SamPredictor


sam_predictor= SamPredictor(sam_model_registry[SAM_ENCODER_VERSION](checkpoint=SAM_WEIGHTS_PATH).to(device=DEVICE))

def determine_masks(sam_predictor: SamPredictor, image: np.ndarray, xyxy: np.ndarray) -> np.ndarray:
    LOGGER.info("determine_masks")
    sam_predictor.set_image(image)
    result_masks = []
    for box in xyxy:
        masks, scores, logits = sam_predictor.predict(
            box=box,
            multimask_output=True
        )
        index = np.argmax(scores)
        result_masks.append(masks[index])
    return np.array(result_masks)

def segment(detections: sv.Detections, image_path: str):
    image = cv2.imread(image_path)
    detections.mask = determine_masks(
    sam_predictor=sam_predictor,
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
    xyxy=detections.xyxy
    )
    mask_annotator = sv.MaskAnnotator()
    segmented_image = mask_annotator.annotate(scene=image.copy(), detections=detections)
    LOGGER.info("Segmentation terminée")

    return segmented_image, detections


def display_segmented_img_with_boxes(annotated_image,detections, detetected_labels):
    box_annotator = sv.BoxAnnotator()
    annotated_image = box_annotator.annotate(scene=annotated_image, detections=detections, labels=detetected_labels)
    return annotated_image

