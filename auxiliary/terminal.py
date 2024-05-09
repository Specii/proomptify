from os import system, name
from shutil import get_terminal_size
from rich.text import Text


class Terminal:
    @staticmethod
    def width():
        return get_terminal_size().columns

    @staticmethod
    def height():
        return get_terminal_size().lines

    @staticmethod
    def clear():
        system('cls' if name == 'nt' else 'clear')

    def center(self, lines):
        if isinstance(lines, str):
            lines = [lines]

        max_plain_text_length = max(len(Text.from_markup(line).plain) for line in lines)

        return (self.width() - max_plain_text_length) // 2

    def bottom(self, view_height):
        return self.height() - view_height - 6
