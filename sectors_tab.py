#!/bin/python3

from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta

from rich.text import Text
from textual import on
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Label, TabPane, DataTable

from time_to_die import TimeToDie
from yahoo_client import YahooClient
from helper import percent_gain

class SectorsTab(TabPane):
    BINDINGS = [
            Binding("ctrl+q", "quit", "Quit"),
            ]
    def __init__(self):
        super().__init__("Sectors", id="sectors")
        self.USE_CACHE = True
        self.today = datetime.now()
        self.client = YahooClient()
        self.sort_descending = True

        self.sectors = {
            "FSELX":"Semiconductors",
            "FSPTX":"Technology",
            "FSENX":"Energy",
            "FENY":"Energy",
            "FMAT":"Materials",
            "FUTY":"Utilities",
            "FREL":"Real Estate",
            "FSPHX":"Health Care",
            "FIDRX": "Industrials",
            "FTEC": "Informtn Technology",
            "FDIS": "Consumer Discret",
            "FSTA": "Consumer Staples",
            "FCOM": "Comunictn Services",
            "FHLC": "Health Care",
            "FNCL": "Financials",
            "FIDU": "Industrials",
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
    #end init

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
        '''
        def sort_percent(val):
            try:
                return float(val.replace("%", "").strip())
            except ValueError:
                return float('-inf')  # Put invalid or empty values at the bottom

        sector_tbl.sort('col7', key=sort_percent)
        '''

        sector_tbl.refresh()
        self.build_table()
#end on mount

    @on(DataTable.HeaderSelected, "#sector-table")
    def on_header_clicked(self, event: DataTable.HeaderSelected):
        # Check if the selected column key is 'col7' (the 20 Yr header)
        if event.column_key.value in ('col7', 'col6', 'col5', 'col4', 'col3', 'col2', 'col1'):
            sector_tbl = event.data_table
            self.sort_descending = not self.sort_descending

            def sort_percent(val):
                try:
                    return float(val.replace("%", "").strip())
                except ValueError:
                    return float('-inf')

            # Toggles sorting direction if clicked multiple times, or defaults to descending
            # for easy reading of highest performers.
            sector_tbl.sort(
                event.column_key,
                key=sort_percent,
                reverse=self.sort_descending
            )
            sector_tbl.refresh()

    def build_table(self):
        sector_tbl = self.query_one("#sector-table", DataTable)
        sector_tbl.clear()
        for sector in self.sectors:
            self.show_hist_data(sector)

    def price_on_or_after(self, hist, target):

        for row in hist:
            if row["date"] >= target:
                return {"date": row["date"].date(), "price": row["close"]}
        return None
    #end price on or after

    def get_history(self, symbol):
        '''
        Pull full price history for a symbol via YahooClient, which
        handles disk caching and TimeToDie-based expiry on its own.
        Returns list of {"date": datetime, "close": float}, sorted
        oldest to newest, with any null-close rows dropped.
        '''
        raw = self.client.history(symbol, range="max", interval="1d")

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

    def show_hist_data(self, symbol):
        hist = self.get_history(symbol)

        if not hist:
            print(f"{symbol:<8} no data")
            return

        prices = {
                "CURRENT": {
                    "date": hist[-1]["date"].date(),
                    "price": hist[-1]["close"],
                    }
                }

        for period, target in self.dates.items():
            if period == "CURRENT":
                continue
            else:
                prices[period] = self.price_on_or_after(hist, target)
        current = prices["CURRENT"]["price"]
        returns = {}

        for period in ("YTD", "1Y", "5Y", "10Y", "15Y", "20Y"):
            past = prices[period]["price"]
            if past is None:
                returns[period] = None 
            else:
                returns[period] = percent_gain(past, current)

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

