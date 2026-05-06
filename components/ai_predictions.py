import streamlit as st
import time


def render_ai_predictions(risk_level):

    with st.spinner("🧠 AI analyzing patient vitals..."):
        time.sleep(1)

    st.subheader("🧠 AI Health Predictions")

    if risk_level == "Low":
        st.success("• No immediate health risk detected")
        st.info("• Oxygen trend stable")

    elif risk_level == "Moderate":
        st.warning("• Continuous monitoring recommended")

    else:
        st.error("• Emergency medical support recommended")
