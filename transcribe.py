"""
Audio recorder and transcriber using OpenAI Whisper.
Records audio from the microphone and transcribes it to text.
"""

import queue
import sys
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
from pathlib import Path

# Configuration
SAMPLE_RATE = 16000
CHANNELS = 17
DEVICE = 7  # Change this to select a different microphone
FILE_NAME = "output_sounddevice.wav"
DTYPE = 'int16'
MODEL_NAME = "turbo"  # Options: tiny, base, small, medium, large, turbo

# Global variables
recording = True
q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


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
    global q, recording
    recording = True
    
    print(f"Using device: {DEVICE}")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Channels: {CHANNELS}")
    
    stop_thread = threading.Thread(target=wait_for_enter)
    stop_thread.start()
    
    try:
        with sf.SoundFile(FILE_NAME, mode='w', samplerate=SAMPLE_RATE,
                      channels=1) as file:
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype=DTYPE,
                device=DEVICE,
                callback=callback
            ):
                while recording:
                    if CHANNELS > 1:
                        # TODO: Separate channels into different files, and transcribe them separately
                        data = np.mean(q.get(), axis=1, dtype=DTYPE)
                    else:
                        data = q.get()
                    file.write(data)
    except Exception as e:
        print(f"Error during recording: {e}", file=sys.stderr)
        return False
    
    stop_thread.join()
    return True


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
    
    # Transcribe
    transcribe_audio()


if __name__ == "__main__":
    main()
