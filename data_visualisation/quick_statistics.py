import streamlit as st
import pandas as pd

def display_quick_statistics(clients, merged_data, transactions):
    """
    Displays the Quick Statistics section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data
        merged_data (pd.DataFrame): Merged clients and memberships data
        transactions (pd.DataFrame): Processed transactions data
    """
    # Section header
    st.markdown("---")
    st.subheader("🚀 Quick Statistics")

    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)

    # Total Clients
    with col1:
        total_clients = clients['client_id'].nunique()
        st.metric(
            label="Total Clients", 
            value=total_clients,
            help="Total number of unique clients in the system"
        )

    # Active Memberships
    with col2:
        active_memberships = merged_data[merged_data['status'] == 'ACTIVE']['membership_id'].nunique()
        st.metric(
            label="Active Memberships", 
            value=active_memberships,
            help="Number of currently active memberships"
        )

    # Total Transactions
    with col3:
        total_transactions = transactions['transaction_id'].nunique()
        st.metric(
            label="Total Transactions", 
            value=total_transactions,
            help="Total number of transactions processed"
        )

    # Total Transaction Amount
    with col4:
        total_amount = transactions['amount'].sum()
        formatted_amount = f"${total_amount:,.2f}"
        st.metric(
            label="Total Transaction Amount", 
            value=formatted_amount,
            help="Cumulative sum of all transaction amounts"
        )

    # Optional: Add a small description below the metrics
    st.caption(
        """
        These quick statistics provide an overview of key business metrics. 
        Hover over each metric for more information.
        """
    )