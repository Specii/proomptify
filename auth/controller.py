import sys
from os import path, getcwd
import json
from time import sleep

from requests import exceptions
import hashlib
from rich.console import Console
from rich.panel import Panel

from auth.keyauth import api
from auxiliary.terminal import Terminal
from views.auth import Auth
from views.header import Header


class Authenticator:
    def __init__(self):
        self.__auth_file_path = path.join(getcwd(), 'auth.json')
        self.console = Console()
        self.terminal = Terminal()
        self.header = Header()

        self.__username = None
        self.__password = None

        try:
            self.keyauth_app = api(
                name='Synthebase',
                ownerid='dMWQeKIum3',
                secret='60421e35dfb597a6bae879c9592e7df930f8fff93fcac14bd205bcca02373aab',
                version='1.0',
                hash_to_check=self.hash_to_check()
            )
        except exceptions.ConnectionError:
            pass

    @staticmethod
    def hash_to_check():
        md5_hash = hashlib.md5()

        with open(sys.argv[0], 'rb') as file:
            md5_hash.update(file.read())

        return md5_hash.hexdigest()

    def initialize(self):
        if path.isfile(self.__auth_file_path):
            try:
                with open(self.__auth_file_path, 'r') as f:
                    auth = json.load(f)

                    if auth.get('auth_username') == '':
                        if self.__user_auth_response():
                            return self.initialize()

                    elif hasattr(self, 'keyauth_app'):
                        self.__username = auth.get('auth_username')
                        self.__password = auth.get('auth_password')

                        if self.__username and self.__password:
                            if auth_response := self.keyauth_app.login(self.__username, self.__password):
                                return self.__auth_handler(auth_response)

                        return False
                    else:
                        print('Connection anomaly occurred. Please check your internet connection')
                        return False
            except Exception as e:
                print(e)
                return False
        else:
            self.__create_auth_file()
            return self.initialize()

    def __auth_handler(self, auth_response):
        if 'Success' in auth_response:
            try:
                self.__update_auth_file(self.__username, self.__password)
                return self.keyauth_app.user_data
            except Exception as e:
                print(e)
        elif 'Invalid Username' in auth_response or 'Invalid Password' in auth_response:
            self.__user_auth_response(message='Invalid credentials')
            return self.initialize()
        elif 'Username Taken' in auth_response:
            self.__user_auth_response(message='The username you\'ve chosen is already in use')
            return self.initialize()
        elif 'Invalid License' in auth_response:
            self.__user_auth_response(message='Invalid license key')
            sleep(3)
            return self.initialize()
        elif 'Invalid HWID' in auth_response:
            self.terminal.clear()

            for line in self.header.content():
                self.console.print(line)

            self.console.print(
                Panel(
                    '[white]INVALID HWID DETECTED | PLEASE CONTACT OUR SUPPORT TEAM[/white]',
                    title='{-} Error {-}',
                    width=93
                ),
                style='purple',
                justify='center'
            )

            self.console.print('\n\n')
            sleep(10)
            sys.exit()
        elif 'Used License' in auth_response:
            self.__user_auth_response(message='The license key is already in use')
            sleep(3)
            return self.initialize()
        elif 'Expired' in auth_response:
            self.terminal.clear()

            for line in self.header.content():
                self.console.print(line)

            self.console.print(
                Panel(
                    '[white]LICENSE KEY EXPIRED | PLEASE PURCHASE A NEW LICENSE KEY[/white]',
                    title='{-} Expired License {-}',
                    width=93
                ),
                style='purple',
                justify='center'
            )

            self.console.print('\n\n')
            sleep(10)
            sys.exit()
        elif 'Banned' in auth_response:
            self.console.clear()

            for line in self.header.content():
                self.console.print(line)

            self.console.print(
                Panel(
                    '[white]YOU HAVE BEEN BANNED BECAUSE YOU ARE A LIL BITCH[/white]',
                    title='{-} Banned {-}',
                    width=93
                ),
                style='purple',
                justify='center'
            )

            self.console.print('\n\n')
            sleep(10)
            sys.exit()
        else:
            self.console.clear()

            for line in self.header.content():
                self.console.print(line)

            self.console.print(
                Panel(
                    '[white]FATAL AUTHENTICATION ANOMALY OCCURRED[/white]',
                    title='{-} Error {-}',
                    width=93
                ),
                style='purple',
                justify='center'
            )

            self.console.print('\n\n')
            sleep(3)
            sys.exit()

    def __user_auth_response(self, message=None):
        auth = Auth()
        res = auth.menu(message=message)

        if res == '1':
            self.__username, self.__password = auth.signin()

            if self.__username and self.__password:
                if auth_response := self.keyauth_app.login(self.__username, self.__password):
                    return self.__auth_handler(auth_response)

            return self.__user_auth_response(message='Please enter valid credentials')

        elif res == '2':
            self.__username, self.__password, license_key = auth.signup()

            if self.__username and self.__password:
                if auth_response := self.keyauth_app.register(self.__username, self.__password, license_key):
                    return self.__auth_handler(auth_response)

            return self.__user_auth_response(message='Please enter valid credentials')
        else:
            return self.__user_auth_response(message='Please select a valid option')

    def __create_auth_file(self):
        credentials = {
            'auth_username': '',
            'auth_password': ''
        }

        try:
            with open(self.__auth_file_path, 'w') as auth_file:
                json.dump(credentials, auth_file, sort_keys=False, indent=4)

            return True
        except Exception as e:
            print(e)
            return False

    def __update_auth_file(self, username, password):
        try:
            with open(self.__auth_file_path, 'r') as auth_file:
                credentials = json.load(auth_file)

            credentials['auth_username'] = username
            credentials['auth_password'] = password

            with open(self.__auth_file_path, 'w') as auth_file:
                json.dump(credentials, auth_file, sort_keys=False, indent=4)

            return True
        except Exception as e:
            print(e)
            return False

# TODO: Add support for case where user tries to register a new account with an expired license - It's called No scubsciption in api but we need to get the error message when our license expired