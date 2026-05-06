import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


def render_status_card(risk_score, risk_level, risk_color, patient_status):

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown(f"""
        <div style='
        background: linear-gradient(90deg,{risk_color},#0ea5e9);
        padding:1.8rem;
        border-radius:25px;
        color:white;
        margin-bottom:1rem;
        box-shadow:0 8px 20px rgba(0,0,0,0.15);
        '>

        <h2>{patient_status}</h2>

        <h3>❤️ Health Score: {risk_score}/100</h3>

        <p>🕒 Last Updated: {datetime.now().strftime('%H:%M:%S')}</p>

        <p>☁ Cloud Sync: Connected</p>

        <p>📡 IoT Monitoring: Active</p>

        <p>⚠ Risk Level: {risk_level}</p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        score_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00d4ff"}
            }
        ))

        score_fig.update_layout(height=320)

        st.plotly_chart(score_fig, use_container_width=True)
