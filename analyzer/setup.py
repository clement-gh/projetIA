
import os
import subprocess
import torch
import supervision as sv
import wget
from const import *


URL_YOLO_CUSTOM_WEIGHTS ="https://github.com/clement-gh/4A-Internship/raw/main/best.pt"
URL_YOLO_WEIGHTS="https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt"
URL_DINO_WEIGHTS_T = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
URL_DINO_WEIGHTS_B = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth"
URL_SAM_WEIGHTS = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
URL_SAM_WEIGHTS_HQ = "https://drive.google.com/file/d/1Uk17tDKX1YAKas5knI4y9ZJCo0lRVL0G/view"

#### To use if not running in docker ####
def install_requirements():
    subprocess.run(["pip","install","-r","./requirements.txt"])
    print("requirements bien installés")
#### -------------------------------- ####


def clone_dino():
    subprocess.run(["git", "clone", "https://github.com/IDEA-Research/GroundingDINO.git"])
    subprocess.run(["pip","install","-e","./GroundingDINO"])
    print("GroundingDINO bien installé")
def clone_segment_anything():
    subprocess.run(["git", "clone", "https://github.com/facebookresearch/segment-anything.git","segment_anything"])
    subprocess.run(["pip","install","-e","./segment_anything"])
    print("segment_anything bien installé")
def clone_yolov7():
    subprocess.run(["git", "clone", "https://github.com/WongKinYiu/yolov7.git"])
    print("yolov7 bien installé")


def clone_and_setup_py():
    if not os.path.isdir("./GroundingDINO"):
        clone_dino()

    if not os.path.isdir("./segment_anything"):
        clone_segment_anything()
    if not os.path.isdir("./yolov7"):
        clone_yolov7()

    if os.path.isdir("./GroundingDINO") and os.listdir("./GroundingDINO") == []:
        os.rmdir("./GroundingDINO")
        clone_dino()

    if os.path.isdir("./segment_anything") and os.listdir("./segment_anything") == []:
        os.rmdir("./segment_anything")
        clone_segment_anything()
    if os.path.isdir("./yolov7") and os.listdir("./yolov7") == []:
        os.rmdir("./yolov7")
        clone_yolov7()
    print("Tout est bien installé")

def download_weights():
    if not os.path.isdir(WEIGTHS_FOLDER):
        os.mkdir(WEIGTHS_FOLDER)
    if not os.path.isfile(SAM_WEIGHTS_PATH):
        wget.download(URL_SAM_WEIGHTS, SAM_WEIGHTS_PATH)
    if not os.path.isfile(SAM_HQ_WEIGHTS_PATH):
        wget.download(URL_SAM_WEIGHTS_HQ, SAM_HQ_WEIGHTS_PATH)
    if not os.path.isfile(GROUNDING_DINO_T_CHECKPOINT_PATH):
        wget.download(URL_DINO_WEIGHTS_T, GROUNDING_DINO_T_CHECKPOINT_PATH)
    if not os.path.isfile(GROUNDING_DINO_B_CHECKPOINT_PATH):
        wget.download(URL_DINO_WEIGHTS_B, GROUNDING_DINO_B_CHECKPOINT_PATH)
    if not os.path.isfile(YOLO_CUSTOM_WEIGHTS_PATH):
        wget.download(URL_YOLO_CUSTOM_WEIGHTS, YOLO_CUSTOM_WEIGHTS_PATH)
    if not os.path.isfile(YOLO_WEIGHTS_PATH):
        wget.download(URL_YOLO_WEIGHTS, YOLO_WEIGHTS_PATH)
    print("Tout les poids sont bien téléchargés")


