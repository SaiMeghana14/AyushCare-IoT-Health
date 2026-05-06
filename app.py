import streamlit as st
from pages.login import page_login
from pages.register import page_register
from pages.dashboard import page_dashboard

st.set_page_config(
    page_title="AyushCare",
    page_icon="🩺",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "register"

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Navigation
if st.session_state.page == "register":
    page_register()

elif st.session_state.page == "login":
    page_login()

elif st.session_state.page == "dashboard":
    page_dashboard()
