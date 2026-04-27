"""
Orchestrates recording, transcription, and summarization.

Usage:
    python agent.py <skill>
    python agent.py <skill> --transcription <file>
    python agent.py <skill> --audio <file>

    <skill>              Name of a skill file in skills/ (without .md extension)
    --transcription      Path to a transcription file. Skips recording and transcription.
    --audio              Path to an audio file. Skips recording but still transcribes.
"""

import sys
import re
import argparse
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
    skills = list_skills()
    parser = argparse.ArgumentParser(description="Record, transcribe, and summarize audio.")
    parser.add_argument("skill", choices=skills, help="Skill to use for summarization.")
    parser.add_argument(
        "--transcription",
        metavar="FILE",
        type=Path,
        help="Path to a transcription file. Skips recording and transcription.",
    )
    parser.add_argument(
        "--audio",
        metavar="FILE",
        type=Path,
        help="Path to an audio file. Skips recording but still transcribes.",
    )
    args = parser.parse_args()

    if args.transcription and args.audio:
        parser.error("--transcription and --audio are mutually exclusive.")

    skill_prompt = load_skill(args.skill)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    transcription_path = Path(f"transcriptions/transcription_{timestamp}.txt")
    summary_path = Path(f"summaries/summary_{timestamp}.md")
    transcription_path.parent.mkdir(exist_ok=True)
    summary_path.parent.mkdir(exist_ok=True)

    if args.transcription:
        if not args.transcription.exists():
            print(f"Transcription file not found: {args.transcription}", file=sys.stderr)
            sys.exit(1)
        transcription = args.transcription.read_text(encoding="utf-8")
    else:
        if args.audio:
            if not args.audio.exists():
                print(f"Audio file not found: {args.audio}", file=sys.stderr)
                sys.exit(1)
            audio_file = str(args.audio)
        else:
            audio_file = f"audio/output_{timestamp}.wav"
            Path("audio").mkdir(exist_ok=True)

            print("=== Audio Recorder & Transcriber ===\n")
            list_audio_devices()

            if not record_audio(DEVICE, SAMPLE_RATE, CHANNELS, audio_file, DTYPE):
                print("Recording failed.")
                return

        transcription = transcribe_audio(audio_file, WHISPER_MODEL)
        if not transcription:
            print("No transcription available.")
            return

        transcription_path.write_text(transcription, encoding="utf-8")
        print(f"Transcription saved to {transcription_path}")

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
