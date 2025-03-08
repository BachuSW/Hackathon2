import streamlit as st
import pandas as pd
import plotly.express as px

def display_membership_spending(memberships, transactions):
    """
    Displays the Membership Spending Analysis section of the dashboard.
    
    Parameters:
        memberships (pd.DataFrame): Processed memberships data
        transactions (pd.DataFrame): Processed transactions data
    """
    # Section header
    st.markdown("---")
    st.subheader("🏅 Membership Loyalty Program Insights")

    try:
        # Merge transactions and memberships data with safety checks
        required_columns = {'client_id', 'tier', 'amount'}
        
        # Validate data before merging
        if not all(col in memberships.columns for col in ['client_id', 'tier']):
            st.error("Missing required columns in memberships data")
            return
            
        if not all(col in transactions.columns for col in ['client_id', 'amount']):
            st.error("Missing required columns in transactions data")
            return

        merged_data = pd.merge(
            transactions, 
            memberships, 
            on='client_id',
            how='inner',
            validate='m:1'
        )

        # Clean merged data
        merged_data = merged_data.drop(columns=['_id_x', '_id_y'], errors='ignore')
        merged_data = merged_data[merged_data['amount'] > 0]

        # Define the order of tiers
        tier_order = ['No Membership', 'Bronze', 'Silver', 'Gold', 'Platinum']

        # Ensure the 'tier' column is categorical with the specified order
        merged_data['tier'] = pd.Categorical(
            merged_data['tier'], 
            categories=tier_order, 
            ordered=True
        )

        # Create columns for layout
        col1, col2 = st.columns(2)

        # Box Plot: Spending Distribution by Tier
        with col1:
            st.markdown("### Spending Distribution by Tier")
            if not merged_data.empty:
                fig = px.box(merged_data, 
                            x='tier', 
                            y='amount', 
                            color='tier',
                            color_discrete_sequence=['#BED739'],  # Use #BED739 for all tiers
                            labels={'tier': 'Membership Tier', 'amount': 'Amount Spent ($)'},
                            category_orders={'tier': tier_order})

                fig.update_layout(
                    xaxis_title="Membership Tier",
                    yaxis_title="Amount Spent ($)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for box plot")

        # Bar Chart: Average Spending by Tier
        with col2:
            st.markdown("### Average Spending by Tier")
            if not merged_data.empty:
                # Handle FutureWarning for groupby
                avg_spending = merged_data.groupby(
                    'tier', 
                    observed=False  # Explicitly set to handle categorical warning
                )['amount'].mean().reset_index()
                
                fig = px.bar(avg_spending,
                            x='tier',
                            y='amount',
                            color='tier',
                            color_discrete_sequence=['#BED739'],  # Use #BED739 for all tiers
                            labels={'tier': 'Membership Tier', 'amount': 'Average Amount Spent ($)'},
                            text_auto='.2f')

                fig.update_layout(
                    xaxis_title="Membership Tier",
                    yaxis_title="Average Amount Spent ($)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for bar chart")

        # Optional: Add insights or explanations
        st.caption(
            """
            These visualizations show how spending patterns vary across different membership tiers.
            The box plot reveals the distribution of spending, while the bar chart shows average spending per tier.
            Use these insights to understand the spending behavior of different membership levels.
            """
        )

    except Exception as e:
        st.error(f"Error in membership spending section: {str(e)}")
        st.exception(e)