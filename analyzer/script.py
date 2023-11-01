
import os
import subprocess
subprocess.run(["pip", "install", "-r", "./requirements.txt"])

import torch

HOME = os.getcwd()

# Cloner les dépôts
#ne pas cloner si les dossiers existent déjà
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






# Importer le module 'supervision'

# download DINO  an SAM weights
if not os.path.isdir("./weights"):

    os.makedirs("weights", exist_ok=True)
    os.chdir("weights")
    url = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
    urlSam= "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
    # Utilisez curl pour télécharger le fichier
    os.system(f'curl -O {url}')
    
    os.system(f'curl -O {urlSam}')
    os.chdir("..")
    # download yolov7.pt

# si le fichier best.pt n'existe pas, le télécharger
if not os.path.isfile("./yolov7/best.pt"):
    os.chdir("./yolov7")
    import wget
    urlyolobest= "https://github.com/clement-gh/4A-Internship/raw/main/best.pt"
    wget.download(urlyolobest, out="best.pt")



subprocess.run(["pip", "install", "-e", "./GroundingDINO"])





print("Tout est bien installé")