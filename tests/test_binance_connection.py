# tests/test_binance_connection.py
import ccxt
import pytest


def test_binance_connection():
    exchange = ccxt.binance(
        {
            "enableRateLimit": True,  # avoid being banned
        }
    )

    try:
        # Fetch server time as a lightweight connectivity check
        server_time = exchange.fetch_time()
        assert isinstance(server_time, int)  # should return a timestamp
        print(f"Binance server time: {server_time}")
    except ccxt.NetworkError:
        pytest.fail("Network error: cannot connect to Binance")
    except ccxt.ExchangeError:
        pytest.fail("Exchange error: Binance API returned an error")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
