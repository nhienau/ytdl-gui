import json
import yt_dlp

def extract(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        result = ydl.sanitize_info(info)
    return result