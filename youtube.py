# pip install yt-dlp

import yt_dlp

def download_youtube_short(url, output_path="%(title)s.%(ext)s", cookies_file=None):
    ydl_opts = {
        'format': 'best',  # best available quality (video+audio combined)
        'outtmpl': output_path,
    }

    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file  # path to cookies.txt exported from browser extension

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    short_url = input("Enter YouTube Short URL: ").strip()
    use_cookies = input("Use cookies file? (y/n): ").strip().lower()

    cookies_path = None
    if use_cookies == 'y':
        cookies_path = input("Path to cookies.txt: ").strip()

    download_youtube_short(short_url, cookies_file=cookies_path)
    print("Done! Check the 'downloads' folder.")