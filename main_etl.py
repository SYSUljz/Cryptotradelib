# -*- coding: utf-8 -*-
import argparse
from data_fetcher.fetch_historical import HistoricalFetcher
from data_processor.writer import save_to_parquet, register_metadata
from reporting.quality_check import generate_quality_report


def run_etl(exchange_id: str, symbol: str, start_date: str, timeframe: str = "1m"):
    """
    执行ETL主流程: 拉取、处理、存储、报告
    :param exchange_id: 交易所
    :param symbol: 交易对
    :param start_date: 起始日期
    :param timeframe: 时间周期
    """
    print(f"Starting ETL process for {exchange_id} - {symbol} from {start_date}")

    # 1. 初始化Fetcher
    fetcher = HistoricalFetcher(exchange_id=exchange_id)

    # 2. 拉取数据
    ohlcv_df = fetcher.fetch_all_history(
        symbol=symbol, timeframe=timeframe, start_date_str=start_date
    )

    if ohlcv_df.empty:
        print(f"No OHLCV data found for {symbol}. Exiting.")
        return

    # 3. 存储数据
    save_to_parquet(
        df=ohlcv_df, data_type="ohlcv_1m", exchange=exchange_id, symbol=symbol
    )

    # 4. 登记元数据 (示例)
    register_metadata(
        schema=ohlcv_df.dtypes.to_dict(),
        frequency=timeframe,
        missing_info="Forward fill or interpolation can be applied later.",
    )

    # 5. 生成数据质量报告
    generate_quality_report(df=ohlcv_df.copy(), timeframe_str=timeframe)

    print("ETL process finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the data pipeline ETL job.")
    parser.add_argument(
        "--exchange", type=str, required=True, help="Exchange ID (e.g., 'binance')"
    )
    parser.add_argument(
        "--symbol", type=str, required=True, help="Trading symbol (e.g., 'BTC/USDT')"
    )
    parser.add_argument(
        "--start_date", type=str, required=True, help="Start date in YYYY-MM-DD format"
    )

    args = parser.parse_args()

    run_etl(exchange_id=args.exchange, symbol=args.symbol, start_date=args.start_date)
