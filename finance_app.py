#!/bin/python3
"""
Textual Grid layout example.

Row 1: Label + Input
Row 2: Label + Input
Row 3: Button (spans full width)
Row 4: spacer
Row 5: DataTable (spans full width, edge to edge)
Row 6: Static text with a border box (spans full width)
"""
from stocks_tab import StockTab
from portfolio_tab import PortfolioTab
from sectors_tab import SectorsTab

import traceback

from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import (
        Label, Input, Button, Footer,
        Header, DataTable, Static, 
        TabbedContent, TabPane)


class FinanceApp(App):
    CSS_PATH = "finance_app.tcss" 
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
            Binding("ctrl+q", "quit", "Quit")
            ]

    def __init__(self):
        super().__init__()
        self.stock_tab = StockTab()
        self.portfolio_tab = PortfolioTab()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent():
            yield self.stock_tab
            yield self.portfolio_tab
        yield Footer()

    def on_mount(self) -> None:
        self.stock_tab.query_one("#add-btn", Button).press()
            
if __name__ == "__main__":
    try:
        FinanceApp().run()
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        last_frame = tb[-1]
        file_name = last_frame.filename
        line_number = last_frame.lineno
        print(f"Error: {file_name} - Line {line_number}")
