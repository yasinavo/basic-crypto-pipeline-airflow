CREATE DATABASE airflow;
CREATE DATABASE crypto_data;

-- Grant permissions to the airflow user
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
GRANT ALL PRIVILEGES ON DATABASE crypto_data TO airflow;