#!/usr/bin/env python3
"""
Extract audio from an MP4 (or other video) file.

Usage:
    python extract_audio.py input.mp4
    python extract_audio.py input.mp4 -o output.mp3
    python extract_audio.py input.mp4 -f wav

Requires ffmpeg to be installed and available on your PATH.
On most systems:
    macOS:   brew install ffmpeg
    Ubuntu:  sudo apt install ffmpeg
    Windows: https://ffmpeg.org/download.html
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def extract_audio(input_path: Path, output_path: Path, audio_format: str) -> None:
    if not shutil.which("ffmpeg"):
        sys.exit(
            "Error: ffmpeg is not installed or not on your PATH.\n"
            "Install it first (e.g. 'brew install ffmpeg' or 'sudo apt install ffmpeg')."
        )

    if not input_path.exists():
        sys.exit(f"Error: input file not found: {input_path}")

    # Codec selection based on desired output format
    codec_map = {
        "mp3": ["-vn", "-acodec", "libmp3lame", "-q:a", "2"],
        "wav": ["-vn", "-acodec", "pcm_s16le"],
        "aac": ["-vn", "-acodec", "aac", "-b:a", "192k"],
        "flac": ["-vn", "-acodec", "flac"],
        "m4a": ["-vn", "-acodec", "aac", "-b:a", "192k"],
    }

    codec_args = codec_map.get(audio_format)
    if codec_args is None:
        sys.exit(f"Error: unsupported audio format '{audio_format}'. "
                  f"Choose from: {', '.join(codec_map)}")

    cmd = ["ffmpeg", "-y", "-i", str(input_path), *codec_args, str(output_path)]

    print(f"Extracting audio from '{input_path}' -> '{output_path}' ...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if result.returncode != 0:
        print(result.stdout)
        sys.exit("ffmpeg failed to extract audio (see output above).")

    print("Done!")


def main():
    parser = argparse.ArgumentParser(description="Extract audio from a video file using ffmpeg.")
    parser.add_argument("input", type=Path, help="Path to the input video file (e.g. video.mp4)")
    parser.add_argument("-o", "--output", type=Path, default=None,
                         help="Path to the output audio file. Defaults to same name with new extension.")
    parser.add_argument("-f", "--format", default="mp3",
                         choices=["mp3", "wav", "aac", "flac", "m4a"],
                         help="Audio format to extract (default: mp3)")
    args = parser.parse_args()

    output_path = args.output or args.input.with_suffix(f".{args.format}")
    extract_audio(args.input, output_path, args.format)


if __name__ == "__main__":
    main()


# python extract_audio.py video.mp4              # -> video.mp3
# python extract_audio.py video.mp4 -f wav        # -> video.wav
# python extract_audio.py video.mp4 -o audio.mp3  # custom output name