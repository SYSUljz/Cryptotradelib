import logging
import backtrader as bt

logger = logging.getLogger("backtest")


class MacdStrategy(bt.Strategy):
    """
    A strategy using the MACD indicator.
    It buys when the MACD line crosses above the signal line and
    sells when the MACD line crosses below the signal line.
    """

    params = (
        ("fast_period", 12),
        ("slow_period", 26),
        ("signal_period", 9),
        ("printlog", False),
    )

    def log(self, txt, dt=None, doprint=False):
        """Logging function for this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            logger.info(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        """
        Initializes the strategy.
        - Sets up data and indicators.
        - Initializes order tracking.
        """
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MACD indicator
        self.macd = bt.indicators.MACD(
            self.datas[0],
            period_me1=self.params.fast_period,
            period_me2=self.params.slow_period,
            period_signal=self.params.signal_period,
        )
        # CrossOver indicator for buy/sell signals
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

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
        """
        Defines the logic for each bar.
        """
        self.log(
            f"Close, {self.dataclose[0]:.2f}, MACD: {self.macd.macd[0]:.2f}, Signal: {self.macd.signal[0]:.2f}"
        )

        # Check if an order is pending. If so, we cannot send a 2nd one.
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not in the market, look for a buy signal
            if self.crossover > 0:
                self.log(f"BUY CREATE, {self.dataclose[0]:.2f}")
                self.order = self.buy()
        else:
            # Already in the market, look for a sell signal
            if self.crossover < 0:
                self.log(f"SELL CREATE, {self.dataclose[0]:.2f}")
                self.order = self.sell()
