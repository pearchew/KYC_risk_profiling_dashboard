# 🛡️ AML Compliance Command Center: End-to-End Risk Lifecycle

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-F7931E)

> **Business Context:** In Anti-Money Laundering (AML) and Risk management, customer evaluation isn't just an isolated machine learning model. It is a lifecycle. This project bridges the gap between **Phase 1: Onboarding (KYC)** and **Phase 2: Activity Monitoring (Transactional Fraud)** to provide a holistic view of customer risk.

`![Dashboard Screenshot](dashboard_ss.png`

## 📖 Overview
The **AML Compliance Command Center** is an interactive web dashboard built with Streamlit. It transitions terminal-based scripts into a tangible UI designed for Compliance Officers and Risk Analysts. 

By uploading client and transaction data, users can visually triage customer risk. The system automatically assigns a KYC risk tier using a rule-based engine and monitors subsequent transactional behavior using an integrated Machine Learning model.

This repository integrates the transaction-scoring ML model originally developed [here](https://github.com/pearchew/fraud_detection_model).

## ✨ Core Features

### 1. Phase 1: KYC Onboarding Engine (Rule-Based)
* **Data Ingestion:** Drag-and-drop CSV upload for mock customer demographics (Age, Nationality, Occupation, Income).
* **Automated Risk Tiering:** Applies compliance logic to categorize users into `Low`, `Medium`, or `High` risk tiers (e.g., Flagging cash-intensive occupations from high-risk jurisdictions).
* **Visual Triage:** Interactive Plotly pie charts and filtered Pandas DataFrames displaying customers requiring Enhanced Due Diligence (EDD).

### 2. Phase 2: Transaction Monitoring (ML-Based)
* **Model Integration:** Loads a pre-trained `scikit-learn` model (`.pkl`) to evaluate transactional data.
* **Fraud Probability Scoring:** Processes customer transactions and outputs a `Fraud_Probability` score.
* **Lifecycle Mapping:** Links `Customer_ID` between the KYC phase and the Transaction phase to highlight compound risks (e.g., High KYC Risk + High Fraud Probability).

## 🛠️ Technology Stack
* **UI & Web Framework:** `streamlit`
* **Data Manipulation:** `pandas`, `numpy`
* **Data Visualization:** `plotly.express`
* **Machine Learning:** `scikit-learn`
* **Development:** VS Code, Jupyter Notebooks

## 🚀 Quick Start / Installation

**1. Clone the repository**
```bash
git clone [https://github.com/pearchew/aml-compliance-dashboard.git](https://github.com/pearchew/aml-compliance-dashboard.git)
cd aml-compliance-dashboard