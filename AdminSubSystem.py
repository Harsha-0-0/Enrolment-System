class AdminSubSystem:
    def __init__(self, database):
        self.database = database
    def launch(self):
        print("Hello" + self.database.db_file_name)