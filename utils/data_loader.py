import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    """
    Loads and pre-processes the traffic violation data.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

    # --- Data Cleaning & Preprocessing ---

    # 1. Combine Date and Time into a datetime column
    # Ensure Date and Time are strings before combining
    df['Date'] = df['Date'].astype(str)
    df['Time'] = df['Time'].astype(str)
    
    # Attempt to parse standard formats
    try:
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    except Exception as e:
        st.warning(f"Could not parse some Date/Time values: {e}")
        df['Datetime'] = pd.to_datetime(df['Date'], errors='coerce') # Fallback

    # 2. Extract Temporal Features
    df['Month'] = df['Datetime'].dt.month_name()
    df['Month_Num'] = df['Datetime'].dt.month
    df['Day_of_Week'] = df['Datetime'].dt.day_name()
    df['Hour'] = df['Datetime'].dt.hour
    
    # 3. Numeric Conversions
    df['Fine_Amount'] = pd.to_numeric(df['Fine_Amount'], errors='coerce').fillna(0)
    df['Recorded_Speed'] = pd.to_numeric(df['Recorded_Speed'], errors='coerce')
    df['Speed_Limit'] = pd.to_numeric(df['Speed_Limit'], errors='coerce')
    df['Driver_Age'] = pd.to_numeric(df['Driver_Age'], errors='coerce')

    # 4. Fill Missing Values
    df['Helmet_Worn'] = df['Helmet_Worn'].fillna('Unknown')
    df['Seatbelt_Worn'] = df['Seatbelt_Worn'].fillna('Unknown')
    df['Comments'] = df['Comments'].fillna('None')

    # 5. Categorical Consistency (Optional cleaning based on inspection)
    # Ensure consistent casing
    categorical_cols = ['Violation_Type', 'Location', 'Vehicle_Type', 'Gender', 'Payment_Method']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()

    return df
