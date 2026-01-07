import streamlit as st
import plotly.express as px

def show(df):
    st.title("🚗 Vehicle Risk Analysis")

    
    # --- Interactive Filter ---
    with st.expander("Filter Options", expanded=True):
        st.markdown("### Vehicle Analysis Options")
        vehicle_types = df['Vehicle_Type'].dropna().unique().tolist()
        selected_vehicles = st.multiselect("Select Vehicle Types", vehicle_types, default=vehicle_types[:5])
    
    filtered_df = df[df['Vehicle_Type'].isin(selected_vehicles)] if selected_vehicles else df
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vehicle Risk Hierarchy")
        # TreeMap: Vehicle Type -> Color 
        if not filtered_df.empty:
            count_data = filtered_df.groupby(['Vehicle_Type', 'Vehicle_Color']).size().reset_index(name='Count')
            fig_tree = px.treemap(count_data, path=['Vehicle_Type', 'Vehicle_Color'], values='Count',
                                  title="Risk by Vehicle Composition")
            st.plotly_chart(fig_tree, use_container_width=True)
        
    with col2:
        st.subheader("Fine Distribution by Vehicle")
        # Violin Plot
        fig_violin = px.violin(filtered_df, y="Fine_Amount", x="Vehicle_Type", box=True, points=False,
                               color="Vehicle_Type", title="Fine Spread per Vehicle")
        st.plotly_chart(fig_violin, use_container_width=True)

    st.subheader("Vehicle Details Drill-down")
    st.dataframe(filtered_df[['Vehicle_Type', 'Vehicle_Color', 'Vehicle_Model_Year', 'Violation_Type', 'Fine_Amount']].head(100))
