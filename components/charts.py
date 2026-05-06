import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

from services.history_service import load_history


# --------------------------------------------------------------
# ECG MONITOR
# --------------------------------------------------------------
def render_ecg():

    st.subheader("❤️ Live ECG Monitor")

    x = np.linspace(0, 10, 500)

    y = (
        np.sin(15 * x)
        + 0.3 * np.sin(50 * x)
        + 0.1 * np.random.randn(len(x))
    )

    fig_ecg = px.line(x=x, y=y)

    fig_ecg.update_layout(
        height=250,
        template="plotly_dark",
        showlegend=False,
        xaxis_title="Time",
        yaxis_title="Signal"
    )

    st.plotly_chart(
        fig_ecg,
        use_container_width=True
    )


# --------------------------------------------------------------
# PREMIUM VITALS CHART
# --------------------------------------------------------------
def render_vitals_chart(vitals):

    st.subheader("📊 Live Vitals Analytics")

    fig = go.Figure(
        data=[
            go.Bar(
                x=[
                    "Temperature",
                    "Heart Rate",
                    "SpO₂",
                    "Resp Rate"
                ],

                y=[
                    vitals["temperature"],
                    vitals["heart_rate"],
                    vitals["spo2"],
                    vitals["respiratory_rate"]
                ],

                marker_color=[
                    "#00d4ff",
                    "#ff4d6d",
                    "#06d6a0",
                    "#ffd166"
                ]
            )
        ]
    )

    fig.update_layout(
        height=450,
        template="plotly_dark",
        title="Real-Time Patient Vitals",
        xaxis_title="Health Metrics",
        yaxis_title="Values"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------------------
# HISTORY DASHBOARD
# --------------------------------------------------------------
def render_history(selected):

    st.subheader("📈 Real-Time Patient History")

    history = load_history()

    patient_history = history.get(selected, [])

    if patient_history:

        history_df = pd.DataFrame(patient_history)

        fig_history = px.line(
            history_df,
            x="time",
            y=[
                "heart_rate",
                "spo2",
                "temperature"
            ],
            markers=True,
            template="plotly_dark"
        )

        fig_history.update_layout(
            height=450,
            title="Historical Health Trends"
        )

        st.plotly_chart(
            fig_history,
            use_container_width=True
        )

    else:

        st.info(
            "No historical data available yet."
        )
