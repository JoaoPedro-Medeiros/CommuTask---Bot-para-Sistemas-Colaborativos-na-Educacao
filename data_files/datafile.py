import discord as client
from os.path import join, dirname, abspath

class Datafile_CommuTask:

    def __init__(self):
        self.token = self.__read_token()

    def __read_token(self) -> str | None :
        try:
            with open(join(dirname(abspath(__file__)), "token.txt")) as file:
                print(file)
                str_in = file.read()
        except FileNotFoundError:
            str_in = None
        return str_in