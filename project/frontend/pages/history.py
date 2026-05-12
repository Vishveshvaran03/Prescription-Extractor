"""History page — view, search, export, and delete prescription records."""

import streamlit as st
import requests
import pandas as pd

st.title("📋 Prescription History")

API_URL = "http://localhost:8000"


def fetch_prescriptions():
    """Fetch all prescriptions from the API."""
    try:
        response = requests.get(f"{API_URL}/prescriptions", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Is FastAPI running?")
        return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []


def delete_prescription(pid):
    """Delete a prescription by ID and refresh the page."""
    try:
        response = requests.delete(f"{API_URL}/prescription/{pid}", timeout=10)
        if response.status_code == 200:
            st.success(f"✅ Prescription #{pid} deleted!")
            st.rerun()
        else:
            st.error("Failed to delete. Record may not exist.")
    except Exception as e:
        st.error(f"Error deleting: {e}")


# ── Fetch and display data ───────────────────────────────────────────────
prescriptions = fetch_prescriptions()

if not prescriptions:
    st.info("No prescriptions found. Go to **Upload** to add one!")
else:
    df = pd.DataFrame(prescriptions)

    # ── Search / Filter ──────────────────────────────────────────────
    search_term = st.text_input("🔍 Search by Patient or Doctor Name:")
    if search_term:
        mask = (
            df["patient_name"].str.contains(search_term, case=False, na=False)
            | df["doctor_name"].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]

    st.markdown(f"**Found {len(df)} record(s)**")

    # ── Data Table ───────────────────────────────────────────────────
    display_cols = [
        c
        for c in ["id", "date", "patient_name", "doctor_name", "hospital_name", "medicine", "dosage", "created_at"]
        if c in df.columns
    ]
    st.dataframe(df[display_cols], use_container_width=True)

    # ── Export ────────────────────────────────────────────────────────
    st.markdown("### 📥 Export Data")
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="prescriptions.csv", mime="text/csv")
    with col2:
        json_data = df.to_json(orient="records")
        st.download_button("Download JSON", data=json_data, file_name="prescriptions.json", mime="application/json")

    # ── Delete ────────────────────────────────────────────────────────
    st.markdown("### 🗑️ Delete Record")
    del_id = st.number_input("Enter prescription ID to delete:", min_value=1, step=1)
    if st.button("Delete Record", type="primary"):
        delete_prescription(del_id)
