import pandas as pd

# Define our risk parameters based on the mock data we generated
HIGH_RISK_COUNTRIES = ['North Korea', 'Panama', 'Cayman Islands']
HIGH_RISK_OCCUPATIONS = ['Casino Operator', 'Cash-Intensive Business Owner']

def assign_risk_tier(row):
    """
    Evaluates a single customer record (row) and returns a risk tier.
    """
    is_high_risk_country = row['Nationality'] in HIGH_RISK_COUNTRIES
    is_high_risk_occ = row['Occupation'] in HIGH_RISK_OCCUPATIONS
    income = row['Estimated_Annual_Income']
    
    # Rule 1: High Risk Country ALWAYS triggers High Risk
    if is_high_risk_country:
        return 'High'
    
    # Rule 2: High Risk Occupation triggers Medium Risk (or High if income is massive)
    elif is_high_risk_occ:
        if income > 300000:
            return 'High'
        return 'Medium'
        
    # Rule 3: High income alone might warrant a closer look (Medium EDD)
    elif income > 400000:
        return 'Medium'
        
    # Default: If no rules are triggered, the customer is Low Risk
    else:
        return 'Low'

def process_kyc_data(df):
    """
    Applies the risk rules to the entire dataframe and adds a 'Risk_Tier' column.
    """
    processed_df = df.copy() # Good practice: work on a copy to avoid altering the original unexpectedly
    
    # The .apply() method runs our assign_risk_tier function on every single row (axis=1)
    processed_df['Risk_Tier'] = processed_df.apply(assign_risk_tier, axis=1)
    
    return processed_df