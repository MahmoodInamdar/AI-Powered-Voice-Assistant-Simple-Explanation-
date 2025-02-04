import pyttsx3
import openai
import os
import wave
import sounddevice as sd
import numpy as np
import whisper
from dotenv import load_dotenv
load_dotenv()

def init_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    return engine

from gtts import gTTS
import os

def speak(text):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("afplay response.mp3") 

def record_audio(filename="temp_audio.wav", duration=5, rate=44100, channels=1):
    print("Recording...")
    audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=channels, dtype=np.int16)
    sd.wait()
    print("Recording finished.")
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(audio_data.tobytes())
    
    return filename

def recognize_speech(filename="temp_audio.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result.get('text', "")

def chat_with_ai(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "API key is missing. Please set the OPENAI_API_KEY environment variable."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

if __name__ == "__main__":
    tts_engine = init_tts()
    while True:
        audio_file = record_audio()
        user_input = recognize_speech(audio_file)
        if not user_input.strip():
            print("No speech detected. Try again.")
            continue
        
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        ai_response = chat_with_ai(user_input)
        print("AI:", ai_response)
        speak(ai_response)
