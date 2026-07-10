from textual import on
from textual.widgets import Button, Static
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
class DeleteStockScreen(ModalScreen[bool]):

	def __init__(self, symbol: str):
		super().__init__()
		self.symbol = symbol

	def compose(self):
		with Vertical(id="dialog"):
			yield Static(f"Delete {self.symbol}?")
			with Horizontal():
				yield Button("Yes", id="yes", variant="error")
				yield Button("No", id="no")

	@on(Button.Pressed)
	def button_pressed(self, event: Button.Pressed):
		if event.button.id == "yes":
			self.dismiss(True)
		else:
			self.dismiss(False)
