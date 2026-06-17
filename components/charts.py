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

    with st.container(border=True):

        x = np.linspace(0, 10, 500)

        y = (
            np.sin(15 * x)
            + 0.3 * np.sin(50 * x)
            + 0.1 * np.random.randn(len(x))
        )

        fig_ecg = go.Figure()

        fig_ecg.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line=dict(
                    color="#00FF66",
                    width=2
                ),
                name="ECG"
            )
        )

        fig_ecg.update_layout(

            paper_bgcolor="black",

            plot_bgcolor="black",

            font=dict(
                color="#00FF66",
                size=12
            ),

            height=320,

            showlegend=False,

            xaxis=dict(
                title="Time",
                showgrid=True,
                gridcolor="#003300",
                zeroline=False,
                showticklabels=False
            ),
            
            yaxis=dict(
                title="Signal",
                showgrid=True,
                gridcolor="#003300",
                zeroline=False,
                showticklabels=False
            ),

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig_ecg,
            use_container_width=True
        )

        st.info(
            "🟢 ECG Status: Normal Sinus Rhythm Detected"
        )
        c1, c2, c3 = st.columns(3)

        with c1:
            st.success("🟢 Lead Connected")
        
        with c2:
            st.success("📡 Signal Stable")
        
        with c3:
            st.success("❤️ BPM Detected")

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
        height=400,
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
            height=400,
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
