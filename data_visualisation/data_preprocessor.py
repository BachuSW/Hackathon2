import pandas as pd
import numpy as np
import pycountry
from datetime import datetime

def preprocess_data(raw_clients, raw_memberships, raw_transactions):
    """
    Preprocesses raw client, membership, and transaction data.
    
    Parameters:
        raw_clients (pd.DataFrame): Raw clients data
        raw_memberships (pd.DataFrame): Raw memberships data
        raw_transactions (pd.DataFrame): Raw transactions data
    
    Returns:
        tuple: Processed clients, memberships, transactions, and merged data
    """
    # Create copies of the input DataFrames to avoid modifying originals
    clients = raw_clients.copy()
    memberships = raw_memberships.copy()
    transactions = raw_transactions.copy()

    # Convert MongoDB ObjectIds to strings (if present)
    for df in [clients, memberships, transactions]:
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)

    # Define date columns for each DataFrame
    date_columns = {
        'clients': ['date_joined', 'birthdate'],
        'memberships': ['start_date', 'end_date'],
        'transactions': ['date']
    }

    # Convert date columns with error handling
    for df_name, cols in date_columns.items():
        df = locals()[df_name]  # Get the DataFrame by name
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')  # Coerce invalid dates to NaT

    # Clean and standardize client_id across all datasets
    for df in [clients, memberships, transactions]:
        if 'client_id' in df.columns:
            df['client_id'] = (
                df['client_id']
                .astype(str)
                .str.replace('[^0-9]', '', regex=True)  # Remove non-numeric characters
                .replace('', '0')  # Replace empty strings with '0'
                .astype(int)  # Convert to integer
            )

    # Check for duplicate client_ids in clients and memberships
    if 'client_id' in clients.columns:
        duplicate_clients = clients.duplicated('client_id', keep=False)
        if duplicate_clients.any():
            print(f"Warning: Found {duplicate_clients.sum()} duplicate client_ids in clients data")

    if 'client_id' in memberships.columns:
        duplicate_memberships = memberships.duplicated('client_id', keep=False)
        if duplicate_memberships.any():
            print(f"Warning: Found {duplicate_memberships.sum()} duplicate client_ids in memberships data")

    # Merge clients and memberships data
    if 'client_id' in clients.columns and 'client_id' in memberships.columns:
        merged_data = pd.merge(
            clients,
            memberships,
            on='client_id',
            how='inner',  # Use inner join to keep only matching records
            validate='many_to_one'  # Allow many clients to one membership
        )
    else:
        merged_data = pd.DataFrame()
        print("Warning: client_id missing in clients or memberships - merge skipped")

    # Add ISO Alpha-3 country codes based on nationality
    if 'nationality' in clients.columns:
        clients['country_code'] = clients['nationality'].apply(get_iso_alpha3)

    # Calculate client ages safely
    if 'birthdate' in clients.columns:
        clients['age'] = (
            (pd.Timestamp.now() - clients['birthdate']).dt.days // 365.25  # Calculate age in years
        ).clip(0, 120)  # Clip ages to a reasonable range
        clients['age'] = clients['age'].fillna(0).astype(int)  # Fill NaNs and convert to integers

    # Filter out invalid transactions
    if 'amount' in transactions.columns:
        transactions = transactions[transactions['amount'] > 0]

    return clients, memberships, transactions, merged_data


def get_iso_alpha3(country_name):
    """
    Converts a country name to its ISO Alpha-3 code using fuzzy matching.
    
    Parameters:
        country_name (str): Name of the country
    
    Returns:
        str: ISO Alpha-3 code or None if not found
    """
    try:
        country = pycountry.countries.search_fuzzy(country_name)
        return country[0].alpha_3 if country else None
    except (LookupError, AttributeError):
        return None