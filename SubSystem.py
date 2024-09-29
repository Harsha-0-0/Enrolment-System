from abc import ABC

# The abstract SubSystem is just a parent class containing the duplicate operations
class SubSystem(ABC):
     def __init__(self, database):
        self.database = database