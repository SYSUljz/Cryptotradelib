import backtrader as bt


class GoldenCrossStrategy(bt.Strategy):
    """
    Implements the 'Golden Cross' strategy.
    A long position is taken when the short-term moving average (e.g., 50-day)
    crosses above the long-term moving average (e.g., 200-day).
    The position is closed when the short-term MA crosses back below.
    """

    params = (("fast_ma", 50), ("slow_ma", 200), ("printlog", False))

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        # Short-term and long-term moving averages
        self.sma_fast = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.fast_ma
        )
        self.sma_slow = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.slow_ma
        )

        # The crossover signal
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

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

        if not self.position:  # Not in the market
            if self.crossover > 0:  # Fast MA crosses above Slow MA
                self.log(f"BUY CREATE (Golden Cross), {self.dataclose[0]:.2f}")
                self.order = self.buy()
        else:  # Already in the market
            if self.crossover < 0:  # Fast MA crosses below Slow MA
                self.log(f"SELL CREATE (Death Cross), {self.dataclose[0]:.2f}")
                self.order = self.sell()


# ====================================================================
# 3. RSI Strategy: Relative Strength Index
# ====================================================================
class RsiStrategy(bt.Strategy):
    """
    A strategy based on the Relative Strength Index (RSI).
    It buys when the RSI enters an oversold region (e.g., below 30) and
    sells when it enters an overbought region (e.g., above 70).
    """

    params = (
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30),
        ("printlog", False),
    )

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.rsi = bt.indicators.RSI_SMA(self.datas[0], period=self.params.rsi_period)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi < self.params.rsi_oversold:
                self.log(f"BUY CREATE (RSI Oversold), {self.dataclose[0]:.2f}")
                self.order = self.buy()
        else:
            if self.rsi > self.params.rsi_overbought:
                self.log(f"SELL CREATE (RSI Overbought), {self.dataclose[0]:.2f}")
                self.order = self.sell()
