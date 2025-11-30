import os 
import requests
from urllib.parse import urlparse, parse_qs
import yt_dlp

AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

# checks if it is You Tube link
def is_youtube_link(url):
    return (
        'youtube.com' in url or 
        'youtu.be' in url
    )


# checks if it is direct audio link
def is_direct_audio_link(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    return ext in ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a']


# gets the audio name from the link
def get_filename(url, response):
    cd = response.headers.get("content-disposition")
    if cd:
        parts = cd.split("filename=")
        if len(parts) > 1:
            return parts[1].strip('"; ')
    name = os.path.basename(urlparse(url).path)
    if name:
        return name
    return "downloaded_audio"

def save_audio(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()

    filename = get_filename(url, r)
    filepath = os.path.join(AUDIO_DIR, filename)

    with open(filepath, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    print('Saved:', filepath)


def extract_youtube(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{AUDIO_DIR}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

