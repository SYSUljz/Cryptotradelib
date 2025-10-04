# 数据获取与存储系统

本项目旨在构建一个稳定的数据获取与存储层，为后续的回测与监控系统提供基础。

## 项目结构

```
Cryptotradelib/
├── data_fetcher/               # 数据获取模块
│   ├── __init__.py
│   ├── fetch_historical.py     # 拉取历史数据 (OHLCV, Funding Rate等)
│   └── stream_live.py          # WebSocket 实时数据订阅
├── data_processor/             # 数据处理与存储模块
│   ├── __init__.py
│   └── writer.py               # 数据写入Parquet及元数据登记
├── indicators/                 # 指标计算库
│   ├── __init__.py
│   └── metrics.py              # 计算手续费、滑点、资金费率、基差等
├── reporting/                  # 数据质量报告模块
│   ├── __init__.py
│   └── quality_check.py        # 生成数据质量报告
├── scheduler/                  # 任务调度
│   └── daily_etl.sh            # 每日增量ETL任务脚本
├── main_etl.py                 # 主ETL任务执行入口
├── config.py                   # 配置文件 (API密钥, 路径等)
└── requirements.txt            # Python依赖包
```

## 安装与配置

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

在 `config.py` 文件中填入您的交易所 API 密钥（如需）、数据存储的根路径等信息。

## 如何运行

### 历史数据拉取

直接运行主 ETL 脚本来执行历史数据的回补：

```bash
python main_etl.py --symbol 'BTC/USDT' --exchange 'binance' --start_date '2023-01-01'
```

### 实时数据订阅

运行 `stream_live.py` 脚本来订阅实时数据流：

```bash
python data_fetcher/stream_live.py
```

### 每日增量任务

使用 cron 或其他调度工具来每日定时执行 `scheduler/daily_etl.sh` 脚本，以获取前一天的增量数据。

编辑 crontab：

```bash
crontab -e
```

添加如下行，表示每天凌晨 2 点执行：

```
0 2 * * * /path/to/your/project/scheduler/daily_etl.sh
```

## 核心功能模块

- **data_fetcher**：使用 CCXT 库获取多交易所的 OHLCV、资金费率、合约规格等历史数据，并通过 WebSocket 订阅实时 Ticker 和 L2 Orderbook。
- **data_processor**：将获取的数据清洗、格式化，并以 `exchange/symbol/date` 的分区格式存储为 Parquet 文件。
- **indicators**：包含常用的指标计算模型，如滑点、年化资金费率等。
- **reporting**：生成数据质量报告，监控数据的完整性、延迟和异常值。

