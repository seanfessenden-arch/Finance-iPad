#!/bin/python3

from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
import yfinance as yf
import pandas as pd

from rich.text import Text
from textual import on
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Label, TabPane, DataTable

class SectorsTab(TabPane):
    BINDINGS = [
            Binding("ctrl+q", "quit", "Quit"),
            ]
    def __init__(self):
        super().__init__("Sectors", id="sectors")
        self.USE_CACHE = True
        self.today = datetime.now()

            #"FCYIX":"Industrials",
        self.sectors = {
            "FSELX":"Semiconductors",
            "FSPTX":"Technology",
            "FSENX":"Energy",
            "FSPHX":"Health Care",
            "FIDSX":"Financial Services"
        }

        self.dates = {
	        "CURRENT": self.today,
	        "YTD": datetime(self.today.year, 1, 1),
	        "1Y": self.today - relativedelta(years=1),
	        "5Y": self.today - relativedelta(years=5),
	        "10Y": self.today - relativedelta(years=10),
	        "15Y": self.today - relativedelta(years=15),
	        "20Y": self.today - relativedelta(years=20),
        }

    def compose(self) -> ComposeResult:
        yield Label("Sector Section")
        yield DataTable(id="sector-table")

    def on_mount(self):
        sector_tbl = self.query_one("#sector-table", DataTable)
        sector_tbl.cursor_type = "row"
        sector_tbl.zebra_stripes=True
        #sector_tbl.add_columns(
        sector_tbl.add_column("Sector (Symbol)", key="col1")
        sector_tbl.add_column(Text("YTD", justify="right"), key="col2")
        sector_tbl.add_column(Text("1 Yr", justify="right"), key="col3")
        sector_tbl.add_column(Text("5 Yr", justify="right"), key="col4")
        sector_tbl.add_column(Text("10 Yr", justify="right"), key="col5")
        sector_tbl.add_column(Text("15 Yr", justify="right"), key="col6")
        sector_tbl.add_column(Text("20 Yr", justify="right"), key="col7")

        for index, col in enumerate(sector_tbl.columns.values()):
            col.auto_width = False

            col.width = 27 if index==0 else 9

        sector_tbl.refresh()

        self.build_table()
#end on mount

    def build_table(self):
        sector_tbl = self.query_one("#sector-table", DataTable)
        sector_tbl.clear()
        for sector in self.sectors:
            self.show_hist_data(sector)

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

        sector_tbl = self.query_one("#sector-table", DataTable)
        sector_tbl.add_row(
            f"{self.sectors[symbol]} ({symbol})",
            f"{returns['YTD']:>8.1f}%",
            f"{returns['1Y']:>8.1f}%",
            f"{returns['5Y']:>8.1f}%",
            f"{returns['10Y']:>8.1f}%",
            f"{returns['15Y']:>8.1f}%",
            f"{returns['20Y']:>8.1f}%"
        )

def main():
    for symbol in sectors.keys():
        print(sectors[symbol])
        try:
            my_sectors.show_hist_data(symbol)
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()

