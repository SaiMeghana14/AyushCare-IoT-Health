import streamlit as st
import pandas as pd
import json


def render_patient_monitor():

    st.subheader("🏥 Multi-Patient Monitoring")

    patient_overview = pd.DataFrame([
        ["P001", "Stable", "Low"],
        ["P002", "Critical", "High"],
        ["P003", "Observation", "Moderate"],
        ["P004", "Stable", "Low"]
    ], columns=["Patient", "Status", "Risk"])

    st.dataframe(
        patient_overview,
        use_container_width=True
    )


def render_download(selected, vitals):

    st.download_button(
        label="📥 Download Patient Report",
        data=json.dumps({selected: vitals}, indent=2),
        file_name=f"{selected}_report.json",
        mime="application/json"
    )
