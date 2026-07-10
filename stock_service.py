#!/bin/python3
import time
import yfinance as yf

class StockService:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self._cache = {}  
        # symbol -> (price, timestamp)

    def _fetch_price(self, symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")

        if data.empty:
            {}

        row = data.iloc[-1]

        return {
            "date": row.name.strftime("%Y-%m-%d"),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        }
#end _fetch_price

    def price(self, symbol):
        """
        Retrieve the most recent daily
        pricing information.

        Returns a dictionary containing:
            date
            high
            low
            close

        Returns an empty dictionary if 
        no pricing data exists.
        """
        now = time.time()

		# ---- cache hit (FAST PATH) ----
        if symbol in self._cache:
            price, ts = self._cache[symbol]

			# still fresh → return immediately
            if now - ts < self.ttl:
                return price

			# stale but usable → return old value first (IMPORTANT for UI)
            stale_price = price
        else:
            stale_price = None

		# ---- refresh happens ONLY when called ----
        try:
            price = self._fetch_price(symbol)
        except Exception:
			# if API fails, fallback to stale value
            return stale_price

        if price is None:
             stale_price

        self._cache[symbol] = (price, now)
        return price


if __name__ == '__main__':
    ss = StockService()
    price = ss.price('CVNA')
    print(f'{price=}')

    for i in range(5):
        print(f"sleeping...{i}")
        time.sleep(1)
    price = ss.price('CVNA')
    print(f'{price=}')
