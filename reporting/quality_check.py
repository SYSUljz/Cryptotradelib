# -*- coding: utf-8 -*-
import pandas as pd


def generate_quality_report(df: pd.DataFrame, timeframe_str: str):
    """
    生成数据质量报告
    :param df: 数据 (必须有'timestamp'列)
    :param timeframe_str: 时间周期字符串, e.g., '1m', '1h'
    """
    if df.empty:
        print("Cannot generate report for empty dataframe.")
        return

    print("\n--- Data Quality Report ---")

    # 1. 缺失值检查
    df.sort_values("timestamp", inplace=True)
    expected_interval = pd.to_timedelta(timeframe_str).total_seconds() * 1000
    df["time_diff"] = df["timestamp"].diff()

    missing_count = (df["time_diff"] > expected_interval * 1.5).sum()
    print(f"Total rows: {len(df)}")
    print(f"Expected interval (ms): {expected_interval}")
    print(f"Number of potential missing data points (gaps): {missing_count}")

    # 2. 延迟检查 (假设数据是准点生成的)
    df["delay"] = df["timestamp"] % expected_interval
    avg_delay = df["delay"].mean()
    print(f"Average timestamp delay from perfect interval (ms): {avg_delay:.2f}")

    # 3. 异常值检测 (简单示例：价格突变)
    df["price_change"] = df["close"].pct_change().abs()
    abnormal_moves = df[df["price_change"] > 0.05]  # 筛选出价格变动超过5%的记录
    print(f"Number of abnormal price moves (>5%): {len(abnormal_moves)}")
    if not abnormal_moves.empty:
        print("Abnormal moves found at timestamps:")
        print(abnormal_moves[["datetime", "close", "price_change"]])

    print("---------------------------\n")
