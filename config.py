# -*- coding: utf-8 -*-
import os

# -----------------------------------------------------------------------------
# API Keys Configuration
# -----------------------------------------------------------------------------
EXCHANGE_CONFIGS_WITH_API_KEYS = {
    "binance": {
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET_KEY"),
        "options": {
            "defaultType": "spot",
        },
    },
    "binanceusdm": {  # Binance USDT-M Perpetual Futures
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET_KEY"),
        "enableRateLimit": True,
        "options": {
            "defaultType": "future",
        },
    },
    "okx": {
        "apiKey": "YOUR_OKX_API_KEY",
        "secret": "YOUR_OKX_SECRET_KEY",
        "password": "YOUR_OKX_API_PASSWORD",
        "options": {
            "defaultType": "swap",
        },
    },
}

# -----------------------------------------------------------------------------
# Exchanges without API keys (for public data)
# -----------------------------------------------------------------------------
EXCHANGE_CONFIGS_WITHOUT_API_KEYS = {
    "binance": {
        "enableRateLimit": True,
        "options": {
            "defaultType": "spot",
        },
    },
    "binanceusdm": {
        "enableRateLimit": True,
        "options": {
            "defaultType": "future",
        },
    },
    "okx": {
        "enableRateLimit": True,
        "options": {
            "defaultType": "swap",
        },
    },
}

# -----------------------------------------------------------------------------
# Data Storage Configuration
# -----------------------------------------------------------------------------
DATA_ROOT_PATH = "data/"

# -----------------------------------------------------------------------------
# WebSocket Subscription Configuration
# -----------------------------------------------------------------------------
WS_SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
]

WS_EXCHANGES = ["binance", "binanceusdm", "okx"]

USE_SANDBOX = False
