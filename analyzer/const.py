# weights location

import torch
import os
import logging

import sys
from pathlib import Path


# WEIGHTS FOLDER GLOBAL
WEIGTHS_FOLDER = "./Poids"

# WEIGHTS PATH FOR SAM
# SAM
SAM_WEIGHTS_PATH = WEIGTHS_FOLDER + "/sam_vit_h_4b8939.pth"
SAM_ENCODER_VERSION = "vit_h"

#SAM HQ
SAM_HQ_WEIGHTS_PATH = WEIGTHS_FOLDER + "/sam_hq_vit_l.pth"
SAM_HQ_ENCODER_VERSION = "vit_l"

# WEIGHTS PATH FOR GROUNDING DINO
GROUNDING_DINO_T_CHECKPOINT_PATH = WEIGTHS_FOLDER + "/groundingdino_swint_ogc.pth"
GROUNDING_DINO_B_CHECKPOINT_PATH = WEIGTHS_FOLDER + "/groundingdino_swinb_cogcoor.pth"
GROUNDING_DINO_CONFIG_PATH_FOR_T ="./GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
GROUNDING_DINO_CONFIG_PATH_FOR_B ="./GroundingDINO/groundingdino/config/GroundingDINO_SwinB_cfg.py"

# WEIGHTS PATH FOR YOLO
YOLO_CUSTOM_WEIGHTS_PATH = WEIGTHS_FOLDER + "/best.pt"
YOLO_WEIGHTS_PATH = WEIGTHS_FOLDER + "/yolov7.pt"
 
# URLS FOR WEIGHTS if not found in the folder

URL_YOLO_CUSTOM_WEIGHTS ="https://github.com/clement-gh/4A-Internship/raw/main/best.pt"
URL_YOLO_WEIGHTS="https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt"
URL_DINO_WEIGHTS_T = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
URL_DINO_WEIGHTS_B = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth"
URL_SAM_WEIGHTS = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
URL_SAM_WEIGHTS_HQ = "https://huggingface.co/lkeab/hq-sam/resolve/main/sam_hq_vit_l.pth"
#https://drive.google.com/file/d/1Uk17tDKX1YAKas5knI4y9ZJCo0lRVL0G/view




DEVICE=torch.device('cuda' if torch.cuda.is_available() else 'cpu')

log_format = '%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s'
logging.basicConfig(filename='./logFile.log', level=logging.DEBUG, format=log_format, filemode='w')
LOGGER = logging.getLogger()
LOGGER.info('Logger initialized')
LOGGER.info('Device used : {}'.format(DEVICE))
yolov7_path = Path('./yolov7')
sys.path.append(str(yolov7_path.resolve()))
LOGGER.info("yolov7 chargé")


PATH_PERSON = "data/persons/" # path to the person images
PATH_IMGS= "data/imgbrut/"

### TODO: use this function befor any call to the models !!
def check_available_weights():
    return os.path.isfile(SAM_WEIGHTS_PATH) and os.path.isfile(GROUNDING_DINO_T_CHECKPOINT_PATH) and os.path.isfile(GROUNDING_DINO_B_CHECKPOINT_PATH)
