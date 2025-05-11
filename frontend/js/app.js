document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
   
    const recordButton = document.getElementById('recordButton');
    const audioPlayback = document.getElementById('audioPlayback');
    const recordingStatus = document.getElementById('recordingStatus');
    const languageSelect = document.getElementById('language');
    const modelSelect = document.getElementById('model');
    const statusMessage = document.getElementById('statusMessage');
    const spinner = document.getElementById('spinner');
    const transcriptText = document.getElementById('transcriptText');
    const copyButton = document.getElementById('copyButton');
    
    // State variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let audioBlob = null;
    let sessionInfo = null;
    
    // Initialize MediaRecorder
    async function setupMediaRecorder() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                audioPlayback.src = URL.createObjectURL(audioBlob);
                // Upload the audio file
                await uploadAudio();
            };
            
            return true;
        } catch (error) {
            console.error('Error accessing microphone:', error);
            statusMessage.textContent = 'Error: Could not access microphone. Check permissions.';
            return false;
        }
    }
    
    // Toggle recording state
    async function toggleRecording() {
        if (!mediaRecorder && !await setupMediaRecorder()) {
            return;
        }
        
        if (!isRecording) {
            // Start recording
            audioChunks = [];
            mediaRecorder.start();
            isRecording = true;
            
            // Update UI
            recordButton.classList.add('recording');
            recordButton.innerHTML = '<i class="fas fa-stop"></i>';
            recordingStatus.textContent = 'Recording...';
            transcriptText.value = '';
            audioPlayback.src = '';
            sessionInfo = null;
        } else {
            // Stop recording
            mediaRecorder.stop();
            isRecording = false;
            
            // Update UI
            recordButton.classList.remove('recording');
            recordButton.innerHTML = '<i class="fas fa-microphone"></i>';
            recordingStatus.textContent = 'Processing...';
        }
    }
    

    // Upload audio to server
    async function uploadAudio() {
        try {
            // Show loading spinner
            spinner.classList.remove('hidden');
            statusMessage.textContent = 'Uploading audio...';
            
            // Create form data
            const formData = new FormData();
            formData.append('file', audioBlob, 'audio.webm');
            formData.append('language', languageSelect.value);
          
            // Upload the audio file
            
            const response = await fetch('http://localhost:8000/api/upload-audio', {
                method: 'POST',
                body: formData,
            });
           
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
            }
            
            // Get the response data
            sessionInfo = await response.json();
           
            // Start transcription
            await transcribeAudio();
            
        } catch (error) {
            console.error('Error uploading audio:', error);
            spinner.classList.add('hidden');
            statusMessage.textContent = `Error: ${error.message}`;
        }
    }
    
    // Transcribe audio
    async function transcribeAudio() {
        if (!sessionInfo) {
            statusMessage.textContent = 'Error: No session information available';
            spinner.classList.add('hidden');
            return;
        }
        
        try {
            statusMessage.textContent = 'Transcribing audio...';
            // Request transcription
       
            const response = await fetch('http://localhost:8000/api/transcribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    date_folder: sessionInfo.date_folder,
                    session_folder: sessionInfo.session_folder,
                    language: sessionInfo.language,
                    model_size: modelSelect.value
                }),
            });
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
            }
            
            // Get the transcription data
            const transcriptionData = await response.json();
            
            // Update the transcript text
            transcriptText.value = transcriptionData.transcription;
            
            // Hide loading spinner and update status
            spinner.classList.add('hidden');
            statusMessage.textContent = 'Transcription complete!';
            recordingStatus.textContent = 'Ready to record';
            
        } catch (error) {
            console.error('Error transcribing audio:', error);
            spinner.classList.add('hidden');
            statusMessage.textContent = `Error: ${error.message}`;
        }
    }
    
    // Copy transcription to clipboard
    function copyTranscription() {
        if (!transcriptText.value) {
            statusMessage.textContent = 'Nothing to copy.';
            return;
        }
        
        transcriptText.select();
        document.execCommand('copy');
        
        // Show notification
        statusMessage.textContent = 'Copied to clipboard!';
        setTimeout(() => {
            statusMessage.textContent = '';
        }, 2000);
    }
    
    // Event listeners
    recordButton.addEventListener('click', toggleRecording);
    copyButton.addEventListener('click', copyTranscription);
    
    // Check for MediaRecorder support
    if (!window.MediaRecorder) {
        statusMessage.textContent = 'Error: Your browser does not support MediaRecorder. Please use a modern browser.';
        recordButton.disabled = true;
    }
}); 