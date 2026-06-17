import streamlit as st


def render_sidebar():

    st.sidebar.title("☰ Options")

    dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

    data_source = st.sidebar.radio(
        "📦 Data Source",
        ["Local JSON", "Upload CSV"]
    )

    show_gauge = st.sidebar.checkbox(
        "📊 Show Gauge Meters",
        value=True)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.current_user = None
        st.session_state.page = "login"
        st.rerun()

    st.sidebar.markdown("---")
    with st.sidebar.expander(
        "☁ AWS Cloud Status",
        expanded=True
    ):
    
        st.info("☁ AWS IoT Connected")
        st.info("🗄 DynamoDB Active")
        st.info("📨 SNS Alerts Enabled")
        st.info("🤖 AI Insights Running")

    st.sidebar.markdown("---")
    with st.sidebar.expander(
        "📡 Device Status",
        expanded=True
    ):
    
        st.info("🟢 ESP32 Connected")
        st.info("❤️ MAX30102 Active")
        st.info("🌡 Temperature Sensor Online")
        st.info("📡 Signal Strength: Excellent")
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "🌿 AyushCare v2.0\n\nAWS + IoT + AI Healthcare Platform"
)

    return dark_mode, data_source, show_gauge
