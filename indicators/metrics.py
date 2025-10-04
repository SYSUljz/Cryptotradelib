# -*- coding: utf-8 -*-
import pandas as pd


def calculate_annualized_funding_rate(
    df: pd.DataFrame, periods_per_day: int
) -> pd.DataFrame:
    """
    计算年化资金费率
    :param df: 包含'fundingRate'列的DataFrame
    :param periods_per_day: 每日资金费率结算次数 (e.g., Binance是3次，每8小时一次)
    :return: 带有'annualizedRate'列的DataFrame
    """
    if "fundingRate" in df.columns:
        df["annualizedRate"] = ((1 + df["fundingRate"]) ** (periods_per_day * 365)) - 1
    return df


def slippage_model(order_size: float, orderbook_df: pd.DataFrame) -> float:
    """
    一个简单的滑点模型示例
    :param order_size: 下单数量
    :param orderbook_df: 订单簿快照
    :return: 预计的滑点成本
    """
    # 这是一个非常简化的模型，实际模型会复杂得多
    # 这里仅为演示功能占位
    print(f"Calculating slippage for order size {order_size}...")
    return 0.0005 * order_size  # 假设一个线性滑点


def calculate_basis(spot_price: pd.Series, future_price: pd.Series) -> pd.Series:
    """
    计算基差 (期货价格 - 现货价格)
    :param spot_price: 现货价格序列
    :param future_price: 期货/永续合约价格序列
    :return: 基差序列
    """
    basis = future_price - spot_price
    return basis
