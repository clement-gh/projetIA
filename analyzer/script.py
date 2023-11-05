
import os
import subprocess
import torch
import supervision as sv
import wget

def script_setup():
    
    url_dino = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
    url_sam= "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
    url_yolo_best = "https://github.com/clement-gh/4A-Internship/raw/main/best.pt"
    url_yolo='https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt'
    download()
    import_weights(url_dino, url_sam, url_yolo_best)
    print("Tout est bien installé")
    grounding_dino_model, sam_predictor = set_up_models()
    print("Models bien installés")






    
def download():
    if not os.path.isdir("./GroundingDINO"):

        subprocess.run(["git", "clone", "https://github.com/IDEA-Research/GroundingDINO.git"])
        os.chdir("./GroundingDINO")
        subprocess.run(["git", "checkout", "-q", "57535c5a79791cb76e36fdb64975271354f10251"])
        subprocess.run(["pip","install","-q","-e","."])
        os.chdir("..")
    if not os.path.isdir("./segmentAnything"):
        subprocess.run(["git", "clone", "https://github.com/facebookresearch/segment-anything.git","segmentAnything"])

    if not os.path.isdir("./yolov7"):
        subprocess.run(["git", "clone", "https://github.com/WongKinYiu/yolov7.git"])

def  import_weights(url_dino, url_sam, url_yolo_best):
    if not os.path.isdir("./weights"):
        os.makedirs("weights", exist_ok=True)

    os.chdir("weights")
    if not os.path.isdir("./sam_vit_h_4b8939.pth"):
        os.system(f'curl -O {url_sam}')
    if not os.path.isdir("./groundingdino_swint_ogc.pth"):
        os.system(f'curl -O {url_dino}')
    if not os.path.isdir("./best.pt"):
        os.system(f'curl -O {url_yolo_best}')
    os.chdir("..")
    print ("Poids importés")

    # verfier la taille des fichiers
    if os.path.getsize("./weights/sam_vit_h_4b8939.pth") == 0:
        print("Fichier sam_vit_h_4b8939.pth vide")
    if os.path.getsize("./weights/groundingdino_swint_ogc.pth") == 0:
        print("Fichier groundingdino_swint_ogc.pth vide")
    if os.path.getsize("./weights/best.pt") == 0:
        print("Fichier best.pt vide")



def set_up_models():
    GROUNDING_DINO_CHECKPOINT_PATH = "./weights/groundingdino_swint_ogc.pth"
    SAM_CHECKPOINT_PATH = "./weights/sam_vit_h_4b8939.pth"
    assert os.path.isfile(GROUNDING_DINO_CHECKPOINT_PATH), f"Le fichier {GROUNDING_DINO_CHECKPOINT_PATH} n'existe pas"
    assert os.path.isfile(SAM_CHECKPOINT_PATH), f"Le fichier {SAM_CHECKPOINT_PATH} n'existe pas"
    GROUNDING_DINO_CONFIG_PATH ="./GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
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