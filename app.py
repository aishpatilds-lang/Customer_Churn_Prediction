import streamlit as st
import pandas as pd
import joblib
import os
import re
import plotly.graph_objects as go
from fpdf import FPDF

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Customer Churn Intelligence", layout="wide")
os.makedirs("output", exist_ok=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
pipeline = joblib.load("pipeline.pkl")

# -----------------------------
# CLEAN TEXT FOR PDF
# -----------------------------
def clean_text(text):
    return str(text).encode("latin-1", "replace").decode("latin-1")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Customer Profile")

customer_name = st.sidebar.text_input("Customer Name", "Aishwarya")
tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Monthly Charges", 0.0, 1000.0, 50.0)

contract = st.sidebar.selectbox(
    "Contract Type", ["Month-to-month", "One year", "Two year"]
)

internet = st.sidebar.selectbox(
    "Internet Service", ["DSL", "Fiber optic", "No"]
)

payment = st.sidebar.selectbox(
    "Payment Method",
    ["Electronic check", "Mailed check",
     "Bank transfer (automatic)", "Credit card (automatic)"]
)

tech_support = st.sidebar.selectbox("Tech Support", ["Yes", "No"])
online_security = st.sidebar.selectbox("Online Security", ["Yes", "No"])

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Customer Churn Prediction & Decision Support System")
st.caption("Predict • Explain • Take Action")
st.markdown("---")

# -----------------------------
# PREDICT
# -----------------------------
if st.button("🚀 Predict Churn"):

    input_df = pd.DataFrame({
        "tenure": [tenure],
        "MonthlyCharges": [monthly_charges],
        "Contract": [contract],
        "InternetService": [internet],
        "PaymentMethod": [payment],
        "TechSupport": [tech_support],
        "OnlineSecurity": [online_security]
    })

    prob = pipeline.predict_proba(input_df)[0][1] * 100

    # Risk classification
    risk = "LOW CHURN" if prob < 50 else "HIGH CHURN"
    revenue_risk = (prob / 100) * monthly_charges * 6

    # -----------------------------
    # CUSTOMER DETAILS
    # -----------------------------
    st.subheader(f"👤 Customer: {customer_name}")

    colA, colB = st.columns(2)
    with colA:
        st.write(f"**Tenure:** {tenure} months")
        st.write(f"**Monthly Charges:** ${monthly_charges}")
        st.write(f"**Contract:** {contract}")

    with colB:
        st.write(f"**Internet:** {internet}")
        st.write(f"**Payment:** {payment}")
        st.write(f"**Tech Support:** {tech_support} | Security: {online_security}")

    st.markdown("---")

    # -----------------------------
    # METRICS
    # -----------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Churn Probability", f"{prob:.2f}%")
    col2.metric("Risk Level", risk)
    col3.metric("Revenue Risk (6 months)", f"${revenue_risk:.2f}")

    st.markdown("---")

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    st.subheader("📊 Churn Risk Dashboard")

    st.markdown("""
    <div style="background-color:#1f3b57;padding:15px;border-radius:10px">
        <b>Risk Guide:</b><br><br>
        🟢 0 – 50 → LOW CHURN<br>
        🔴 50 – 100 → HIGH CHURN
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    # -------- GAUGE --------
    with col_left:
        st.markdown("### 🔴 Churn Probability")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            number={'suffix': "%", 'font': {'size': 42}},
            title={'text': "Risk Indicator", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00C6FF"},
                'steps': [
                    {'range': [0, 50], 'color': "#2ECC71"},
                    {'range': [50, 100], 'color': "#E74C3C"}
                ]
            }
        ))

        gauge.update_layout(
            height=350,
            margin=dict(t=40, b=20),
            paper_bgcolor="#0E1117",
            font={'color': "white"}
        )

        st.plotly_chart(gauge, use_container_width=True)
        gauge.write_image("output/gauge.png")

    # -------- DONUT --------
    with col_right:
        st.markdown("### 🟢 Churn vs Retention")

        pie = go.Figure(data=[go.Pie(
            labels=["Churn", "Retention"],
            values=[prob, 100 - prob],
            hole=0.65,
            textinfo='percent',
            textfont=dict(size=24, color="white", family="Arial Black"),
            marker=dict(colors=["#FF4B4B", "#2ECC71"])
        )])

        pie.update_layout(
            height=350,
            margin=dict(t=40, b=20),
            paper_bgcolor="#0E1117",
            font=dict(color="white"),
            annotations=[dict(
                text=f"<b>{prob:.0f}%</b><br><span style='font-size:14px;color:#AAAAAA'>Churn Risk</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                align="center",
                font=dict(size=30, color="white")
            )]
        )

        st.plotly_chart(pie, use_container_width=True)
        pie.write_image("output/pie.png")

    st.markdown("---")

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    influences = []

    if contract == "Month-to-month":
        influences.append("Short-term contract increases churn risk")
    if internet == "Fiber optic":
        influences.append("Fiber users show higher churn trends")
    if payment == "Electronic check":
        influences.append("Electronic check users churn more frequently")
    if tenure < 12:
        influences.append("Low tenure indicates weak loyalty")
    if monthly_charges > 80:
        influences.append("High charges increase churn risk")

    st.subheader("📌 What influenced this prediction")

    if influences:
        for i in influences:
            st.write(f"• {i}")
    else:
        st.write("Customer profile is stable")

    # -----------------------------
    # KEY INSIGHTS
    # -----------------------------
    st.subheader("🧠 Key Insights")

    if risk == "HIGH CHURN":
        st.write("• Customer is highly likely to churn")
        st.write("• Immediate retention action required")
    else:
        st.write("• Customer is stable with low churn risk")

    # -----------------------------
    # ACTIONS
    # -----------------------------
    st.subheader("💡 Recommended Actions")

    actions = []

    if contract == "Month-to-month":
        actions.append("Offer long-term contract discount")
    if payment == "Electronic check":
        actions.append("Encourage auto-payment methods")
    if monthly_charges > 80:
        actions.append("Provide better pricing plans")
    if tenure < 12:
        actions.append("Improve onboarding experience")

    if not actions:
        actions.append("Maintain engagement strategy")

    for a in actions:
        st.write(f"• {a}")

    # -----------------------------
    # PDF REPORT (FINAL)
    # -----------------------------
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '', customer_name.replace(" ", "_"))
    file_path = f"output/{safe_name}_report.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Customer Churn Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, clean_text(f"""
Customer: {customer_name}
Churn Probability: {prob:.2f}%
Risk Level: {risk}
Revenue Risk (6 months): ${revenue_risk:.2f}
"""))

    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Influencing Factors:", ln=True)

    pdf.set_font("Arial", "", 11)
    if influences:
        for i in influences:
            pdf.multi_cell(0, 8, clean_text(f"- {i}"))
    else:
        pdf.multi_cell(0, 8, "Customer profile is stable")

    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Key Insights:", ln=True)

    pdf.set_font("Arial", "", 11)
    if risk == "HIGH CHURN":
        pdf.multi_cell(0, 8, clean_text(
            "- Customer is highly likely to churn\n"
            "- Immediate retention action required"
        ))
    else:
        pdf.multi_cell(0, 8, clean_text(
            "- Customer is stable with low churn risk"
        ))

    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recommendations:", ln=True)

    pdf.set_font("Arial", "", 11)
    for a in actions:
        pdf.multi_cell(0, 8, clean_text(f"- {a}"))

    # -------- PAGE 2 (BOTH CHARTS) --------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Churn Analysis Charts", ln=True, align="C")

    pdf.image("output/gauge.png", x=25, y=30, w=160)
    pdf.image("output/pie.png", x=25, y=150, w=160)

    pdf.output(file_path)

    with open(file_path, "rb") as f:
        st.download_button("📥 Download Report", f, file_name=f"{safe_name}_report.pdf")