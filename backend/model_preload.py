import torch
import os
import logging
from transcription import model_pool, get_device
from hf_transcription import preload_hf_model, DEFAULT_MODEL_ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preload_model(model_size="large-v3", use_hf=False):
    """
    Preload model into memory to avoid cold start delays
    
    Args:
        model_size: Size of the Whisper model to use ('tiny', 'base', 'small', 'medium', 'large-v3', 'turbo')
        use_hf: Whether to use the HuggingFace model instead of the original Whisper model
    """
    # Force garbage collection to free up memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    if use_hf:
        logger.info(f"Preloading HuggingFace Whisper model...")
        model = preload_hf_model(DEFAULT_MODEL_ID)
        logger.info(f"Successfully preloaded HuggingFace Whisper model")
    else:
        logger.info(f"Preloading {model_size} model...")
        device = get_device()
        # Preload model into pool
        model = model_pool.get_model(model_size)
        logger.info(f"Successfully preloaded {model_size} model on {device}")
    
    return model

def preload_all_models():
    """Preload both the standard Whisper (large-v3 and turbo) and HuggingFace Whisper models"""
    logger.info("Preloading all Whisper models...")
    preload_model("large-v3", use_hf=False)
    preload_model("turbo", use_hf=False)
    
    # Optionally load HuggingFace model if needed
    # preload_model(use_hf=True)
    
    return {"message": "All models preloaded successfully"}

if __name__ == "__main__":
    # Preload model when script is run directly
    preload_all_models()
