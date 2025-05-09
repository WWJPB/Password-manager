from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Input, Button
from textual.containers import Container, Vertical, Center
from textual import on

from db import Connection

class UpdatePasswordScreen(Screen):

    CSS_PATH = "../styles/update.scss"

    def __init__(self, purpose: str, on_success_callback=None) -> None:
        super().__init__()
        self.purpose = purpose
        self.on_success_callback = on_success_callback

    def compose(self) -> ComposeResult:
        with Container(id="update-container"):
            with Vertical(id="update-box"):
                yield Input(placeholder="New password", id="new-password", password=True)
                yield Input(placeholder="Confirm password", id="confirm-password", password=True)
                yield Static("", id="error-message")
                yield Center(Button("Update", id="submit-update", variant="success"))

    @on(Button.Pressed, "#submit-update")
    def handle_update(self) -> None:
        new_pw = self.query_one("#new-password", Input).value
        confirm_pw = self.query_one("#confirm-password", Input).value
        error_msg = self.query_one("#error-message", Static)

        if not new_pw or not confirm_pw:
            error_msg.update("Both fields are required.")
            return

        if new_pw != confirm_pw:
            error_msg.update("Passwords do not match.")
            return

        try:
            with Connection() as (cursor, connection):
                cursor.execute(
                    "UPDATE passwords SET HASLO = %s WHERE przeznaczenie = %s",
                    (new_pw, self.purpose),
                )
            self.app.pop_screen()
            if self.on_success_callback:
                self.on_success_callback()
        except Exception as e:
            error_msg.update(f"DB Error: {e}")
