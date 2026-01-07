import streamlit as st
import plotly.express as px

def show(df):
    st.title("🧍 Driver Behavior Analysis")

    # --- Interactive Filters ---
    with st.expander("Filter Options", expanded=True):
        st.markdown("### Driver Demographics")
        age_range = st.slider("Select Driver Age Range", 
                                      int(df['Driver_Age'].min()), 
                                      int(df['Driver_Age'].max()), 
                                      (18, 60))
                                      
    filtered_df = df[(df['Driver_Age'] >= age_range[0]) & (df['Driver_Age'] <= age_range[1])]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Age Distribution (Violin)")
        fig_violin = px.violin(filtered_df, x='Driver_Gender', y='Driver_Age', 
                               color='Driver_Gender', box=True, 
                               title="Age Spread by Gender")
        st.plotly_chart(fig_violin, use_container_width=True)

    with col2:
        st.subheader("Gender vs Fine Impact")
        fig_box = px.box(filtered_df, x='Driver_Gender', y='Fine_Amount',
                         title="Who pays more?")
        st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Recidivism (Repeat Offenders)")
    # Assuming 'Previous_Violations' is a count
    repeat_offenders = filtered_df[filtered_df['Previous_Violations'] > 0]
    st.metric("Repeat Offenders in Range", len(repeat_offenders))
    
    if not repeat_offenders.empty:
        fig_rep = px.scatter(repeat_offenders, x='Driver_Age', y='Previous_Violations', 
                             color='Driver_Gender', size='Fine_Amount',
                             title="Repeat Violations vs Age")
        st.plotly_chart(fig_rep, use_container_width=True)
