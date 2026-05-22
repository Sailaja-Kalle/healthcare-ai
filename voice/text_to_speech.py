from gtts import gTTS
import os
import streamlit as st

def text_to_speech(text, language="en"):
    """Convert text to speech and save as audio file"""
    try:
        lang_map = {
            "English": "en",
            "Telugu": "te",
            "Hindi": "hi"
        }
        lang_code = lang_map.get(language, "en")
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        audio_path = "temp_audio_output.mp3"
        tts.save(audio_path)
        
        return audio_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

def play_audio_in_streamlit(text, language="English"):
    """Play audio directly in Streamlit"""
    try:
        audio_path = text_to_speech(text, language)
        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
            os.remove(audio_path)
    except Exception as e:
        st.error(f"Audio error: {str(e)}")