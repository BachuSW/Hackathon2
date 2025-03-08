import streamlit as st
import pandas as pd
import plotly.express as px

def display_demographic_insights(clients):
    """
    Displays the Demographic Insights section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data with age information
    """
    # Section header
    st.markdown("---")
    st.subheader("📈 Demographic Insights")

    # Create columns for layout
    col1, col2 = st.columns([2, 1])

    # Age Group Distribution Histogram
    with col1:
        # Define age groups
        age_groups = pd.cut(clients['age'], 
                          bins=[0, 18, 25, 35, 45, 55, 65, 100],
                          labels=['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+'])

        # Ensure age groups are sorted
        age_groups = pd.Categorical(age_groups, categories=[
            '0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+'
        ], ordered=True)

        # Create histogram
        fig = px.histogram(x=age_groups, 
                          title="Age Group Distribution",
                          color_discrete_sequence=['#BED739'],  # Use #BED739 as the main color
                          category_orders={'x': [
                              '0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+'
                          ]})

        # Update layout
        fig.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Count",
            xaxis={'categoryorder': 'array', 'categoryarray': [
                '0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+'
            ]}
        )

        st.plotly_chart(fig, use_container_width=True)

    # Age Statistics
    with col2:
        st.markdown("### Age Statistics")
        
        # Calculate basic statistics
        avg_age = clients['age'].mean()
        median_age = clients['age'].median()
        youngest = clients['age'].min()
        oldest = clients['age'].max()

        # Display metrics
        st.metric("Average Age", f"{avg_age:.1f} years")
        st.metric("Median Age", f"{median_age:.1f} years")
        st.metric("Youngest Client", f"{youngest} years")
        st.metric("Oldest Client", f"{oldest} years")

    # Optional: Add insights or explanations
    st.caption(
        """
        Demographic insights provide valuable information about the age distribution of clients.
        The histogram shows the distribution across age groups, while the statistics provide
        key metrics about the client base.
        """
    )