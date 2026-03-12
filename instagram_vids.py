import yt_dlp

url = "https://www.instagram.com/reel/DEdbxQ5PKI-/?igsh=eWI3cmhiOTIycTYw"

ydl_opts = {
    "cookiefile": "cookies.txt",
    "outtmpl": "%(title)s.%(ext)s",
    "format": "mp4"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
