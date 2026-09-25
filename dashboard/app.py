import streamlit as st
import requests
import time

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Heavy Vehicle Safety AI",
    page_icon="🚛",
    layout="wide"
)

# Change this to the L3 laptop's IP address.
# Example: http://192.168.1.25:5000
SERVER_URL = "http://127.0.0.1:5000"


# ---------------------------------------------------------
# PAGE STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .status-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        border: 2px solid;
    }

    .small-label {
        font-size: 14px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🚛 Intelligent Heavy Vehicle Safety AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Driver Monitoring + Road Monitoring + Intelligent Risk Assessment</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# GET DATA FROM L3
# ---------------------------------------------------------

def get_status():

    try:

        response = requests.get(
            f"{SERVER_URL}/status",
            timeout=2
        )

        response.raise_for_status()

        return response.json(), None

    except Exception as error:

        return None, str(error)


data, error = get_status()


# ---------------------------------------------------------
# CONNECTION STATUS
# ---------------------------------------------------------

if error:

    st.error(
        "L3 Safety Engine is not reachable. "
        "Check that L3 server is running and SERVER_URL is correct."
    )

    st.code(error)

    st.stop()


driver = data["driver"]
road = data["road"]
safety = data["safety"]


# ---------------------------------------------------------
# TOP STATUS
# ---------------------------------------------------------

risk_level = safety["risk_level"]
risk_score = safety["risk_score"]

if risk_level == "SAFE":
    status_text = "🟢 SAFE"
elif risk_level == "WARNING":
    status_text = "🟡 WARNING"
else:
    status_text = "🔴 CRITICAL"

st.markdown(
    f'<div class="status-box">SAFETY STATUS: {status_text}<br>'
    f'<span style="font-size:20px;">Risk Score: {risk_score}/100</span></div>',
    unsafe_allow_html=True
)

st.write("")


# ---------------------------------------------------------
# COLUMNS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)


# ---------------------------------------------------------
# DRIVER STATUS
# ---------------------------------------------------------

with col1:

    st.subheader("👤 Driver Monitoring")

    st.metric(
        "Drowsiness",
        "HIGH" if driver["drowsiness"] else "LOW"
    )

    st.metric(
        "Distraction",
        "HIGH" if driver["distraction"] else "LOW"
    )

    st.metric(
        "Yawning",
        "DETECTED" if driver["yawning"] else "NOT DETECTED"
    )


# ---------------------------------------------------------
# ROAD STATUS
# ---------------------------------------------------------

with col2:

    st.subheader("🛣️ Road Monitoring")

    st.metric(
        "Vehicles",
        road["vehicles"]
    )

    st.metric(
        "Trucks",
        road["trucks"]
    )

    st.metric(
        "People",
        road["people"]
    )

    st.metric(
        "Motorcycles",
        road["motorcycles"]
    )


# ---------------------------------------------------------
# EMERGENCY RESPONSE
# ---------------------------------------------------------

with col3:

    st.subheader("🚨 Safety Response")

    if safety["controlled_braking"]:
        st.error("🐢 CONTROLLED BRAKING: ACTIVE")
    else:
        st.success("🐢 CONTROLLED BRAKING: INACTIVE")

    if safety["hazard_lights"]:
        st.error("🚨 HAZARD LIGHTS: ON")
    else:
        st.success("🚨 HAZARD LIGHTS: OFF")


# ---------------------------------------------------------
# REASONS
# ---------------------------------------------------------

st.divider()

st.subheader("🧠 Risk Analysis")

if safety["reasons"]:

    for reason in safety["reasons"]:
        st.warning(reason)

else:

    st.success("No active risk factors detected.")


# ---------------------------------------------------------
# SYSTEM INFORMATION
# ---------------------------------------------------------

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("System Status")

    st.write("L1 Driver AI: Connected through L3")
    st.write("L2 Road AI: Connected through L3")
    st.write("L3 Safety Engine: 🟢 Online")
    st.write("L4 Dashboard: 🟢 Online")

with right:

    st.subheader("Prototype Emergency Logic")

    st.write(
        "Critical risk → driver warning → "
        "controlled-braking simulation + hazard-light simulation."
    )


# ---------------------------------------------------------
# AUTO REFRESH
# ---------------------------------------------------------

time.sleep(1)
st.rerun()
