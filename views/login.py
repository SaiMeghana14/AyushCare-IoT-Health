import streamlit as st
import time
from services.auth_service import load_users


def page_login():

    st.markdown(
        """
        <h1 style='text-align:center;color:#0077b6;'>
        🏥 AyushCare Login
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align:center;'>
        AI-Powered Rural Healthcare Monitoring Platform
        </p>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    remember = st.checkbox("Remember Me")

    users = load_users()

    if st.button("🚀 Login"):

        if username in users:

            if verify_password(password,users[username]["password"]):

                st.success("✅ Login Successful")

                st.session_state.current_user = users[username]["name"]

                time.sleep(1)

                st.session_state.page = "dashboard"

                st.rerun()

            else:
                st.error("❌ Incorrect Password")

        else:
            st.error("❌ User Not Found")

    st.write("---")

    if st.button("🆕 Create New Account"):
        st.session_state.page = "register"
        st.rerun()
