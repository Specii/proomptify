import sys
from rich.console import Console
from rich.padding import Padding
from rich.text import Text

try:
    import termios
    import tty
except ImportError:
    import msvcrt

    termios = None
    tty = None


class Prompt:
    def __init__(self):
        self.console = Console()

    @staticmethod
    def __char_input_unix():
        file_descriptor = sys.stdin.fileno()
        original_settings = termios.tcgetattr(file_descriptor)

        try:
            tty.setraw(file_descriptor)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, original_settings)

        return char

    def __char_input_windows(self):
        return msvcrt.getch().decode('utf-8')

    def response(self, user='Root', message='#', char_input=False, is_password=False, padding=0):
        renderable = f'[purple dim] ╭─[ [/purple dim][purple]{user}@Synthebase[/purple][purple dim] ]──([/purple dim][white] {message} [/white][purple dim])[/purple dim]'

        self.console.print(Padding(renderable, (padding - 1, 0, 0, 0)))
        self.console.print(Text(f' │ ', style='purple dim'))

        if char_input:
            self.console.print(Text(' ╰───', style='purple dim'), end='')
            self.console.print(Text('(~)', style='purple'), end='')
            self.console.print(Text(' ', style='purple dim'), end='')

            try:
                if sys.platform.startswith('win'):
                    user_res = self.__char_input_windows()
                else:
                    user_res = self.__char_input_unix()
            except UnicodeDecodeError:
                user_res = ''
        else:
            user_res = self.console.input('[purple dim] ╰───[/purple dim][purple](~)[/purple] ', password=is_password)

        return user_res
