import os
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient

def load_data_from_mongodb():
    """
    Connects to MongoDB Atlas using credentials from the .env file and fetches data from the `key_task` database.
    Returns three DataFrames: clients, memberships, transactions.
    """
    # Load environment variables from the .env file
    load_dotenv()

    # Get MongoDB connection details from environment variables
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    if not MONGO_URI or not DB_NAME:
        raise ValueError("MongoDB URI or Database name not found in the .env file.")

    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]

        # Fetch collections
        clients = pd.DataFrame(list(db.clients.find()))
        memberships = pd.DataFrame(list(db.memberships.find()))
        transactions = pd.DataFrame(list(db.transactions.find()))

        # Close the connection
        client.close()

        return clients, memberships, transactions

    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

