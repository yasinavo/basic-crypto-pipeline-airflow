import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timezone

# Function to fetch coin IDs from the database
def get_coin_ids_from_db():
    # Connect to the database to fetch coin IDs
    engine = create_engine('postgresql://airflow:airflow@postgres/crypto_data')
    query = "SELECT coin_id FROM coins WHERE is_active = 1"  # Replace with your actual table and column names
    df = pd.read_sql(query, engine)
    
    # Extract the list of coin IDs from the dataframe
    return df['coin_id'].tolist()

# Function to extract coin data
def extract_coin_data():
    # Get coin IDs from the database
    coin_ids = get_coin_ids_from_db()
    
    # Prepare the API request
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(coin_ids),  # Join coin IDs dynamically
        "order": "market_cap_desc",
        "per_page": len(coin_ids),
        "page": 1,
        "sparkline": "false"
    }
    
    # Send the API request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        raise Exception("Failed to parse JSON response")

    # Prepare the DataFrame
    df = pd.DataFrame([{
        "timestamp": datetime.now(timezone.utc),
        "coin_id": coin["id"],
        "symbol": coin["symbol"].upper(),
        "price_usd": coin["current_price"],
        "market_cap": coin["market_cap"],
        "volume_24h": coin["total_volume"]
    } for coin in data])

    return df

# Function to load data into PostgreSQL
def load_to_postgres(df):
    # Connect to the PostgreSQL database and load data
    engine = create_engine('postgresql://airflow:airflow@postgres/crypto_data')
    df.to_sql('crypto_prices', engine, if_exists='append', index=False)

# Main execution block
if __name__ == "__main__":
    # Fetch the coin data
    df = extract_coin_data()  # Fetch data dynamically based on the coin IDs
    
    # Load data into PostgreSQL
    load_to_postgres(df)
