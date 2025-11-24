from transformers import pipeline
import os

# Folders
audio_file = 'audio.mp3' 
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
        result = pipe(audio_file, return_timestamps="word", language="uz")
    else:
        result = pipe(audio_file, return_timestamps="char")

    text = result["text"]

    out_file = os.path.join(results_folder, f"{model_name.replace('/', '_')}_transcription.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcription: {out_file}")
