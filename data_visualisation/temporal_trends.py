# data_visualisation/temporal_trends.py

import streamlit as st
import pandas as pd
import plotly.express as px

def display_temporal_trends(clients, memberships):
    """
    Displays a line chart showing the monthly trends of new clients and memberships
    from January 2024 to the end of January 2025.

    Args:
        clients (pd.DataFrame): DataFrame containing client data with a 'date_joined' column.
        memberships (pd.DataFrame): DataFrame containing membership data with a 'start_date' column.
    """
    st.subheader("Temporal Trends (Jan 2024 - Jan 2025)")
    
    # Ensure 'date_joined' and 'start_date' columns are in datetime format
    clients['date_joined'] = pd.to_datetime(clients['date_joined'])
    memberships['start_date'] = pd.to_datetime(memberships['start_date'])
    
    # Define the date range filter
    start_date = pd.to_datetime('2024-01-01')
    end_date = pd.to_datetime('2025-01-31')
    
    # Filter clients and memberships data to the specified date range
    clients_filtered = clients[(clients['date_joined'] >= start_date) & (clients['date_joined'] <= end_date)]
    memberships_filtered = memberships[(memberships['start_date'] >= start_date) & (memberships['start_date'] <= end_date)]
    
    # Group by month and count new clients
    clients_monthly = clients_filtered.resample('ME', on='date_joined').size().reset_index(name='New Clients')
    
    # Group by month and count new memberships
    memberships_monthly = memberships_filtered.resample('ME', on='start_date').size().reset_index(name='New Memberships')
    
    # Merge the two dataframes on the month
    trends_data = pd.merge(
        clients_monthly,
        memberships_monthly,
        left_on='date_joined',
        right_on='start_date',
        how='outer'
    ).fillna(0)
    
    # Rename the merged date column for clarity
    trends_data.rename(columns={'date_joined': 'Month'}, inplace=True)
    
    # Plot the line chart
    fig = px.line(
        trends_data,
        x='Month',
        y=['New Clients', 'New Memberships'],
        title="New Clients/Memberships Over Time (Jan 2024 - Jan 2025)",
        labels={'Month': 'Month', 'value': 'Count'},
        color_discrete_map={
            'New Clients': '#1f77b4',  # Blue for new clients
            'New Memberships': '#ff7f0e'  # Orange for new memberships
        }
    )
    
    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Count",
        legend_title="Metric",
        hovermode="x unified"
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)