import streamlit as st

def render_voice_input(language="English"):
    lang_map = {
        "English": "en",
        "Telugu": "te",
        "Hindi": "hi"
    }

    st.subheader("🎤 Voice Input")

    try:
        from streamlit_mic_recorder import speech_to_text

        lang_code = lang_map.get(language, "en")

        text = speech_to_text(
            language=lang_code,
            start_prompt="🎤 Click & Speak",
            stop_prompt="⏹️ Stop",
            just_once=True,
            use_container_width=True,
            key="mic_input"
        )

        if text:
            st.success(f"✅ Heard: {text}")
            st.session_state["symptoms_from_voice"] = text
            return text

    except Exception as e:
        st.error(f"Voice error: {str(e)}")

    return st.session_state.get("symptoms_from_voice", "")