
from fastmcp import FastMCP
import threading
import transcribe

mcp = FastMCP(
    name = "Demo 🚀")

@mcp.tool(description="Starts a recording.")
def start_recording():
    print("starting recording")
    threading.Thread(target=transcribe.record_audio).start()

@mcp.tool(description="Get the recording transcription.")
def get_transcription():
    print("stopping recording")
    transcribe.recording = False
    return transcribe.transcribe_audio()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)