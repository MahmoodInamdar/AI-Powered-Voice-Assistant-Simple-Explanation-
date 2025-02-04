
import streamlit as st
import os
import wave
import sounddevice as sd
import numpy as np
import whisper
import openai
from app import init_tts, speak, recognize_speech, chat_with_ai

def record_audio(filename="temp_audio.wav", duration=10, rate=44100, channels=1):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=channels, dtype=np.int16)
    sd.wait()
    st.write("Recording finished.")
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(audio_data.tobytes())
    
    return filename

# Streamlit UI
st.title("AI Teaching Assistant")
st.write("Speak or type to interact with the AI.")

if st.button("Record Audio"):
    audio_file = record_audio()
    user_input = recognize_speech(audio_file)
    st.write("You said:", user_input)
    
    if user_input.strip():
        ai_response = chat_with_ai(user_input)
        st.write("AI:", ai_response)
        speak(ai_response)  # ✅ Removed extra argument (tts_engine)
    else:
        st.write("No speech detected. Try again.")

user_text = st.text_input("Or type your message below:")
if st.button("Send"):
    if user_text.strip():
        ai_response = chat_with_ai(user_text)
        st.write("AI:", ai_response)
        speak(ai_response)  # ✅ Removed extra argument (tts_engine)
    else:
        st.write("Please enter a valid message.")
