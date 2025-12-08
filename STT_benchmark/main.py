from transformers import pipeline
import os
from functions import *   # keeps your AUDIO_DIR, is_youtube_link, extract_youtube, save_audio, is_direct_audio_link, etc.
from user_service import get_or_create_user, add_url

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def pick_audio_file(audios_folder):
    """
    Return the most recent audio file path inside audios_folder.
    Returns None if no audio files found.
    """
    if not os.path.isdir(audios_folder):
        return None

    files = [
        f for f in os.listdir(audios_folder)
        if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"))
    ]
    if not files:
        return None

    files.sort(key=lambda fn: os.path.getmtime(os.path.join(audios_folder, fn)), reverse=True)
    return os.path.join(audios_folder, files[0])


def main():
    # 1) Ask for user name & get/create user
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    user = get_or_create_user(name)
    if not user:
        print("Failed to create or fetch user. Check Supabase connection.")
        return

    user_id = user.get("id")
    print(f"Welcome {name}! Your user ID: {user_id}")

    # 2) Get URL from user
    input_url = input("Enter audio or YouTube URL: ").strip()
    if not input_url:
        print("No URL provided.")
        return

    # 3) Save URL in Supabase
    try:
        add_url(user_id, input_url)
    except Exception as e:
        print("Warning: failed to save URL to Supabase:", e)

    # 4) Download audio
    print("Downloading audio...")
    download_result = None

    if is_youtube_link(input_url):
        download_result = extract_youtube(input_url)
    elif is_direct_audio_link(input_url):
        download_result = save_audio(input_url)
    else:
        print("Invalid URL. Cannot extract audio.")
        return

    # download_result may be:
    # - None (failure)
    # - a folder path like "audios"
    # - a full file path like "audios/somefile.mp3"
    if not download_result:
        print("Audio download failed.")
        return

    # Determine audios folder (prefer AUDIO_DIR from functions if present)
    audios_folder = globals().get("AUDIO_DIR", "audios")
    # if the download_result is a folder path, prefer it; if it's a file path, get its folder
    if os.path.isdir(download_result):
        audios_folder = download_result
    else:
        # download_result might be a file path; get its directory
        parent = os.path.dirname(download_result)
        if parent:
            audios_folder = parent

    # 5) Pick the best audio file inside audios_folder
    audio_path = pick_audio_file(audios_folder)
    if not audio_path:
        print("No audio files found in", audios_folder)
        return

    print(f"Using file: {audio_path}")

    # 6) Run transcription models
    models = [
        "mustafoyev202/whisper-uz",
        # "openai/whisper-small",
        # "ipilot7/uzbek_speach_to_text",
    ]

    for model_name in models:
        print(f"\nRunning model: {model_name}...")
        try:
            pipe = pipeline("automatic-speech-recognition", model=model_name)
            if "whisper" in model_name:
                result = pipe(audio_path, return_timestamps="word", language="uz")
            else:
                result = pipe(audio_path, return_timestamps="char")
        except Exception as e:
            print(f"Model {model_name} failed:", e)
            continue

        text = result.get("text", "")

        # 7) Save output to results folder
        safe_name = model_name.replace("/", "_")
        out_file = os.path.join(RESULTS_DIR, f"{safe_name}_transcription.txt")

        try:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved transcription: {out_file}")
        except Exception as e:
            print("Failed to save transcription:", e)

    print("\nDONE — transcription finished!")


if __name__ == "__main__":
    main()
