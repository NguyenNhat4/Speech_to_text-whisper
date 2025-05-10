# Speech-to-Text Web Application

A web application that helps users quickly convert speech to text using OpenAI's Whisper model running locally. The application supports both English and Vietnamese languages.

## Features

- Record audio directly from your microphone
- Convert speech to text with OpenAI Whisper model
- Support for English and Vietnamese languages
- Choose different Whisper model sizes for varying accuracy/speed
- Automatically save recordings and transcriptions in an organized folder structure
- Copy transcriptions to clipboard with a single click

## Requirements

- Python 3.8+
- Web browser with MediaRecorder API support (most modern browsers)
- Sufficient RAM and processing power to run Whisper models:
  - Recommended: 16GB RAM, CUDA-capable GPU (for medium/large models)
  - Minimum: 8GB RAM (for tiny/base models)

## Setup and Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd speech-to-text-app
   ```

2. Create a Python virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required Python packages:
   ```
   pip install -r backend/requirements.txt
   ```

4. Start the application:
   ```
   cd backend
   python main.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

## Usage

1. Select your preferred language (English or Vietnamese)
2. Select the Whisper model size (trade-off between speed and accuracy)
3. Click the microphone button to start recording
4. Speak into your microphone
5. Click the stop button to end recording
6. Wait for the transcription process to complete
7. View your transcription and use the copy button to copy it to clipboard

## Folder Structure

```
speech-to-text-app/
├── backend/             # Python FastAPI backend
│   ├── main.py          # Main FastAPI application
│   ├── transcription.py # Whisper transcription module
│   └── requirements.txt # Python dependencies
├── frontend/            # Web frontend
│   ├── index.html       # Main HTML page
│   ├── css/             # CSS styles
│   │   └── style.css
│   └── js/              # JavaScript
│       └── app.js
├── storage/             # Recordings and transcriptions storage
│   └── YYYY-MM-DD/      # Date folders
│       └── HHMMSS/      # Session folders
│           ├── audio.webm       # Audio recording
│           └── transcription.txt # Transcription text
└── README.md            # Project documentation
```

## Technical Details

- **Backend**: Python with FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Speech-to-Text**: OpenAI Whisper model (running locally)
- **Data Storage**: Local file system with organized folder structure

## License

This project is open source and available under the [MIT License]. 