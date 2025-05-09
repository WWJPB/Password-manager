from textual.app import App
from textual.events import Mount
from db import Database
from screens.login import LoginScreen, LoginSuccess
from screens.main_screen import MainScreen


class PasswordManagerApp(App):
    CSS_PATH = "styles/main.scss"

    def on_mount(self, event: Mount) -> None:
        self.db = Database()
        self.push_screen(LoginScreen())

    def on_login_success(self, _: LoginSuccess) -> None:
        self.pop_screen()
        self.push_screen(MainScreen())


if __name__ == "__main__":
    PasswordManagerApp().run()

