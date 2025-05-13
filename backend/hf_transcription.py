import os
import logging
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from threading import Lock
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default model ID for Whisper Large V3 Turbo from HuggingFace
DEFAULT_MODEL_ID = "openai/whisper-large-v3-turbo"

class HFModelPool:
    def __init__(self, max_models=1):
        self.models = {}
        self.processors = {}  # Store processors alongside models
        self.pipelines = {}  # Store complete pipelines
        self.last_used = {}
        self.max_models = max_models
        self.lock = Lock()
  
    def get_pipeline(self, model_id=DEFAULT_MODEL_ID):
        """Get or create a speech-to-text pipeline for the specified model"""
        with self.lock:
            device = get_device()
            key = f"{model_id}_{device}"
            
            if key in self.pipelines:
                self.last_used[key] = time.time()
                return self.pipelines[key]
            
            logger.info(f"Loading HuggingFace model {model_id} on {device}...")
            
            # Load model and processor
            torch_dtype = torch.float16 if device == "cuda" else torch.float32
            
            try:
                model = AutoModelForSpeechSeq2Seq.from_pretrained(
                    model_id,
                    torch_dtype=torch_dtype,
                    low_cpu_mem_usage=True,
                    use_safetensors=True
                )
                model.to(device)
                
                processor = AutoProcessor.from_pretrained(model_id)
                
                # Create the pipeline
                pipe = pipeline(
                    "automatic-speech-recognition",
                    model=model,
                    tokenizer=processor.tokenizer,
                    feature_extractor=processor.feature_extractor,
                    max_new_tokens=128,
                    chunk_length_s=30,
                    batch_size=16,
                    return_timestamps=True,
                    torch_dtype=torch_dtype,
                    device=device,
                )
                
                # Remove oldest pipeline if pool is full
                if len(self.pipelines) >= self.max_models:
                    oldest_key = min(self.last_used.items(), key=lambda x: x[1])[0]
                    logger.info(f"Removing oldest model {oldest_key} from pool")
                    del self.pipelines[oldest_key]
                    del self.last_used[oldest_key]
                
                self.pipelines[key] = pipe
                self.last_used[key] = time.time()
                
                return pipe
                
            except Exception as e:
                logger.error(f"Error loading HuggingFace model: {str(e)}")
                if device == "cuda":
                    logger.info("Falling back to CPU model")
                    return self.get_pipeline(model_id)  # Recursive call will use CPU
                else:
                    raise

# Create global model pool
hf_model_pool = HFModelPool(max_models=1)  # Set to 1 to manage memory usage

def get_device():
    """Determine the appropriate device (CUDA GPU or CPU) for running the model."""
    cuda_available = torch.cuda.is_available()
    logger.info(f"CUDA available: {cuda_available}")
    
    if cuda_available:
        # Get GPU memory info
        device_props = torch.cuda.get_device_properties(0)
        logger.info(f"GPU device: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU memory: {device_props.total_memory / 1024**3:.2f} GB")
        device = "cuda"
    else:
        logger.info("No CUDA device available. Using CPU instead.")
        device = "cpu"
        
    return device

def preload_hf_model(model_id=DEFAULT_MODEL_ID):
    """Preload the HuggingFace Whisper model into memory"""
    logger.info(f"Preloading HuggingFace model {model_id}...")
    device = get_device()
    
    # Force garbage collection to free up memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Preload model into pool
    pipeline = hf_model_pool.get_pipeline(model_id)
    logger.info(f"Successfully preloaded HuggingFace model {model_id} on {device}")
    return pipeline

def transcribe_with_hf(audio_path, language="tiếng việt", model_id=DEFAULT_MODEL_ID):
    """
    Transcribe the audio file using the HuggingFace Whisper model.
    
    Args:
        audio_path: Path to the audio file to transcribe
        language: Language of the audio (english or vietnamese)
        model_id: HuggingFace model ID to use
        
    Returns:
        Transcription text
    """
    try:
        # Map UI language choices to Whisper language codes
        language_map = {
            "english": "en",
            "tiếng việt": "vi"
        }
        
        language_code = language_map.get(language.lower(), "vi")
        audio_path = os.path.abspath(audio_path)
        
        # Log transcription start
        logger.info(f"Starting HF transcription for {audio_path} in {language_code}")
        
        # Get the pipeline
        pipe = hf_model_pool.get_pipeline(model_id)
        
        # Generate transcription
        logger.info("Running transcription...")
        result = pipe(
            audio_path,
            generate_kwargs={"language": language_code, "task": "transcribe"}
        )
        
        # Extract the transcribed text
        transcription = result["text"]
        
        # Log successful transcription
        logger.info(f"HF Transcription complete: {len(transcription)} characters")
        
        return transcription
        
    except Exception as e:
        logger.error(f"HF Transcription error: {str(e)}")
        raise
