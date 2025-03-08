import streamlit as st
import pandas as pd

def display_monthly_statistics(clients, memberships, merged_data):
    """
    Displays the Monthly Statistics section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data
        memberships (pd.DataFrame): Processed memberships data
        merged_data (pd.DataFrame): Merged clients and memberships data
    """
    # Section header
    st.markdown("---")
    st.subheader("📅 Monthly Statistics")

    # Month names for display
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Create columns for selectors
    col_month, col_year = st.columns(2)

    # Month selector
    with col_month:
        selected_month = st.selectbox(
            "Select Month",
            options=range(1, 13),  # Values: 1-12
            format_func=lambda x: month_names[x - 1],  # Display month names
            index=9  # Default to October (index 9)
        )

    # Year selector
    with col_year:
        selected_year = st.selectbox(
            "Select Year",
            options=range(2020, 2026),  # Values: 2020-2025
            index=4  # Default to 2024 (index 4)
        )

    # Format selected month and year for display
    selected_month_year = f"{month_names[selected_month - 1]} {selected_year}"

    # Create columns for metrics
    col1, col2 = st.columns(2)

    # Filter and display signups
    with col1:
        filtered_clients = clients[
            (clients['date_joined'].dt.year == selected_year) & 
            (clients['date_joined'].dt.month == selected_month)
        ]
        st.metric(
            label=f"Signups in {selected_month_year}", 
            value=len(filtered_clients),
            help="Number of new client signups in the selected month"
        )

    # Filter and display memberships
    with col2:
        filtered_memberships = memberships[
            (memberships['start_date'].dt.year == selected_year) & 
            (memberships['start_date'].dt.month == selected_month)
        ]
        st.metric(
            label=f"Memberships in {selected_month_year}", 
            value=len(filtered_memberships),
            help="Number of new memberships started in the selected month"
        )

    # Optional: Add a small description below the metrics
    st.caption(
        """
        Monthly statistics show trends in client acquisition and membership growth. 
        Use the selectors to view data for specific months.
        """
    )