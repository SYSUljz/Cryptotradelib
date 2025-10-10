from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import os
import sys
import pandas as pd
import backtrader as bt
import logging
from data_processor.loader import load_from_parquet
import matplotlib

# === Set up logging ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"backtest_{datetime.datetime.now():%Y%m%d_%H%M%S}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),  # also print to console
    ],
)


class TestStrategy(bt.Strategy):
    params = (
        ("maperiod", 15),
        ("printlog", False),
    )

    def log(self, txt, dt=None, doprint=False):
        """Logging function for this strategy"""
        dt = dt or bt.num2date(self.datas[0].datetime[0])
        message = f"{dt.isoformat()}, {txt}"
        if self.params.printlog or doprint:
            logging.info(message)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()

    def stop(self):
        self.log(
            "(MA Period %2d) Ending Value %.2f"
            % (self.params.maperiod, self.broker.getvalue()),
            doprint=True,
        )


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
    logging.info(f"Logs saved to: {LOG_FILE}")
    cerebro.plot()
