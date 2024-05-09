from rich.console import Console
from rich.padding import Padding

from auxiliary.terminal import Terminal


class Header:
    def __init__(self):
        self.console = Console()
        self.terminal = Terminal()

    def content(self, message=None):
        text = []

        logo = [
            '███████╗ ██╗   ██╗ ███╗   ██╗ ████████╗ ██╗  ██╗ ███████╗ ██████╗   █████╗  ███████╗ ███████╗',
            '██╔════╝ ╚██╗ ██╔╝ ████╗  ██║ ╚══██╔══╝ ██║  ██║ ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔════╝ ██╔════╝',
            '███████╗  ╚████╔╝  ██╔██╗ ██║    ██║    ███████║ █████╗   ██████╔╝ ███████║ ███████╗ █████╗  ',
            '╚════██║   ╚██╔╝   ██║╚██╗██║    ██║    ██╔══██║ ██╔══╝   ██╔══██╗ ██╔══██║ ╚════██║ ██╔══╝  ',
            '███████║    ██║    ██║ ╚████║    ██║    ██║  ██║ ███████╗ ██████╔╝ ██║  ██║ ███████║ ███████╗',
            '╚══════╝    ╚═╝    ╚═╝  ╚═══╝    ╚═╝    ╚═╝  ╚═╝ ╚══════╝ ╚═════╝  ╚═╝  ╚═╝ ╚══════╝ ╚══════╝',
        ]

        responsive_logo = [
            '███████╗',
            '██╔════╝',
            '███████╗',
            '╚════██║',
            '███████║',
            '╚══════╝'
        ]

        text.append('')
        text.append('')

        if message:
            logo.append(message)

        if self.console.width < 93:
            for line in responsive_logo:
                text.append(Padding(line, (0, self.terminal.center(line)), style='purple', expand=False))
        else:
            for line in logo:
                text.append(Padding(line, (0, self.terminal.center(line)), style='purple', expand=False))

        text.append('')
        text.append('')

        return text
