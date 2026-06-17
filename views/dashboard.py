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

from components.voice_alert import (
    play_voice_alert
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

from services.pdf_service import (
    generate_report
)

st.markdown("""
<style>

@media (max-width: 768px) {

    h1 {
        font-size: 2rem !important;
    }

    .block-container {
        padding: 1rem !important;
    }

}

</style>
""", unsafe_allow_html=True)

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
    # ANALYTICS OVERVIEW
    # ----------------------------------------------------------
    
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric(
        "👨‍⚕️ Patients Online",
        "24"
    )
    
    c2.metric(
        "🚨 Alerts Today",
        "2"
    )
    
    c3.metric(
        "🏡 Villages Covered",
        "8"
    )
    
    c4.metric(
        "☁ AWS Uptime",
        "99.9%"
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
    # LOAD DATA
    # ----------------------------------------------------------
    
    if data_source == "Local JSON":
    
        data = load_json_data()
    
        patients = list(data.keys())
    
        selected = st.sidebar.selectbox(
            "👤 Select Patient",
            patients
        )
    
        vitals = data[selected]
    
    elif data_source == "Upload CSV":
    
        csv_df = upload_csv()
    
        if csv_df is not None:
    
            patients = (
                csv_df["patient_id"]
                .unique()
                .tolist()
            )
    
            selected = st.sidebar.selectbox(
                "👤 Select Patient",
                patients
            )
    
            patient_df = (
                csv_df[
                    csv_df["patient_id"] == selected
                ]
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
    
        else:
    
            st.warning("📂 Upload a CSV file to continue")
            st.stop()

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
        patient_status,
        show_gauge
    )

    # ----------------------------------------------------------
    # EMERGENCY MODE
    # ----------------------------------------------------------
    render_emergency(risk_level)
    if risk_level == "Critical":
    
        play_voice_alert(
            f"Emergency detected for patient {selected}"
        )
    render_timeline()

    # ----------------------------------------------------------
    # NOTIFICATION CENTER
    # ----------------------------------------------------------
    
    st.subheader("🔔 Notification Center")
    
    notifications = [
    
        "AWS Sync Successful",
    
        "Vitals Received",
    
        "AI Analysis Completed",
    
        "Doctor Review Pending"
    
    ]
    
    for n in notifications:
    
        st.info(n)
        
    # ----------------------------------------------------------
    # MULTI PATIENT MONITOR
    # ----------------------------------------------------------
    render_patient_monitor()

    # ----------------------------------------------------------
    # LIVE DEVICE FEED
    # ----------------------------------------------------------
    render_device_feed()

    import random
    
    packet_count = random.randint(
        4000,
        6000
    )
    
    c1, c2 = st.columns(2)
    
    with c1:
    
        st.metric(
            "📦 Packets Received",
            packet_count,
            "+12"
        )
    
    with c2:
    
        st.metric(
            "📡 Signal Quality",
            "Excellent"
        )
    
    st.progress(95)
    
    st.caption(
        "Signal Quality: Excellent"
    )

    # ----------------------------------------------------------
    # METRICS
    # ----------------------------------------------------------
    if show_gauge:
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

    st.success(
        "🏡 Rural Healthcare Coverage Expanded Across Multiple Villages"
    )
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
    render_doctor_notes(selected)

    # ----------------------------------------------------------
    # DOWNLOAD REPORT
    # ----------------------------------------------------------
    render_download(selected, vitals)
    
    report_data = {
    
        "patient": selected,
    
        "risk_level": risk_level,
    
        "risk_score": risk_score,
    
        "heart_rate": vitals["heart_rate"],
    
        "spo2": vitals["spo2"],
    
        "temperature": vitals["temperature"],
    
        "bp": vitals["bp"],
    
        "respiratory_rate":
            vitals["respiratory_rate"]
    }
    
    generate_report(
        "patient_report.pdf",
        report_data
    )
    
    with open(
        "patient_report.pdf",
        "rb"
    ) as pdf:
    
        st.download_button(
            "📄 Download PDF Report",
            pdf,
            file_name="patient_report.pdf",
            mime="application/pdf"
        )
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

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

st.markdown("---")

st.markdown(
"""
<div style='
text-align:center;
padding:20px;
color:#666;
'>

🌿 AyushCare v2.0

<br>

AWS + IoT + AI Rural Healthcare Platform

<br><br>

Built by K.N.V. Sai Meghana

</div>
""",
unsafe_allow_html=True
)
