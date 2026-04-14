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


def list_skills():
    skills_dir = Path(__file__).parent / "skills"
    return sorted(p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists())


def main():
    if len(sys.argv) < 2:
        skills = list_skills()
        print("Usage: python agent.py <skill>\n", file=sys.stderr)
        print("Available skills:", file=sys.stderr)
        for skill in skills:
            print(f"  {skill}", file=sys.stderr)
        sys.exit(1)

    skill_prompt = load_skill(sys.argv[1])

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"audio/output_{timestamp}.wav"
    summary_path = Path(f"summaries/summary_{timestamp}.md")

    Path("audio").mkdir(exist_ok=True)
    summary_path.parent.mkdir(exist_ok=True)

    print("=== Audio Recorder & Transcriber ===\n")

    list_audio_devices()

    if not record_audio(DEVICE, SAMPLE_RATE, CHANNELS, file_name, DTYPE):
        print("Recording failed.")
        return

    transcription = transcribe_audio(file_name, WHISPER_MODEL)
    if not transcription:
        print("No transcription available.")
        return

    print("\nSummarizing with AWS Bedrock...")
    summary = summarize(
        transcription, MODEL_ID, REGION,
        aws_profile=AWS_PROFILE,
        system_prompt=skill_prompt
    )
    if not summary:
        print("Summarization failed.")
        return

    print("\n=== Summary ===")
    print(summary)
    print("=" * 50)

    summary_path.write_text(summary, encoding="utf-8")
    print(f"\nSummary saved to {summary_path}")


if __name__ == "__main__":
    main()
