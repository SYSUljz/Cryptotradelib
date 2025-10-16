import logging
import backtrader as bt


class BollingerBandsStrategy(bt.Strategy):
    """
    A mean-reversion strategy using Bollinger Bands.
    It buys when the price touches or crosses below the lower band and
    sells when the price touches or crosses above the upper band.
    """

    params = (
        ("period", 20),
        ("devfactor", 2.0),  # Standard deviation factor
        ("printlog", False),
    )

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bollinger = bt.indicators.BollingerBands(
            self.datas[0], period=self.params.period, devfactor=self.params.devfactor
        )

    def notify_order(self, order):
        """
        Handles order notifications.
        Resets self.order when the order is completed.
        """
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    f"SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}"
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # Reset order status
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if (
                self.dataclose[0] < self.bollinger.lines.bot[0]
            ):  # Price is below the lower band
                self.log(f"BUY CREATE (Below Lower Bollinger), {self.dataclose[0]:.2f}")
                self.order = self.buy()
        else:
            if (
                self.dataclose[0] > self.bollinger.lines.top[0]
            ):  # Price is above the upper band
                self.log(
                    f"SELL CREATE (Above Upper Bollinger), {self.dataclose[0]:.2f}"
                )
                self.order = self.sell()
