# frontend/streamlit_app.py

import streamlit as st
import pandas as pd
import requests

API_BASE = "http://127.0.0.1:8000"

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Exam Signal OS",
    layout="wide"
)

st.title("📊 Exam Signal OS")
st.caption(
    "Based on analysis of past exam papers — showing what is actually tested, not what is claimed."
)

# ---------------- LOGIN ----------------
st.subheader("🔐 Login")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login / Register")

if submitted:
    resp = requests.post(
        f"{API_BASE}/auth/register",
        json={"email": email, "password": password}
    )

    if resp.status_code == 200:
        st.session_state["token"] = resp.json()["access_token"]
        st.success("Logged in successfully")
    else:
        st.error("Authentication failed")

# Block app if not logged in
if "token" not in st.session_state:
    st.warning("Please log in to access exam insights.")
    st.stop()

# ---------------- LOAD DATA (AFTER LOGIN) ----------------
headers = {
    "Authorization": f"Bearer {st.session_state['token']}"
}

resp = requests.get(
    f"{API_BASE}/signals/",
    headers=headers
)

if resp.status_code != 200:
    st.error("Failed to load signals from backend")
    st.stop()

signals_df = pd.DataFrame(resp.json()["data"])

questions = pd.read_csv("data/processed/questions_with_predictions.csv")
units_df = pd.read_csv("data/processed/syllabus_units.csv")

# ---------------- HOW TO USE ----------------
st.markdown("---")

with st.expander("ℹ️ How to use this dashboard"):
    st.markdown("""
    **Start with the Unit Importance Ranking**
    - Focus first on units with higher *Questions Asked* and *Marks Weight*
    - Use the trend chart to see if a unit is rising or declining

    **Use the Evidence View**
    - Click any unit to see real exam questions
    - This shows *why* the unit matters
    """)

# ---------------- UNIT IMPORTANCE ----------------
st.header("🔥 What Matters Most in the Exam")

signals_view = signals_df.merge(
    units_df[["unit_id", "unit_name"]],
    on="unit_id",
    how="left"
).sort_values(by="frequency", ascending=False)

signals_view_renamed = signals_view.rename(columns={
    "unit_id": "Unit Code",
    "unit_name": "Unit Name",
    "frequency": "Questions Asked",
    "total_marks": "Marks Weight",
    "years_active": "Years Active"
})

st.dataframe(signals_view_renamed, use_container_width=True)

# ---------------- UNIT EVIDENCE ----------------
st.markdown("---")
st.header("🔍 Proof from Past Exams")

selected_unit = st.selectbox(
    "Select a syllabus unit",
    signals_view["unit_id"].unique()
)

unit_name = units_df.loc[
    units_df["unit_id"] == selected_unit,
    "unit_name"
].values[0]

st.subheader(f"Unit: {unit_name} ({selected_unit})")

mask = (
    questions["predicted_units"]
    .fillna("")
    .astype(str)
    .str.contains(selected_unit, regex=False)
)

unit_questions = questions[mask]

st.markdown(f"**Questions mapped to this unit:** {len(unit_questions)}")

# ---------------- TREND CHART ----------------
st.subheader("📈 Unit Trend Over Years")

trend_df = (
    unit_questions
    .groupby("year")
    .size()
    .reset_index(name="question_count")
    .sort_values("year")
)

if not trend_df.empty:
    st.line_chart(trend_df.set_index("year"))
else:
    st.info("Not enough data to show trend.")

# ---------------- QUESTION LIST ----------------
for _, row in unit_questions.iterrows():
    st.markdown(
        f"- **({row['year']}, {row['marks']} marks)** {row['question_text']}"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Exam Signal OS • Data-backed exam intelligence • Built for serious preparation"
)

st.info(
    "🔒 Advanced features like multi-exam comparison, predictions, and institute dashboards are part of the Pro version."
)
