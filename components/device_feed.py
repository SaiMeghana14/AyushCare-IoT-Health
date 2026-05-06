import streamlit as st
from datetime import datetime
import random


def render_device_feed():

    st.subheader("📡 Live IoT Device Feed")

    signal = random.choice([
        "Excellent",
        "Strong",
        "Moderate"
    ])

    packets = random.randint(1200, 5000)

    st.markdown(f"""
    <div style='
    background:rgba(255,255,255,0.7);
    padding:1.5rem;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
    margin-bottom:1rem;
    '>

    <h3>
    🟢 ESP32 Device Connected
    </h3>

    <hr>

    <p><b>Sensor:</b> MAX30102</p>

    <p><b>Status:</b> Connected</p>

    <p><b>Signal Strength:</b> {signal}</p>

    <p><b>Packets Transmitted:</b> {packets}</p>

    <p><b>Last Packet:</b>
    {datetime.now().strftime('%H:%M:%S')}</p>

    <p><b>Cloud Sync:</b> Active</p>

    </div>
    """, unsafe_allow_html=True)
