#The Database is a service class that runs operations against the InMemoryDatabase and stores the information in a data file and a single one is created by the SubSystem at runtime
class Database:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name