import streamlit as st
import json, os, time, hashlib
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd

# -----------------------------
# Persistent user storage (JSON)
# -----------------------------
USERS_FILE = Path("users.json")
SALT = "ayushcare_salt_v1"  # simple salt; for production use bcrypt/argon2

def hash_password(pw: str) -> str:
    return hashlib.sha256((SALT + pw).encode("utf-8")).hexdigest()

def load_users() -> dict:
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

# -----------------------------
# Session state defaults
# -----------------------------
if "users" not in st.session_state:
    st.session_state.users = load_users()  # {username: {"hash": "...", "role": "doctor"}}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "step" not in st.session_state:
    # Start at Register if no users exist; otherwise Login
    st.session_state.step = "register" if len(st.session_state.users) == 0 else "login"

# -----------------------------
# UI helpers
# -----------------------------
def header():
    st.markdown(
        "<h1 style='text-align:center;margin-bottom:0'>AyushCare – Access Portal</h1>"
        "<p style='text-align:center;color:#6b7280;margin-top:4px'>Secure sign-up & login to your rural health dashboard</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)

def switch_to(step: str):
    st.session_state.step = step
    st.experimental_rerun()

def center_container():
    # Narrow layout feel
    st.markdown(
        """
        <style>
            .main .block-container { max-width: 720px; padding-top: 2rem; }
            .stButton > button { width: 100%; border-radius: 12px; padding: 0.6rem 1rem; }
            .stTextInput > div > div > input { border-radius: 10px; }
            .stPassword > div > div > input { border-radius: 10px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Pages
# -----------------------------
def page_register():
    st.subheader("📝 Create your AyushCare account")
    with st.form("register_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username").strip()
        with col2:
            role = st.selectbox("Role", ["Doctor", "Health Worker", "Viewer"])

        pw = st.text_input("Password", type="password")
        pw2 = st.text_input("Confirm Password", type="password")
        agree = st.checkbox("I agree to use AyushCare responsibly.")

        submitted = st.form_submit_button("Create account")
        if submitted:
            if not username or not pw or not pw2:
                st.error("Please fill all fields.")
            elif pw != pw2:
                st.error("Passwords do not match.")
            elif username in st.session_state.users:
                st.error("This username is already taken.")
            elif not agree:
                st.error("You must agree before continuing.")
            else:
                st.session_state.users[username] = {
                    "hash": hash_password(pw),
                    "role": role.lower()
                }
                save_users(st.session_state.users)
                st.success("Registration successful! Redirecting to Login…")
                time.sleep(1.2)
                switch_to("login")

    st.caption("Already have an account?")
    st.button("Go to Login", on_click=lambda: switch_to("login"))

def page_login():
    st.subheader("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username").strip()
        pw = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = st.session_state.users.get(username)
            if user and user["hash"] == hash_password(pw):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success(f"Welcome, {username}!")
                time.sleep(0.8)
                switch_to("dashboard")
            else:
                st.error("Invalid username or password.")

    st.caption("New to AyushCare?")
    st.button("Create an account", on_click=lambda: switch_to("register"))

def page_dashboard():
    st.markdown(
        "<h2 style='margin-bottom:0'>🏥 AyushCare Dashboard</h2>"
        f"<p style='color:#6b7280;margin-top:4px'>Signed in as <b>{st.session_state.current_user}</b></p>",
        unsafe_allow_html=True,
    )
    colA, colB = st.columns([3, 1])
    with colB:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            switch_to("login")

    # Sample vitals area (replace with your live data)
    st.markdown("### Patient Vitals (demo)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Heart Rate (BPM)", 78, "-2")
    with col2:
        st.metric("SpO₂ (%)", 97, "+1")
    with col3:
        st.metric("Temp (°C)", 36.8, "0")

    st.markdown("### Notes")
    st.info(
        "Hook these tiles to your live data (Blynk/Firebase/ESP32). "
        "This page is shown **only after** Register → Login."
    )

# -----------------------------
# App Router
# -----------------------------
st.set_page_config(page_title="AyushCare", page_icon="🏥", layout="centered")
center_container()
header()

if not st.session_state.logged_in:
    if st.session_state.step == "register":
        page_register()
    else:  # "login"
        page_login()
else:
    page_dashboard()

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
