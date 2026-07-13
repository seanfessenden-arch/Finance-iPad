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

class PortfolioTab(TabPane):
    def __init__(self):
        super().__init__("Portfolio", id="portfolio")

    def compose(self) -> ComposeResult:
        yield Label("Name:", id="row1-label")
#end class PortfolioTab

