# -*- coding: utf-8 -*-
import pandas as pd
import os
from config import DATA_ROOT_PATH


def save_to_parquet(df: pd.DataFrame, data_type: str, exchange: str, symbol: str):
    """
    将DataFrame按分区格式存储为Parquet文件
    分区: exchange/symbol/date
    :param df: 数据
    :param data_type: 数据类型, e.g., 'ohlcv', 'funding_rate'
    :param exchange: 交易所
    :param symbol: 交易对 (文件名会把'/'替换成'_')
    """
    if df.empty:
        print("Dataframe is empty, skipping save.")
        return

    # 从datetime列创建date分区
    if "datetime" in df.columns:
        df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")
    else:
        print("Warning: 'datetime' column not found. Cannot create date partition.")
        return

    symbol_path_name = symbol.replace("/", "_")

    base_path = os.path.join(
        DATA_ROOT_PATH, data_type, f"exchange={exchange}", f"symbol={symbol_path_name}"
    )

    # 使用 a dataset API with partitioning
    try:
        df.to_parquet(
            base_path,
            engine="fastparquet",
            partition_cols=["date"],
            append=True,  # 增量写入
            write_index=False,
        )
        print(f"Successfully saved {len(df)} rows to {base_path}")
    except Exception as e:
        print(f"Failed to save data to Parquet: {e}")


def register_metadata(schema, frequency, missing_info):
    """
    登记元数据 (此处为示例，实际可写入数据库或文件中)
    """
    print("\n--- Metadata Registration ---")
    print(f"Schema: {schema}")
    print(f"Sampling Frequency: {frequency}")
    print(f"Missing Value Handling: {missing_info}")
    print("----------------------------\n")
