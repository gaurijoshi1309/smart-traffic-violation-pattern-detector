import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def show(df):
    # --- Title Section (Above Image) ---
    st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🚦 SMART TRAFFIC DETECTOR 🚦</h1>", unsafe_allow_html=True)

    # --- Custom Banner Image ---
    try:
        bin_str = get_base64_of_bin_file("assets/banner.png")
        st.markdown(
            f"""
            <style>
            .banner-container {{
                width: 100%;
                height: 300px; /* LinkedIn Flyer approx height */
                overflow: hidden;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                margin-bottom: 30px;
                display: flex;
                justify_content: center;
                align_items: center;
            }}
            .banner-img {{
                width: 100%;
                height: 100%;
                object-fit: cover; /* This "crops" the image to fill the rectangle */
                object-position: center;
            }}
            </style>
            <div class="banner-container">
                <img class="banner-img" src="data:image/png;base64,{bin_str}">
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Could not load banner: {e}")
        
    # --- Top KPIs ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_violations = len(df)
        st.metric("Total Violations", f"{total_violations:,}")

    with col2:
        total_fines = df['Fine_Amount'].sum()
        st.metric("Total Fines Collected", f"₹{total_fines:,.0f}")

    with col3:
        # Use simple Numpy calculation for avg and std dev
        if not df.empty:
            fine_array = df['Fine_Amount'].to_numpy()
            avg_fine = np.mean(fine_array)
            std_fine = np.std(fine_array)
        else:
            avg_fine = 0
            std_fine = 0
            
        st.metric("Avg Fine Amount", f"₹{avg_fine:,.0f}", delta=f"±₹{std_fine:.0f} SD")
        
    with col4:
        # Most common violation
        if not df.empty:
            top_violation = df['Violation_Type'].mode()[0]
        else:
            top_violation = "N/A"
        st.metric("Top Violation", top_violation)

    st.markdown("---")

    # --- Basic Graphs (Simple Streamlit Charts) ---
    st.subheader("General Statistics (Basic Charts)")
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        st.write("**Top 5 Violations (Simple Bar)**")
        if not df.empty:
            # Preparing data for st.bar_chart
            top_5 = df['Violation_Type'].value_counts().head(5)
            st.bar_chart(top_5)
            
    with b_col2:
        st.write("**Violation Counts by State**")
        if not df.empty and 'Location' in df.columns:
            state_counts = df['Location'].value_counts().reset_index()
            state_counts.columns = ['State', 'Count']
            
            # Using Plotly to assign different colors to each state
            fig_state = px.bar(state_counts, x='State', y='Count', color='State',
                               title="Violations by State", template="plotly_dark")
            fig_state.update_layout(showlegend=False)
            st.plotly_chart(fig_state, use_container_width=True)

    st.markdown("---")

    # --- Recent Trends (Sparkline style) ---
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("Violation Distribution")
        if not df.empty:
            viol_counts = df['Violation_Type'].value_counts().reset_index()
            viol_counts.columns = ['Violation Type', 'Count']
            fig_viol = px.bar(viol_counts, x='Count', y='Violation Type', orientation='h',
                              color='Count', color_continuous_scale='Viridis',
                              title="Violations by Type")
            st.plotly_chart(fig_viol, use_container_width=True)
            
    with col_graph2:
        st.subheader("Violations & Fines Over Time")
        if not df.empty and 'Datetime' in df.columns:
            # Group by date for a time series
            daily_stats = df.groupby(df['Datetime'].dt.date).agg(
                Violations=('Violation_ID', 'count'),
                Daily_Fines=('Fine_Amount', 'sum')
            ).reset_index()
            daily_stats['Cumulative_Fines'] = daily_stats['Daily_Fines'].cumsum()
            
            # Interactive Area Chart with Range Slider
            fig_trend = px.area(daily_stats, x='Datetime', y='Violations',
                                title="Daily Violation Volume (Interactive)",
                                template="plotly_dark",
                                markers=True)
            fig_trend.update_xaxes(rangeslider_visible=True)
            # Force legend to show "Total Violations"
            fig_trend.update_traces(name="Daily Violations", showlegend=True)
            st.plotly_chart(fig_trend, use_container_width=True)

    # --- Insightful Quick Stats & Advanced Graph ---
    st.markdown("---")
    st.subheader("💡 Deep Insights")
    
    i_col1, i_col2 = st.columns([1, 2])
    
    with i_col1:
        st.markdown("### Key Metrics")
        if not df.empty:
            # Top State
            top_state = df['Location'].mode()[0]
            st.info(f"**Highest Violation State**: {top_state}")

            # Max Fine
            max_fine_row = df.loc[df['Fine_Amount'].idxmax()]
            st.warning(f"**Highest Single Fine**: ₹{max_fine_row['Fine_Amount']:,} ({max_fine_row['Violation_Type']})")

            # Payment Rate
            paid_count = df[df['Fine_Paid'] == 'Yes'].shape[0]
            total_violations = len(df)
            payment_rate = (paid_count / total_violations) * 100
            st.success(f"**Fine Payment Rate**: {payment_rate:.1f}%")

    with i_col2:
        st.markdown("### Cumulative Revenue Impact")
        if not df.empty and 'Datetime' in df.columns:
            # Cumulative Fines Line Chart
            fig_rev = px.line(daily_stats, x='Datetime', y='Cumulative_Fines',
                              title="Cumulative Fines Collected (Financial Growth)",
                              template="plotly_dark",
                              line_shape='spline')
            fig_rev.update_traces(fill='tozeroy', line_color='#00CC96', name="Total Collected", showlegend=True)
            st.plotly_chart(fig_rev, use_container_width=True)

