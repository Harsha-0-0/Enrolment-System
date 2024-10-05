from abc import ABC
from colorama import Fore
from Database import Database

# The abstract SubSystem is just a parent class containing the duplicate operations


class SubSystem(ABC):
    def __init__(self, database: Database, print_colour: str):
        self.database = database
        self.print_colour = print_colour

    def print_error(self, message):
        print(Fore.RED + message + self.print_colour)

    def print_line(self, message):
        print(self.print_colour + message)
