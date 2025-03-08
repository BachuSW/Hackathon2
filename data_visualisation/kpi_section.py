import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def display_kpi_section(clients, memberships):
    """
    Displays the KPI (Key Performance Indicators) section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data
        memberships (pd.DataFrame): Processed memberships data
    """
    # Section header
    st.markdown("---")
    st.subheader("📊 Key Performance Indicators")

    # Create columns for visualizations
    col1, col2 = st.columns(2)

    # Membership Distribution Pie Chart
    with col1:
        # Merge clients with memberships
        membership_status = clients.merge(
            memberships[['client_id', 'tier']].drop_duplicates(subset='client_id'),
            on='client_id',
            how='left'
        )
        
        # Create membership classification
        membership_status['membership_status'] = np.where(
            membership_status['tier'] == 'No Membership',
            'No Membership',
            'Has Membership'
        )
        
        # Create pie chart
        fig = px.pie(membership_status, 
                     names='membership_status', 
                     title='Membership Distribution',
                     hole=0.4,
                     color='membership_status',
                     color_discrete_map={
                         'Has Membership': '#BED739',  # Updated to use #BED739
                         'No Membership': '#ffffff'   # Keep the contrast color
                     })
        
        # Format labels and tooltips
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Count: %{value}</br>Percentage: %{percent}"
        )
        
        fig.update_layout(
            showlegend=True,
            margin=dict(l=20, r=20, t=40, b=20),
            uniformtext_minsize=12
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Membership Tier Distribution Bar Chart
    with col2:
        # Count membership tiers
        tier_counts = memberships['tier'].value_counts()

        # Define colors for each tier
        tier_colors = {
            'No Membership': '#BED739',  # Beige
            'Bronze': '#BED739',         # Bronze
            'Silver': '#BED739',         # Silver
            'Gold': '#BED739',           # Updated to use #BED739
            'Platinum': '#BED739'        # Platinum
        }

        # Create bar chart
        fig = px.bar(tier_counts, 
                     orientation='v', 
                     title='Membership Tier Distribution',
                     labels={'index':'Tier', 'value':'Count'},
                     color=tier_counts.index,
                     color_discrete_map=tier_colors,
                     text_auto=True)

        fig.update_layout(
            showlegend=False, 
            xaxis_title=None, 
            yaxis_title=None
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Optional: Add insights or explanations
    st.caption(
        """
        Key Performance Indicators provide insights into membership trends and distributions. 
        The pie chart shows the proportion of clients with active memberships, while the bar 
        chart breaks down membership tiers.
        """
    )