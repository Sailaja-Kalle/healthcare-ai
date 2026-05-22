import streamlit as st
from database.auth import login_user, register_user

def render_login_page():

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🏥 Healthcare AI</h1>
            <p style='color: gray;'>Your Personal Health Assistant</p>
        </div>
    """, unsafe_allow_html=True)

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True,
                     type="primary" if st.session_state["auth_mode"] == "login" else "secondary"):
            st.session_state["auth_mode"] = "login"
    with col2:
        if st.button("📝 Register", use_container_width=True,
                     type="primary" if st.session_state["auth_mode"] == "register" else "secondary"):
            st.session_state["auth_mode"] = "register"

    st.markdown("---")

    if st.session_state["auth_mode"] == "login":
        st.subheader("🔑 Login to your account")

        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

        if st.button("Login", type="primary", use_container_width=True):
            if not username or not password:
                st.warning("Please enter both username and password.")
            else:
                success, user, message = login_user(username, password)
                if success:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"]
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    else:
        st.subheader("📝 Create new account")

        full_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_fullname")
        username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
        password = st.text_input("Password", type="password", placeholder="Choose a password", key="reg_password")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="reg_confirm")

        if st.button("Create Account", type="primary", use_container_width=True):
            if not username or not password or not full_name:
                st.warning("Please fill all fields.")
            elif password != confirm:
                st.error("❌ Passwords do not match.")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters.")
            else:
                success, message = register_user(username, password, full_name)
                if success:
                    st.success(message)
                    st.info("Now login with your new account!")
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
                else:
                    st.error(message)

    st.markdown("---")
    if st.button("👤 Continue as Guest", use_container_width=True):
        st.session_state["logged_in"] = True
        st.session_state["user"] = None
        st.session_state["user_id"] = None
        st.session_state["username"] = "Guest"
        st.rerun()