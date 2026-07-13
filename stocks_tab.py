from db import DB
from stock_service import StockService
from delete_stock import DeleteStockScreen
from enums import Mode, Cache 

from textual import on
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import (
        Label, Input, Button, Footer,
        Header, DataTable, Static, 
        TabbedContent, TabPane)

class StockTab(TabPane):
    BINDINGS = [
            Binding("ctrl+q", "quit", "Quit"),
            Binding("ctrl+d", "set_del_stock", "Delete")
            ]

    def __init__(self):
        super().__init__("Stocks", id="stocks")
        self.db = DB("portfolio.db")
        self.mode = Mode.NORMAL
        self.ss = StockService()
#end init

    def on_mount(self):
        stock_tbl = self.query_one("#fund-table", DataTable)
        stock_tbl.cursor_type = "row"
        stock_tbl.zebra_stripes = True
        stock_tbl.add_columns(
                "Symbol",
                "Company"
                )
        self.refresh_stock_list()
        # refresh the list of stocks   
#end on_mount

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Company:", id="row1-label"),
            Input(placeholder="Enter company name", id="name-input"),

            Label("Ticker:", id="row2-label"),
            Input(placeholder="Enter ticker", id="value-input"),

            Button("Submit", id="add-btn", variant="primary"),

            Static("", id="spacer"),
            DataTable(id="fund-table"),
            Static("Status: Ready",id="footer-box"),
        )
#end compose

    @on(DataTable.RowSelected, "#fund-table")
    def on_fund_selected(self, event: DataTable.RowSelected) -> None:
        try:
            if self.mode == Mode.DELETE: 
                self.delete_stock(event)
                return
            else:
                self.show_stock_price(event)
        except Exception as e:
            self.notify(str(e))
#end on fund selected   

    def get_selected_symbol(self, event: DataTable.RowSelected):
        table = event.data_table
        row_data = table.get_row(event.row_key)
        
        # event.row_key gives the internal ID of the row
        # row_data contains the list of values for row
        sel_ticker = row_data[0]
        return sel_ticker
#end get selected symbol

    def show_stock_price(self, event):
        sel_ticker = self.get_selected_symbol(event)
        price = self.ss.price(sel_ticker)
        self.query_one("#footer-box", Static).update(
        f"{sel_ticker} : ${price['close']:.2f}")
#end show stock price

    def action_set_del_stock(self):
        self.mode = Mode.DELETE
        self.query_one("#footer-box", Static).update(
		"Delete Mode - Select a stock")

    def delete_stock(self, event):
            sel_ticker = self.get_selected_symbol(event)
            self.app.push_screen(
                DeleteStockScreen(sel_ticker),
               lambda result: self.del_stock_db(sel_ticker, result)
                )
            self.mode = Mode.NORMAL
            self.refresh_stock_list()
#end delete stock

    def del_stock_db(self, sel_ticker, confirmed: bool):
        self.mode = Mode.NORMAL
        if not confirmed:
            return
        self.db.delete_stock(sel_ticker)
        self.refresh_stock_list()
        self.query_one("#footer-box", Static).update(
            f"{sel_ticker} : Deleted"
        )
#end delete stock

    def refresh_stock_list(self):
        table = self.query_one("#fund-table", DataTable)
        table.clear()

        for row in self.db.get_stock_list():
            table.add_row(row[0], row[1])
#end refresh stock list

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-btn":
            name = self.query_one("#name-input", Input).value
            ticker = self.query_one("#value-input", Input).value
            self.db.add_stock(ticker.upper(), name.upper())
            footer = self.query_one("#footer-box", Static)
            footer.update(f"Added: '{name}', '{ticker}'")
            self.query_one("#name-input", Input).value = ""
            self.query_one("#value-input", Input).value = ""
        self.refresh_stock_list()
