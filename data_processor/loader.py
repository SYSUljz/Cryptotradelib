import os
import pandas as pd
from datetime import datetime


def load_from_parquet(
    data_root: str,
    data_type: str,
    exchange: str,
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    columns: list[str] = None,
) -> pd.DataFrame:
    """
    Load OHLCV (or other) data from partitioned parquet files.

    Parameters
    ----------
    data_root : str
        Root path of the dataset.
    data_type : str
        Data category, e.g. 'ohlcv' or 'funding_rate'.
    exchange : str
        Exchange name.
    symbol : str
        Trading pair, e.g. 'BTC/USDT'.
    start_date : str, optional
        Inclusive lower bound (format 'YYYY-MM-DD').
    end_date : str, optional
        Inclusive upper bound (format 'YYYY-MM-DD').
    columns : list[str], optional
        Columns to load from parquet.

    Returns
    -------
    pd.DataFrame
        Concatenated DataFrame with all rows in the requested date range.
    """
    symbol_path_name = symbol.replace("/", "_")
    base_path = os.path.join(data_root, data_type, exchange, symbol_path_name)

    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Data path not found: {base_path}")

    # list available date partitions
    partitions = [
        d
        for d in os.listdir(base_path)
        if d.startswith("date=") and os.path.isdir(os.path.join(base_path, d))
    ]
    if not partitions:
        raise FileNotFoundError(f"No date partitions found under {base_path}")

    # extract and sort partition dates
    partition_dates = sorted(d.split("date=")[1] for d in partitions)

    # filter by start/end date
    def in_range(date_str: str) -> bool:
        if start_date and date_str < start_date:
            return False
        if end_date and date_str > end_date:
            return False
        return True

    selected_dates = [d for d in partition_dates if in_range(d)]
    if not selected_dates:
        raise ValueError(f"No partitions in range {start_date} - {end_date}")

    # load and concatenate
    dfs = []
    for d in selected_dates:
        p = os.path.join(base_path, f"date={d}")
        try:
            df = pd.read_parquet(p, columns=columns)
            dfs.append(df)
        except Exception as e:
            print(f"Failed to read {p}: {e}")

    if not dfs:
        raise RuntimeError("No data loaded from any partition.")

    data = pd.concat(dfs, ignore_index=True).sort_values("datetime")

    # ensure datetime dtype
    if "datetime" in data.columns:
        data["datetime"] = pd.to_datetime(data["datetime"], errors="coerce")
        data = data.dropna(subset=["datetime"])

    return data.reset_index(drop=True)
