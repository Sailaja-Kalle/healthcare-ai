import os
import streamlit as st

def get_supported_languages():
    return {
        "English": "en",
        "Telugu": "te",
        "Hindi": "hi"
    }

def clean_text_for_speech(text):
    """Clean text before converting to speech"""
    import re
    text = re.sub(r'[*#_~`]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    if len(text) > 500:
        text = text[:500] + "..."
    return text

def render_audio_player(text, language="English"):
    """Render audio player for given text"""
    from voice.text_to_speech import play_audio_in_streamlit
    
    clean = clean_text_for_speech(text)
    if clean:
        st.subheader("🔊 Listen to Response")
        if st.button("▶️ Play Audio Response"):
            with st.spinner("Generating audio..."):
                play_audio_in_streamlit(clean, language)