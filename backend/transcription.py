import os
import logging
import whisper
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the loaded models
models = {}

def get_device():
    """Determine the appropriate device (CUDA GPU or CPU) for running Whisper."""
    cuda_available = torch.cuda.is_available()
    logger.info(f"CUDA available: {cuda_available}")
    
    if cuda_available:
        logger.info(f"CUDA version: {torch.version.cuda}")
        logger.info(f"GPU device: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU device count: {torch.cuda.device_count()}")
        device = "cuda"
    else:
        logger.info("No CUDA device available. Using CPU instead.")
        device = "cpu"
        
    return device

def get_model(model_size="base"):
    """
    Get or load the Whisper model of the specified size.
    
    Args:
        model_size: Size of the Whisper model ('tiny', 'base', 'small', 'medium', 'large')
        
    Returns:
        The loaded Whisper model
    """
    device = get_device()
    
    # Check if model is already loaded
    model_key = f"{model_size}_{device}"
    if model_key in models:
        return models[model_key]
    
    # Log model loading information
    logger.info(f"Loading Whisper {model_size} model on {device}...")
    
    try:
        # Force CUDA device if it's available
        if device == "cuda":
            # Set PyTorch to use GPU
            torch.cuda.set_device(0)
            
        # Load the model
        model = whisper.load_model(model_size, device=device)
        
        # Cache the model for future use
        models[model_key] = model
        
        logger.info(f"Whisper {model_size} model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading Whisper model: {str(e)}")
        # Fallback to CPU if GPU loading fails
        if device == "cuda":
            logger.info("Falling back to CPU model")
            model = whisper.load_model(model_size, device="cpu")
            models[f"{model_size}_cpu"] = model
            return model
        else:
            raise

def transcribe_audio(audio_path, language="tiếng việt", model_size="base"):
    """
    Transcribe the audio file using the Whisper model.
    
    Args:
        audio_path: Path to the audio file to transcribe
        language: Language of the audio (english or vietnamese)
        model_size: Size of the Whisper model to use
        
    Returns:
        Transcription text
    """
    try:
        # Map UI language choices to Whisper language codes
        language_map = {
            "english": "en",
            "tiếng việt": "vi"
        }
        audio_path = os.path.abspath(audio_path)
        language_code = language_map.get(language.lower(), "vi")
        
        # Log transcription start
        logger.info(f"Starting transcription for {audio_path} in {language_code}")
        
        # Get the model
        model = get_model(model_size)
        
        # Set transcription options
        transcribe_options = {
            "language": language_code,
            "task": "transcribe",
        }
        
        # Perform transcription
        result = model.transcribe(audio_path, **transcribe_options)
        
        # Extract and return the transcribed text
        transcription = result["text"]
        
        # Log successful transcription
        logger.info(f"Transcription complete: {len(transcription)} characters")
        
        return transcription
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise
        
def save_transcription(transcription, output_path):
    """
    Save the transcription text to a file.
    
    Args:
        transcription: The transcription text to save
        output_path: Path where to save the transcription text file
        
    Returns:
        Path to the saved transcription file
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription)
        
        logger.info(f"Transcription saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error saving transcription: {str(e)}")
        raise 