"""
Audio recorder and transcriber using OpenAI Whisper.
Records audio from the microphone and transcribes it to text.
"""

import sys
import os
import whisper
import sounddevice as sd
import numpy as np
import threading
import wave
from pathlib import Path

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
DEVICE = 0  # Change this to select a different microphone
FILE_NAME = "output_sounddevice.wav"
DTYPE = 'int16'
MODEL_NAME = "turbo"  # Options: tiny, base, small, medium, large, turbo

# Global variables
recorded_frames = []
recording = True


def callback(indata, frames, time, status):
    """Callback function to capture audio data."""
    if status:
        print(f"Status: {status}", file=sys.stderr)
    recorded_frames.append(indata.copy())


def wait_for_enter():
    """Wait for user to press Enter to stop recording."""
    input("Recording... Press Enter to stop.\n")
    global recording
    recording = False


def list_audio_devices():
    """Display available audio devices."""
    print("\n=== Available Audio Devices ===")
    devices = sd.query_devices()
    print(devices)
    print("=" * 50 + "\n")


def record_audio():
    """Record audio from the microphone."""
    global recorded_frames, recording
    recorded_frames = []
    recording = True
    
    print(f"Using device: {DEVICE}")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Channels: {CHANNELS}")
    
    stop_thread = threading.Thread(target=wait_for_enter)
    stop_thread.start()
    
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
    
    stop_thread.join()
    return True


def save_audio():
    """Save recorded audio to a WAV file."""
    if not recorded_frames:
        print("No audio data to save.")
        return False
    
    try:
        audio_data = np.concatenate(recorded_frames)
        with wave.open(FILE_NAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
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


def main():
    """Main function to orchestrate recording and transcription."""
    print("=== Audio Recorder & Transcriber ===\n")
    
    # List available devices
    list_audio_devices()
    
    # Record audio
    if not record_audio():
        print("Recording failed.")
        return
    
    # Save audio
    if not save_audio():
        print("Saving audio failed.")
        return
    
    # Transcribe
    transcribe_audio()


if __name__ == "__main__":
    main()
