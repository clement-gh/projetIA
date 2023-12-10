
import os
import subprocess
import torch
import supervision as sv
import wget
from const import *

def script_setup():
    
    url_dino = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
    url_sam= "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
    url_yolo_best = "https://github.com/clement-gh/4A-Internship/raw/main/best.pt"
    url_yolo='https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt'
    download()
    #import_weights(url_dino, url_sam, url_yolo_best)
    print("Tout est bien installé")
    print("Models bien installés")


def clone_dino():
    subprocess.run(["git", "clone", "https://github.com/IDEA-Research/GroundingDINO.git"])
    subprocess.run(["pip","install","-e","./GroundingDINO"])
    print("GroundingDINO bien installé")
def clone_segment_anything():
    subprocess.run(["git", "clone", "https://github.com/facebookresearch/segment-anything.git","segment_anything"])
    subprocess.run(["pip","install","-e","./segment_anything"])
def clone_yolov7():
    subprocess.run(["git", "clone", "https://github.com/WongKinYiu/yolov7.git"])

def download():
    subprocess.run(["pip","install","-r","requirements.txt"])
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



