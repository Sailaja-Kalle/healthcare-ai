import streamlit as st
from frontend.sidebar import render_sidebar
from frontend.chatbot_ui import render_chatbot
from frontend.hospital_cards import render_hospital_list, render_cost_card, render_emergency_card
from backend.recommendation_engine import get_recommendations
from backend.emergency_detector import detect_emergency, get_first_aid_tips
from backend.cost_estimator import get_treatment_cost
from utils.prompts import get_symptom_analysis_prompt
from backend.groq_client import get_ai_response
from frontend.login_ui import render_login_page
from frontend.history_ui import render_history_tab
from frontend.symptom_checker_ui import render_symptom_checker
from database.history import save_history
from gtts import gTTS
import os
import re

def clean_cost_for_speech(text):
    text = re.sub(r'(\d+)\.0L', r'\1 lakh', text)
    text = re.sub(r'(\d+\.\d+)L', lambda m: f"{int(float(m.group(1)))} lakh" if float(m.group(1)) == int(float(m.group(1))) else f"{m.group(1)} lakh", text)
    text = re.sub(r'(\d+)L', r'\1 lakh', text)
    text = re.sub(r'(\d+)K', r'\1 thousand', text)
    text = text.replace("₹", "").replace("–", "to")
    return text

def speak_text(text, language="English"):
    try:
        lang_map = {"English": "en", "Telugu": "te", "Hindi": "hi"}
        lang_code = lang_map.get(language, "en")
        clean_text = text[:500].replace("*","").replace("#","")
        tts = gTTS(text=clean_text, lang=lang_code, slow=False)
        audio_path = "response_audio.mp3"
        tts.save(audio_path)
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        os.remove(audio_path)
        return audio_bytes
    except:
        return None

def audio_player(text, language, label="🔊 Listen:"):
    audio_bytes = speak_text(text, language)
    if audio_bytes:
        st.markdown(f"**{label}**")
        st.audio(audio_bytes, format="audio/mp3")

def render_main_ui():
    st.set_page_config(
        st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #fce4ec, #f3e5f5, #e1f5fe, #fffde7);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8bbd0, #e1bee7);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e91e8c, #9c27b0) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 500 !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #ad1457, #6a1b9a) !important;
        transform: scale(1.02);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: #fce4ec !important;
        border-radius: 20px !important;
        color: #880e4f !important;
        margin-right: 6px !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e91e8c, #9c27b0) !important;
        color: white !important;
    }

    /* Input boxes */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid #ce93d8 !important;
        border-radius: 12px !important;
        background: #fdf6ff !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #9c27b0 !important;
        box-shadow: 0 0 0 2px #e1bee7 !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #fce4ec, #e1bee7) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border: 1px solid #f48fb1 !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #6a1b9a !important;
    }

    /* Info/Success boxes */
    .stInfo {
        background: #e1f5fe !important;
        border-left: 4px solid #03a9f4 !important;
        border-radius: 10px !important;
    }

    .stSuccess {
        background: #f3e5f5 !important;
        border-left: 4px solid #9c27b0 !important;
        border-radius: 10px !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border: 2px solid #ce93d8 !important;
        border-radius: 12px !important;
        background: #fdf6ff !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #fce4ec, #e1f5fe) !important;
        border-radius: 10px !important;
        color: #6a1b9a !important;
    }

    /* Title bar color */
    .stTitle {
        color: #ad1457 !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #9c27b0 !important;
    }
