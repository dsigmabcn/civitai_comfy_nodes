import hashlib
import json
import os
import requests
import sys
import time
from tqdm import tqdm

import folder_paths
import comfy.sd
import comfy.utils
from nodes import CheckpointLoaderSimple

from .CivitAI_Model import CivitAI_Model
from .utils import short_paths_map, model_path


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT_PATH = folder_paths.folder_names_and_paths["checkpoints"][0][0]
CHECKPOINTS = folder_paths.folder_names_and_paths["checkpoints"][0]
# I cannot find the animatediff_models_folder with folder_names_and_paths, so I directly write the path
#CHECKPOINTS = ["/workspace/ComfyUI/models/animatediff_models"]
#CHECKPOINT_PATH = "/workspace/ComfyUI/models/animatediff_models"
print(CHECKPOINTS)
print(ROOT_PATH)


MSG_PREFIX = '\33[1m\33[34m[CivitAI] \33[0m'

class CivitAI_mm_Loader:
    """
        Implements the CivitAI Motion modeles AnimateDiff Loader node for ComfyUI 
    """
    def __init__(self):
        self.ckpt_loader = None

    @classmethod
    def INPUT_TYPES(cls):
        checkpoints = folder_paths.get_filename_list("animatediff_models")
        checkpoints.insert(0, 'none')
        checkpoint_paths = short_paths_map(CHECKPOINTS)
        
        return {
            "required": {
                "ckpt_air": ("STRING", {"default": "{model_id}@{model_version}", "multiline": False}),
                "ckpt_name": (checkpoints,),
            },
            "optional": {
                "download_chunks": ("INT", {"default": 4, "min": 1, "max": 12, "step": 1}),
                "download_path": (list(checkpoint_paths.keys()),),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    #RETURN_TYPES = ("MOTION_MODEL_ADE")#, "CLIP", "VAE")
    
    RETURN_TYPES = ("*",) #Used 'any' type, so it can be connected to the AnimateDiff Loader (with string I could not do it)
    FUNCTION = "load_checkpoint"

    CATEGORY = "CivitAI/Loaders"

    def load_checkpoint(self, ckpt_air, ckpt_name, download_chunks=None, download_path=None, extra_pnginfo=None):
        print("start load function")
        print(ckpt_name)
        if extra_pnginfo:
            if not extra_pnginfo['workflow']['extra'].__contains__('ckpt_airs'):
                extra_pnginfo['workflow']['extra'].update({'ckpt_airs': []})

        if not self.ckpt_loader:
            self.ckpt_loader = CheckpointLoaderSimple()
            #self.ckpt_loader = LoadAnimateDiffModelNode()
            #self.ckpt_loader = load_motion_module_gen2()
            
        if ckpt_name == 'none':
        
            ckpt_id = None
            version_id = None
            
            if '@' in ckpt_air:
                ckpt_id, version_id = ckpt_air.split('@')
            else:
                ckpt_id = ckpt_air
                
            ckpt_id = int(ckpt_id) if ckpt_id else None
            version_id = int(version_id) if version_id else None
            
            checkpoint_paths = short_paths_map(CHECKPOINTS)
            if download_path:
                if checkpoint_paths.__contains__(download_path):
                    download_path = checkpoint_paths[download_path]
                else:
                    download_path = CHECKPOINTS[0]
            
            civitai_model = CivitAI_Model(model_id=ckpt_id, model_version=version_id, model_types=["MotionModule",], save_path=download_path, model_paths=CHECKPOINTS, download_chunks=download_chunks)
                
            if not civitai_model.download():
               return None, None, None 
               
            ckpt_name = civitai_model.name
            if extra_pnginfo:
                air = f'{civitai_model.model_id}@{civitai_model.version}'
                if air not in extra_pnginfo['workflow']['extra']['ckpt_airs']: 
                    extra_pnginfo['workflow']['extra']['ckpt_airs'].append(air)
                    
        else:
        
            ckpt_path = model_path(ckpt_name, CHECKPOINTS)

            model_id, version_id, details = CivitAI_Model.sha256_lookup(ckpt_path)
            
            if model_id and version_id and extra_pnginfo:
                air = f'{model_id}@{version_id}'
                if air not in extra_pnginfo['workflow']['extra']['ckpt_airs']: 
                    extra_pnginfo['workflow']['extra']['ckpt_airs'].append(air)
            
            print(f"{MSG_PREFIX}Loading checkpoint from disk: {ckpt_path}")
        
        #out = self.ckpt_loader.load_checkpoint(model = ckpt_name)
        # Change to only have the output as a name, which needs to be connected to an AnimateDiff Loader
        out = [ckpt_name]
        
        #print("end of function")
        #print(ckpt_name)
        #print(out)

        return out #, out[1], out[2], { "extra_pnginfo": extra_pnginfo }



