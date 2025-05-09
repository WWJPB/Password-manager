from textual.containers import VerticalScroll, Vertical, HorizontalGroup
from textual.widgets import Button, Static
from textual.app import ComposeResult
from textual import on

from screens.ask import Ask
from screens.delete import DeleteAsk
from db import Connection

class ButtonPair(Static):
    def __init__(self, purpose: str) -> None:
        super().__init__()
        self.purpose = purpose

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Button(label=self.purpose, variant="primary", classes="password", id=f"password-{self.purpose}")
            yield Button(label="🗑", variant="error", classes="delete", id=f"delete-{self.purpose}")

class ManagePasswordsScreen(Static):

    DEFAULT_CSS = """
    .center-container {
        width: 100%;
        align: center middle;
        background: #141414;
    }

    .password-box {
        height: 22;
        width: 40;
        border: round white;
        padding: 1;
    }

    #title {
        align: center middle;
        color: white;
        height: 3;
    }

    VerticalScroll {
        height: 1fr;
        scrollbar-color: white;
    }

    Button {
        height: 3;
        content-align: center middle;
        text-style: bold;
    }

    .password {
        min-width: 25;
    }

    .delete {
        min-width: 5;
        padding: 0;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(classes="center-container"):
            with Vertical(classes="password-box"):
                yield Static("Manage your passwords here:", id="title")
                self.password_list = VerticalScroll(id="password-scroll")
                yield self.password_list

    def on_mount(self) -> None:
        self.refresh_passwords()

    def on_show(self) -> None:
        self.refresh_passwords()

    def refresh_passwords(self) -> None:
        with Connection() as (cursor, connection):
            cursor.execute("SELECT przeznaczenie FROM passwords")
            rows = cursor.fetchall()
        self.password_list.remove_children()
        for row in rows:
            purpose = row[0]
            self.password_list.mount(ButtonPair(purpose))
        self.refresh()

    @on(Button.Pressed)
    async def handle_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if "password" in event.button.classes and button_id.startswith("password-"):
            purpose = button_id.removeprefix("password-")
            pin = await self.app.push_screen(Ask(purpose))
            if pin:
                self.refresh_passwords()
        elif "delete" in event.button.classes and button_id.startswith("delete-"):
            purpose = button_id.removeprefix("delete-")
            confirmed = await self.app.push_screen(DeleteAsk(purpose))
            if confirmed:
                self.refresh_passwords()