</style>
""", unsafe_allow_html=True)
        page_title="AI Healthcare Assistant",
        page_icon="⚕️",
        layout="wide"
    )

    # ═══════════════ LOGIN GATE ═══════════════
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        render_login_page()
        return

    # ═══════════════ TOP BAR (after login) ═══════════════
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("⚕️ AI Healthcare Assistant")
    with col2:
        username = st.session_state.get("username", "Guest")
        st.markdown(f"<br>👤 **{username}**", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["logged_in", "user", "user_id", "username"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("### Find the right hospital and treatment guidance across India")
    st.markdown("---")

    settings = render_sidebar()
    language = settings["language"]
    city = settings["city"]
    hospital_type = settings["hospital_type"]

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Find Hospitals",
    "💬 AI Chat",
    "💰 Cost Estimator",
    "📚 Medical Knowledge Base",
    "📜 My History",
    "🤖 Symptom Checker"
])

    # ═══════════════ TAB 1 - FIND HOSPITALS ═══════════════
    with tab1:
        st.subheader("🔍 Describe Your Health Problem")

        from voice.speech_to_text import render_voice_input
        voice_text = render_voice_input(language)
        if voice_text:
            st.session_state["symptoms_from_voice"] = voice_text
            st.session_state["symptoms_area"] = voice_text

        default_symptoms = st.session_state.get("symptoms_from_voice", "")

        symptoms = st.text_area(
            "Enter your symptoms",
            value=default_symptoms,
            placeholder="e.g. I have chest pain and breathing problem...",
            height=100,
            key="symptoms_area"
        )

        col1, col2 = st.columns(2)
        with col1:
            from streamlit_mic_recorder import speech_to_text as stt_city
            city_voice = stt_city(
                language="en",
                start_prompt="🎤 Speak City",
                stop_prompt="⏹️ Stop",
                just_once=True,
                use_container_width=True,
                key="city_mic"
            )
            if city_voice:
                st.session_state["city_from_voice"] = city_voice
                st.success(f"✅ City: {city_voice}")

            search_city = st.text_input(
                "Your City",
                value=st.session_state.get("city_from_voice", city),
                placeholder="e.g. Hyderabad"
            )

        with col2:
            h_type = st.selectbox(
                "Hospital Type",
                ["All", "Government", "Private"],
                key="tab1_hospital_type"
            )

        lang_messages = {
            "English": "Please enter your city name and click Find Hospitals button",
            "Telugu": "దయచేసి మీ నగరం పేరు నమోదు చేయండి మరియు హాస్పిటల్స్ వెతకండి బటన్ నొక్కండి",
            "Hindi": "कृपया अपने शहर का नाम दर्ज करें और हॉस्पिटल खोजें बटन दबाएं"
        }
        audio_bytes = speak_text(lang_messages.get(language, lang_messages["English"]), language)
        if audio_bytes:
            st.markdown("🔊 **Instructions:**")
            st.audio(audio_bytes, format="audio/mp3")

        if st.button("🔍 Find Hospitals", type="primary"):
            if not symptoms:
                st.warning("Please enter your symptoms first.")
            elif not search_city:
                st.warning("Please enter your city.")
            else:
                with st.spinner("Finding best hospitals for you..."):

                    emergency = detect_emergency(symptoms)
                    render_emergency_card(emergency)

                    if emergency.get("is_emergency"):
                        emergency_msgs = {
                            "English": "Emergency detected! Please call 108 immediately!",
                            "Telugu": "అత్యవసర పరిస్థితి! దయచేసి వెంటనే 108 కి కాల్ చేయండి!",
                            "Hindi": "आपातकाल! कृपया तुरंत 108 पर कॉल करें!"
                        }
                        audio_player(emergency_msgs.get(language, emergency_msgs["English"]), language, "🚨 Emergency Alert:")

                    prompt = get_symptom_analysis_prompt(symptoms, language)
                    ai_analysis = get_ai_response(prompt)

                    st.subheader("🤖 AI Analysis")
                    st.info(ai_analysis)
                    audio_player(ai_analysis, language, "🔊 Listen to AI Analysis:")

                    # Save to history
                    if st.session_state.get("user_id"):
                        save_history(st.session_state["user_id"], "hospital_search", symptoms, ai_analysis, language)

                    recommendations = get_recommendations(symptoms, search_city, h_type)
                    hospitals = recommendations["hospitals"]
                    render_hospital_list(hospitals, f"🏥 Hospitals in {search_city}")

                    if hospitals is not None and not hospitals.empty:
                        st.markdown("---")
                        st.subheader(f"🗺️ Hospital Locations in {search_city}")
                        from frontend.map_view import render_hospital_map
                        render_hospital_map(hospitals, search_city)

                    if hospitals is not None and not hospitals.empty:
                        hospital_names = ", ".join(hospitals["hospital_name"].tolist())
                        hospital_msgs = {
                            "English": f"Found {len(hospitals)} hospitals near you: {hospital_names}",
                            "Telugu": f"మీ దగ్గర {len(hospitals)} ఆసుపత్రులు దొరికాయి: {hospital_names}",
                            "Hindi": f"आपके पास {len(hospitals)} अस्पताल मिले: {hospital_names}"
                        }
                        audio_player(hospital_msgs.get(language, hospital_msgs["English"]), language, "🔊 Hospital Info:")

                    if recommendations["cost_info"]:
                        render_cost_card(recommendations["cost_info"])
                        cost = recommendations["cost_info"]
                        gov = clean_cost_for_speech(cost['government_cost'])
                        pvt = clean_cost_for_speech(cost['private_cost'])
                        cost_msgs = {
                            "English": f"Government hospital cost is {gov} rupees. Private hospital cost is {pvt} rupees. Treatment takes about {cost['duration_days']} days.",
                            "Telugu": f"ప్రభుత్వ ఆసుపత్రి ఖర్చు {gov} రూపాయలు. ప్రైవేట్ ఆసుపత్రి ఖర్చు {pvt} రూపాయలు. చికిత్స సుమారు {cost['duration_days']} రోజులు పడుతుంది.",
                            "Hindi": f"सरकारी अस्पताल में {gov} रुपये। प्राइवेट में {pvt} रुपये। इलाज में {cost['duration_days']} दिन लगते हैं।"
                        }
                        audio_player(cost_msgs.get(language, cost_msgs["English"]), language, "🔊 Cost Information:")

                    tips = get_first_aid_tips(symptoms)
                    if tips:
                        st.subheader("💊 First Aid Tips")
                        for tip in tips:
                            st.write(f"• {tip}")
                        tips_text = ". ".join(tips)
                        tips_msgs = {
                            "English": f"First aid tips: {tips_text}",
                            "Telugu": f"ప్రథమ చికిత్స సూచనలు: {tips_text}",
                            "Hindi": f"प्राथमिक उपचार सुझाव: {tips_text}"
                        }
                        audio_player(tips_msgs.get(language, tips_msgs["English"]), language, "🔊 First Aid Tips:")

    # ═══════════════ TAB 2 - AI CHAT ═══════════════
    with tab2:
        render_chatbot(language, city, hospital_type)

    # ═══════════════ TAB 3 - COST ESTIMATOR ═══════════════
    with tab3:
        st.subheader("💰 Treatment Cost Estimator")

        if "disease_from_voice" not in st.session_state:
            st.session_state["disease_from_voice"] = ""

        from streamlit_mic_recorder import speech_to_text as stt_disease
        disease_voice = stt_disease(
            language="en",
            start_prompt="🎤 Speak Disease Name",
            stop_prompt="⏹️ Stop",
            just_once=True,
            use_container_width=True,
            key="disease_mic"
        )

        if disease_voice and disease_voice.strip():
            st.session_state["disease_text_input"] = disease_voice.strip()
            st.success(f"✅ Heard: {disease_voice.strip()}")

        disease_input = st.text_input(
            "Enter disease or condition",
            placeholder="e.g. kidney stone, heart surgery...",
            key="disease_text_input"
        )

        h_type_cost = st.selectbox(
            "Hospital Type",
            ["All", "Government", "Private"],
            key="cost_hospital_type"
        )

        if st.button("💰 Estimate Cost", type="primary"):
            if not disease_input:
                st.warning("Please enter a disease or condition.")
            else:
                with st.spinner("Estimating cost..."):
                    cost_info = get_treatment_cost(disease_input, h_type_cost)
                    if cost_info:
                        render_cost_card(cost_info)
                        st.success(f"Department: {cost_info['department']}")
                        st.info(f"Estimated stay: {cost_info['duration_days']} days")
                        gov_cost = clean_cost_for_speech(cost_info['government_cost'])
                        pvt_cost = clean_cost_for_speech(cost_info['private_cost'])
                        cost_msgs = {
                            "English": f"For {cost_info['disease']}, government hospital costs {gov_cost} rupees and private hospital costs {pvt_cost} rupees. Treatment takes {cost_info['duration_days']} days.",
                            "Telugu": f"{cost_info['disease']} కోసం, ప్రభుత్వ ఆసుపత్రి ఖర్చు {gov_cost} రూపాయలు మరియు ప్రైవేట్ ఆసుపత్రి ఖర్చు {pvt_cost} రూపాయలు. చికిత్స {cost_info['duration_days']} రోజులు పడుతుంది.",
                            "Hindi": f"{cost_info['disease']} के लिए सरकारी अस्पताल में {gov_cost} रुपये और प्राइवेट में {pvt_cost} रुपये खर्च होता है। इलाज में {cost_info['duration_days']} दिन लगते हैं।"
                        }
                        audio_player(cost_msgs.get(language, cost_msgs["English"]), language, "🔊 Cost Details:")

                        # Save to history
                        if st.session_state.get("user_id"):
                            save_history(st.session_state["user_id"], "cost_estimate", disease_input, f"Gov: {cost_info['government_cost']} | Pvt: {cost_info['private_cost']} | Days: {cost_info['duration_days']}", language)
                    else:
                        st.warning("Cost information not found. Try different condition name.")

    # ═══════════════ TAB 4 - RAG KNOWLEDGE BASE ═══════════════
    with tab4:
        st.subheader("📚 Medical Knowledge Base")
        st.markdown("Ask anything about diseases, medicines, government schemes, or hospital costs.")

        if "rag_loaded" not in st.session_state:
            with st.spinner("📂 Loading medical knowledge base..."):
                from rag.document_loader import load_knowledge_to_chromadb
                load_knowledge_to_chromadb()
                st.session_state["rag_loaded"] = True

        rag_category = st.selectbox(
            "Filter by Category (optional)",
            ["All", "Disease Info", "Medicine Info", "Government Schemes", "Hospital Info"],
            key="rag_category"
        )

        category_map = {
            "All": None,
            "Disease Info": "disease",
            "Medicine Info": "medicine",
            "Government Schemes": "government_scheme",
            "Hospital Info": "hospital_info"
        }

        from streamlit_mic_recorder import speech_to_text as stt_rag
        rag_voice = stt_rag(
            language="en",
            start_prompt="🎤 Speak Question",
            stop_prompt="⏹️ Stop",
            just_once=True,
            use_container_width=True,
            key="rag_mic"
        )

        if rag_voice and rag_voice.strip():
            st.session_state["rag_text_input"] = rag_voice.strip()
            st.success(f"✅ Heard: {rag_voice.strip()}")

        rag_query = st.text_input(
            "Type your health question",
            placeholder="e.g. What is Ayushman Bharat? How to treat diabetes? Cost of dialysis?",
            key="rag_text_input"
        )

        if st.button("🔍 Search Knowledge Base", type="primary"):
            if not rag_query:
                st.warning("Please enter a question.")
            else:
                with st.spinner("Searching knowledge base..."):
                    from rag.embeddings import stream_rag_response
                    from rag.retriever import retrieve_relevant_docs

                    selected_category = category_map.get(rag_category)
                    retrieved = retrieve_relevant_docs(rag_query, n_results=4, category_filter=selected_category)

                    st.subheader("🤖 AI Answer")
                    response_placeholder = st.empty()
                    full_response = ""

                    for chunk, full, docs in stream_rag_response(rag_query, language):
                        full_response = full
                        response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)
                    audio_player(full_response, language, "🔊 Listen to Answer:")

                    # Save to history
                    if st.session_state.get("user_id"):
                        save_history(st.session_state["user_id"], "rag_search", rag_query, full_response, language)

                    if retrieved:
                        st.markdown("---")
                        st.subheader("📖 Sources Used")
                        for i, doc in enumerate(retrieved, 1):
                            category_label = doc["category"].replace("_", " ").title()
                            with st.expander(f"Source {i} — {category_label}"):
                                st.write(doc["text"])

    # ═══════════════ TAB 5 - HISTORY ═══════════════
    with tab5:
        render_history_tab()

    with tab6:
        render_symptom_checker()