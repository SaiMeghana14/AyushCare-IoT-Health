import streamlit as st

from views.login import page_login
from views.register import page_register
from views.dashboard import page_dashboard
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------
st.set_page_config(
    page_title="AyushCare",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st_autorefresh(
    interval=5000,
    key="live_refresh"
)

# --------------------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef7ff,
        #dbeafe
    );
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# SESSION STATE
# --------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "register"

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --------------------------------------------------------------
# NAVIGATION
# --------------------------------------------------------------
if st.session_state.page == "register":

    page_register()

elif st.session_state.page == "login":

    page_login()

elif st.session_state.page == "dashboard":

    page_dashboard()
