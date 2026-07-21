#!/bin/python3

import json
import requests
from pathlib import Path

from time_to_die import TimeToDie
from helper import convert_epoch, percent_gain


class YahooClient:

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.ttd = TimeToDie()

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent":
                "Mozilla/5.0"
            }
        )

    #---------------------------------------------------------
    def _get_json(self, url):

        r = self.session.get(url, timeout=15)
        r.raise_for_status()

        return r.json()

    #-------------------------------------------------
    def quote(self, symbol):

        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            f"?interval=1d"
            f"&range=5d"
        )

        data = self._get_json(url)["chart"]["result"][0]

        meta = data["meta"]

        return {
			"symbol": symbol,
			"price": meta.get("regularMarketPrice"),
			"previous_close": meta.get("previousClose"),
			"currency": meta.get("currency"),
			"exchange": meta.get("exchangeName")
		}
    #--------------------------------------------------
    def quotes(self, symbols):
        prices = []
        for symbol in symbols:
            print(symbol)
            data = self.quote(symbol)
            prices.append(data)

        return prices

    #---------------------------------------------------
    def chart(
        self,
        symbol,
        range="5y",
        interval="1d"
    ):

        url = (
            "https://query1.finance.yahoo.com/"
            f"v8/finance/chart/{symbol}"
            f"?range={range}"
            f"&interval={interval}"
            "&includePrePost=false"
            "&events=div,splits"
        )

        data = self._get_json(url)

        result = data["chart"]["result"]

        if not result:
            return []

        result = result[0]

        timestamps = result["timestamp"]

        quote = result["indicators"]["quote"][0]

        history = []

        for i, ts in enumerate(timestamps):

            history.append(
                {
                    "timestamp":
                        ts,

                    "open":
                        quote["open"][i],

                    "high":
                        quote["high"][i],

                    "low":
                        quote["low"][i],

                    "close":
                        quote["close"][i],

                    "volume":
                        quote["volume"][i]
                }
            )

        return history

    #---------------------------------------------------
    def _history_file(self, symbol, range, interval):
        filename = f"{symbol}_{range}_{interval}.json"
        return self.data_dir / filename

    #---------------------------------------------------
    def _load_history_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    #---------------------------------------------------
    def _save_history_file(self, path, history):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

    #---------------------------------------------------
    def history(self, symbol, 
		range="5y", interval="1d"):

        path = self._history_file(symbol, range, interval)
        cache_key = f"HISTORY_{symbol}"

        expired = self.ttd.cache_expired(cache_key)

        if path.exists() and not expired:
            print(f"{symbol}: using cache")
            return self._load_history_file(path)

        print(f"{symbol}: downloading...")

        data = self.chart(symbol, range=range, interval=interval)

        self._save_history_file(path, data)

        self.ttd.reset_cache(cache_key)

        return data

if __name__ == "__main__":

    y = YahooClient()

    print(y.quote("AAPL")['price'])
    print(y.quotes(('MSFT','AAPL')))
    data = y.history("AAPL")
    ''' 
    oldest_price =0
    current_price = 0
    x = 0
    for record in data:
        x += 1
        if x ==1:
            old_price = record['close']
        if x % 40 == 0:
            print(convert_epoch(record['timestamp']))
            curr_price = record['close']
            print(f"{curr_price} {percent_gain(old_price, curr_price)}")
        else:
            exit
            '''
