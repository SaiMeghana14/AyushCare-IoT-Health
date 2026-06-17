import json
import pandas as pd
import streamlit as st


def load_json_data():
    with open("sample_vitals.json") as f:
        return json.load(f)


def upload_csv():

    uploaded = st.sidebar.file_uploader(
        "Upload vitals CSV",
        type="csv"
    )

    if uploaded:

        df = pd.read_csv(uploaded)

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        patients = df["patient_id"].unique().tolist()

        selected = st.sidebar.selectbox(
            "👤 Select Patient",
            patients
        )

        patient_df = (
            df[df["patient_id"] == selected]
            .sort_values("timestamp")
        )

        latest = patient_df.iloc[-1]

        vitals = {
            "heart_rate": latest["heart_rate"],
            "spo2": latest["spo2"],
            "temperature": latest["temperature"],
            "bp": latest["bp"],
            "respiratory_rate": latest["respiratory_rate"]
        }

        with st.expander(
            "📄 View Uploaded CSV Data"
        ):
            st.dataframe(df)

        return vitals, selected, df

    return None, None, None
