import streamlit as st
import json
import plotly.graph_objects as go

# Load sample data
with open("sample_vitals.json") as f:
    data = json.load(f)

# Sidebar patient selection
st.sidebar.title("Select Patient")
patient_ids = list(data.keys())
selected = st.sidebar.selectbox("Patient ID", patient_ids)

# Get selected patient data
vitals = data[selected]

# Display vitals
st.title(f"Vitals for {selected}")
st.write("### Live Parameters")
st.write(f"Temperature: {vitals['temperature']} °C")
st.write(f"Heart Rate: {vitals['heart_rate']} BPM")
st.write(f"SpO₂: {vitals['spo2']} %")
st.write(f"Blood Pressure: {vitals['bp']}")
st.write(f"Respiratory Rate: {vitals['respiratory_rate']}")

# Bar chart
fig = go.Figure(data=[
    go.Bar(
        x=["Temp", "HR", "SpO₂", "Resp"],
        y=[vitals['temperature'], vitals['heart_rate'], vitals['spo2'], vitals['respiratory_rate']],
        marker_color='teal'
    )
])
fig.update_layout(title="Vitals Overview", yaxis_title="Value", height=400)
st.plotly_chart(fig)
