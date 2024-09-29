from SubSystem import SubSystem
import json

class StudentSubSystem(SubSystem):
    def __init__(self, database):
        super().__init__(database)
    def launch(self):
        print("Test " + self.database.db_file_name)

class Register: 
    def __init__(self):
        self.email = input("Enter email: ")
        self.password = input("Enter Password: ") 
        RegisteredStudents(self.email, self.password).__checkStudent__()
    
class RegisteredStudents:

    def __init__(self, email, password):
        self.studentList = dict()

        try:
            with open("student_list.json", 'r') as s:
                self.studentList = json.loads(s.read())
        except json.decoder.JSONDecodeError:
            pass
        
        self.email =email
        self.password = password
    
    def __checkStudent__(self):
        if self.email in self.studentList:
            print('Email ID already exists. Please log in or Register with new Email ID')
        else:
            self.add_student()

    def add_student(self): 
        new = {self.email:self.password}

        try:
            with open("student_list.json", 'w') as s:
                self.studentList.update(new)
                json.dump(self.studentList, s, indent=4)
        except json.decoder.JSONDecodeError:
            pass