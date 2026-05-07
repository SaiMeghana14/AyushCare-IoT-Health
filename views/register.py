import streamlit as st
import time
import re

from services.auth_service import (
    load_users,
    save_users,
    hash_password
)

def page_register():

    st.markdown(
        """
        <h1 style='text-align:center;color:#0077b6;'>
        🩺 AyushCare Register
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align:center;'>
        Create your healthcare monitoring account
        </p>
        """,
        unsafe_allow_html=True
    )

    full_name = st.text_input("👤 Full Name")

    email = st.text_input("📧 Email Address")

    username = st.text_input("🆔 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    confirm_password = st.text_input(
        "🔒 Confirm Password",
        type="password"
    )

    users = load_users()

    if st.button("✨ Create Account"):

        if not all([
            full_name,
            email,
            username,
            password,
            confirm_password
        ]):

            st.error("Please fill all fields")

        elif username in users:

            st.error("Username already exists")

        elif password != confirm_password:

            st.error("Passwords do not match")

        elif len(password) < 6:

            st.warning(
                "Password should contain at least 6 characters"
            )

        elif not re.match(
            r"[^@]+@[^@]+\.[^@]+",
            email
        ):

            st.warning("Enter valid email address")

        else:

            users[username] = {
                "name": full_name,
                "email": email,
                "password": hash_password(password)
            }

            save_users(users)

            st.success("🎉 Account Created Successfully")

            st.balloons()

            time.sleep(1)

            st.session_state.page = "login"

            st.rerun()

    st.write("---")

    if st.button("🔐 Already have an account? Login"):

        st.session_state.page = "login"

        st.rerun()
