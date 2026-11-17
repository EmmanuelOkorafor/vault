#!/usr/bin/env python3
"""
Combine a still image + an audio file into a video (great for Instagram posts).

Usage:
    python image_audio_to_video.py photo.jpg audio.mp3
    python image_audio_to_video.py photo.jpg audio.mp3 -o birthday.mp4
    python image_audio_to_video.py photo.jpg audio.mp3 --square

Requires ffmpeg to be installed and available on your PATH.
    macOS:   brew install ffmpeg
    Ubuntu:  sudo apt install ffmpeg
    Windows: https://ffmpeg.org/download.html
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def combine(image_path: Path, audio_path: Path, output_path: Path, square: bool, fit: str) -> None:
    if not shutil.which("ffmpeg"):
        sys.exit(
            "Error: ffmpeg is not installed or not on your PATH.\n"
            "Install it first (e.g. 'brew install ffmpeg' or 'sudo apt install ffmpeg')."
        )

    for p in (image_path, audio_path):
        if not p.exists():
            sys.exit(f"Error: file not found: {p}")

    # Build the scale/pad filter so the image fills a clean, Instagram-friendly frame
    # without distortion.
    if square:
        target_w, target_h = 1080, 1080
    else:
        target_w, target_h = 1080, 1920  # vertical, good for Reels/Stories

    if fit == "cover":
        # Fill the frame completely, cropping any overflow.
        vf = (
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
            f"crop={target_w}:{target_h}"
        )
    else:
        # Fit the whole image inside the frame, padding with black bars if needed.
        vf = (
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
            f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:color=black"
        )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image_path),   # loop the still image
        "-i", str(audio_path),                 # the audio track
        "-vf", vf,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",                           # stop when audio ends
        "-movflags", "+faststart",
        str(output_path),
    ]

    print(f"Creating video from '{image_path}' + '{audio_path}' -> '{output_path}' ...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if result.returncode != 0:
        print(result.stdout)
        sys.exit("ffmpeg failed to create the video (see output above).")

    print("Done! Your video is ready to post.")


def main():
    parser = argparse.ArgumentParser(description="Combine a still image and audio into a video.")
    parser.add_argument("image", type=Path, help="Path to the image file (e.g. photo.jpg)")
    parser.add_argument("audio", type=Path, help="Path to the audio file (e.g. audio.mp3)")
    parser.add_argument("-o", "--output", type=Path, default=Path("output_video.mp4"),
                         help="Output video path (default: output_video.mp4)")
    parser.add_argument("--square", action="store_true",
                         help="Use a 1:1 square frame (1080x1080) instead of vertical 9:16 (1080x1920)")
    parser.add_argument("--fit", choices=["cover", "contain"], default="cover",
                         help="'cover' fills the frame and crops overflow (default). "
                              "'contain' shows the whole image with black bars if needed.")
    args = parser.parse_args()

    combine(args.image, args.audio, args.output, args.square, args.fit)


if __name__ == "__main__":
    main()

# python image_audio_to_video.py photo.jpg audio.mp3