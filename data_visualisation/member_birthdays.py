import streamlit as st
import pandas as pd
from datetime import datetime

def display_birthdays(clients):
    """
    Displays the Upcoming Member Birthdays section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data with birthdate information
    """
    # Section header
    st.markdown("---")
    st.subheader("🎂 Upcoming Member Birthdays")

    # Calculate days until next birthday
    def days_until_birthday(birthdate):
        today = pd.Timestamp.now().normalize()
        next_birthday = birthdate.replace(year=today.year)
        
        # If birthday has already passed this year, set it to next year
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        
        return (next_birthday - today).days

    # Add days until next birthday to clients
    clients['days_until_birthday'] = clients['birthdate'].apply(days_until_birthday)

    # Sort by days until birthday (ascending)
    upcoming_birthdays = clients.sort_values(by='days_until_birthday')

    # Highlight rows where birthday is today
    def highlight_birthday_today(row):
        today = pd.Timestamp.now().normalize()
        birthday = row['birthdate'].replace(year=today.year)
        
        if birthday == today:
            return ['background-color: #FFD700; color: black'] * len(row)  # Gold background with black font
        else:
            return [''] * len(row)

    # Apply highlighting
    highlighted_birthdays = upcoming_birthdays.style.apply(highlight_birthday_today, axis=1)

    # Display the list
    st.dataframe(
        highlighted_birthdays,
        column_config={
            "client_id": "Client ID",
            "name": "Name",
            "birthdate": "Birthdate",
            "days_until_birthday": "Days Until Birthday"
        },
        hide_index=True,
        use_container_width=True
    )

    # Optional: Add insights or explanations
    st.caption(
        """
        This list shows upcoming client birthdays, sorted by how soon they occur.
        Birthdays happening today are highlighted in gold. Use this information
        for personalized marketing or client engagement opportunities.
        """
    )