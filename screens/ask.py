from textual import on
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static
from textual.containers import Container, Vertical, Horizontal
from textual.app import ComposeResult
from screens.update import UpdatePasswordScreen
from db import Connection

PIN_CODE = "1234"

class Ask(ModalScreen[str]):
    CSS_PATH = "../styles/ask.scss"

    def __init__(self, purpose: str) -> None:
        super().__init__()
        self.purpose = purpose

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            with Vertical(id="modal-box"):
                yield Input(placeholder="Input PIN", password=True, id="pin-id")
                yield Static(id="result-label")
                with Horizontal(id="button-row"):
                    update = Button("Update", id="update-button", variant="success")
                    update.styles.opacity = 0
                    update.disabled = True
                    yield update
                    yield Button("Cancel", id="cancel-button", variant="error")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def check_pin(self, event: Input.Submitted) -> None:
        pin_input = event.input
        result_label = self.query_one("#result-label", Static)
        close_btn = self.query_one("#update-button", Button)

        if pin_input.value == PIN_CODE:
            with Connection() as (cursor, connection):
                cursor.execute("SELECT HASLO FROM passwords WHERE przeznaczenie = %s", (self.purpose,))
                result = cursor.fetchone()

            if result:
                result_label.update(f"Password: {result[0]}")
            close_btn.styles.opacity = 1
            close_btn.disabled = False
            pin_input.display = False
        else:
            pin_input.value = ""
            pin_input.placeholder = "Try again"

    @on(Button.Pressed, "#update-button")
    def go_to_update(self) -> None:
        def after_update():
            self.app.push_screen(Ask(self.purpose))

        self.dismiss()
        self.app.push_screen(UpdatePasswordScreen(self.purpose, after_update))

    @on(Button.Pressed, "#cancel-button")
    def cancel_and_return(self) -> None:
        self.dismiss()
