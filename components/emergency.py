import streamlit as st
from datetime import datetime


def render_emergency(risk_level):

    if risk_level == "Critical":

        st.markdown("""
        <div style='
        background:#7f1d1d;
        color:white;
        padding:1rem;
        border-radius:15px;
        border:3px solid red;
        '>
        🚨 EMERGENCY ALERT ACTIVE 🚨
        </div>
        """, unsafe_allow_html=True)
        
        play_voice_alert(
        "Emergency detected for patient P001"
    )

        st.error("📞 Emergency contact notification triggered")


def render_timeline():

    st.subheader("⏱ Emergency Response Timeline")

    st.markdown(f"""
    ✅ {datetime.now().strftime('%H:%M:%S')} - IoT vitals received

    ☁ AWS synchronization completed

    🧠 AI analysis generated

    📨 Emergency monitoring active
    """)
