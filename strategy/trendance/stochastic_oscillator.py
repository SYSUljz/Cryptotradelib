import backtrader as bt

# ====================================================================
# 6. Stochastic Oscillator Strategy
# ====================================================================
class StochasticStrategy(bt.Strategy):
    """
    A strategy using the Stochastic Oscillator.
    Buys when the oscillator is oversold and the %K line crosses above %D.
    Sells when the oscillator is overbought and the %K line crosses below %D.
    """

    params = (
        ("period", 14),
        ("period_d_slow", 3),
        ("upperband", 80.0),
        ("lowerband", 20.0),
        ("printlog", False),
    )

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.stochastic = bt.indicators.Stochastic(
            self.datas[0],
            period=self.params.period,
            period_d_slow=self.params.period_d_slow,
        )

    def next(self):
        if self.order:
            return

        # Check for buy signal
        if not self.position:
            if (
                self.stochastic.lines.percK[-1] < self.params.lowerband
                and self.stochastic.lines.percD[-1] < self.params.lowerband
                and self.stochastic.lines.percK[0] > self.stochastic.lines.percD[0]
            ):
                self.log(
                    f"BUY CREATE (Stochastic Oversold Cross), {self.dataclose[0]:.2f}"
                )
                self.order = self.buy()

        # Check for sell signal
        else:
            if (
                self.stochastic.lines.percK[-1] > self.params.upperband
                and self.stochastic.lines.percD[-1] > self.params.upperband
                and self.stochastic.lines.percK[0] < self.stochastic.lines.percD[0]
            ):
                self.log(
                    f"SELL CREATE (Stochastic Overbought Cross), {self.dataclose[0]:.2f}"
                )
                self.order = self.sell()