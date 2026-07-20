#!/bin/python3

from datetime import datetime
from dateutil.relativedelta import relativedelta
import traceback

from yahoo_client import YahooClient

today = datetime.now()

dates = {
    "CURRENT": today,
    "YTD": datetime(today.year, 1, 1),
    "1Y": today - relativedelta(years=1),
    "5Y": today - relativedelta(years=5),
    "10Y": today - relativedelta(years=10),
    "15Y": today - relativedelta(years=15),
    "20Y": today - relativedelta(years=20),
}

client = YahooClient()


def price_on_or_after(hist, target):
    for row in hist:
        if row["date"] >= target:
            return {"date": row["date"].date(), "price": row["close"]}

    return None
#end price on or after


def get_history(symbol):
    '''
        Pull full price history for a symbol via YahooClient, which
        handles disk caching and TimeToDie-based expiry on its own.
        Returns a list of {"date": datetime, "close": float}, sorted
        oldest to newest, with any null-close rows dropped.
    '''
    raw = client.history(symbol, range="max", interval="1d")

    hist = []

    for row in raw:
        if row["close"] is None:
            continue

        hist.append({
            "date": datetime.fromtimestamp(row["timestamp"]),
            "close": row["close"],
        })

    hist.sort(key=lambda r: r["date"])

    return hist
#end get history


def show_hist_data(symbol):
    hist = get_history(symbol)

    if not hist:
        print(f"{symbol:<8}no data")
        return

    prices = {
        "CURRENT": {
            "date": hist[-1]["date"].date(),
            "price": hist[-1]["close"],
        }
    }

    for period, target in dates.items():
        if period == "CURRENT":
            continue
        prices[period] = price_on_or_after(hist, target)

    current = prices["CURRENT"]["price"]
    returns = {}

    for period in ("YTD", "1Y", "5Y", "10Y", "15Y", "20Y"):
        entry = prices[period]
        returns[period] = None if entry is None else (current - entry["price"]) / entry["price"] * 100

    def fmt(period):
        value = returns[period]
        return f"{value:>8.1f}%" if value is not None else f"{'n/a':>9}"

    print(
        f"{symbol:<8}"
        f"{fmt('YTD')}"
        f"{fmt('1Y')}"
        f"{fmt('5Y')}"
        f"{fmt('10Y')}"
        f"{fmt('15Y')}"
        f"{fmt('20Y')}"
    )
#end show hist data


def main():
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
        "FSELX": "Semiconductors",
        "FSPTX": "Technology",
        "FSENX": "Energy",
        "FSPHX": "Health Care",
        "FIDRX": "Industrials",
        "FIDSX": "Financial Services"
    }

    for symbol in sectors.keys():
        print(sectors[symbol])
        try:
            show_hist_data(symbol)
        except Exception as e:
            print(f"{symbol}: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()
