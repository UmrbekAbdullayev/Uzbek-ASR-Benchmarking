# Audio Transcription Tool

This project allows you to download audio from YouTube or direct audio links and transcribe it using multiple speech recognition models, including Whisper and Uzbek speech-to-text models.

## Features

Download audio from YouTube videos.

Download direct audio files (.mp3, .wav, .aac, .ogg, .flac, .m4a).

Transcribe audio using multiple models:

openai/whisper-small (supports timestamps)

ipilot7/uzbek_speach_to_text

mustafoyev202/whisper-uz

Save transcriptions to text files in a results folder.

## Requirements

Python 3.10+

pip packages:

pip install transformers yt_dlp requests


FFmpeg must be installed for audio extraction from YouTube:
FFmpeg Installation Guide

## Project Structure
project/

│

├── merged_folder/       # Up-to-date code and scripts

├── audios/              # Folder where audio files are saved

├── results/             # Folder where transcription results are saved

└── README.md

## Usage

Run the main script:

python main.py


Enter the audio URL (YouTube or direct link) when prompted:

url: https://www.youtube.com/watch?v=example


The script will:

Download the audio into the audios folder

Run all configured speech recognition models

Save each transcription in the results folder as a .txt file

## Notes

For YouTube videos, the audio will be extracted in .mp3 format.

Whisper models support timestamps at the word level, while other models support character-level timestamps.

Ensure a stable internet connection when downloading audio.
