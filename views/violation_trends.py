import streamlit as st
import plotly.express as px
import pandas as pd

def show(df):
    st.title("📊 Violation Trends")
    
    if df.empty:
        st.write("No data available.")
        return

    
    
    # --- Interactive Filters ---
    with st.expander("Filter Options", expanded=True):
        st.markdown("### Violation Trends Options")
        min_fine = st.slider("Minimum Fine Amount", 
                                     min_value=int(df['Fine_Amount'].min()), 
                                     max_value=int(df['Fine_Amount'].max()), 
                                     value=0, step=100)
    
    filtered_df = df[df['Fine_Amount'] >= min_fine]
    
    col1, col2 = st.columns(2)

    with col1:
        # Sunburst Chart: Violation Type -> Vehicle Type
        st.subheader("Violation Hierarchy")
        if not filtered_df.empty:
            fig_sun = px.sunburst(filtered_df, path=['Violation_Type', 'Vehicle_Type'], 
                                  values='Fine_Amount', color='Violation_Type',
                                  title="Violation Type > Vehicle Type Distribution")
            st.plotly_chart(fig_sun, use_container_width=True)
        else:
            st.info("No data for current filter.")

    with col2:
        # Scatter Plot: Fine Amount vs Speed
        st.subheader("Fine Amount vs Speed")
        if not filtered_df.empty and 'Recorded_Speed' in filtered_df.columns:
            fig_scatter = px.scatter(filtered_df, x='Recorded_Speed', y='Fine_Amount',
                                     color='Violation_Type', size='Fine_Amount',
                                     hover_data=['Location'],
                                     title="Correlation: Speed vs Fine")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Insufficient data for scatter plot.")

    # Box Plot remains relevant for distribution analysis
    st.subheader("Fine Amount Distribution (Box Plot)")
    if not filtered_df.empty:
        fig_box = px.box(filtered_df, x='Violation_Type', y='Fine_Amount', color='Violation_Type',
                         title="Fine Variations by Type")
        st.plotly_chart(fig_box, use_container_width=True)
