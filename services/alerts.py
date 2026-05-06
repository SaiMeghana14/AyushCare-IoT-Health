import time
import streamlit as st


def get_alerts(vitals):

    alerts = []

    if vitals["spo2"] < 90:
        alerts.append(("SpO₂", "critical", "Low oxygen detected"))

    if vitals["heart_rate"] > 100:
        alerts.append(("Heart Rate", "warning", "Possible tachycardia"))

    if vitals["temperature"] > 38.9:
        alerts.append(("Temperature", "warning", "High fever detected"))

    return alerts


def calculate_risk(vitals):

    risk_score = 100

    if vitals["spo2"] < 95:
        risk_score -= 20

    if vitals["heart_rate"] > 100:
        risk_score -= 15

    if vitals["temperature"] > 38:
        risk_score -= 15

    if risk_score >= 85:
        risk_level = "Low"
        risk_color = "#16a34a"
        patient_status = "🟢 Patient Stable"

    elif risk_score >= 60:
        risk_level = "Moderate"
        risk_color = "#f59e0b"
        patient_status = "🟡 Monitoring Required"

    else:
        risk_level = "Critical"
        risk_color = "#dc2626"
        patient_status = "🔴 Critical Condition"

    return risk_score, risk_level, risk_color, patient_status
