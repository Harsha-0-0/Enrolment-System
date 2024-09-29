from SubSystem import SubSystem

class AdminSubSystem(SubSystem):
    def __init__(self, database):
        super().__init__(database)
    def launch(self):
        print("Test " + self.database.db_file_name)