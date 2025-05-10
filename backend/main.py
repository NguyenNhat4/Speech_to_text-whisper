from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime
import logging
from transcription import transcribe_audio, save_transcription

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
    allow_origins=["http://localhost:8000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory for storing recordings
STORAGE_DIR = "storage"

# Create storage directory if it doesn't exist
os.makedirs(STORAGE_DIR, exist_ok=True)

# Serve the frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/api/health")
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...), language: str = "english"):
    """
    Endpoint to upload audio file and store it
    
    Args:
        file: The audio file to upload
        language: The language of the audio (english or vietnamese)
    
    Returns:
        Dict with the storage path information
    """
    try:
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
            
        logger.info(f"Audio saved to {audio_path}")
        
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

@app.post("/api/transcribe")
async def transcribe(date_folder: str, session_folder: str, language: str = "english", model_size: str = "base"):
    """
    Endpoint to transcribe an audio file
    
    Args:
        date_folder: The date folder containing the session folder
        session_folder: The session folder containing the audio file
        language: The language of the audio (english or vietnamese)
        model_size: The Whisper model size to use for transcription
    
    Returns:
        Dict with the transcription and file paths
    """
    try:
        # Validate language
        if language.lower() not in ["english", "tiếng việt"]:
            raise HTTPException(status_code=400, detail="Unsupported language")
            
        # Validate model size
        valid_model_sizes = ["tiny", "base", "small", "medium", "large"]
        if model_size.lower() not in valid_model_sizes:
            raise HTTPException(status_code=400, detail=f"Invalid model size. Choose from: {', '.join(valid_model_sizes)}")
        
        # Construct the path to the audio file
        session_dir = os.path.join(STORAGE_DIR, date_folder, session_folder)
        audio_path = os.path.join(session_dir, "audio.webm")
        
        # Check if audio file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
            
        # Transcribe the audio
        transcription = transcribe_audio(audio_path, language, model_size)
        
        # Save the transcription
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 