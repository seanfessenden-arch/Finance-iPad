#!/bin/python3

from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
import yfinance as yf
import pandas as pd

class SectorsTab:
    def __init__(self):
        self.USE_CACHE = True
        self.today = datetime.now()

        self.dates = {
	        "CURRENT": self.today,
	        "YTD": datetime(self.today.year, 1, 1),
	        "1Y": self.today - relativedelta(years=1),
	        "5Y": self.today - relativedelta(years=5),
	        "10Y": self.today - relativedelta(years=10),
	        "15Y": self.today - relativedelta(years=15),
	        "20Y": self.today - relativedelta(years=20),
        }

    def price_on_or_after(self, hist, target):
        mask = hist.index >= target

        if not mask.any():
            return None

        row = hist.loc[mask].iloc[0]

        return {
            "date": row.name.date(),
            "price": row["Close"],
        }
    #end price on or after

    def get_history(self, symbol):

        cache_file = Path(f"{symbol}.json")

        if self.USE_CACHE and cache_file.exists():
            hist = pd.read_json(
                cache_file,
                orient="table"
            )
        else:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="max", auto_adjust=True)
            hist.to_json(
                cache_file,
                orient="table",
                date_format="iso"
    )

        # Always make the index timezone-naive
        if hist.index.tz is not None:
            hist.index = hist.index.tz_localize(None)
        return hist
    #end get history


    def show_hist_data(self, symbol):
        prices = {}
        hist = self.get_history(symbol)

        for period, target in self.dates.items():
            if period == "CURRENT":
                row = hist.iloc[-1]
                prices[period] = {
                "date": row.name.date(),
                "price": row["Close"],
                }
            else:
                prices[period] = self.price_on_or_after(hist, target)

        returns = {}

        current = prices["CURRENT"]["price"]

        for period in ("YTD", "1Y", "5Y", "10Y", "15Y", "20Y"):
            past = prices[period]["price"]
            returns[period] = (current - past) / past * 100

        print(
            f"{symbol:<8}"
            f"{returns['YTD']:>8.1f}%"
            f"{returns['1Y']:>8.1f}%"
            f"{returns['5Y']:>8.1f}%"
            f"{returns['10Y']:>8.1f}%"
            f"{returns['15Y']:>8.1f}%"
            f"{returns['20Y']:>8.1f}%"
        )

def main():
    my_sectors = Sectors()
    print(
	    f"{'Symbol':<8}"
	    f"{'YTD':>10}"
	    f"{'1Y':>10}"
	    f"{'5Y':>10}"
	    f"{'10Y':>10}"
	    f"{'15Y':>10}"
	    f"{'20Y':>10}"
    )

    print("-" * 68)

    sectors = {
            "FSELX":"Semiconductors",
            "FSPTX":"Technology",
            "FSENX":"Energy",
            "FSPHX":"Health Care",
            "FCYIX":"Industrials",
            "FIDSX":"Financial Services"
    }
    for symbol in sectors.keys():
        print(sectors[symbol])
        try:
            my_sectors.show_hist_data(symbol)
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()

