# -*- coding: utf-8 -*-
import ccxt
import pandas as pd
from datetime import datetime
import time

from config import EXCHANGE_CONFIGS_WITHOUT_API_KEYS, USE_SANDBOX


class HistoricalFetcher:
    """
    用于从交易所拉取各类历史数据的类
    """

    def __init__(self, exchange_id: str):
        """
        初始化
        :param exchange_id: 交易所ID, e.g., 'binance'
        """
        if exchange_id not in EXCHANGE_CONFIGS_WITHOUT_API_KEYS:
            raise ValueError(f"Exchange '{exchange_id}' is not configured in config.py")

        config = EXCHANGE_CONFIGS_WITHOUT_API_KEYS[exchange_id]
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class(config)
        if USE_SANDBOX == True:
            self.exchange.set_sandbox_mode(True)
        self.exchange.load_markets()
        print(f"Initialized fetcher for {exchange_id}.")

    def fetch_ohlcv(
        self, symbol: str, timeframe: str = "1m", since: int = None, limit: int = 1000
    ) -> pd.DataFrame:
        """
        获取OHLCV数据
        :param symbol: 交易对, e.g., 'BTC/USDT'
        :param timeframe: 时间周期, e.g., '1m', '1h'
        :param since: 起始时间戳 (ms)
        :param limit: 单次请求数量
        :return: DataFrame
        """
        if not self.exchange.has["fetchOHLCV"]:
            print(f"{self.exchange.id} does not support fetchOHLCV.")
            return pd.DataFrame()

        print(
            f"Fetching OHLCV for {symbol} on {self.exchange.id} from {datetime.fromtimestamp(since/1000) if since else 'latest'}..."
        )
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_funding_rate(
        self, symbol: str, since: int = None, limit: int = 100
    ) -> pd.DataFrame:
        """
        获取资金费率历史
        :param symbol: 交易对
        :param since: 起始时间戳 (ms)
        :param limit: 数量
        :return: DataFrame
        """
        if not self.exchange.has["fetchFundingRateHistory"]:
            print(f"{self.exchange.id} does not support fetchFundingRateHistory.")
            return pd.DataFrame()

        print(f"Fetching funding rate for {symbol} on {self.exchange.id}...")
        try:
            params = {"symbol": symbol}
            funding_rates = self.exchange.fetch_funding_rate_history(
                symbol, since, limit, params
            )
            df = pd.DataFrame(funding_rates)
            # 数据清洗和格式化
            df = df[["timestamp", "datetime", "fundingRate"]]
            return df
        except Exception as e:
            print(f"Error fetching funding rates for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_all_history(
        self, symbol: str, timeframe: str, start_date_str: str
    ) -> pd.DataFrame:
        """
        循环拉取一个交易对的全部历史OHLCV数据
        :param symbol: 交易对
        :param timeframe: 时间周期
        :param start_date_str: 起始日期字符串 'YYYY-MM-DD'
        :return: 包含所有历史数据的DataFrame
        """
        all_ohlcv = []
        since = self.exchange.parse8601(start_date_str + "T00:00:00Z")

        while True:
            ohlcv = self.fetch_ohlcv(symbol, timeframe, since, 1000)
            if ohlcv is None or len(ohlcv) == 0:
                break

            all_ohlcv.append(ohlcv)
            new_since = ohlcv["timestamp"].iloc[-1]

            if new_since == since:  # 如果时间戳没有前进，说明已经获取完毕
                break
            since = new_since

            time.sleep(self.exchange.rateLimit / 1000)  # 遵守交易所的请求频率限制

        if not all_ohlcv:
            return pd.DataFrame()

        full_df = pd.concat(all_ohlcv, ignore_index=True)
        full_df.drop_duplicates(subset=["timestamp"], keep="first", inplace=True)
        return full_df


# 示例
if __name__ == "__main__":
    fetcher = HistoricalFetcher("binance")

    # 获取OHLCV
    ohlcv_df = fetcher.fetch_all_history("BTC/USDT", "1m", "2023-10-01")
    if not ohlcv_df.empty:
        print("Fetched OHLCV data:")
        print(ohlcv_df.head())
        print(ohlcv_df.tail())

    # 获取资金费率
    funding_df = fetcher.fetch_funding_rate("BTC/USDT")
    if not funding_df.empty:
        print("\nFetched Funding Rate data:")
        print(funding_df.head())
