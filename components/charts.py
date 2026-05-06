import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from services.history_service import load_history


def render_ecg():

    st.subheader("❤️ Live ECG Monitor")

    x = np.linspace(0, 10, 500)

    y = (
        np.sin(15*x)
        + 0.3*np.sin(50*x)
        + 0.1*np.random.randn(len(x))
    )

    fig_ecg = px.line(x=x, y=y)

    fig_ecg.update_layout(
        height=250,
        template="plotly_dark"
    )

    st.plotly_chart(fig_ecg, use_container_width
