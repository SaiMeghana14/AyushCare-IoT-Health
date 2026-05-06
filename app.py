import streamlit as st
import json, os, time, hashlib
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
import boto3
from datetime import datetime

# --------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------
st.set_page_config(page_title="AyushCare", page_icon="🩺", layout="centered")

USERS_FILE = "users.json"

# --------------------------------------------------------------
# AWS CONFIGURATION
# --------------------------------------------------------------
AWS_REGION = st.secrets["AWS_REGION"]

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

table = dynamodb.Table("AyushCareVitals")

sns_client = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

ALERT_PHONE = "+91XXXXXXXXXX"
ALERT_EMAIL = "doctor@example.com"

# --------------------------------------------------------------
# USER MANAGEMENT
# --------------------------------------------------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Initialize session vars
if "page" not in st.session_state:
    st.session_state.page = "register"
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --------------------------------------------------------------
# PAGE: REGISTER
# --------------------------------------------------------------
def page_register():
    st.markdown("<h2 style='text-align:center;'>🆕 Create Your AyushCare Account</h2>", unsafe_allow_html=True)
    username = st.text_input("Choose a Username", placeholder="Enter username")
    password = st.text_input("Create a Password", placeholder="Enter password", type="password")

    if st.button("Create Account", use_container_width=True):
        if username and password:
            if username in st.session_state.users:
                st.error("⚠ Username already exists! Try another.")
            else:
                st.session_state.users[username] = password
                save_users(st.session_state.users)
                st.success("🎉 Registration successful! Please log in.")
                st.session_state.page = "login"
        else:
            st.error("❗ Please fill in both fields.")

    st.write("---")
    if st.button("Already have an account? Login →", use_container_width=True):
        st.session_state.page = "login"

# --------------------------------------------------------------
# PAGE: LOGIN
# --------------------------------------------------------------
def page_login():
    st.markdown("<h2 style='text-align:center;'>🔐 Login to AyushCare</h2>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", placeholder="Enter password", type="password")

    if st.button("Login", use_container_width=True):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.current_user = username
            st.success("✅ Login successful!")
            st.session_state.page = "dashboard"
        else:
            st.error("❌ Invalid username or password.")

    st.write("---")
    if st.button("New user? Register →", use_container_width=True):
        st.session_state.page = "register"

# --------------------------------------------------------------
# PAGE: DASHBOARD (UI only)
# --------------------------------------------------------------
def page_dashboard():
    st.markdown(f"<h2 style='text-align:center;'>🏥 AyushCare Dashboard</h2>", unsafe_allow_html=True)
    st.write(f"### Welcome, **{st.session_state.current_user}** 👋")
    st.write("Real-time vitals monitoring starts below.")

# --------------------------------------------------------------
# NAVIGATION
# --------------------------------------------------------------
if st.session_state.page == "register":
    page_register()

elif st.session_state.page == "login":
    page_login()

elif st.session_state.page == "dashboard":
    if not st.session_state.current_user:
        st.session_state.page = "login"
        st.stop()
    page_dashboard()

# ----------------------------------------------------------
# SIDEBAR (Dashboard only)
# ----------------------------------------------------------
st.sidebar.title("☰ Options")
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
data_source = st.sidebar.radio("📦 Data Source", ["Local JSON", "Upload CSV"])
show_gauge = st.sidebar.checkbox("📊 Show Gauge Meters")

# --------------------------------------------------------------
# LOAD JSON DATA
# --------------------------------------------------------------
def load_json_data():
    with open("sample_vitals.json") as f:
        return json.load(f)

# --------------------------------------------------------------
# SAVE DATA TO AWS DYNAMODB
# --------------------------------------------------------------
def save_to_dynamodb(patient_id, vitals):
    try:
        table.put_item(
            Item={
                "patient_id": patient_id,
                "timestamp": datetime.now().isoformat(),
                "temperature": vitals["temperature"],
                "heart_rate": vitals["heart_rate"],
                "spo2": vitals["spo2"],
                "bp": vitals["bp"],
                "respiratory_rate": vitals["respiratory_rate"]
            }
        )
    except Exception as e:
        st.warning(f"AWS Upload Failed: {e}")

# --------------------------------------------------------------
# SEND EMERGENCY ALERTS USING AWS SNS
# --------------------------------------------------------------
def send_emergency_alert(message):
    try:
        sns_client.publish(
            PhoneNumber=ALERT_PHONE,
            Message=message
        )
    except Exception as e:
        st.warning(f"SNS Alert Failed: {e}")

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

# Upload patient vitals to AWS DynamoDB
save_to_dynamodb(selected, vitals)

