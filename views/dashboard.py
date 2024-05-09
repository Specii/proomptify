import sys
from datetime import datetime
from time import sleep

from rich.console import Console
from rich.panel import Panel

from auxiliary.terminal import Terminal
from controller import SupervisorController
from views.header import Header
from views.prompt import Prompt
from views.file_processor import FileProcessor


class Dashboard:
    def __init__(self):
        self.console = Console(record=True)
        self.terminal = Terminal()

        self.header = Header()
        self.prompt = Prompt()
        self.file_processor = FileProcessor()

    @staticmethod
    def format_timestamp(timestamp):
        return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    def initialize(self, user, message=None):
        self.terminal.clear()

        username = user.username
        ip_address = user.ip
        subscriptions = user.subscriptions
        days_remaining = 0

        for i, license_data in enumerate(subscriptions, start=1):
            days_remaining = license_data.get('timeleft') // (60 * 60 * 24)

        if days_remaining <= 3:
            days_color = 'bright_red'
        elif days_remaining <= 7:
            days_color = 'bright_yellow'
        else:
            days_color = 'bright_green'

        with self.console.capture() as capture:
            for line in self.header.content(
                    message=f'[dim]Welcome back,[/dim] [gold1 bold dim]{username}[/gold1 bold dim]'):
                self.console.print(line)

            self.console.print(f'IP Address: [bold]{ip_address}[/bold]', style='purple dim', justify='center')
            self.console.print(f'Access Remaining: [{days_color} bold]{days_remaining} Days[/{days_color} bold]',
                               style='purple dim', justify='center')

            self.console.print('')

            self.console.print(
                Panel(
                    '[white]\n{ 1 } Base Editor  \n{ 2 } Duplicate Remover  \n{ 3 } Shuffle base  \n{ 4 } Settings  \n\n{ x } Sign Out  \n[/white]',
                    title='{+} Supervisor {+}',
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
            message = f'[red]Supervisor | {message}[/red]'
        else:
            message = f'Supervisor'

        user_response = self.prompt.response(
            user=user.username,
            message=message,
            char_input=True,
            padding=self.console.height - content_len
        )

        if user_response == '1':
            if file_path := self.file_processor.initialize():
                if SupervisorController().launch(input_file=file_path):
                    return self.initialize(user)
            else:
                return self.initialize(user, 'Please select a valid base')
        elif user_response == '2':
            return self.initialize(user, 'Duplicate remover will be added on the next update')
        elif user_response == '3':
            return self.initialize(user, 'Shuffle base will be added on the next update')
        elif user_response == '4':
            return self.initialize(user, 'Settings will be added on the next update')
        elif user_response == 'x':
            self.terminal.clear()
            for line in self.header.content(message=f'[purple]Thank you for choosing Synthebase. Have a great day {user.username}![/purple]'):
                self.console.print(line)
            sleep(5)
            exit()
        else:
            return self.initialize(user, 'Please select a valid option')
