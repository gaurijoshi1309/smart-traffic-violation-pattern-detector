import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS to clean up the Streamlit UI and match the desired aesthetic.
    """
    st.markdown("""
        <style>
        /* Remove default Streamlit 'Made with' footer */
        footer {visibility: hidden;}
        
        /* Adjust sidebar width and color if needed (Streamlit themes handle most of this) */
        /*
        [data-testid="stSidebar"] {
            background-color: #f0f2f6; 
        }
        */

        /* Custom styling for metrics */
        div[data-testid="metric-container"] {
            background-color: #ffffff10;
            border: 1px solid #ffffff20;
            padding: 10px;
            border-radius: 5px;
            transition: transform 0.2s;
        }

        div[data-testid="metric-container"]:hover {
            transform: scale(1.02);
            border-color: #ffffff50;
        }

        /* Titles and Headers */
        h1, h2, h3 {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 600;
        }
        
        /* Clean up top padding */
        .block-container {
            padding-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

def sidebar_filters(df):
    """
    Common sidebar filters that can be reused or modified.
    Returns the filtered dataframe.
    """
    st.sidebar.header("Filters")
    
    # Date Range
    if 'Datetime' in df.columns and not df['Datetime'].isnull().all():
        min_date = df['Datetime'].min().date()
        max_date = df['Datetime'].max().date()
        
        try:
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            if len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df['Datetime'].dt.date >= start_date) & (df['Datetime'].dt.date <= end_date)]
        except Exception:
            pass # Handle date input errors gracefully

    # State/Location Filter
    if 'Location' in df.columns:
        all_locations = sorted(df['Location'].unique().tolist())
        selected_locations = st.sidebar.multiselect("Select State/Location", all_locations, default=all_locations)
        if selected_locations:
            df = df[df['Location'].isin(selected_locations)]
            
    # Violation Type Filter
    if 'Violation_Type' in df.columns:
        all_violations = sorted(df['Violation_Type'].unique().tolist())
        selected_violations = st.sidebar.multiselect("Select Violation Type", all_violations, default=all_violations)
        if selected_violations:
            df = df[df['Violation_Type'].isin(selected_violations)]

    return df
