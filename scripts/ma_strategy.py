from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import os
import sys
import pandas as pd
import backtrader as bt
import logging
from data_processor.loader import load_from_parquet
from strategy.move_avg import TestStrategy
import matplotlib
from utils.logger import setup_logger

logger = setup_logger("backtest")

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy, maperiod=15, printlog=False)

    df = load_from_parquet(
        data_root="data",
        data_type="ohlcv_1m",
        exchange="binance",
        symbol="BTC/USDT",
        start_date="2025-10-01",
        end_date="2025-10-05",
    )

    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize(None)

    data = bt.feeds.PandasData(
        dataname=df,
        datetime="datetime",
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.001)
    cerebro.broker.setcommission(commission=0.01)

    logging.info("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
    logging.info("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
    # logging.info(f"Logs saved to: {LOG_FILE}")
    cerebro.plot()
