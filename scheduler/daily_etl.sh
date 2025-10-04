#!/bin/bash

# 获取昨天的日期 (YYYY-MM-DD)
YESTERDAY=$(date -d "yesterday" '+%Y-%m-%d')

# 项目根目录 (请根据你的实际路径修改)
PROJECT_DIR="/path/to/your/project"

# 激活你的Python虚拟环境 (如果有的话)
# source /path/to/your/venv/bin/activate

cd $PROJECT_DIR

echo "Running daily incremental ETL for date: $YESTERDAY"

# 为不同的交易所和交易对执行ETL任务
python main_etl.py --exchange 'binance' --symbol 'BTC/USDT' --start_date $YESTERDAY
python main_etl.py --exchange 'binance' --symbol 'ETH/USDT' --start_date $YESTERDAY

# 可以添加更多...
# python main_etl.py --exchange 'okx' --symbol 'BTC/USDT' --start_date $YESTERDAY

echo "Daily ETL job finished."
