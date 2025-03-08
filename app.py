import streamlit as st
from data_loader import load_data_from_mongodb
from data_visualisation.data_preprocessor import preprocess_data
from data_visualisation.quick_statistics import display_quick_statistics
from data_visualisation.temporal_trends import display_temporal_trends  # Import the new function
from data_visualisation.monthly_statistics import display_monthly_statistics
from data_visualisation.kpi_section import display_kpi_section
from data_visualisation.global_distribution import display_global_distribution
from data_visualisation.demographic_insights import display_demographic_insights
from data_visualisation.member_birthdays import display_birthdays
from data_visualisation.top_spenders import display_top_spenders
from data_visualisation.membership_retention import display_retention_rate
from data_visualisation.membership_spending import display_membership_spending
from data_visualisation.transactions_scatter_plot import display_transaction_scatter
from data_visualisation.transactions_line_graph import display_transaction_trends

def main():
    # Set page config with favicon
    st.set_page_config(
        layout="wide",
        page_icon="assets/logo.png",
        page_title="Customer Data Platform"
    )
    
    # Header with logo
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("assets/long_logo.png", use_container_width=True)
    with col2:
        st.title("Customer Data Platform")

    # Load and preprocess data
    raw_clients, raw_memberships, raw_transactions = load_data_from_mongodb()
    clients, memberships, transactions, merged_data = preprocess_data(
        raw_clients, raw_memberships, raw_transactions
    )

    # Dashboard sections
    display_quick_statistics(clients, merged_data, transactions)
    display_temporal_trends(clients, memberships)  # Add the new line graph here
    display_monthly_statistics(clients, memberships, merged_data)
    display_kpi_section(clients, memberships)
    display_global_distribution(clients)
    display_demographic_insights(clients)
    display_birthdays(clients)
    display_top_spenders(clients, transactions)
    display_retention_rate(memberships, merged_data)
    display_membership_spending(memberships, transactions)
    display_transaction_scatter(transactions)
    display_transaction_trends(transactions)

if __name__ == "__main__":
    main()