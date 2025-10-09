# -*- coding: utf-8 -*-
import os

# -----------------------------------------------------------------------------
# API Keys Configuration
# -----------------------------------------------------------------------------
# 在此处填入你的交易所API密钥和私钥
# 建议使用环境变量或更安全的密钥管理方式
EXCHANGE_CONFIGS_WITH_API_KEYS = {
    "binance": {
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET_KEY"),
        "options": {
            "defaultType": "spot",  # or 'future', 'spot'
        },
    },
    "okx": {
        "apiKey": "YOUR_OKX_API_KEY",
        "secret": "YOUR_OKX_SECRET_KEY",
        "password": "YOUR_OKX_API_PASSWORD",  # OKX需要额外的密码
        "options": {
            "defaultType": "swap",
        },
    },
    # 在此添加更多交易所
}

EXCHANGE_CONFIGS_WITHOUT_API_KEYS = {
    "binance": {
        "options": {
            "defaultType": "spot",  # or 'future', 'spot'
        },
    },
    "okx": {
        "options": {
            "defaultType": "swap",
        },
    },
    # 在此添加更多交易所
}

# -----------------------------------------------------------------------------
# Data Storage Configuration
# -----------------------------------------------------------------------------
# 数据存储的根目录
DATA_ROOT_PATH = "data/"

# -----------------------------------------------------------------------------
# WebSocket Subscription Configuration
# -----------------------------------------------------------------------------
# 需要通过WebSocket订阅的交易对
WS_SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
]

# 需要订阅的交易所
WS_EXCHANGES = ["binance", "okx"]

USE_SANDBOX = False
