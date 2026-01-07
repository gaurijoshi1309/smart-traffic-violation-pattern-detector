import streamlit as st
import plotly.express as px

def show(df):
    st.title("💳 Payment Trend Analysis")

    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Payment Status Distribution")
        fig_nop = px.pie(df, names='Fine_Paid', title="Percentage of Fines Paid", hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_nop, use_container_width=True)

    with c2:
        st.subheader("Payment Method Preferences")
        # filter only paid
        paid_df = df[df['Fine_Paid'] == 'Yes']
        if not paid_df.empty:
            fig_meth = px.bar(paid_df['Payment_Method'].value_counts(), orientation='h', 
                              title="Preferred Payment Methods",
                              color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig_meth, use_container_width=True)
        else:
            st.info("No payment data available.")
            
    st.subheader("Payment Analysis by Violation Type")
    # Stacked Bar: Violation Type -> Paid vs Unpaid
    payment_breakdown = df.groupby(['Violation_Type', 'Fine_Paid']).size().reset_index(name='Count')
    fig_stack = px.bar(payment_breakdown, x='Violation_Type', y='Count', color='Fine_Paid',
                       title="Who pays their fines?", barmode='stack')
    st.plotly_chart(fig_stack, use_container_width=True)
