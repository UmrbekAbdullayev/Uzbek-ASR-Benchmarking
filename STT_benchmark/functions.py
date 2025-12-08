import os
import requests
from urllib.parse import urlparse
import yt_dlp

AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)


# checks if it is YouTube link
def is_youtube_link(url):
    if not url:
        return False
    return (
        'youtube.com' in url.lower() or
        'youtu.be' in url.lower()
    )


# checks if it is direct audio link
def is_direct_audio_link(url):
    if not url:
        return False

    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    return ext in ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a']


# gets the audio name from the link or content-disposition header
def get_filename(url, response):
    if not url:
        return "downloaded_audio"

    cd = response.headers.get("content-disposition", "")
    if "filename=" in cd:
        filename = cd.split("filename=")[1].strip('"; ')
        if filename:
            return filename

    # fallback to URL path
    name = os.path.basename(urlparse(url).path)
    return name if name else "downloaded_audio"


# save audio from direct link
def save_audio(url):
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("Error downloading audio:", e)
        return None

    filename = get_filename(url, r)
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

        print("Saved:", filepath)
        return filepath  # better return: full path, not folder
    except Exception as e:
        print("Failed saving audio:", e)
        return None


# extract audio from youtube
def extract_youtube(url):
    if not url:
        return None

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{AUDIO_DIR}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
        "quiet": True,  # no spam output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            final_filename = f"{AUDIO_DIR}/{result['title']}.mp3"
            return final_filename
    except Exception as e:
        print("YouTube download error:", e)
        return None
