import os
import json
from huggingface_hub import hf_hub_download

# ==============================================================================
# MODEL REGISTRY (Sovereign Tensor Manifolds)
# ==============================================================================
MODELS = {
    "phi-3-mini": {
        "repo": "microsoft/Phi-3-mini-4k-instruct-gguf",
        "file": "Phi-3-mini-4k-instruct-q4.gguf"
    },
    "bitnet-7b": {
        "repo": "1bitLLM/bitnet_b1_58-large",
        "file": "bitnet_b1_58-large-q4_k_m.gguf"
    }
}

def get_model(choice, progress_callback=None):
    """
    Fetch model weights from HuggingFace or return local path if cached
    
    Args:
        choice: Model key ('phi-3-mini' or 'bitnet-7b')
        progress_callback: Optional function to receive status messages
    
    Returns:
        Local file path to .gguf model or None on failure
    """
    spec = MODELS.get(choice, MODELS["phi-3-mini"])
    local_path = os.path.join(os.getcwd(), spec["file"])
    
    # Return cached model if exists
    if os.path.exists(local_path):
        if progress_callback:
            progress_callback(f"Model {choice} cached locally")
        return local_path

    # Seamless download from HuggingFace to local project manifold
    try:
        if progress_callback:
            progress_callback(f"Fetching {choice} Weights...")
        print(f"[MODEL_MANAGER] Downloading {choice} from {spec['repo']}")
        return hf_hub_download(
            repo_id=spec["repo"],
            filename=spec["file"],
            local_dir=os.getcwd()
        )
    except Exception as e:
        print(f"[MODEL_MANAGER] Fetch Error: {e}")
        if progress_callback:
            progress_callback(f"Error fetching {choice}")
        return None

def list_models():
    """Return available model choices"""
    return list(MODELS.keys())

def validate_model(choice):
    """Verify model choice is registered"""
    return choice in MODELS
