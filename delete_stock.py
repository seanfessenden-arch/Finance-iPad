from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Static, Label
from textual.containers import Horizontal, Vertical, Container
from textual.screen import ModalScreen
class DeleteStockScreen(ModalScreen[bool]):

    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label(f"Delete {self.symbol}?", id="question")
            with Horizontal(id="buttons"):
                yield Button("Yes", id="yes", variant="error")
                yield Button("No", id="no", variant="primary")

    @on(Button.Pressed)
    def button_pressed(self, event: Button.Pressed):
        # Dismiss and return True if 'yes', False otherwise
        self.dismiss(event.button.id == "yes")

