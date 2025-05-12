from fastapi import FastAPI, Form ,UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime
import logging
from transcription import transcribe_with_pool, save_transcription
from pydantic import BaseModel
import time
import torch
import subprocess
from model_preload import preload_model
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Speech-to-Text API")

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory for storing recordings
STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))

# Create storage directory if it doesn't exist
os.makedirs(STORAGE_DIR, exist_ok=True)

# Serve the frontend static files
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")




@app.get("/api/health")
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...), language: str =Form("tiếng việt") ):
    """
    Endpoint to upload audio file and store it
    
    Args:
        file: The audio file to upload
        language: The language of the audio (english or vietnamese)
    
    Returns:
        Dict with the storage path information
    """
    try:
        logger.info(f"Language being chosen: {language}")
        
        # Validate language
        if language.lower() not in ["english", "tiếng việt"]:
            raise HTTPException(status_code=400, detail="Unsupported language")
            
        # Create directory structure based on date and time
        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H%M%S")
        
        date_dir = os.path.join(STORAGE_DIR, today)
        session_dir = os.path.join(date_dir, timestamp)
        
        os.makedirs(session_dir, exist_ok=True)
        
        # Save the audio file
        audio_path = os.path.join(session_dir, "audio.webm")
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"Audio file uploaded successfully")
        # logger.info(f"Language being chosen: {language}")
        
        return {
            "message": "Audio file uploaded successfully",
            "date_folder": today,
            "session_folder": timestamp,
            "file_path": audio_path,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Error uploading audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
# Define request models for validation
class TranscriptionRequest(BaseModel):
    date_folder: str
    session_folder: str
    language: str = "tiếng việt"
    model_size: str = "base"

@app.post("/api/transcribe")
async def transcribe(request: TranscriptionRequest):
    """
    Endpoint to transcribe an audio file
    
    Args:
        request: The TranscriptionRequest containing path and settings
    
    Returns:
        Dict with the transcription and file paths
    """
    try:
        # Validate language
        if request.language.lower() not in ["english", "tiếng việt"]:
            raise HTTPException(status_code=400, detail="Unsupported language")
             
        # Validate model size
        valid_model_sizes = ["tiny", "base", "small", "medium", "large-v3"]
        if request.model_size.lower() not in valid_model_sizes:
            raise HTTPException(status_code=400, detail=f"Invalid model size. Choose from: {', '.join(valid_model_sizes)}")
        
        # Construct the path to the audio file
        session_dir = os.path.join(STORAGE_DIR, request.date_folder, request.session_folder)
        audio_path = os.path.join(session_dir, "audio.webm")
        
        # Check if audio file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        start_time = time.time()
        # Transcribe the audio
        transcription = transcribe_with_pool(audio_path, request.language, request.model_size)
        end_time = time.time()
        # Save the transcription
        duration = end_time - start_time
        logger.info(f"Transcription took {duration:.6f} seconds")
        
        transcription_path = os.path.join(session_dir, "transcription.txt")
        save_transcription(transcription, transcription_path)
        
        return {
            "message": "Transcription completed successfully",
            "transcription": transcription,
            "audio_path": audio_path,
            "transcription_path": transcription_path
        }
        
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# We will add more endpoints for speech-to-text conversion later

# Preload the model during startup
@app.on_event("startup")
async def startup_event():
    try:
        # Optimize CUDA settings if available
        if torch.cuda.is_available():
            # Set TensorFloat32 for better performance
            torch.set_float32_matmul_precision('high')
            # Pre-allocate memory to avoid fragmentation
            torch.cuda.empty_cache()
        
        # Preload the large-v3 model
        logger.info("Preloading large-v3 model at startup...")
        preload_model("large-v3")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Set number of workers to 1 to avoid model duplication
    # Set timeout to accommodate longer processing times
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=1, timeout_keep_alive=120) 