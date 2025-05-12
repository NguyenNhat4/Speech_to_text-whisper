import torch
import os
import logging
from transcription import model_pool, get_device

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preload_model(model_size="large-v3"):
    """
    Preload model into memory to avoid cold start delays
    """
    logger.info(f"Preloading {model_size} model...")
    device = get_device()
    
    # Force garbage collection to free up memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Preload model into pool
    model = model_pool.get_model(model_size)
    logger.info(f"Successfully preloaded {model_size} model on {device}")
    return model

if __name__ == "__main__":
    # Preload model when script is run directly
    preload_model("large-v3")
