"""
Orchestrates recording, transcription, and summarization.

Usage:
    python agent.py <skill>

    <skill>  Name of a skill file in skills/ (without .md extension)
             The skill body is used as the system prompt for summarization.
"""

import sys
import re
from datetime import datetime
from pathlib import Path

from record import list_audio_devices, record_audio
from transcribe import transcribe_audio
from summarize import summarize

# Recording configuration
DEVICE = 8
SAMPLE_RATE = 16000
CHANNELS = 17
FILE_NAME = f"audio/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
DTYPE = 'int16'

# Transcription configuration
WHISPER_MODEL = "turbo"  # Options: tiny, base, small, medium, large, turbo

# Summarization configuration
MODEL_ID = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"
REGION = "eu-central-1"
AWS_PROFILE = "mykn-analytics-dev-admin"


def load_skill(name):
    """Load the body of a skill file from skills/<name>.md, stripping YAML frontmatter."""
    path = Path(__file__).parent / "skills" / name / "SKILL.md"
    if not path.exists():
        print(f"Skill not found: {path}", file=sys.stderr)
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    # Strip YAML frontmatter (--- ... ---)
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)
    return content.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python agent.py <skill>", file=sys.stderr)
        sys.exit(1)

    skill_prompt = load_skill(sys.argv[1])

    Path("audio").mkdir(exist_ok=True)

    print("=== Audio Recorder & Transcriber ===\n")

    list_audio_devices()

    if not record_audio(DEVICE, SAMPLE_RATE, CHANNELS, FILE_NAME, DTYPE):
        print("Recording failed.")
        return

    transcription = transcribe_audio(FILE_NAME, WHISPER_MODEL)
    if not transcription:
        print("No transcription available.")
        return

    print("\nSummarizing with AWS Bedrock...")
    summary = summarize(
        transcription, MODEL_ID, REGION,
        aws_profile=AWS_PROFILE,
        system_prompt=skill_prompt
    )
    print("\n=== Summary ===")
    print(summary)
    print("=" * 50)


if __name__ == "__main__":
    main()
