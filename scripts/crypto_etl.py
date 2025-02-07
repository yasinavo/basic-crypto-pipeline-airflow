import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime , timezone

def extract_coin_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum",
        "order": "market_cap_desc",
        "per_page": 2,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url,params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        raise Exception("Failed to parse JSON response")

    df = pd.DataFrame([{
        "timestamp": datetime.now(timezone.utc),
        "coin_id": coin["id"],
        "symbol": coin["symbol"].upper(),
        "price_usd": coin["current_price"],
        "market_cap": coin["market_cap"],
        "volume_24h": coin["total_volume"]
    } for coin in data])

    return df

def load_to_postgres(df):
    engine = create_engine('postgresql://airflow:airflow@postgres/crypto_data')
    df.to_sql('crypto_prices', engine, if_exists='append', index=False)

if __name__ == "__main__":
    df = extract_coin_data()
    load_to_postgres(df)