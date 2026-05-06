import streamlit as st
import pandas as pd
import plotly.express as px


def render_health_map():

    st.subheader("🗺 Rural Healthcare Coverage Map")

    df = pd.DataFrame({
        "Village": [
            "Anantapur",
            "Kadapa",
            "Kurnool",
            "Chittoor",
            "Nellore"
        ],

        "lat": [
            14.6819,
            14.4673,
            15.8281,
            13.2172,
            14.4426
        ],

        "lon": [
            77.6006,
            78.8242,
            78.0373,
            79.1003,
            79.9865
        ],

        "Patients": [
            14,
            22,
            10,
            17,
            9
        ]
    })

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="Patients",
        hover_name="Village",
        zoom=5,
        height=450
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={
            "r":0,
            "t":0,
            "l":0,
            "b":0
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
