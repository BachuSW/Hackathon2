import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import country_converter as coco

def get_country_name(country_code):
    """
    Get the country name for a given country code.
    
    Parameters:
        country_code (str): The 2-letter country code.
    
    Returns:
        str: The full country name, or 'Unknown' if not found.
    """
    try:
        # Try using pycountry first
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if country:
            return country.name
        else:
            # Fallback to country_converter if pycountry fails
            country_name = coco.convert(names=country_code, to='name_short')
            return country_name if country_name != "not found" else 'Unknown'
    except (KeyError, AttributeError):
        return 'Unknown'

def display_global_distribution(clients):
    """
    Displays the Global Client Distribution section of the dashboard.
    
    Parameters:
        clients (pd.DataFrame): Processed clients data with country codes
    """
    # Section header
    st.markdown("---")
    st.subheader("🌐 Client World Distribution")

    # Count clients by country
    country_counts = clients['country_code'].value_counts().reset_index()
    country_counts.columns = ['country_code', 'count']

    # Map country codes to country names
    country_counts['country_name'] = country_counts['country_code'].apply(get_country_name)

    # Create choropleth map
    fig = px.choropleth(country_counts,
                        locations="country_code",
                        color="count",
                        hover_name="country_name",
                        color_continuous_scale=[ '#BED739', '#4B8D3A'],  # Gradient colors
                        projection="natural earth",
                        height=600)

    # Update layout for better visualization
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(
            showframe=True,
            showcoastlines=True,
            showcountries=True,
            countrycolor="#404040",
            countrywidth=1.5,
            landcolor="white",
            bgcolor="rgba(0,0,0,0)",
            subunitcolor="white"
        ),
        coloraxis_colorbar=dict(
            title="Client Count",
            thickness=20,
            len=0.75
        )
    )

    # Update geographical styling
    fig.update_geos(
        coastlinecolor="#404040",
        coastlinewidth=1.5,
        oceancolor="white",
        lakecolor="white"
    )

    # Create two columns: one for the map and one for the country list
    col1, col2 = st.columns([3, 1])  # Ratio of columns: map takes 3 parts, list takes 1 part

    # Display the map in the first column
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    # Display the country list in the second column
    with col2:
        for idx, row in country_counts.iterrows():
            st.write(f"{row['country_name']}: {row['count']}")

    # Optional: Add insights or explanations
    st.caption(
        """
        This world map shows the geographical distribution of clients. 
        Darker shades indicate higher concentrations of clients in those regions.
        Hover over countries to see exact client counts.
        """
    )

# Example usage
if __name__ == "__main__":
    # Sample data
    data = {
        'country_code': ['US', 'GB', 'CA', 'FR', 'DE', 'IN', 'JP', 'BR', 'AU', 'CN', 'XX']
    }
    clients = pd.DataFrame(data)
    display_global_distribution(clients)