import subprocess

input_video = "Video by primemovies.mp4"
output_video = "Video by primemovies no audio.mp4"

volume_level = 0.3  # 30% volume

command = [
    "ffmpeg",
    "-y",
    "-i", input_video,
    "-filter:a", f"volume={volume_level}",
    "-c:v", "copy",      # keep video untouched
    output_video
]

subprocess.run(command, check=True)