st.title(f"🧑‍⚕️ Vitals for Patient {selected}")

# --------------------------------------------------------------
# DISPLAY VITALS
# --------------------------------------------------------------
def display_vital(label, value, unit="", alert_level=None):
    if alert_level == "critical":
        st.markdown(f"<div style='color:red'><strong>{label}:</strong> {value} {unit}</div>", unsafe_allow_html=True)
    elif alert_level == "warning":
        st.markdown(f"<div style='color:orange'><strong>{label}:</strong> {value} {unit}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div><strong>{label}:</strong> {value} {unit}</div>", unsafe_allow_html=True)

# --------------------------------------------------------------
# ALERT LOGIC
# --------------------------------------------------------------
def get_alerts(v):
    alerts = []

    if v["spo2"] < 90:
        alerts.append(("SpO₂", "critical", "Low oxygen!"))

    if v["heart_rate"] > 100:
        alerts.append(("Heart Rate", "warning", "Possible tachycardia"))

    if v["temperature"] > 38.9:
        alerts.append(("Temperature", "warning", "High fever detected"))

    return alerts

alerts = get_alerts(vitals)

# --------------------------------------------------------------
# AUTO SNS ALERTS
# --------------------------------------------------------------
critical_messages = []

if vitals["spo2"] < 90:
    critical_messages.append("Critical Alert: Patient oxygen level is very low.")

if vitals["temperature"] > 38.9:
    critical_messages.append("Critical Alert: High fever detected.")

if critical_messages:
    send_emergency_alert(
        f"Patient {selected}: " + " | ".join(critical_messages)
    )

# --------------------------------------------------------------
# DISPLAY VITALS
# --------------------------------------------------------------
display_vital("Temperature", vitals["temperature"], "°C",
              "warning" if vitals["temperature"] > 38.9 else None)

display_vital("Heart Rate", vitals["heart_rate"], "BPM",
              "warning" if vitals["heart_rate"] > 100 else None)

display_vital("SpO₂", vitals["spo2"], "%",
              "critical" if vitals["spo2"] < 90 else None)

display_vital("Blood Pressure", vitals["bp"])
display_vital("Respiratory Rate", vitals["respiratory_rate"])

# --------------------------------------------------------------
# ALERTS + RECOMMENDATIONS
# --------------------------------------------------------------
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
        st.info("Monitor fever and seek medical attention.")

# --------------------------------------------------------------
# AI HEALTH INSIGHTS
# --------------------------------------------------------------
st.subheader("🧠 AI Health Insights")

if vitals["spo2"] < 90:
    st.warning("Patient shows consistently low oxygen levels.")

elif vitals["heart_rate"] > 110:
    st.warning("Abnormally high heart rate detected.")

elif vitals["temperature"] > 38.9:
    st.warning("Patient may have severe fever symptoms.")

else:
    st.success("Vitals appear stable.")

# --------------------------------------------------------------
# BAR CHART
# --------------------------------------------------------------
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

fig.update_layout(
    title="Vitals Overview",
    yaxis_title="Value",
    height=400
)

st.plotly_chart(fig)

# --------------------------------------------------------------
# PATIENT HISTORY DASHBOARD
# --------------------------------------------------------------
st.subheader("📈 Patient History Dashboard")

history_data = pd.DataFrame([
    {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Temperature": vitals["temperature"],
        "Heart Rate": vitals["heart_rate"],
        "SpO2": vitals["spo2"]
    }
])

st.line_chart(history_data.set_index("Time"))

# --------------------------------------------------------------
# OPTIONAL GAUGES
# --------------------------------------------------------------
if show_gauge:
    st.subheader("📟 Gauge Meters")

    gauge_cols = st.columns(2)

    with gauge_cols[0]:
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number",
            value=vitals["heart_rate"],
            title={"text": "Heart Rate"},
            gauge={
                "axis": {"range": [0, 160]},
                "bar": {"color": "crimson"}
            }
        )), use_container_width=True)

    with gauge_cols[1]:
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number",
            value=vitals["spo2"],
            title={"text": "SpO₂ %"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "royalblue"}
            }
        )), use_container_width=True)

# --------------------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------------------
st.download_button(
    "📥 Download This Patient's Data (JSON)",
    json.dumps({selected: vitals}, indent=2),
    file_name=f"{selected}_vitals.json"
)

# --------------------------------------------------------------
# DARK MODE CSS
# --------------------------------------------------------------
if dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #111 !important;
            color: #fff !important;
        }
        .css-1d391kg {
            color: #fff !important;
        }
        </style>
    """, unsafe_allow_html=True)
