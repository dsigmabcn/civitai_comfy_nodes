from .civitai_lora_loader import CivitAI_LORA_Loader
from .civitai_checkpoint_loader import CivitAI_Checkpoint_Loader
from .civitai_mm_loader import CivitAI_mm_Loader

NODE_CLASS_MAPPINGS = {
    "CivitAI_Lora_Loader": CivitAI_LORA_Loader,
    "CivitAI_Checkpoint_Loader": CivitAI_Checkpoint_Loader,
    "CivitAI_mm_Loader": CivitAI_mm_Loader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CivitAI_Lora_Loader": "CivitAI Lora Loader",
    "CivitAI_Checkpoint_Loader": "CivitAI Checkpoint Loader",
    "CivitAI_mm_Loader": "CivitAI_mm_Loader"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
