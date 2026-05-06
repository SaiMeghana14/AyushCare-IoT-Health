import streamlit as st


def render_metrics(vitals, risk_level, risk_score):

    st.subheader("🧑‍⚕️ Live Patient Vitals")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="❤️ Heart Rate",
            value=f"{vitals['heart_rate']} BPM"
        )

    with c2:
        st.metric(
            label="🫁 SpO₂",
            value=f"{vitals['spo2']}%"
        )

    with c3:
        st.metric(
            label="🌡 Temperature",
            value=f"{vitals['temperature']} °C"
        )

    with c4:
        st.metric(
            label="⚠ Risk",
            value=risk_level,
            delta=f"{risk_score}/100"
        )
