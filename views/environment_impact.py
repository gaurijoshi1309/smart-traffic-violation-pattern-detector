import streamlit as st
import plotly.express as px

def show(df):
    st.title("🌨️ Environment Impact Analysis")
    st.write("Analyzing how weather and road conditions correlate with violations.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Violations by Weather")
        fig_w = px.histogram(df, x='Weather_Condition', color='Weather_Condition', 
                             title="Impact of Weather")
        st.plotly_chart(fig_w, use_container_width=True)
        
    with col2:
        st.subheader("Violations by Road Condition")
        fig_r = px.histogram(df, x='Road_Condition', color='Road_Condition',
                             title="Impact of Road Conditions")
        st.plotly_chart(fig_r, use_container_width=True)
