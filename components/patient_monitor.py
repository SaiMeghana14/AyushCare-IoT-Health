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

    safe_vitals = {}

    for k, v in vitals.items():

        if hasattr(v, "item"):
            safe_vitals[k] = v.item()

        else:
            safe_vitals[k] = v

    st.download_button(
        label="⬇ Download Patient Data",
        data=json.dumps(
            {selected: safe_vitals},
            indent=2
        ),
        file_name=f"{selected}_report.json",
        mime="application/json"
    )

def highlight_status(row):
    if row["Risk"] == "High":
        return ["background-color:#ffcccc"] * len(row)

    elif row["Risk"] == "Moderate":
        return ["background-color:#fff4cc"] * len(row)

    return ["background-color:#d4edda"] * len(row)
    
    st.dataframe(
        df.style.apply(
            highlight_status,
            axis=1
        )
    )
