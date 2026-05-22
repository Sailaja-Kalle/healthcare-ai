import streamlit as st
from backend.symptom_agent import analyze_symptoms, get_urgency_color, get_probability_color
from database.history import save_history

def render_symptom_checker():
    st.subheader("🤖 AI Symptom Checker")
    st.markdown("Fill in your details and get an instant AI health assessment.")

    st.markdown("---")

    # ── FORM ──
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Your Name", placeholder="e.g. Ravi Kumar")
    with col2:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    symptoms = st.text_area(
        "Describe Your Symptoms *",
        placeholder="e.g. I have fever, headache, body pain and sore throat since 2 days...",
        height=100
    )

    col4, col5 = st.columns(2)
    with col4:
        duration = st.selectbox(
            "How long have you had these symptoms?",
            ["Less than 1 day", "1-2 days", "3-5 days",
             "1 week", "2 weeks", "More than 2 weeks", "More than 1 month"]
        )
    with col5:
        severity = st.slider(
            "Severity (1=Mild, 10=Very Severe)",
            min_value=1, max_value=10, value=5
        )

    existing_conditions = st.text_input(
        "Existing Medical Conditions (optional)",
        placeholder="e.g. Diabetes, Hypertension, Asthma..."
    )

    language = st.session_state.get("language", "English")

    st.markdown("---")

    if st.button("🔍 Analyze My Symptoms", type="primary", use_container_width=True):
        if not symptoms:
            st.warning("⚠️ Please describe your symptoms first.")
            return
        if not name:
            st.warning("⚠️ Please enter your name.")
            return

        with st.spinner("🤖 AI is analyzing your symptoms..."):
            success, result = analyze_symptoms(
                name, age, gender, symptoms,
                duration, severity, existing_conditions, language
            )

        if not success:
            st.error(f"❌ {result}")
            return

        # ── URGENCY BANNER ──
        urgency = result.get("urgency_level", "Visit Soon")
        urgency_icon = get_urgency_color(urgency)
        urgency_reason = result.get("urgency_reason", "")

        if urgency == "Emergency":
            st.error(f"🚨 {urgency_icon} EMERGENCY — {urgency_reason}")
            st.error("**Call 108 immediately or go to nearest emergency room!**")
        elif urgency == "Visit Soon":
            st.warning(f"⚠️ {urgency_icon} VISIT DOCTOR SOON — {urgency_reason}")
        else:
            st.success(f"✅ {urgency_icon} HOME CARE — {urgency_reason}")

        st.markdown("---")

        # ── POSSIBLE DISEASES ──
        st.subheader("🦠 Possible Conditions")
        diseases = result.get("possible_diseases", [])
        for disease in diseases:
            prob = disease.get("probability", "Medium")
            icon = get_probability_color(prob)
            with st.expander(f"{icon} {disease.get('name', '')} — {prob} Probability"):
                st.write(disease.get("description", ""))

        st.markdown("---")

        # ── TWO COLUMNS ──
        col_a, col_b = st.columns(2)

        with col_a:
            # Doctor to visit
            st.subheader("👨‍⚕️ Doctor to Visit")
            doctor = result.get("doctor_to_visit", "General Physician")
            st.info(f"**{doctor}**")

            # Warning signs
            st.subheader("⚠️ Warning Signs")
            st.markdown("*Seek immediate help if you notice:*")
            warnings = result.get("warning_signs", [])
            for w in warnings:
                st.write(f"🔴 {w}")

        with col_b:
            # Home remedies
            st.subheader("🌿 Home Remedies")
            remedies = result.get("home_remedies", [])
            for remedy in remedies:
                st.write(f"✅ {remedy}")

        st.markdown("---")

        # ── GENERAL ADVICE ──
        st.subheader("💡 General Advice")
        st.info(result.get("general_advice", ""))

        # ── FIND HOSPITALS LINK ──
        st.subheader("🏥 Nearby Hospitals")
        from backend.recommendation_engine import get_recommendations
        from frontend.hospital_cards import render_hospital_list
        from frontend.map_view import render_hospital_map

        city = st.session_state.get("city", "Hyderabad")
        st.info(f"📍 Showing hospitals in **{city}** — change city in sidebar")

        recommendations = get_recommendations(symptoms, city, "All")
        hospitals = recommendations["hospitals"]
        render_hospital_list(hospitals, f"🏥 Hospitals in {city}")

        if hospitals is not None and not hospitals.empty:
            render_hospital_map(hospitals, city)

        # ── SAVE TO HISTORY ──
        if st.session_state.get("user_id"):
            summary = f"Diseases: {', '.join([d['name'] for d in diseases])} | Urgency: {urgency} | Doctor: {result.get('doctor_to_visit','')}"
            save_history(
                st.session_state["user_id"],
                "ai_chat",
                f"Symptom Check: {symptoms[:100]}",
                summary,
                language
            )
            st.caption("✅ Saved to your history.")