import streamlit as st

from components.sidebar import render_sidebar

from components.status_card import (
    render_status_card
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


def page_dashboard():

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

    dark_mode, data_source, show_gauge = (
        render_sidebar()
    )

    if data_source == "Upload CSV":
        upload_csv()

    data = load_json_data()

    patients = list(data.keys())

    selected = st.sidebar.selectbox(
        "🧑 Select Patient",
        patients
    )

    vitals = data[selected]

    save_to_dynamodb(selected, vitals)

    (
        risk_score,
        risk_level,
        risk_color,
        patient_status
    ) = calculate_risk(vitals)

    render_status_card(
        risk_score,
        risk_level,
        risk_color,
        patient_status
    )

    render_emergency(risk_level)

    render_timeline()

    render_patient_monitor()

    render_metrics(
        vitals,
        risk_level,
        risk_score
    )

    render_ai_predictions(risk_level)

    render_doctor_notes()

    render_ecg()

    render_vitals_chart(vitals)

    render_history(selected)

    render_download(selected, vitals)

    if dark_mode:

        st.markdown(
            """
            <style>

            body, .stApp {
                background-color:#111 !important;
                color:white !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )
