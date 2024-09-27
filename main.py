import json
from json.decoder import JSONDecodeError

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
       

class SubSystem:
    def __init__(self):
        option = input("Enter s for student or a for admin: ")
        if option == 's':
            print('Student')
            Register()
        elif option == 'a':
            print('admin')
        else:
            print('Invalid option')


# Main execution
if __name__ == "__main__":
    subSystem=SubSystem()


