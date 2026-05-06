import streamlit as st

from components.sidebar import render_sidebar

from components.status_card import (
    render_status_card
)

from components.device_feed import (
    render_device_feed
)

from components.metrics import (
    render_metrics
)

from components.ai_predictions import (
    render_ai_predictions
)

from components.doctor_notes import (
    render_doctor_notes
)

from components.charts import (
    render_ecg,
    render_vitals_chart,
    render_history
)

from components.health_map import (
    render_health_map
)

from components.emergency import (
    render_emergency,
    render_timeline
)

from components.patient_monitor import (
    render_patient_monitor,
    render_download
)

from services.data_loader import (
    load_json_data,
    upload_csv
)

from services.aws_service import (
    save_to_dynamodb
)

from services.alerts import (
    calculate_risk
)


# --------------------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------------------
def page_dashboard():

    # ----------------------------------------------------------
    # WELCOME CARD
    # ----------------------------------------------------------
    st.markdown(f"""
    <div style='
    background:white;
    padding:1rem;
    border-radius:15px;
    margin-bottom:1rem;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
    '>

    <h3>
    👋 Welcome, {st.session_state.current_user}
    </h3>

    <p>
    Real-time rural healthcare monitoring is active.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # HERO SECTION
    # ----------------------------------------------------------
    st.markdown(
        """
        <h1 style='color:#0077b6;'>
        🏥 AyushCare Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='
        background:linear-gradient(90deg,#0077b6,#00b4d8);
        padding:1.5rem;
        border-radius:20px;
        color:white;
        margin-bottom:1rem;
        '>

        <h2>🌿 Smart Rural Healthcare Monitoring</h2>

        <p>
        AI-powered real-time patient monitoring
        using AWS cloud and IoT healthcare sensors.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------------------------
    # LIVE CLOUD STATUS
    # ----------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.success("☁ AWS Connected")

    with c2:
        st.success("📡 IoT Active")

    with c3:
        st.success("🔒 Secure")

    with c4:
        st.success("🧠 AI Running")

    # ----------------------------------------------------------
    # SIDEBAR
    # ----------------------------------------------------------
    dark_mode, data_source, show_gauge = (
        render_sidebar()
    )

    # ----------------------------------------------------------
    # CSV UPLOAD
    # ----------------------------------------------------------
    if data_source == "Upload CSV":
        upload_csv()

    # ----------------------------------------------------------
    # LOAD DATA
    # ----------------------------------------------------------
    data = load_json_data()

    patients = list(data.keys())

    selected = st.sidebar.selectbox(
        "🧑 Select Patient",
        patients
    )

    vitals = data[selected]

    # ----------------------------------------------------------
    # SAVE TO AWS
    # ----------------------------------------------------------
    save_to_dynamodb(selected, vitals)

    # ----------------------------------------------------------
    # RISK CALCULATION
    # ----------------------------------------------------------
    (
        risk_score,
        risk_level,
        risk_color,
        patient_status
    ) = calculate_risk(vitals)

    # ----------------------------------------------------------
    # STATUS CARD
    # ----------------------------------------------------------
    render_status_card(
        risk_score,
        risk_level,
        risk_color,
        patient_status
    )

    # ----------------------------------------------------------
    # EMERGENCY MODE
    # ----------------------------------------------------------
    render_emergency(risk_level)

    render_timeline()

    # ----------------------------------------------------------
    # MULTI PATIENT MONITOR
    # ----------------------------------------------------------
    render_patient_monitor()

    # ----------------------------------------------------------
    # LIVE DEVICE FEED
    # ----------------------------------------------------------
    render_device_feed()

    # ----------------------------------------------------------
    # METRICS
    # ----------------------------------------------------------
    render_metrics(
        vitals,
        risk_level,
        risk_score
    )

    # ----------------------------------------------------------
    # ECG MONITOR
    # ----------------------------------------------------------
    render_ecg()

    # ----------------------------------------------------------
    # VITALS CHART
    # ----------------------------------------------------------
    render_vitals_chart(vitals)

    # ----------------------------------------------------------
    # HEALTH COVERAGE MAP
    # ----------------------------------------------------------
    render_health_map()

    # ----------------------------------------------------------
    # HISTORY DASHBOARD
    # ----------------------------------------------------------
    render_history(selected)

    # ----------------------------------------------------------
    # AI PREDICTIONS
    # ----------------------------------------------------------
    render_ai_predictions(risk_level)

    # ----------------------------------------------------------
    # DOCTOR NOTES
    # ----------------------------------------------------------
    render_doctor_notes()

    # ----------------------------------------------------------
    # DOWNLOAD REPORT
    # ----------------------------------------------------------
    render_download(selected, vitals)

    # ----------------------------------------------------------
    # DARK MODE
    # ----------------------------------------------------------
    if dark_mode:

        st.markdown(
            """
            <style>

            .stApp {
                background: linear-gradient(
                    135deg,
                    #0f172a,
                    #111827
                );

                color:white !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )
