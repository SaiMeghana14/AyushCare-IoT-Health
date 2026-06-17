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
    
        st.success("☁ AWS IoT Connected")
        st.success("🗄 DynamoDB Active")
        st.success("📨 SNS Alerts Enabled")
        st.success("🤖 AI Insights Running")

    st.sidebar.markdown("---")
    with st.sidebar.expander(
        "📡 Device Status",
        expanded=True
    ):
        st.sidebar.success("ESP32 Connected")
        st.sidebar.success("MAX30102 Active")
        st.sidebar.success("Temperature Sensor Online")
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "🌿 AyushCare v2.0\n\nAWS + IoT + AI Healthcare Platform"
)

    return dark_mode, data_source, show_gauge
