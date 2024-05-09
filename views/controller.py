from os import environ

from views.header import Header
from views.prompt import Prompt


class ViewController:
    def __init__(self):
        environ['TERM'] = 'xterm'

    @staticmethod
    def header():
        return Header()

    @staticmethod
    def prompt():
        return Prompt().initialize('Please drag & drop your base')


view = ViewController()
print(view.prompt())


# TODO: finish this page for better readebility