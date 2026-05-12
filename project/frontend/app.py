"""
Prescription Extractor System — Streamlit Frontend
Main landing page and navigation setup.
"""

import streamlit as st

st.set_page_config(
    page_title="Prescription Extractor",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Header ───────────────────────────────────────────────────────────────
st.title("⚕️ Prescription Extractor System")

st.markdown("""
Welcome to the **Prescription Extractor System**!

This AI-powered tool helps you:
- 📤 **Upload** handwritten or printed medical prescriptions
- 🔍 **Extract** text and important fields automatically using OCR
- ✏️ **Review & Correct** extracted data before saving
- 💾 **Store** records securely in a Supabase database
- 📈 **Analyze** your prescription history with charts

Use the **sidebar** to navigate between pages.
""")

# ── Sidebar ──────────────────────────────────────────────────────────────
st.sidebar.title("Navigation")
st.sidebar.info("Use the pages above to navigate through the application.")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Quick Start:**
1. Go to **Upload** to scan a prescription
2. Review and save the extracted data
3. View **History** for all records
4. Check **Analytics** for insights
""")

# ── Custom Styling ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)
