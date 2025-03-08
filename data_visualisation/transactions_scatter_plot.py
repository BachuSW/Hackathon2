import streamlit as st
import pandas as pd
import plotly.express as px

def display_transaction_scatter(transactions):
    """
    Displays the Transaction Scatter Plot section of the dashboard.
    
    Parameters:
        transactions (pd.DataFrame): Processed transactions data
    """
    # Section header
    st.markdown("---")
    st.subheader("📊 Transaction Scatter Plot")

    # Add time frame selector
    col_start, col_end = st.columns(2)

    with col_start:
        start_date = st.date_input(
            "Start Date for Scatter Plot", 
            value=pd.Timestamp.now() - pd.Timedelta(days=365),
            help="Select the start date for the scatter plot"
        )

    with col_end:
        end_date = st.date_input(
            "End Date for Scatter Plot", 
            value=pd.Timestamp.now(),
            help="Select the end date for the scatter plot"
        )

    # Filter transactions within the selected time frame
    filtered_transactions = transactions[
        (transactions['date'] >= pd.Timestamp(start_date)) &
        (transactions['date'] <= pd.Timestamp(end_date))
    ]

    # Create scatter plot
    fig = px.scatter(filtered_transactions, 
                     x='date', 
                     y='amount', 
                     title='Transaction Scatter Plot',
                     labels={'date': 'Date', 'amount': 'Amount ($)'},
                     color='amount',
                     color_continuous_scale=['#BED739', '#2E8B57'],  # Custom color scale with #BED739
                     hover_data=['transaction_id', 'client_id'])

    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        coloraxis_colorbar=dict(title="Amount ($)"),
        hovermode='x unified'
    )

    # Add range slider for better date navigation
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Optional: Add insights or explanations
    st.caption(
        """
        This scatter plot shows individual transactions over time. 
        The color intensity represents the transaction amount, with darker colors indicating higher amounts.
        Use the range slider to zoom in on specific time periods.
        """
    )