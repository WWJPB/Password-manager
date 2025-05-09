from textual.containers import Vertical, Container, Center
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult
from textual import on

from db import Connection

class AddPasswordScreen(Static):
    CSS_PATH = "../styles/add_password.scss"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
                Container(
                    Static("Add your password here: ", id="title"),
                    Input(placeholder="Insert media", id="login"),
                    Input(placeholder="Insert your password", password=True, id="password"),
                    Center(Button(label="Add", id="add", variant="success")),
                    id="form"
                ),
                id="outer"
            ),
        )

    @on(Button.Pressed, "#add")
    def add_password_to_db(self) -> None:
        login_input = self.query_one("#login", Input).value.strip()
        password_input = self.query_one("#password", Input).value.strip()

        if (" " in login_input or " " in password_input or
            (login_input and login_input[0].isdigit()) or
            (password_input and password_input[0].isdigit())):
            self.query_one("#login", Input).value = ""
            self.query_one("#password", Input).value = ""
            self.query_one("#login", Input).placeholder = "No spaces / no digit first"
            self.query_one("#password", Input).placeholder = "No spaces / no digit first"
            return

        if login_input and password_input:
            try:
                with Connection() as (cursor, connection):
                    query = "INSERT INTO passwords(przeznaczenie, HASLO) VALUES (%s, %s)"
                    cursor.execute(query, (login_input, password_input))
                self.query_one("#login", Input).value = ""
                self.query_one("#password", Input).value = ""
                self.query_one("#login", Input).placeholder = "Added!"
                self.query_one("#password", Input).placeholder = "Added!"
            except Exception as e:
                self.query_one("#login", Input).placeholder = "Error!"
                self.query_one("#password", Input).placeholder = "Error!"
                print("DB Error:", e)
        else:
            self.query_one("#login", Input).placeholder = "Required"
            self.query_one("#password", Input).placeholder = "Required"
