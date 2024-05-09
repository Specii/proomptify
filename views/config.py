import os
import shutil
from random import choice
from rich.console import Console
from rich.padding import Padding

from header import Header
from prompt import Prompt


class Auth:
    def __init__(self):
        self.console = Console()

    def initialize(self):
        Header()

        self.console.print(f' Configuration ', style='bold red', justify='center')

Auth()