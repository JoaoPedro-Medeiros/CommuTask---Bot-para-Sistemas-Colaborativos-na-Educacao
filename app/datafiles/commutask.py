from os.path import join, dirname, abspath

class DatafileCommuTask:

    def __init__(self):
        self.__token = self.__read_token()

    def __read_token(self) -> str | None :
        try:
            with open(join(dirname(abspath(__file__)), "token.txt")) as file:
                print(file)
                str_in = file.read()
        except FileNotFoundError:
            str_in = None
        return str_in

    def get_token(self) -> str:
        return self.__token