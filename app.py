import streamlit as st
from data_loader import load_data_from_mongodb
from data_visualisation.data_preprocessor import preprocess_data
from data_visualisation.quick_statistics import display_quick_statistics
from data_visualisation.temporal_trends import display_temporal_trends
from data_visualisation.monthly_statistics import display_monthly_statistics

from data_visualisation.display_monthly_statistics_fast import display_combined_tables

from data_visualisation.kpi_section import display_kpi_section
from data_visualisation.global_distribution import display_global_distribution
from data_visualisation.demographic_insights import display_demographic_insights
from data_visualisation.member_birthdays import display_birthdays
from data_visualisation.top_spenders import display_top_spenders
from data_visualisation.membership_retention import display_retention_rate
from data_visualisation.membership_spending import display_membership_spending
from data_visualisation.transactions_scatter_plot import display_transaction_scatter
from data_visualisation.transactions_line_graph import display_transaction_trends
from data_visualisation.chatbot import chatbot

# Custom CSS for sidebar styling
def inject_custom_css():
    st.markdown(
        """
        <style>
            /* Make sidebar narrower */
            section[data-testid="stSidebar"] {
                width: 220px !important;
            }
            
            /* Sidebar logo sizing */
            .sidebar .sidebar-content .stImage img {
                width: 80px !important;
                margin: 0 auto 20px auto;
                display: block;
            }
            
            /* Navigation container */
            div[role="radiogroup"] {
                gap: 8px !important;
                padding: 0 !important;
            }
            
            /* Equal-sized outline buttons */
            div[role="radiogroup"] > label {
                font-size: 14px !important;
                padding: 10px 15px !important;
                margin: 0 0 6px 0 !important;
                border-radius: 6px !important;
                border: 1.5px solid #BED739 !important;
                background-color: transparent !important;
                color: #BED739 !important;
                transition: all 0.2s ease !important;
                width: 100% !important;
                text-align: center !important;
                box-sizing: border-box !important;
                min-height: 40px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            
            /* Selected item - outline only */
            div[role="radiogroup"] > label[data-baseweb="radio"] {
                background-color: transparent !important;
                color: #BED739 !important;
                border: 1.5px solid #BED739 !important;
                font-weight: 600 !important;
            }
            
            /* Hover effects - fill with color */
            div[role="radiogroup"] > label:hover {
                background-color: #BED739 !important;
                color: white !important;
            }
            
            /* Selected item hover */
            div[role="radiogroup"] > label[data-baseweb="radio"]:hover {
                background-color: #BED739 !important;
                color: white !important;
            }
            
            /* Hide radio button circles */
            div[role="radiogroup"] > label > div:first-child {
                display: none !important;
            }
            
            /* Center button text */
            div[role="radiogroup"] > label > div:nth-child(2) {
                width: 100% !important;
                padding-left: 0 !important;
                justify-content: center !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Cache data loading and preprocessing
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_all_data():
    raw_clients, raw_memberships, raw_transactions = load_data_from_mongodb()
    return preprocess_data(raw_clients, raw_memberships, raw_transactions)

def main():
    # Set page config
    st.set_page_config(
        layout="wide",
        page_icon="assets/logo.png",
        page_title="Customer Data Platform"
    )
    
    # INJECT THE CSS - THIS WAS MISSING IN YOUR CODE
    inject_custom_css()

    # Load all data (cached)
    clients, memberships, transactions, merged_data = load_all_data()
    
# Sidebar navigation with improved styling
    with st.sidebar:
        # Smaller logo with centered alignment
        st.image("assets/logo.png", width=80)  # Adjust width as needed
        
        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation with larger text
        page = st.radio(
            "NAVIGATION",
            [
                "📊 Overview",
                "🌍 Geographic",
                "👥 Demographic",
                "💳 Membership",
                "💸 Transaction",
                "🤖 Chatbot"
            ],
            # Add index to maintain selection state
            index=0,
            # Custom label styling
            label_visibility="collapsed"
        )
        
        # Optional: Add some space at the bottom
        st.markdown("<br><br>", unsafe_allow_html=True)

    # Rest of your app code remains the same...
    # Header with logo
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("assets/long_logo.png", use_container_width=True)
    with col2:
        st.title("Customer Data Platform")


    # Create containers for all pages (initially hidden)
    overview = st.container()
    geographic = st.container()
    demographic = st.container()
    membership = st.container()
    transactions_page = st.container()
    chatbot_page = st.container()

    # Render all pages but only show the selected one
    with overview:
        if page == "📊 Overview":
            st.header("Overview Dashboard")
            display_quick_statistics(clients, merged_data, transactions)
            display_combined_tables()
            display_kpi_section(clients, memberships)
            display_temporal_trends(clients, memberships)
        else:
            st.empty()  # Hide when not selected

    with geographic:
        if page == "🌍 Geographic":
            st.header("Geographic Analysis")
            display_global_distribution(clients)
        else:
            st.empty()

    with demographic:
        if page == "👥 Demographic":
            st.header("Demographic Insights")
            display_birthdays(clients)
            display_demographic_insights(clients)
        else:
            st.empty()

    with membership:
        if page == "💳 Membership":
            st.header("Membership Analytics")
            display_retention_rate(memberships, merged_data)
            display_membership_spending(memberships, transactions)
        else:
            st.empty()

    with transactions_page:
        if page == "💸 Transaction":
            st.header("Transaction Patterns")
            display_top_spenders(clients, transactions)
            display_transaction_scatter(transactions)
            display_transaction_trends(transactions)
        else:
            st.empty()

    # New Chatbot Page
    with chatbot_page:
        if page == "🤖 Chatbot":
            st.header("AI Assistant")
            chatbot()
        else:
            st.empty()

if __name__ == "__main__":
    main()
