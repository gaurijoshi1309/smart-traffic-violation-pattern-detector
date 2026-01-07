import streamlit as st
import plotly.express as px
import pandas as pd

def show(df):
    st.title("⏱️ Time & Trend Analysis")

    if df.empty:
        st.write("No data.")
        return

    # --- Interactive Filters for Comparison ---
    with st.expander("Filter Options", expanded=True):
        st.markdown("### Time Analysis Options")
        violation_options = df['Violation_Type'].unique().tolist()
        selected_viols = st.multiselect("Compare Violation Types", violation_options, default=violation_options[:3])
    
    filtered_df = df[df['Violation_Type'].isin(selected_viols)] if selected_viols else df

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Trends (Stacked Area)")
        if 'Month_Num' in filtered_df.columns:
            # Aggregate by Month and Violation Type
            monthly_data = filtered_df.groupby(['Month_Num', 'Month', 'Violation_Type']).size().reset_index(name='Count')
            monthly_data = monthly_data.sort_values('Month_Num')
            
            fig_area = px.area(monthly_data, x='Month', y='Count', color='Violation_Type',
                               title="Volume Evolution Over Time", markers=True)
            st.plotly_chart(fig_area, use_container_width=True)

    with col2:
        st.subheader("Peak Hours (Polar Plot)")
        if 'Hour' in filtered_df.columns:
            hourly_counts = filtered_df.groupby('Hour').size().reset_index(name='Count')
            fig_polar = px.bar_polar(hourly_counts, r='Count', theta='Hour',
                                     template='plotly_dark',
                                     title="24-Hour Violation Clock")
            st.plotly_chart(fig_polar, use_container_width=True)

    # Detailed Heatmap remains useful
    st.subheader("Intensity Heatmap: Day vs Hour")
    if 'Hour' in filtered_df.columns and 'Day_of_Week' in filtered_df.columns:
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        filtered_df['Day_of_Week'] = pd.Categorical(filtered_df['Day_of_Week'], categories=days_order, ordered=True)
        
        heatmap_data = filtered_df.groupby(['Day_of_Week', 'Hour']).size().unstack(fill_value=0)
        fig_heat = px.imshow(heatmap_data, labels=dict(x="Hour", y="Day", color="Violations"),
                             title="When do most violations occur?", aspect="auto")
        st.plotly_chart(fig_heat, use_container_width=True)
