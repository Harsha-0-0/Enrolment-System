from colorama import Fore
from SubSystem import SubSystem
import json
from Stduent.Student import student

class StudentSubSystem(SubSystem):
    def __init__(self, database):
        super().__init__(database, Fore.YELLOW)
    def launch(self):
        self.print_line("Welcome to Student SubSystem")
        while True:
                option = input("(1) Register Student, (2) Login Student, (99) ExitSubSystem: ")
                if option == '1':
                    self.register_student_prompt()
                elif option == '2':
                    self.login_student_prompt()           
                elif option == '99':
                    self.print_line('Exiting SubSystem')
                    break
                else:
                    self.print_error('Invalid option')    
    def register_student_prompt(self):
        self.print_line('Hello1') 
        # TODO UserStory-101, Sign up with a valid email and password, 
        # TODO UserStory-102, Verify email address in the “firstname.lastname@university.com” format
        # TODO UserStory-103, Validate password against displayed criteria
        # TODO UserStory-103, Automatically generate a unique 6-digits student ID during registration
        # TODO UserStory-107, Add name to student
        stu =  student()
        passw = 'password here'
        emailadd = 'email add here'
        if not stu.verify_student_email(emailadd):
            print('invalid email address')
            # may need to re-enter the email address
        if not stu.verify_student_password(passw):
            print('invalid password format')
            # may need to re-enter the password

        stu.set_name('any_name')

        # generate unique student id, need get current number of students or ids

    def login_student_prompt(self):
        self.print_line('Hello2') 
        # TODO UserStory-105, Log in with registered email and password
        # TODO UserStory-106, Display specific error messages for incorrect login details
        self.print_line("Login Successful")
        while True:
                option = input("(1) View My Enrolments, (2) Enrol in Subject, (3) Withdraw from Subject, (4) Change Password, (99) ExitSubSystem: ")
                if option == '1':
                    self.view_my_enrolments_prompt()
                elif option == '2':
                    self.enrol_in_subject_prompt()       
                elif option == '3':
                    self.withdraw_from_subject_prompt()   
                elif option == '4':
                    self.change_password_prompt()          
                elif option == '99':
                    self.print_line('Exiting SubSystem')
                    break
                else:
                    self.print_error('Invalid option') 
    def view_my_enrolments_prompt(self):
        self.print_line('Hello1') 
        # TODO UserStory-301, View list of enrolled subjects 
    def enrol_in_subject_prompt(self):
        self.print_line('Hello2')
        # TODO UserStory-201, Automatically Enrol in subjects   
          
    def withdraw_from_subject_prompt(self):
        self.print_line('Hello3')
        # TODO UserStory-302, Remove a subject from enrolment list  
    def change_password_prompt(self):
        self.print_line('Hello4')
        # TODO UserStory-205, Change the password 


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
            self.print('Email ID already exists. Please log in or Register with new Email ID \n')
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

if __name__ == '__main__':
    stu = student()
    stu.set_name('lol')
    print(stu.name)