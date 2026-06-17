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

        with st.expander(
            "📄 View Uploaded CSV Data"
        ):
            st.dataframe(df)

        return vitals, selected, df

    return None, None, None
