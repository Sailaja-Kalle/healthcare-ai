import streamlit as st
from backend.groq_client import get_ai_response, get_streaming_response
from utils.prompts import get_general_chat_prompt, get_symptom_analysis_prompt
from gtts import gTTS
import os

# ─── Audio helpers ───────────────────────────────────────────
def speak_text_chat(text, language="English"):
    try:
        lang_map = {"English": "en", "Telugu": "te", "Hindi": "hi"}
        lang_code = lang_map.get(language, "en")
        clean_text = text[:600].replace("*", "").replace("#", "")
        tts = gTTS(text=clean_text, lang=lang_code, slow=False)
        audio_path = "chat_audio.mp3"
        tts.save(audio_path)
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        os.remove(audio_path)
        return audio_bytes
    except:
        return None

def audio_player_chat(text, language, label="🔊 Listen to Answer:"):
    audio_bytes = speak_text_chat(text, language)
    if audio_bytes:
        st.markdown(f"**{label}**")
        st.audio(audio_bytes, format="audio/mp3")

# ─── Chat helpers ─────────────────────────────────────────────
def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I am your AI Healthcare Assistant. I can help you find hospitals, understand symptoms, and estimate treatment costs. How can I help you today?"
            }
        ]

def render_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content
    })

# ─── Main chatbot renderer ────────────────────────────────────
def render_chatbot(language="English", city="", hospital_type="All"):

    st.subheader("💬 Chat with AI Healthcare Assistant")

    # Initialize chat
    initialize_chat()

    # ── Mic input for chat query ──────────────────────────────
    from streamlit_mic_recorder import speech_to_text as stt_chat

    st.markdown("🎤 **Speak your health question:**")
    chat_voice = stt_chat(
        language="en",
        start_prompt="🎤 Speak Question",
        stop_prompt="⏹️ Stop",
        just_once=True,
        use_container_width=True,
        key="chat_mic"
    )

    # When mic captures → store in session state key used by chat_input
    if chat_voice and chat_voice.strip():
        st.session_state["chat_voice_input"] = chat_voice.strip()
        st.success(f"✅ Heard: {chat_voice.strip()}")

    # Show auto-filled text box so user can see/edit what was heard
    if st.session_state.get("chat_voice_input"):
        st.info(f"📝 Query ready: **{st.session_state['chat_voice_input']}**")

    # Render chat history
    render_chat_history()

    # ── Chat input (typed or auto-filled from voice) ──────────
    user_input = st.chat_input(
        "Type your symptoms or health question here..."
    )

    # Use voice input if no typed input
    final_input = user_input
    if not final_input and st.session_state.get("chat_voice_input"):
        final_input = st.session_state.pop("chat_voice_input")

    if final_input:
        # Add user message
        add_message("user", final_input)
        with st.chat_message("user"):
            st.markdown(final_input)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                context = f"User is from {city}. Hospital preference: {hospital_type}."

                prompt = get_general_chat_prompt(
                    user_message=final_input,
                    language=language,
                    context=context
                )

                response_placeholder = st.empty()
                full_response = ""

                for chunk in get_streaming_response(prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

        # Add assistant message to history
        add_message("assistant", full_response)

        # ── Voice playback of AI answer ───────────────────────
        audio_player_chat(full_response, language, "🔊 Listen to Answer:")