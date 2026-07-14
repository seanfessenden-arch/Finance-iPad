from textual.widgets import TabPane, Label
from textual.app import ComposeResult

class PortfolioTab(TabPane):
    def __init__(self):
        super().__init__("Portfolio", id="portfolio")

    def compose(self) -> ComposeResult:
        yield Label("Name:", id="row1-label")
#end class PortfolioTab

