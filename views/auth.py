from rich.console import Console
from rich.panel import Panel

from auxiliary.terminal import Terminal
from views.header import Header
from views.prompt import Prompt


class Auth:
    def __init__(self):
        self.console = Console(record=True)
        self.terminal = Terminal()

        self.header = Header()
        self.prompt = Prompt()

    def menu(self, message=None):
        self.terminal.clear()

        with self.console.capture() as capture:
            for line in self.header.content():
                self.console.print(line)

            self.console.print(
                Panel(
                    '[white]\n{ 1 } Sign In  \n[white]{ 2 } Sign Up  \n[/white]',
                    title='{+} Authenticate {+}',
                    subtitle='[dim]Please select an option to proceed[/dim]',
                    width=93
                ),
                style='purple',
                justify='center'
            )

        print(capture.get())

        capture_res = capture.get().split('\n')
        content_len = len(capture_res) + 2

        if message:
            message = f'[red]Authenticate | {message}[/red]'
        else:
            message = f'Authenticate'

        user_response = self.prompt.response(
            message=message,
            char_input=True,
            padding=self.console.height - content_len
        )

        return user_response

    def signin(self):
        self.terminal.clear()

        with self.console.capture() as capture:
            for line in self.header.content():
                self.console.print(line)

        content = capture.get()

        print(content)

        capture_res = capture.get().split('\n')
        content_len = len(capture_res) + 2

        username = self.prompt.response(
            message='Username',
            padding=self.console.height - content_len
        )

        self.terminal.clear()

        print(content)

        password = self.prompt.response(
            message='Password',
            is_password=True,
            padding=self.console.height - content_len
        )

        self.terminal.clear()

        return username, password

    def signup(self):
        self.terminal.clear()

        with self.console.capture() as capture:
            for line in self.header.content():
                self.console.print(line)

        content = capture.get()

        print(content)

        capture_res = capture.get().split('\n')
        content_len = len(capture_res) + 2

        username = self.prompt.response(
            message='Username',
            padding=self.console.height - content_len
        )

        self.terminal.clear()

        print(content)

        password = self.prompt.response(
            message='Password',
            is_password=True,
            padding=self.console.height - content_len
        )

        self.terminal.clear()

        print(content)

        license_key = self.prompt.response(
            message='License Key',
            padding=self.console.height - content_len
        )

        self.terminal.clear()

        return username, password, license_key
