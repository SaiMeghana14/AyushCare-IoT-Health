import streamlit as st


def render_sidebar():

    st.sidebar.title("☰ Options")

    dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

    data_source = st.sidebar.radio(
        "📦 Data Source",
        ["Local JSON", "Upload CSV"]
    )

    show_gauge = st.sidebar.checkbox("📊 Show Gauge Meters")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.current_user = None
        st.session_state.page = "login"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("## ☁ AWS Cloud Status")

    st.sidebar.success("☁ AWS IoT Connected")
    st.sidebar.success("🗄 DynamoDB Active")
    st.sidebar.success("📨 SNS Alerts Enabled")
    st.sidebar.success("🤖 AI Insights Running")

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📡 Device Status")

    st.sidebar.success("ESP32 Connected")
    st.sidebar.success("MAX30102 Active")
    st.sidebar.success("Temperature Sensor Online")

    return dark_mode, data_source, show_gauge
