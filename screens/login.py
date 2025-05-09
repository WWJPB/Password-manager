from textual import events, on
from textual.screen import Screen
from textual.widgets import Input, Button, Static, Header
from textual.containers import Container, Center, Vertical
from textual.app import ComposeResult
from textual.message import Message


PIN_CODE = "1234"

class LoginSuccess(Message):
    """Login successful"""

class LoginScreen(Screen):
    CSS_PATH = '../styles/login.scss'

    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(id="top_bar"),
            Container(
                Container(
                    Static("PIN:", id="label"),
                    Input(password=True, id="pin_input"),
                    Center(Button(label='Login', id="login_button", variant="success")),
                    id="form"
                ),
                id="outer"
            ),
            Container(id="bottom_bar")
        )


    @on(Button.Pressed)
    def on_button_pressed(self) -> None:
        pin_input = self.query_one("#pin_input", Input)
        if pin_input.value == PIN_CODE:
            self.post_message(LoginSuccess())
        else:
            pin_input.value = ""
            pin_input.placeholder = "Try again"

    def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.on_button_pressed()
