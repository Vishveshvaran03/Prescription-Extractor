"""Upload page — upload a prescription image, extract text via OCR, review and save."""

import streamlit as st
import requests
import time

st.title("📤 Upload Prescription")

API_URL = "http://localhost:8000"

st.markdown("Upload a prescription image (**JPG, PNG**) to extract data using OCR.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    # ── Show uploaded image ──────────────────────────────────────────
    with col1:
        st.image(uploaded_file, caption="Uploaded Prescription", use_container_width=True)

    # ── OCR Extraction ───────────────────────────────────────────────
    with col2:
        st.subheader("Extraction Status")

        # Only run OCR if this is a new file
        if (
            "extracted_data" not in st.session_state
            or st.session_state.get("current_file") != uploaded_file.name
        ):
            with st.spinner("🔍 Extracting text using EasyOCR... Please wait (first time takes longer)."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    start_time = time.time()
                    response = requests.post(f"{API_URL}/upload_prescription", files=files, timeout=120)
                    elapsed = time.time() - start_time

                    if response.status_code == 200:
                        result = response.json()
                        st.session_state["extracted_data"] = result["data"]
                        st.session_state["current_file"] = uploaded_file.name
                        st.success(f"✅ Extraction complete in {elapsed:.2f} seconds!")
                    else:
                        st.error(f"Server error: {response.text}")
                        st.stop()
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Is FastAPI running on port 8000?")
                    st.stop()
                except requests.exceptions.Timeout:
                    st.error("⏳ OCR processing timed out. Try a smaller image.")
                    st.stop()

    # ── Show Raw OCR Text + Correction Form ──────────────────────────
    if (
        "extracted_data" in st.session_state
        and st.session_state.get("current_file") == uploaded_file.name
    ):
        data = st.session_state["extracted_data"]

        # Show raw OCR text prominently so user knows what was detected
        st.markdown("---")
        st.subheader("📄 Raw OCR Text (what the AI detected)")
        raw_text = data.get("extracted_text", "")
        st.text_area(
            "Raw OCR Output",
            value=raw_text if raw_text else "(No text was detected in the image)",
            height=200,
            disabled=True,
            label_visibility="collapsed",
        )

        if not raw_text or raw_text == "(No text detected)":
            st.warning("⚠️ OCR couldn't detect text. Please fill in the fields manually below.")

        # ── Correction Form ──────────────────────────────────────────
        st.markdown("---")
        st.subheader("✏️ Review & Fill Details")
        st.info("The fields below are auto-filled from OCR. **If they're empty, fill them manually** from the raw text above.")

        with st.form("correction_form"):
            patient_name = st.text_input("Patient Name", value=data.get("patient_name", ""))
            doctor_name = st.text_input("Doctor Name", value=data.get("doctor_name", ""))
            hospital_name = st.text_input("Hospital / Clinic", value=data.get("hospital_name", ""))
            medicine = st.text_input("Medicine(s)", value=data.get("medicine", ""),
                                     help="Separate multiple medicines with commas")
            dosage = st.text_input("Dosage", value=data.get("dosage", ""),
                                   help="e.g. 500mg, 200mg")
            date = st.text_input("Date", value=data.get("date", ""))

            submitted = st.form_submit_button("💾 Save to Database", type="primary")

            if submitted:
                save_payload = {
                    "patient_name": patient_name,
                    "doctor_name": doctor_name,
                    "hospital_name": hospital_name,
                    "medicine": medicine,
                    "dosage": dosage,
                    "date": date,
                    "extracted_text": raw_text,
                }

                try:
                    save_response = requests.post(
                        f"{API_URL}/save_prescription", json=save_payload, timeout=10
                    )
                    if save_response.status_code == 200:
                        st.success("✅ Prescription saved successfully!")
                        del st.session_state["extracted_data"]
                        del st.session_state["current_file"]
                    else:
                        st.error(f"Failed to save: {save_response.text}")
                except Exception as e:
                    st.error(f"Error saving to database: {e}")
