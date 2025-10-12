# Crypto trade library

This project aims to build a **quantative trade library** for cryptocurrency markets, providing functionalities for data fetching, **strategy backtesting**, and strategy quality reporting based on **ccxt** and **backtrader**. The library is designed to be modular and extensible, allowing users to easily add new features or adapt it to their specific needs.

## Project Structure

Cryptotradelib/
├── data_fetcher/               # Data Fetching Module
│   ├── init.py
│   ├── fetch_historical.py     # Fetch historical data (OHLCV, Funding Rate, etc.)
│   └── stream_live.py          # WebSocket live data subscription
├── data_processor/             # Data Processing and Storage Module
│   ├── init.py
│   └── writer.py               # Write data to Parquet and register metadata
│   └── reader.py                # Read data from Parquet
├── indicators/                 # Indicator Calculation Library
│   ├── init.py
│   └── metrics.py              # Calculate fees, slippage, funding rate, basis, etc.
├── reporting/                  # Data Quality Reporting Module
│   ├── init.py
│   └── quality_check.py        # Generate data quality reports
├── strategy/
│   ├── trendance
│   │...                        # Trend-following strategy example
├── scheduler/                  # Task Scheduling
│   └── daily_etl.sh            # Daily incremental ETL task script
├── scripts/                
├── tests/ 
├── config.py                   # Configuration file (API keys, paths, etc.)
└── requirements.txt            # Python dependencies

    
## Installation and Configuration

### Install Dependencies

```bash
pip install -r requirements.txt
Configuration
Fill in your exchange API keys (if needed), the root path for data storage, and other information in the config.py file.

How to Run
Historical Data Fetching
Run the main ETL script directly to backfill historical data:

Bash
python main_etl.py --symbol 'BTC/USDT' --exchange 'binance' --start_date '2023-01-01'
Live Data Subscription
Run the stream_live.py script to subscribe to the real-time data stream:

Bash
python data_fetcher/stream_live.py
Daily Incremental Task
Use cron or another scheduling tool to execute the scheduler/daily_etl.sh script daily at a fixed time to fetch the previous day's incremental data.
```
