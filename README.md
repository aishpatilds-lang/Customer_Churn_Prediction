# 📊 Customer Churn Intelligence System

A Machine Learning web application that predicts customer churn and provides actionable insights for business decision-making.

Built with Streamlit, this system analyzes customer data and identifies churn risk along with recommendations to improve retention.

---

## 🚀 Features

- Churn prediction using trained ML pipeline
- Risk classification (Low / Medium / High)
- Interactive dashboard (Gauge + Donut chart)
- Key influencing factors
- Business insights & recommendations
- Downloadable PDF report

---

## 🛠️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- Streamlit
- Plotly
- Joblib
- FPDF

---

## 📂 Project Structure


Customer_Churn_Prediction/
│
├── app.py
├── pipeline.pkl
├── telecom_churn_data.csv
├── train.ipynb
├── train_pipeline.py
├── output/
└── README.md


---

## ⚙️ Setup Instructions

### 1. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run the app
streamlit run app.py

📊 Input Features
Tenure (months)
Monthly Charges
Contract Type
Internet Service
Payment Method
Tech Support
Online Security

📈 Output
Churn Probability (%)
Risk Level (Low / Medium / High)
Revenue Risk (6 months)
Visual dashboard
Actionable recommendations

📌 Risk Guide
0–35% → Low Risk
35–65% → Medium Risk
65–100% → High Risk
👩‍💻 Author

Aishwarya Patil
GitHub: https://github.com/aishpatilds-lang

LinkedIn: https://linkedin.com/in/aishwarya-patil-299108338