# Uzbek ASR Benchmarking Tool

**A lightweight pipeline for downloading audio, tracking users, and benchmarking Uzbek speech-to-text models.**

This project lets you:

Ask the user’s name

Create or fetch that user from Supabase

Save the URL they provided

Download audio from YouTube or direct audio links

Run transcription using multiple ASR models

Save results in a results/ folder

Keep the project folder clean (audio stored in audios/ temporarily)

## Features
### User & URL Tracking (Supabase)

* Automatically creates a user if not found

* Assigns user a unique ID

* Stores each URL they submit

* Simple API for future expansion (adding scripts table, storing transcriptions, etc.)

## Audio Handling

**Supports:**

YouTube video → MP3 extraction

Direct audio file links

Automatic file naming and safe paths

## ASR Models

**Currently benchmarks:**

mustafoyev202/whisper-uz
(You can easily add more Whisper or Uzbek models)

Outputs include:

Clean transcription text

Optional timestamps (for Whisper-family models)

## Output

Audio temporarily stored in: audios/

Transcriptions saved to: results/

Both folders are auto-created at runtime.

## Requirements

Python

Python **3.10+**

Install dependencies
pip install transformers yt_dlp requests supabase

FFmpeg

Required for YouTube audio extraction.

FFmpeg install guide: https://ffmpeg.org/download.html

## Project Structure
```bash
project/
│
├── STT_benchmark/
│   ├── main.py              # Main runner script
│   ├── functions.py         # Audio downloading helper functions
│   ├── db.py                # Supabase client connection
│   ├── user_service.py      # User + URL handling logic
│   ├── audios/              # Auto-created temporary folder
│   └── results/             # Auto-created output folder
│
└── README.md
```

## Setup Supabase Credentials

Create a .env file (or set environment variables):

SUPABASE_URL=your_url_here
SUPABASE_SERVICE_KEY=your_service_key_here


Your db.py automatically loads them.

## Usage

Run:

python main.py


**Then follow the prompts:**
```bash
Enter your name: Umrbek
Enter audio or YouTube URL: https://www.youtube.com/watch?v=example
```

The script will:

 1. Create/fetch user

 2. Store the URL in Supabase

 3. Download and process audio

 4. Run ASR model(s)

 5. Save results into:

results/modelname_transcription.txt

## Notes

audios/ and results/ are automatically created.

You should not commit audio or results to Git — they are temporary.

Git ignore rules should contain:

audios/
results/
