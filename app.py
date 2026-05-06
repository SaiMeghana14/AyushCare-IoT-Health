import re
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

# --------------------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #e0f7fa, #f1f8ff);
}

.auth-box {
    background-color: white;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    margin-top: 2rem;
}

.title-text {
    text-align: center;
    font-size: 2.2rem;
    font-weight: bold;
    color: #0077b6;
}

.subtitle-text {
    text-align: center;
    color: #555;
    margin-bottom: 1.5rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-size: 1rem;
    font-weight: 600;
    background: linear-gradient(90deg, #0077b6, #00b4d8);
    color: white;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #023e8a, #0077b6);
    color: white;
}

input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

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
# MODERN REGISTER PAGE
# --------------------------------------------------------------
def page_register():

    st.markdown("<div class='title-text'>🩺 AyushCare</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-text'>Create your healthcare monitoring account</div>", unsafe_allow_html=True)

    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)

    st.subheader("🆕 Register")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("✨ Create Account"):

        if not all([full_name, email, username, password, confirm_password]):
            st.error("Please fill all fields.")

        elif username in st.session_state.users:
            st.error("Username already exists.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        elif len(password) < 6:
            st.warning("Password should contain at least 6 characters.")

        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning("Enter a valid email address.")

        else:
            st.session_state.users[username] = {
                "name": full_name,
                "email": email,
                "password": password
            }

            save_users(st.session_state.users)

            st.success("🎉 Account created successfully!")
            st.balloons()

            time.sleep(1)
            st.session_state.page = "login"
            st.rerun()

    st.write("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("🔐 Already have an account? Login"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
# --------------------------------------------------------------
# MODERN LOGIN PAGE
# --------------------------------------------------------------
def page_login():

    st.markdown("<div class='title-text'>🏥 AyushCare</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-text'>AI-Powered Rural Health Monitoring System</div>", unsafe_allow_html=True)

    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)

    st.subheader("🔐 Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    remember_me = st.checkbox("Remember Me")

    if st.button("🚀 Login"):

        if username in st.session_state.users:

            user_data = st.session_state.users[username]

            if isinstance(user_data, dict):
                correct_password = user_data["password"]
                full_name = user_data["name"]
            else:
                correct_password = user_data
                full_name = username

            if password == correct_password:
                st.session_state.current_user = full_name

                st.success("✅ Login successful!")
                time.sleep(1)

                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error("❌ Incorrect password")

        else:
            st.error("❌ User not found")

    st.write("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("🆕 Create New Account"):
            st.session_state.page = "register"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------
# PAGE: DASHBOARD (UI only)
# --------------------------------------------------------------
def page_dashboard():
    st.markdown(f"<h2 style='text-align:center;'>🏥 AyushCare Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(
    f"""
    <div style='
        background: linear-gradient(90deg,#0077b6,#00b4d8);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    '>
        👋 Welcome to AyushCare, {st.session_state.current_user}
    </div>
    """,
    unsafe_allow_html=True
)
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
