"""
Audio recorder using sounddevice.
Records audio from the microphone and saves it to a WAV file.
"""

import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading

# Global state
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
    print(sd.query_devices())
    print("=" * 50 + "\n")


def record_audio(device, sample_rate, channels, file_name, dtype='int16'):
    """Record audio from the microphone."""
    global q, recording
    recording = True

    print(f"Using device: {device}")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Channels: {channels}")

    stop_thread = threading.Thread(target=wait_for_enter)
    stop_thread.start()

    try:
        with sf.SoundFile(file_name, mode='w', samplerate=sample_rate, channels=1) as file:
            with sd.InputStream(
                samplerate=sample_rate,
                channels=channels,
                dtype=dtype,
                device=device,
                callback=callback
            ):
                while recording:
                    if channels > 1:
                        # TODO: Separate channels into different files, and transcribe them separately
                        data = np.mean(q.get(), axis=1, dtype=dtype)
                    else:
                        data = q.get()
                    file.write(data)
    except Exception as e:
        print(f"Error during recording: {e}", file=sys.stderr)
        return False

    stop_thread.join()
    return True


def stop_recording():
    """Stop the recording by setting the global flag."""
    global recording
    recording = False
