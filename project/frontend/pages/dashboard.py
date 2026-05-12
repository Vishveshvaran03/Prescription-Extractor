"""Dashboard page — overview of system status and recent prescriptions."""

import streamlit as st
import requests

st.title("📊 Dashboard")

API_URL = "http://localhost:8000"

try:
    response = requests.get(f"{API_URL}/analytics", timeout=5)

    if response.status_code == 200:
        data = response.json()
        total = data.get("total_prescriptions", 0)

        # ── Overview Cards ───────────────────────────────────────────
        st.markdown("### Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Prescriptions", total)
        with col2:
            st.metric("System Status", "✅ Online")
        with col3:
            st.metric("OCR Engine", "EasyOCR")

        st.markdown("---")

        # ── Recent Prescriptions ─────────────────────────────────────
        st.markdown("### Recent Prescriptions")
        presc_response = requests.get(f"{API_URL}/prescriptions?skip=0&limit=5", timeout=5)

        if presc_response.status_code == 200:
            recent = presc_response.json()
            if recent:
                for p in recent:
                    date_str = p.get("date") or "Unknown Date"
                    patient_str = p.get("patient_name") or "Unknown Patient"
                    with st.expander(f"📋 {date_str} — {patient_str}"):
                        st.write(f"**Doctor:** {p.get('doctor_name', 'N/A')}")
                        st.write(f"**Hospital:** {p.get('hospital_name', 'N/A')}")
                        st.write(f"**Medicine:** {p.get('medicine', 'N/A')}")
                        st.write(f"**Dosage:** {p.get('dosage', 'N/A')}")
            else:
                st.info("No prescriptions yet. Go to **Upload** to add one!")
        else:
            st.warning("Could not load recent prescriptions.")
    else:
        st.error("Failed to load dashboard data from backend.")

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to backend server. Please ensure FastAPI is running on port 8000.")
except requests.exceptions.Timeout:
    st.error("⏳ Backend server timed out. Please try again.")
