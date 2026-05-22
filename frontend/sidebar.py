import streamlit as st
from utils.constants import LANGUAGES, HOSPITAL_TYPES, COST_RANGES

def render_sidebar():
    """Render sidebar with all filters and settings"""
    
    with st.sidebar:
        st.title("⚕️ Healthcare AI")
        st.markdown("---")

        st.subheader("🌐 Select Language")
        selected_language = st.selectbox(
            "Choose your language",
            options=list(LANGUAGES.keys()),
            index=0
        )

        st.markdown("---")

        st.subheader("📍 Your Location")
        city_input = st.text_input(
            "Enter your city",
            placeholder="e.g. Hyderabad, Kurnool..."
        )

        st.markdown("---")

        st.subheader("🏥 Hospital Filters")
        hospital_type = st.selectbox(
            "Hospital Type",
            options=HOSPITAL_TYPES,
            index=0
        )

        cost_range = st.selectbox(
            "Cost Range",
            options=COST_RANGES,
            index=0
        )

        st.markdown("---")

        st.subheader("🚨 Emergency Helplines")
        st.error("Ambulance: 108")
        st.warning("Police: 100")
        st.info("Fire: 101")
        st.info("Women: 1091")

        st.markdown("---")

        st.subheader("ℹ️ About")
        st.info(
            "AI Healthcare Assistant helps you find the right hospital "
            "and understand treatment costs across India."
        )

    return {
        "language": selected_language,
        "city": city_input,
        "hospital_type": hospital_type,
        "cost_range": cost_range
    }