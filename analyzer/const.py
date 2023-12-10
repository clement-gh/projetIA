# weights location

import torch
import os

WEIGTHS_FOLDER = "H:\IA_project\Poids"
SAM_WEIGHTS_PATH = WEIGTHS_FOLDER + "/sam_vit_h_4b8939.pth"
SAM_ENCODER_VERSION = "vit_h"

SAM_HQ_WEIGHTS_PATH = WEIGTHS_FOLDER + "/sam_hq_vit_l.pth"
SAM_HQ_ENCODER_VERSION = "vit_l"

GROUNDING_DINO_T_CHECKPOINT_PATH = WEIGTHS_FOLDER + "/groundingdino_swint_ogc.pth"
GROUNDING_DINO_B_CHECKPOINT_PATH = WEIGTHS_FOLDER + "/groundingdino_swint_ogc.pth"
GROUNDING_DINO_CONFIG_PATH ="./GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"

DEVICE=torch.device('cuda' if torch.cuda.is_available() else 'cpu')


### TODO: use this function befor any call to the models !!
def check_available_weights():
    return os.path.isfile(SAM_WEIGHTS_PATH) and os.path.isfile(GROUNDING_DINO_T_CHECKPOINT_PATH) and os.path.isfile(GROUNDING_DINO_B_CHECKPOINT_PATH)