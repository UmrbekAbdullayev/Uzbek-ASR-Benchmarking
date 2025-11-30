from transformers import pipeline
import os
import requests
from functions import *

def get_audio():
    input_url = input('url: ').strip()
    if is_youtube_link(input_url):
        return extract_youtube(input_url) 
    elif is_direct_audio_link(input_url):
        return save_audio(input_url)
    else:
        print('Can\'t extract audios from this link')            
        return None


# Folders
folder_path = get_audio()
audio_file = os.listdir(folder_path)
if audio_file:
    file_path = os.path.join(folder_path, audio_file[0])



results_folder = "results"
os.makedirs(results_folder, exist_ok=True)

models = [
    "openai/whisper-small",
    "ipilot7/uzbek_speach_to_text",
    "mustafoyev202/whisper-uz",
]

for model_name in models:
    print(f"Running model: {model_name} ...")
    pipe = pipeline("automatic-speech-recognition", model=model_name)

    if "whisper" in model_name:
        result = pipe(file_path, return_timestamps="word", language="uz")
    else:
        result = pipe(file_path, return_timestamps="char")

    text = result["text"]

    out_file = os.path.join(results_folder, f"{model_name.replace('/', '_')}_transcription.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcription: {out_file}")




if __name__ == "__main__":
    folder_path = get_audio()    # returns "audios"

    if folder_path is None:
        exit()

    audio_files = os.listdir(folder_path)

    if not audio_files:
        print("No audio files found.")
        exit()

    file_path = os.path.join(folder_path, audio_files[0])


