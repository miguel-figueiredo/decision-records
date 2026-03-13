# Decision Records

This project records audio from your microphone, transcribes it using OpenAI's Whisper model, and exposes the functionality as an MCP server.

## Requirements

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

## Installation

### 1. Clone the repository or download the files

### 2. Set up a Python virtual environment (recommended)

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

### 3. Install the required Python packages

```sh
pip install -r requirements.txt
```

### 4. (Optional) Install ffmpeg for Whisper

Whisper may require `ffmpeg` for some audio formats. Install it via:

- **macOS:**  
  ```sh
  brew install ffmpeg
  ```
- **Ubuntu:**  
  ```sh
  sudo apt-get install ffmpeg
  ```
- **Windows:**  
  Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your PATH.

## Usage

### Standalone Script

1. **Activate your virtual environment** (if you created one):

   **macOS/Linux:**
   ```sh
   source .venv/bin/activate
   ```

   **Windows:**
   ```sh
   .venv\Scripts\activate
   ```

2. **Run the script:**

   ```sh
   python transcribe.py
   ```

3. **Follow the prompts:**
   - The script will list available audio devices
   - Speak into your microphone
   - Press Enter to stop recording
   - Wait for transcription

## Project Structure

- **`transcribe.py`** — Standalone audio recording and transcription module. Records from the microphone, saves to WAV, and transcribes using Whisper. Multi-channel audio is mixed down to mono.
- **`server.py`** — FastMCP server that exposes recording and transcription as MCP tools. Imports functionality from `transcribe.py`.

## Features

- **Audio Recording**: Records audio from your microphone using `sounddevice`
- **Speech-to-Text**: Transcribes audio using OpenAI Whisper
- **Multi-Channel Support**: Mixes multi-channel audio down to mono for transcription
- **Language Detection**: Automatically detects the spoken language
- **MCP Server**: FastMCP server for integration with other tools and services

## Recording Configuration

You can modify the following constants in `transcribe.py`:

- `DEVICE`: Microphone device index (default: 0)
- `SAMPLE_RATE`: Audio sample rate (default: 16000 Hz)
- `CHANNELS`: Number of audio channels (default: 1)
- `MODEL_NAME`: Whisper model to use (options: tiny, base, small, medium, large, turbo)
- `FILE_NAME`: Output file name for the recording

## MCP Configuration

Use the mcp-config.json file contents to configure the file `~/.copilot/mcp-config.json`.

## Running the Copilot CLI 

`copilot --agent decision-record-summarizer`

## Running the MCP Server

```sh
python server.py
```

This launches the FastMCP server on `http://127.0.0.1:8000` with the following tools:

- **`start_recording`** — Starts recording audio from the microphone in a background thread.
- **`get_transcription`** — Stops the recording and returns the transcribed text.

## Starting Copilot CLI



## Notes

- You may need to adjust the `DEVICE` variable in `transcribe.py` to select the correct microphone
- For best results, use a quiet environment when recording
- To deactivate the virtual environment when done, simply run: `deactivate`

## Troubleshooting

- If you get a device error, run `python transcribe.py` to see available devices and update the `DEVICE` constant
- If transcription fails, ensure you have `ffmpeg` installed
