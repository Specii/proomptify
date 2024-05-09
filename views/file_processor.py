from time import sleep

from rich.console import Console
from rich.panel import Panel
from tkinter import Tk, filedialog

from controller import SupervisorController
from auxiliary.terminal import Terminal
from views.header import Header
from views.prompt import Prompt


class FileProcessor:
    def __init__(self):
        self.console = Console(record=True)
        self.terminal = Terminal()

        self.header = Header()
        self.prompt = Prompt()

    def initialize(self):
        self.terminal.clear()

        with self.console.capture() as capture:
            for line in self.header.content():
                self.console.print(line)

            self.console.print(
                Panel(
                    '[white]PLEASE SELECT YOUR BASE USING THE FILE EXPLORER[/white]',
                    title='{+} Editor {+}',
                    width=93
                ),
                style='purple',
                justify='center'
            )

        print(capture.get())

        root = Tk()
        root.withdraw()
        root.update()

        file_path = filedialog.askopenfilename(
            title='Please select your base',
            filetypes=[
                ('Text Files', '*.txt'),
                ('All Files', '*.*')
            ]
        )

        root.destroy()
        self.terminal.clear()

        return file_path
