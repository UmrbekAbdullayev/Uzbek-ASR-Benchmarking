import requests
from functions import *

def get_audio():
    input_url = input('url: ').strip()
    if is_youtube_link(input_url):
        extract_youtube(input_url) 
    elif is_direct_audio_link(input_url):
        save_audio(input_url)
    else:
        print('Can\'t extract audios from this link')            

if __name__ == "__main__":
    get_audio()



