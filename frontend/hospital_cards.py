import streamlit as st

def render_hospital_card(hospital):
    """Render a single hospital card"""

    # Set color based on hospital type
    if hospital.get("type") == "Government":
        card_color = "#e8f5e9"
        badge_color = "green"
    else:
        card_color = "#e3f2fd"
        badge_color = "blue"

    with st.container():
        st.markdown(f"""
        <div style="
            background-color: {card_color};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 5px solid {'green' if hospital.get('type') == 'Government' else 'blue'};
        ">
            <h4>🏥 {hospital.get('hospital_name', 'N/A')}</h4>
            <p>📍 {hospital.get('address', 'N/A')}, {hospital.get('city', 'N/A')}</p>
            <p>🏷️ Type: <b>{hospital.get('type', 'N/A')}</b></p>
            <p>🩺 Specialization: <b>{hospital.get('specialization', 'N/A')}</b></p>
            <p>💰 Cost Range: <b>{hospital.get('cost_range', 'N/A')}</b></p>
            <p>📞 Phone: <b>{hospital.get('phone', 'N/A')}</b></p>
        </div>
        """, unsafe_allow_html=True)

def render_hospital_list(hospitals_df, title="🏥 Recommended Hospitals"):
    """Render list of hospital cards"""

    st.subheader(title)

    if hospitals_df is None or hospitals_df.empty:
        st.warning("No hospitals found for your location. Try searching nearby cities.")
        return

    st.success(f"Found {len(hospitals_df)} hospitals")

    for _, hospital in hospitals_df.iterrows():
        render_hospital_card(hospital.to_dict())

def render_cost_card(cost_info):
    """Render treatment cost information card"""

    if not cost_info:
        st.warning("Cost information not available for this condition.")
        return

    st.subheader("💰 Treatment Cost Estimation")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid green;
        ">
            <h4>🏛️ Government Hospital</h4>
            <h2>{cost_info.get('government_cost', 'N/A')}</h2>
            <p>Affordable option</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid blue;
        ">
            <h4>🏥 Private Hospital</h4>
            <h2>{cost_info.get('private_cost', 'N/A')}</h2>
            <p>Premium option</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(f"⏱️ Estimated Duration: {cost_info.get('duration_days', 'N/A')} days")

def render_emergency_card(emergency_info):
    """Render emergency alert card"""

    if emergency_info.get("is_emergency"):
        st.error(f"""
        🚨 EMERGENCY DETECTED!
        
        {emergency_info.get('action', '')}
        
        📞 Call 108 immediately!
        """)
    
    with st.expander("📞 Emergency Helplines"):
        helplines = emergency_info.get("helplines", {})
        for service, number in helplines.items():
            st.write(f"**{service}:** {number}")