# Decision Records

Records audio from your microphone, transcribes it using OpenAI Whisper, and summarizes it using AWS Bedrock.

## Requirements

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

## Installation

### 1. Clone the repository or download the files

### 2. Set up a Python virtual environment

**macOS/Linux:**
```sh
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. (Optional) Install ffmpeg

Whisper may require `ffmpeg` for some audio formats:

- **macOS:** `brew install ffmpeg`
- **Ubuntu:** `sudo apt-get install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Usage

```sh
python agent.py
```

- Lists available audio devices
- Starts recording from the configured device
- Press Enter to stop recording
- Transcribes the audio using Whisper
- Summarizes the transcription using AWS Bedrock

## Project Structure

- **`record.py`** — Records audio from the microphone and saves to WAV. Multi-channel audio is mixed down to mono.
- **`transcribe.py`** — Transcribes the WAV file using Whisper.
- **`summarize.py`** — Summarizes text using AWS Bedrock.
- **`agent.py`** — Orchestrates recording, transcription, and summarization.

## Configuration

### Recording (`record.py`)

- `DEVICE`: Audio device index (default: `7`)
- `SAMPLE_RATE`: Sample rate in Hz (default: `16000`)
- `CHANNELS`: Number of audio channels (default: `17`)
- `FILE_NAME`: Output WAV file (default: `output_sounddevice.wav`)

### Transcription (`transcribe.py`)

- `MODEL_NAME`: Whisper model to use (default: `turbo`; options: `tiny`, `base`, `small`, `medium`, `large`, `turbo`)

### Summarization (`agent.py`)

- `MODEL_ID`: AWS Bedrock model ID
- `REGION`: AWS region
- `AWS_PROFILE`: AWS credentials profile

## Audio Capture with BlackHole

[BlackHole](https://existential.audio/blackhole/) is a macOS virtual audio driver for routing audio between applications — useful for capturing both sides of a call.

### Setup

1. Install BlackHole:
   ```sh
   brew install blackhole-16ch
   ```

2. In **Audio MIDI Setup**, create a **Multi-Output Device** with your speakers and BlackHole 16ch, then set it as your system sound output.

3. (Optional) Create an **Aggregate Device** combining your microphone and BlackHole 16ch to capture mic and system audio together.

4. Find the device index:
   ```sh
   python agent.py
   ```
   Note the index of BlackHole 16ch or your Aggregate Device from the printed list.

5. Update `record.py`:
   ```python
   DEVICE = 7      # Replace with your device index
   CHANNELS = 16   # 16 for blackhole-16ch, 2 for blackhole-2ch
   ```

### Typical Workflows

| Scenario | macOS Sound Output | `DEVICE` |
|---|---|---|
| Record system audio only | Multi-Output Device | BlackHole 16ch |
| Record microphone only | Any | Built-in Microphone |
| Record mic + system audio | Multi-Output Device | Aggregate Device |

### Troubleshooting

- **No audio captured:** Ensure macOS sound output is set to the Multi-Output Device.
- **Echo or feedback:** Do not enable monitoring on BlackHole in Audio MIDI Setup.
- **Device not found:** Run `python agent.py` to list devices; reinstall with `brew reinstall blackhole-16ch` if missing.
- **Permission errors:** Go to **System Settings → Privacy & Security → Microphone** and grant access to your terminal.

## Notes

- To deactivate the virtual environment: `deactivate`
- If transcription fails, ensure `ffmpeg` is installed
