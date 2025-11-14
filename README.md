# Speech-to-Text Recorder

This project records audio from your microphone, saves it as a    - Follow the interactive prompts** to:
   - List available audio devices
   - Record and transcribe audio
   - Transcribe existing audio filesile, transcribes it using OpenAI's Whisper model, and optionally generates a summary using OpenAI's API.

## Implementation notes

https://cyberdom.blog/a-step-by-step-guide-for-microsoft-365-copilot-api-development/

## Requirements

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)
- OpenAI API key (optional, for summarization feature)

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
   python test.py
   ```

3. **Follow the prompts:**
   - The script will list available audio devices
   - Press Enter when you're ready to start recording
   - Speak into your microphone
   - Press Enter again to stop recording
   - Wait for transcription and (if configured) summarization

### Using MCP Client

1. **Run the MCP client:**

   ```sh
   python client.py
   ```

2. **Follow the interactive prompts** to:
   - List available audio devices
   - Record and transcribe audio
   - Transcribe existing audio files
   - Generate summaries of transcribed text

## Features

- **Audio Recording**: Records audio from your microphone
- **Speech-to-Text**: Transcribes audio using OpenAI Whisper
- **Language Detection**: Automatically detects the spoken language
- **MCP Server**: FastMCP server for integration with other tools and services

## Configuration

You can modify the following constants in `test.py`:

- `DEVICE`: Microphone device index (default: 0)
- `SAMPLE_RATE`: Audio sample rate (default: 16000 Hz)
- `MODEL_NAME`: Whisper model to use (options: tiny, base, small, medium, large, turbo)
- `FILE_NAME`: Output file name for the recording

## Notes

- You may need to adjust the `DEVICE` variable in `test.py` to select the correct microphone
- For best results, use a quiet environment when recording
- To deactivate the virtual environment when done, simply run: `deactivate`


## Running the MCP Server

The main MCP server for this project is implemented in `server.py`. You can start the MCP server using:

```sh
python server.py
```

This will launch the FastMCP server, making the following MCP tools available:

- `list_audio_devices()` - List all available audio input devices
- `record_audio(device, sample_rate)` - Record audio from microphone
- `transcribe_audio(file_path, model)` - Transcribe audio file

## Hello World Example

A simple FastMCP server example is included to demonstrate the basics:

### Run the Hello World Server

```sh
python hello_server.py
```

### Run the Hello World Client

```sh
python hello_client.py
```

The Hello World example includes three simple tools:
- `hello(name)` - Returns a greeting message
- `add(a, b)` - Adds two numbers
- `get_info()` - Returns server information

## Troubleshooting

- If you get a device error, run the script to see available devices and update the `DEVICE` constant
- If transcription fails, ensure you have `ffmpeg` installed