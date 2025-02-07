CREATE TABLE IF NOT EXISTS crypto_prices (
    coin_id VARCHAR(255) NOT NULL,                    
    symbol VARCHAR(10) NOT NULL,                      
    price_usd NUMERIC(15, 6),                         
    market_cap NUMERIC(20, 2),                        
    volume_24h NUMERIC(20, 2),   
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,                      
    PRIMARY KEY (coin_id, timestamp)                
);

CREATE TABLE coins (
    id SERIAL PRIMARY KEY,                 
    coin_id VARCHAR(255) NOT NULL,          
    name VARCHAR(255) NOT NULL,             
    symbol VARCHAR(10) NOT NULL,                     
    is_active int,                     
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);