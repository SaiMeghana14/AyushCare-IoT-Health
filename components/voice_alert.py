import streamlit as st


def play_voice_alert(message):

    st.markdown(f"""
    <script>

    const msg = new SpeechSynthesisUtterance(
        "{message}"
    );

    window.speechSynthesis.speak(msg);

    </script>
    """, unsafe_allow_html=True)
