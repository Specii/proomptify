from sys import executable, exit
from os import path, makedirs, getcwd
from subprocess import run, DEVNULL
from logging import basicConfig, ERROR, error
from time import sleep
import importlib

from auxiliary.terminal import Terminal


class VirtualEnvironmentSetup:
    def __init__(self):
        self.terminal = Terminal()
        self.modules = ['requests', 'pywin32', 'pywin32', 'psutil']
        self.retry_attempts = 3

        log_folder_path = path.join(getcwd(), 'logs')
        log_file_path = path.join(log_folder_path, 'log.txt')

        if not path.exists(log_folder_path):
            makedirs(log_folder_path)

        basicConfig(filename=log_file_path, level=ERROR)

    def __setup_module(self, module):
        current_attempt = 0

        while current_attempt < self.retry_attempts:
            try:
                importlib.import_module(module)
                return True
            except (ModuleNotFoundError, ImportError):
                try:
                    run(
                        args=[executable, '-m', 'pip', 'install', module, '--quiet'],
                        stdout=DEVNULL,
                        stderr=DEVNULL
                    )

                    return True
                except Exception as install_error:
                    error(install_error)

                current_attempt += 1

        return False

    def initialize(self):
        self.terminal.clear()

        if self.__setup_module('rich'):
            from rich.console import Console
            from rich.progress import Progress, BarColumn
            from views.header import Header

            console = Console()
            header = Header()

            for line in header.content():
                console.print(line)

            padding = (console.width - 93) // 2 - 1

            with Progress(
                ' ' * padding,
                BarColumn(
                    bar_width=93,
                    complete_style='purple',
                    finished_style='purple'
                )
            ) as progress:
                task = progress.add_task(
                    description='',
                    total=len(self.modules)
                )

                for module in self.modules:
                    if not self.__setup_module(module):
                        print('Environment setup anomaly occurred')
                        sleep(3)
                        exit()

                    progress.update(task, advance=1)

                return True
        return False
