from groundingdino.util.inference import load_model, load_image, predict, annotate, Model
import cv2
import matplotlib.pyplot as plt
import numpy as np
from const import *
import supervision as sv

### TODO: delete theses constants


def detect_with_dino (image_path, text_prompt, box_threshold=0.3, text_threshold=0.3):
    image = cv2.imread(image_path)
    grounding_dino_model = Model(model_config_path=GROUNDING_DINO_CONFIG_PATH, model_checkpoint_path=GROUNDING_DINO_T_CHECKPOINT_PATH, device=DEVICE)

    detections, phrases = grounding_dino_model.predict_with_caption(
        image=image,
        caption=", ".join(text_prompt),
        box_threshold=box_threshold,
        text_threshold=text_threshold
    )
    print (phrases)
    classe_id_list_str =  grounding_dino_model.phrases2classes(phrases, text_prompt)
    detections.class_id = classe_id_list_str
    #detections = detections[detections.class_id != text_prompt.index("trousers")]
    box_annotator = sv.BoxAnnotator()
    annotated_image = box_annotator.annotate(scene=image.copy(), detections=detections)
    if len(detections) == 0:
        raise ValueError("No detections found")
    return annotated_image, detections, phrases



"""
annotated_frame, detections = detect_with_dino(img_path, text_prompt)
print (detections)

cv2.imwrite('assets/61_dino_classes.jpg', annotated_frame)


"""