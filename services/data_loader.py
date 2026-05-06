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
        st.subheader("Uploaded CSV Data")
        st.dataframe(df)
        st.stop()
