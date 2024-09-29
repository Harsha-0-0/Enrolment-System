import json
from colorama import Fore, Style
from json.decoder import JSONDecodeError
from AdminSubSystem import AdminSubSystem
from Database import Database
from StudentSubSystem import StudentSubSystem

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

# Main execution
if __name__ == "__main__":
    while True:
        database = Database("student_list.json")
        option = input(Style.RESET_ALL + "Enter 's' for student or 'a' for admin or 'e' for exit: ")
        if option == 's':
            print(Fore.BLUE + 'Student')
            student_console = StudentSubSystem(database)
            student_console.launch()
        elif option == 'a':
            print(Fore.YELLOW + 'admin')
            admin_console = AdminSubSystem(database)
            admin_console.launch()
        elif option == 'e':
            print('exit')
            break
        else:
            print(Fore.RED + 'Invalid option')