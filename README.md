# Uzbek-ASR-Benchmarking
This project benchmarks multiple Uzbek speech-to-text (ASR) models on the same audio files using Hugging Face pipelines.   It automatically loads each model, runs transcription, and saves the output into a `/results` folder.
## Project Structure
**STT_benchmarking/**

**│**

**├─ audio/ # Your .mp3 / .wav files go here**

**├─ results/ # Transcriptions will be saved here**

**└─ scripts/**

**└─ run_asr_models.py**

## How to Run
```bash
1. Create and activate your conda environment
conda create -n myenv python=3.10
conda activate myenv

2. Install dependencies
pip install torch transformers librosa soundfile

3. Run the script

From the project root folder, run:
python scripts/run_asr_models.py
Transcriptions will be saved automatically in the:
results/
```

## Models Used

The script currently benchmarks:
**openai/whisper-small,**
**ipilot7/uzbek_speach_to_text, 
mustafoyev202/whisper-uz**

You can add more models in the Python script:
```bash
models = [
    "ipilot7/uzbek_speach_to_text",
    "mustafoyev202/whisper-uz",
    # add more models here
]
```

## Notes

The first model download takes time (1–2GB). This is normal.

CPU inference is slower than GPU.

Whisper models only support "word" or "segment" timestamps.
