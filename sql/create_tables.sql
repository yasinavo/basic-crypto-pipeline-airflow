CREATE TABLE IF NOT EXISTS crypto_prices (
    timestamp TIMESTAMP,
    coin_id TEXT,
    symbol TEXT,
    price_usd NUMERIC(12, 2),
    market_cap NUMERIC(18, 2),
    volume_24h NUMERIC(18, 2)
);