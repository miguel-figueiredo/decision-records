
from fastmcp import FastMCP
import threading
import sys

import whisper
import numpy as np
import wave
from pathlib import Path
import sounddevice as sd

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 17
DEVICE = 8  # Change this to select a different microphone
FILE_NAME = "output_sounddevice.wav"
DTYPE = 'int16'
MODEL_NAME = "turbo"  # Options: tiny, base, small, medium, large, turbo

# Global variables
recorded_frames = []
recording = True

mcp = FastMCP(
    name = "Demo 🚀")

def callback(indata, frames, time, status):
    """Callback function to capture audio data."""
    if status:
        print(f"Status: {status}", file=sys.stderr)
    recorded_frames.append(indata.copy())

def list_audio_devices():
    """Display available audio devices."""
    print("\n=== Available Audio Devices ===")
    devices = sd.query_devices()
    print(devices)
    print("=" * 50 + "\n")

def record_audio():
    """Record audio from the microphone."""
    list_audio_devices()
    global recorded_frames, recording
    recorded_frames = []
    recording = True
    
    print(f"Using device: {DEVICE}")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Channels: {CHANNELS}")
    
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            device=DEVICE,
            callback=callback
        ):
            while recording:
                sd.sleep(100)
    except Exception as e:
        print(f"Error during recording: {e}", file=sys.stderr)
        return False
    
    return True


def save_audio():
    """Save recorded audio to a WAV file."""
    if not recorded_frames:
        print("No audio data to save.")
        return False
    
    try:
        audio_data = np.concatenate(recorded_frames)
        # Convert to mono by taking the mean across channels
        if CHANNELS > 1:
            audio_data = np.mean(audio_data, axis=1, dtype=DTYPE)
        with wave.open(FILE_NAME, 'wb') as wf:
            wf.setnchannels(1)  # Save as mono
            wf.setsampwidth(np.dtype(DTYPE).itemsize)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data.tobytes())
        
        file_size = Path(FILE_NAME).stat().st_size / 1024  # KB
        print(f"✓ Recording saved as: {FILE_NAME} ({file_size:.2f} KB)")
        return True
    except Exception as e:
        print(f"Error saving audio: {e}", file=sys.stderr)
        return False
    
def transcribe_audio():
    """Transcribe the recorded audio using Whisper."""
    if not Path(FILE_NAME).exists():
        print(f"Audio file not found: {FILE_NAME}")
        return None
    
    try:
        print(f"\nLoading Whisper model '{MODEL_NAME}'...")
        model = whisper.load_model(MODEL_NAME)
        
        print("Transcribing audio...")
        result = model.transcribe(FILE_NAME, fp16=False)
        
        print("\n=== Transcription ===")
        print(result["text"])
        print("=" * 50)
        
        # Optional: Print detected language
        if "language" in result:
            print(f"Detected language: {result['language']}")
        
        return result["text"]
        
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        return None

@mcp.tool(description="Starts a recording.")
def start_recording():
    print("starting recording")
    threading.Thread(target=record_audio).start()

@mcp.tool(description="Get the recording transcription.")
def get_transcription():
    print("stopping recording")
    global recording
    recording = False
    save_audio()
    return transcribe_audio()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)