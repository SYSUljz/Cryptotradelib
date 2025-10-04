# -*- coding: utf-8 -*-
import ccxt.pro
import asyncio

from config import WS_SYMBOLS, WS_EXCHANGES


async def watch_ticker(exchange_id):
    """
    订阅Ticker数据
    """
    exchange_class = getattr(ccxt.pro, exchange_id)
    exchange = exchange_class()

    while True:
        try:
            for symbol in WS_SYMBOLS:
                ticker = await exchange.watch_ticker(symbol)
                print(
                    f"[{exchange.id}] [{symbol}] Ticker: {ticker['datetime']}, Close: {ticker['close']}"
                )
        except Exception as e:
            print(f"Error watching ticker on {exchange_id}: {e}")
            break  # 出错时退出循环
    await exchange.close()


async def watch_l2_orderbook(exchange_id):
    """
    订阅L2 Orderbook数据
    """
    exchange_class = getattr(ccxt.pro, exchange_id)
    exchange = exchange_class()

    while True:
        try:
            for symbol in WS_SYMBOLS:
                orderbook = await exchange.watch_order_book(symbol)
                print(
                    f"[{exchange.id}] [{symbol}] OrderBook: {orderbook['datetime']}, "
                    f"Best Ask: {orderbook['asks'][0][0]}, Best Bid: {orderbook['bids'][0][0]}"
                )
        except Exception as e:
            print(f"Error watching order book on {exchange_id}: {e}")
            break
    await exchange.close()


async def main():
    tasks = []
    for exchange_id in WS_EXCHANGES:
        tasks.append(watch_ticker(exchange_id))
        tasks.append(watch_l2_orderbook(exchange_id))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # 提示: 实时数据流会持续打印，需要手动停止 (Ctrl+C)
    # 实际项目中，数据会被送入消息队列(如Kafka)或直接存入数据库
    print("Starting WebSocket data streams... Press Ctrl+C to stop.")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping WebSocket streams.")
