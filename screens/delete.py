from textual import on
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static
from textual.containers import Container, Vertical, Center
from textual.app import ComposeResult

from db import Connection

PIN_CODE = "1234"

class DeleteAsk(ModalScreen[str]):
    CSS_PATH = "../styles/delete.scss"

    def __init__(self, purpose: str) -> None:
        super().__init__()
        self.purpose = purpose

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            with Vertical(id="modal-box"):
                yield Input(placeholder="Input PIN", password=True, id="pin-id")
                yield Static(id="result-label")
                yield Center(Button("Cancel", id="cancel-button", variant="error"))

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def check_pin(self, event: Input.Submitted) -> None:
        pin_input = event.input

        if pin_input.value == PIN_CODE:
            with Connection() as (cursor, connection):
                cursor.execute("DELETE FROM passwords WHERE przeznaczenie = %s", (self.purpose,))
            self.dismiss(self.purpose)
        else:
            pin_input.value = ""
            pin_input.placeholder = "Try again"

    @on(Button.Pressed, "#cancel-button")
    def close_modal(self) -> None:
        self.dismiss(None)
