import logging
import backtrader as bt

logger = logging.getLogger("backtest")


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
