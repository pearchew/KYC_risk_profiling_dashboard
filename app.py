import streamlit as st
import pandas as pd
import plotly.express as px
from kyc_rules_engine import process_kyc_data
import joblib
import numpy as np

# st.set_page_config: This must be the very first Streamlit command in your script. 
# We set layout="wide" because data dashboards look terrible when squished into the center of the screen. 
# This tells the app to stretch across the user's entire monitor.
st.set_page_config(page_title="AML Command Center", page_icon="🛡️", layout="wide")

@st.cache_resource
def load_ml_assets():
    model = joblib.load('models/best_fraud_model.joblib')
    scaler = joblib.load('models/robust_scaler.joblib')
    return model, scaler

try:
    loaded_model, loaded_scaler = load_ml_assets()
except Exception as e:
    st.error(f"Error loading ML models: {e}")

# st.title & st.markdown: These print text to the main screen. st.markdown lets you use standard markdown formatting (like ### for smaller headers) directly in the app.
# st.sidebar: Adding .sidebar to any Streamlit command pushes that element to a panel on the left side of the screen. 
# This is a standard UI best practice: put your controls/inputs on the side, and your results in the main viewing area.
# type=['csv']: This is a crucial guardrail. If we didn't include this, a user might upload a PDF or an Excel file, which would immediately crash our Pandas code later on.
st.title("🛡️ AML Compliance Command Center")
st.divider()
tab1, tab2 = st.tabs(["📋 Phase 1: KYC Onboarding", "💳 Phase 2: Transaction Monitoring"])
st.sidebar.header("Data Ingestion")
st.sidebar.markdown("Upload new client data to run through the KYC rule engine.")
uploaded_customer = st.sidebar.file_uploader("Upload KYC CSV", type=['csv'])

# 4. Main App Logic
with tab1:
    st.markdown("### Phase 1: KYC & Onboarding Risk Triage")
    if uploaded_customer is not None:
        df = pd.read_csv(uploaded_customer)
        scored_df = process_kyc_data(df)
        
        total_customers = len(scored_df)
        high_risk_count = len(scored_df[scored_df['Risk_Tier'] == 'High'])
        high_risk_pct = (high_risk_count / total_customers) * 100
        
        # st.columns(3): This splits the screen into three equal vertical columns.
        # st.metric: This is a built-in Streamlit widget designed specifically for dashboards. It displays numbers in a large, bold font. 
        # We put one metric in each column to create a "KPI banner" at the top of the app—exactly what business stakeholders like to see first.
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers Processed", total_customers)
        col2.metric("High Risk Clients", high_risk_count)
        col3.metric("High Risk %", f"{high_risk_pct:.1f}%")
        
        st.divider()
        
        # st.columns([1, 1.5]): Instead of equal columns, we are giving it a ratio. 
        # This creates a 40% / 60% split. We do this because data tables usually need more horizontal room to be readable than pie charts do.
        col_chart, col_table = st.columns([1, 1.5]) # Make the table column slightly wider
        
        with col_chart:
            st.subheader("Risk Tier Distribution")
            # Create a pie chart using Plotly
            fig = px.pie(
                scored_df, 
                names='Risk_Tier', 
                color='Risk_Tier',
                color_discrete_map={'Low': '#00CC96', 'Medium': '#FFA15A', 'High': '#EF553B'},
                hole=0.4 # Makes it a donut chart
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_table:
            st.subheader("🚨 Action Required: High Risk Clients (EDD)")
            # Filter for only High Risk customers
            high_risk_df = scored_df[scored_df['Risk_Tier'] == 'High'].reset_index(drop=True)
            
            if not high_risk_df.empty:
                st.dataframe(high_risk_df, use_container_width=True)
            else:
                st.success("No high-risk clients detected in this batch.")

    else:
        st.info("👈 Please upload the 'mock_kyc_data.csv' file from the sidebar to begin.")

with tab2:
    st.markdown("### Phase 2: Transaction Monitoring & Fraud Detection")
    st.header("ML Fraud Detection")
    uploaded_tx = st.sidebar.file_uploader("2. Upload Transaction CSV", type=['csv'], key="tx_up")
    if uploaded_tx:
        tx_data = pd.read_csv(uploaded_tx)
        ids = tx_data['Customer_ID']
        X_input = tx_data.drop(['Customer_ID', 'Class'], axis=1)
        X_input['scaled_amount'] = loaded_scaler.transform(X_input['Amount'].values.reshape(-1,1))
        X_input['scaled_time'] = loaded_scaler.transform(X_input['Time'].values.reshape(-1,1))
        X_input.drop(['Time', 'Amount'], axis=1, inplace=True)
        preds = loaded_model.predict(X_input)
        probs = loaded_model.predict_proba(X_input)[:, 1]
        tx_data['Is_Fraud'] = preds
        tx_data['Fraud_Probability'] = probs
        
        fraud_hits = tx_data[tx_data['Is_Fraud'] == 1]
        
        st.metric("Total Fraud Alerts", len(fraud_hits))
        
        fig_fraud = px.scatter(
            tx_data, 
            x='Amount', 
            y='Fraud_Probability', 
            color='Is_Fraud',
            title="Transaction Risk Mapping",
            color_discrete_map={0: 'gray', 1: 'red'}
        )
        st.plotly_chart(fig_fraud, use_container_width=True)
        
        st.subheader("High-Probability Fraud Cases")
        st.dataframe(fraud_hits.sort_values(by='Fraud_Probability', ascending=False))