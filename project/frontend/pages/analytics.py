"""Analytics page — charts and statistics using Plotly."""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("📈 Analytics Dashboard")

API_URL = "http://localhost:8000"

try:
    response = requests.get(f"{API_URL}/analytics", timeout=10)

    if response.status_code == 200:
        data = response.json()
        total = data.get("total_prescriptions", 0)
        top_medicines = data.get("top_medicines", [])
        top_doctors = data.get("top_doctors", [])

        # ── Overview Metrics ─────────────────────────────────────────
        st.header("Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Prescriptions", total)
        with col2:
            st.metric("Unique Medicines", len(top_medicines))
        with col3:
            st.metric("Unique Doctors", len(top_doctors))

        st.markdown("---")

        # ── Medicine Analytics ───────────────────────────────────────
        st.header("💊 Most Common Medicines")

        if top_medicines:
            df_meds = pd.DataFrame(top_medicines)

            # Bar chart
            fig_bar = px.bar(
                df_meds,
                x="name",
                y="count",
                title="Medicine Frequency",
                labels={"name": "Medicine", "count": "Times Prescribed"},
                color="count",
                color_continuous_scale="Teal",
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)

            # Pie chart
            fig_pie = px.pie(
                df_meds,
                names="name",
                values="count",
                title="Medicine Distribution",
                hole=0.3,
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Not enough data for medicine analytics. Upload more prescriptions!")

        st.markdown("---")

        # ── Doctor Analytics ─────────────────────────────────────────
        st.header("🩺 Top Prescribing Doctors")

        if top_doctors:
            df_docs = pd.DataFrame(top_doctors)

            fig_doc = px.bar(
                df_docs,
                x="name",
                y="count",
                title="Prescriptions per Doctor",
                labels={"name": "Doctor", "count": "Prescriptions"},
                color="count",
                color_continuous_scale="Purp",
            )
            fig_doc.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_doc, use_container_width=True)
        else:
            st.info("Not enough data for doctor analytics.")

    else:
        st.error("Failed to load analytics data from backend.")

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to backend. Is FastAPI running on port 8000?")
except requests.exceptions.Timeout:
    st.error("⏳ Backend timed out. Please try again.")
except Exception as e:
    st.error(f"Error: {e}")
