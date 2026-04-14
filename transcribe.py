"""
Audio transcriber using OpenAI Whisper.
Transcribes a WAV file to text.
"""

import sys
import whisper
from pathlib import Path


def transcribe_audio(file_name, model_name):
    """Transcribe the recorded audio using Whisper."""
    if not Path(file_name).exists():
        print(f"Audio file not found: {file_name}")
        return None

    try:
        print(f"\nLoading Whisper model '{model_name}'...")
        model = whisper.load_model(model_name)

        print("Transcribing audio...")
        result = model.transcribe(file_name, fp16=False)

        print("\n=== Transcription ===")
        print(result["text"])
        print("=" * 50)

        if "language" in result:
            print(f"Detected language: {result['language']}")

        return result["text"]

    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        return None
