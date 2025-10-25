import requests
import pygame
import io
import time
FISH_API_KEY="4691bc0e3869458b9cb7e8fa91cc2941"

def text_to_speech(text, output_file="output.mp3"):
    url = "https://api.fish.audio/v1/tts"
    
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json",
        "model": "s1"
    }
    
    data = {
        "text": text,
        "format": "mp3",
        "reference_id": "6e445b37225c4b8baa00a50296d93ffa"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise error for bad status codes
        
        pygame.mixer.init()
        audio_buffer = io.BytesIO(response.content)
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False

text = "Hello! Welcome to Fish Audio. This is my first AI-generated voice."
text_to_speech(text, "welcome.mp3")