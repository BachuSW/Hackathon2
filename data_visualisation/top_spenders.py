import streamlit as st
import pandas as pd

def display_top_spenders(clients, transactions):
    """
    Displays the Top 5 Spenders section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data
        transactions (pd.DataFrame): Processed transactions data
    """
    # Section header
    st.markdown("---")
    st.subheader("🏆 Top 5 Spenders")

    # Add time frame selector
    col_start, col_end = st.columns(2)

    with col_start:
        start_date = st.date_input(
            "Start Date", 
            value=pd.Timestamp.now() - pd.Timedelta(days=365),
            help="Select the start date for the analysis period"
        )

    with col_end:
        end_date = st.date_input(
            "End Date", 
            value=pd.Timestamp.now(),
            help="Select the end date for the analysis period"
        )

    # Filter transactions within the selected time frame
    filtered_transactions = transactions[
        (transactions['date'] >= pd.Timestamp(start_date)) &
        (transactions['date'] <= pd.Timestamp(end_date))
    ]

    # Calculate total spending per client
    total_spent = filtered_transactions.groupby('client_id')['amount'].sum().reset_index()

    # Merge with clients to get names
    top_spenders = pd.merge(total_spent, clients, on='client_id').nlargest(5, 'amount')

    # Display the list
    st.dataframe(
        top_spenders[['client_id', 'name', 'amount']],
        column_config={
            "client_id": "Client ID",
            "name": "Client Name",
            "amount": st.column_config.NumberColumn(
                "Total Spent ($)",
                format="$%.2f"
            )
        },
        hide_index=True,
        use_container_width=True
    )

    # Optional: Add insights or explanations
    st.caption(
        """
        This list shows the top 5 clients by total spending within the selected time period.
        Use the date selectors to analyze different time frames and identify your most valuable clients.
        """
    )