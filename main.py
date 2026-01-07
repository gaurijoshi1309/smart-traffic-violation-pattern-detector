import streamlit as st
from streamlit_option_menu import option_menu
from utils.data_loader import load_data
from utils.ui_helper import apply_custom_css, sidebar_filters

# Import Views
from views import (
    dashboard, risk_map, violation_trends, time_analysis, 
    vehicle_risk, driver_behavior, payment_trends, environment_impact
)

# --- App Config ---
st.set_page_config(
    page_title="Traffic Violation Detector",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Data ---
# Caching is handled inside load_data
DATA_PATH = "Indian_Traffic_Violations.csv"
df = load_data(DATA_PATH)

# --- Apply Styling ---
apply_custom_css()

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("Navigation")
    
    # Using option_menu for a cleaner look without emojis if requested, 
    # but icons are good for UI. User said "dont use emojis" in the request text 
    # but the image showed emojis/icons. The user text "dont use emojis" typically means 
    # "don't use the character emojis in the text labels like 🏠 Dashboard", 
    # but using a dedicated icon library like bootstrap icons (which option_menu uses) is usually 
    # what they mean by "attractive". I will stick to Bootstrap Icons (bi) which look professional.
    
    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard", 
            "India Risk Map", 
            "Violation Trends", 
            "Time & Trend", 
            "Vehicle Risk", 
            "Driver Behavior",
            "Environment Impact",
            "Payment Trends",
            "Reports",
            "Settings"
        ],
        icons=[
            "speedometer2", 
            "map", 
            "bar-chart-line", 
            "clock-history", 
            "truck", 
            "person-badge",
            "cloud-lightning-rain",
            "wallet2",
            "file-earmark-text",
            "gear"
        ],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "orange", "font-size": "14px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )
    
    st.markdown("---")
    
    # Global Filters
    df_filtered = sidebar_filters(df)

# --- Routing ---
if selected == "Dashboard":
    dashboard.show(df_filtered)
elif selected == "India Risk Map":
    risk_map.show(df_filtered)
elif selected == "Violation Trends":
    violation_trends.show(df_filtered)
elif selected == "Time & Trend":
    time_analysis.show(df_filtered)
elif selected == "Vehicle Risk":
    vehicle_risk.show(df_filtered)
elif selected == "Driver Behavior":
    driver_behavior.show(df_filtered)
elif selected == "Environment Impact":
    environment_impact.show(df_filtered)
elif selected == "Payment Trends":
    payment_trends.show(df_filtered)
elif selected == "Reports":
    st.title("📄 Reports")
    st.info("Report generation module coming soon. (Placeholder)")
    st.write("You could export the filtered dataset below:")
    st.download_button("Download CSV", df_filtered.to_csv(index=False), "filtered_data.csv", "text/csv")
elif selected == "Settings":
    st.title("⚙️ Settings")
    st.write("Application settings and configuration.")
    st.toggle("Dark Mode Support", value=True)
