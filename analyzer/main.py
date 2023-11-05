import torch
import supervision as sv
import os

from script import *




if __name__ == '__main__':
    if os.getcwd() != "/analyzer":
        os.chdir("./analyzer")
    print(os.getcwd())
  

    script_setup()
    #grounding_dino_model, sam_predictor = set_up_models()

   
    print("Tout est bien installé")