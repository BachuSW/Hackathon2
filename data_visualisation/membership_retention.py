import streamlit as st
import pandas as pd

def display_retention_rate(memberships, merged_data):
    """
    Displays the Membership Retention Rate section of the dashboard.
    
    Parameters:
        memberships (pd.DataFrame): Processed memberships data
        merged_data (pd.DataFrame): Merged clients and memberships data
    """
    # Section header
    st.markdown("---")
    st.subheader("📊 Membership Retention Rate")

    # Calculate retention metrics
    active_memberships = merged_data[merged_data['status'] == 'ACTIVE']['membership_id'].nunique()
    total_memberships = memberships['membership_id'].nunique()
    retention_rate = (active_memberships / total_memberships) * 100

    # Create columns for metrics
    col1, col2 = st.columns(2)

    # Display retention rate
    with col1:
        st.metric(
            label="Retention Rate", 
            value=f"{retention_rate:.2f}%",
            help="Percentage of memberships that are currently active"
        )

    # Display raw counts
    with col2:
        st.metric(
            label="Active Memberships", 
            value=f"{active_memberships:,}",
            help="Number of currently active memberships"
        )

    # Optional: Add a trend indicator
    # (This would require historical data for comparison)
    # st.metric(
    #     label="Retention Rate Trend", 
    #     value=f"{retention_rate:.2f}%",
    #     delta=f"{trend_value:.2f}% from last period"
    # )

    # Create a retention breakdown by tier
    st.markdown("### Retention by Membership Tier")
    
    # Calculate retention by tier
    retention_by_tier = merged_data.groupby('tier')['status'].apply(
        lambda x: (x == 'ACTIVE').mean() * 100
    ).reset_index()
    retention_by_tier.columns = ['Tier', 'Retention Rate']

    # Display the breakdown
    st.dataframe(
        retention_by_tier,
        column_config={
            "Tier": "Membership Tier",
            "Retention Rate": st.column_config.NumberColumn(
                "Retention Rate (%)",
                format="%.2f%%"
            )
        },
        hide_index=True,
        use_container_width=True
    )

    # Optional: Add insights or explanations
    st.caption(
        """
        The retention rate shows the percentage of memberships that remain active.
        A higher retention rate indicates better customer loyalty and satisfaction.
        The breakdown by tier helps identify which membership levels are performing best.
        """
    )