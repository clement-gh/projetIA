import torch
import supervision as sv
import os


def set_up_models():
    GROUNDING_DINO_CHECKPOINT_PATH = "weights/groundingdino_swint_ogc.pth"
    SAM_CHECKPOINT_PATH = "weights/sam_vit_h_4b8939.pth"
    assert os.path.isfile(GROUNDING_DINO_CHECKPOINT_PATH), f"Le fichier {GROUNDING_DINO_CHECKPOINT_PATH} n'existe pas"
    assert os.path.isfile(SAM_CHECKPOINT_PATH), f"Le fichier {SAM_CHECKPOINT_PATH} n'existe pas"
    GROUNDING_DINO_CONFIG_PATH ="GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
    assert os.path.isfile(GROUNDING_DINO_CONFIG_PATH), f"Le fichier {GROUNDING_DINO_CONFIG_PATH} n'existe pas"


    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Utilisation du device {DEVICE}")


    from GroundingDINO.groundingdino.util.inference import load_model, load_image, predict, annotate
    grounding_dino_model = load_model(model_config_path=GROUNDING_DINO_CONFIG_PATH, model_checkpoint_path=GROUNDING_DINO_CHECKPOINT_PATH)
    SAM_ENCODER_VERSION = "vit_h"
    from segmentAnything.segment_anything import sam_model_registry, SamPredictor
    sam = sam_model_registry[SAM_ENCODER_VERSION](checkpoint=SAM_CHECKPOINT_PATH).to(device=DEVICE)
    sam_predictor = SamPredictor(sam)

    return grounding_dino_model, sam_predictor



grounding_dino_model, sam_predictor = set_up_models()
print("Tout est bien installé")

if __name__ == '__main__':
    grounding_dino_model, sam_predictor = set_up_models()
    print("Tout est bien installé")