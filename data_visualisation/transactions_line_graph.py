import streamlit as st
import pandas as pd
import plotly.express as px

def display_transaction_trends(transactions):
    """
    Displays the Transaction Trends Over Time section of the dashboard.
    
    Parameters:
        transactions (pd.DataFrame): Processed transactions data
    """
    # Section header
    st.markdown("---")
    st.subheader("💰 Total Transaction Amount Over Time")

    # Fixed aggregation period (Daily)
    aggregation_period = 'Daily'

    # Aggregate transactions based on the fixed period
    transactions['period'] = transactions['date'].dt.date

    # Group by period and calculate total amount
    period_totals = transactions.groupby('period')['amount'].sum().reset_index()
    period_totals.columns = ['period', 'total_amount']

    # Create line graph
    fig = px.line(period_totals, 
                  x='period', 
                  y='total_amount', 
                  title=f'Total Transaction Amount ({aggregation_period})',
                  labels={'period': 'Date', 'total_amount': 'Total Amount ($)'},
                  line_shape='linear',
                  color_discrete_sequence=['#BED739'])  # Use #BED739 as the line color

    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Amount ($)",
        hovermode='x unified',
        showlegend=False
    )

    # Add range slider for better date navigation


    # Display the graph
    st.plotly_chart(fig, use_container_width=True)

    # Optional: Add insights or explanations
    st.caption(
        f"""
        This line graph shows the {aggregation_period.lower()} total transaction amounts over time.
        Use the range slider to zoom in on specific time periods and identify trends in transaction volumes.
        """
    )