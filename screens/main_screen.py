from textual.screen import Screen
from textual.widgets import Button, ContentSwitcher
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from screens.add_password import AddPasswordScreen
from screens.manage_passwords import ManagePasswordsScreen

class MainScreen(Screen):
    CSS_PATH = "../styles/main_screen.scss"

    def __init__(self):
        super().__init__(id="main")

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Button("Add Password", id="tab-add", classes="tab-button"),
                Button("Manage Passwords", id="tab-manage", classes="tab-button"),
                id="nav"
            ),
            ContentSwitcher(
                AddPasswordScreen(id="tab-add-view"),
                ManagePasswordsScreen(id="tab-manage-view"),
                id="main_content"
            )
        )

    def on_mount(self) -> None:
        self.query_one(ContentSwitcher).current = "tab-add-view"
        self.set_active_tab("tab-add")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in ["tab-add", "tab-manage"]:
            self.query_one(ContentSwitcher).current = f"{event.button.id}-view"
            self.set_active_tab(event.button.id)

    def set_active_tab(self, active_id: str) -> None:
        for btn in self.query(".tab-button"):
            btn.remove_class("active")
        self.query_one(f"#{active_id}", Button).add_class("active")
