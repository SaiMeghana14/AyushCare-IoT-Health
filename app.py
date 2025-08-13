import streamlit as st
import json, os, time, hashlib
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd

USERS_FILE = "users.json"

# Load existing users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Initialize session variables
if "page" not in st.session_state:
    st.session_state.page = "register"
if "users" not in st.session_state:
    st.session_state.users = {}  # Store registered usernames & passwords

def page_register():
    st.title("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        if username and password:
            if username in st.session_state.users:
                st.error("Username already exists!")
            else:
                st.session_state.users[username] = password
                st.success("Registered successfully! Please log in.")
                st.session_state.page = "login"
        else:
            st.error("Please fill in both fields.")

def page_login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.success("Login successful!")
            st.session_state.page = "dashboard"
        else:
            st.error("Invalid username or password.")

def page_dashboard():
    st.title("Dashboard")
    st.write("Welcome to your dashboard!")
    if st.button("Logout"):
        st.session_state.page = "login"

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "register"  # Set default only once

if st.session_state.page == "register":
    if page_register():  # return True when register successful
        st.session_state.page = "login"  # Move to login
        st.experimental_rerun()

elif st.session_state.page == "login":
    if page_login():  # return True when login successful
        st.session_state.page = "dashboard"
        st.experimental_rerun()

elif st.session_state.page == "dashboard":
    st.write("Dashboard content here")

# --- MAIN DASHBOARD ---
st.set_page_config(page_title="AyushCare Dashboard", layout="centered", page_icon="🩺")

st.sidebar.title("☰ Options")
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
data_source = st.sidebar.radio("📦 Data Source", ["Local JSON", "Upload CSV"])
show_gauge = st.sidebar.checkbox("📊 Show Gauge Meters")

# Load from local JSON
def load_json_data():
    with open("sample_vitals.json") as f:
        return json.load(f)

# Upload CSV
if data_source == "Upload CSV":
    uploaded = st.sidebar.file_uploader("Upload vitals CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.subheader("Uploaded CSV Data")
        st.write(df.head())
        st.stop()

# --- Load Sample JSON ---
try:
    data = load_json_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# --- Patient Selector ---
search = st.sidebar.text_input("🔍 Search Patient ID").upper()
patients = [pid for pid in data.keys() if search in pid]
if not patients:
    st.warning("No matching patients found.")
    st.stop()

selected = st.sidebar.selectbox("Select Patient", patients)
vitals = data[selected]

st.title(f"🧑‍⚕️ Vitals for Patient {selected}")

# --- Display Vitals with Color Logic ---
def display_vital(label, value, unit="", alert_level=None):
    if alert_level == "critical":
        st.markdown(f"<div style='color:red'><strong>{label}:</strong> {value} {unit}</div>", unsafe_allow_html=True)
    elif alert_level == "warning":
        st.markdown(f"<div style='color:orange'><strong>{label}:</strong> {value} {unit}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div><strong>{label}:</strong> {value} {unit}</div>", unsafe_allow_html=True)

# --- Logic for Alert Levels ---
def get_alerts(v):
    alerts = []
    if v["spo2"] < 92:
        alerts.append(("SpO₂", "critical", "Low oxygen!"))
    if v["heart_rate"] > 100:
        alerts.append(("Heart Rate", "warning", "Possible tachycardia"))
    if v["temperature"] > 38.0:
        alerts.append(("Temperature", "warning", "Fever detected"))
    return alerts

# --- Display Vitals ---
alerts = get_alerts(vitals)

display_vital("Temperature", vitals["temperature"], "°C",
              "warning" if vitals["temperature"] > 38.0 else None)
display_vital("Heart Rate", vitals["heart_rate"], "BPM",
              "warning" if vitals["heart_rate"] > 100 else None)
display_vital("SpO₂", vitals["spo2"], "%",
              "critical" if vitals["spo2"] < 92 else None)
display_vital("Blood Pressure", vitals["bp"])
display_vital("Respiratory Rate", vitals["respiratory_rate"])

# --- Recommendations ---
if alerts:
    st.subheader("🚨 Alerts")
    for label, level, msg in alerts:
        st.error(f"{label}: {msg}")

    st.subheader("💡 Recommendations")
    if any(a[0] == "SpO₂" for a in alerts):
        st.info("Provide oxygen or ensure fresh air.")
    if any(a[0] == "Heart Rate" for a in alerts):
        st.info("Advise rest and hydration.")
    if any(a[0] == "Temperature" for a in alerts):
        st.info("Monitor fever; consider paracetamol.")

# --- Bar Chart ---
fig = go.Figure(data=[
    go.Bar(
        x=["Temp", "Heart Rate", "SpO₂", "Resp. Rate"],
        y=[
            vitals["temperature"],
            vitals["heart_rate"],
            vitals["spo2"],
            vitals["respiratory_rate"]
        ],
        marker_color="teal"
    )
])
fig.update_layout(title="Vitals Overview", yaxis_title="Value", height=400)
st.plotly_chart(fig)

# --- Optional Gauges ---
if show_gauge:
    st.subheader("📟 Gauge Meters")
    gauge_cols = st.columns(2)

    with gauge_cols[0]:
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number",
            value=vitals["heart_rate"],
            title={"text": "Heart Rate"},
            gauge={"axis": {"range": [0, 160]}, "bar": {"color": "crimson"}}
        )), use_container_width=True)

    with gauge_cols[1]:
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number",
            value=vitals["spo2"],
            title={"text": "SpO₂ %"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "royalblue"}}
        )), use_container_width=True)

# --- Download Button ---
st.download_button("📥 Download This Patient's Data (JSON)",
                   json.dumps({selected: vitals}, indent=2),
                   file_name=f"{selected}_vitals.json")

# --- Dark Mode CSS (Optional) ---
if dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #111 !important;
            color: #fff !important;
        }
        .css-1d391kg { color: #fff !important; }
        </style>
    """, unsafe_allow_html=True)
