import json
from colorama import Fore
from SubSystem import SubSystem
from Student.Student import Student
from datetime import datetime


class StudentSubSystem(SubSystem):
    def __init__(self, database):
        super().__init__(database, Fore.YELLOW)

    def launch(self):
        self.print_line("Welcome to Student SubSystem")
        while True:
            option = input("(1) Register Student, (2) Login Student, (99) ExitSubSystem: ")
            if option == "1":
                self.register_student_prompt()
            elif option == "2":
                self.login_student_prompt()
            elif option == "99":
                self.print_line("Exiting SubSystem")
                break
            else:
                self.print_error("Invalid option")

    # TODO UserStory-101, Sign up with a valid email and password,
    # TODO UserStory-102, Verify email address in the “firstname.lastname@university.com” format
    # TODO UserStory-103, Validate password against displayed criteria
    # TODO UserStory-103, Automatically generate a unique 6-digits student ID during registration
    # TODO UserStory-107, Add name to student
    def register_student_prompt(self):
        while True:
            student = Student()
            self.print_line('Please enter email and password to register')
            self.email = input("Enter email: ")
            self.password = input("Enter Password: ") 
            self.name = input("Enter Name: ")
            
            #verifying the mail and password
            valid_mail = student.verify_student_email(self.email)
            valid_pwd = student.verify_student_password(self.password)
                
            if valid_mail and valid_pwd:
                break
            elif not valid_mail and not valid_pwd:
                self.print_error('The email address and the password is not valid. Please try again.')
            elif not valid_mail:
                self.print_error('The email address is not valid. Please try again.')
            elif not valid_pwd:
                self.print_error('The password is not valid. Please try again.')

        #setting values to student
        student.email = self.email
        student.password = self.password
        student.name = self.name
        
        #Getting data from data_file.json
        self.data = self.database.get_data()

        #Check if student exists. If it is a new email, create generate student id and add to the data_file.json file
        student_list = self.data['students']
        email_list = [d['email'] for d in student_list]

        if self.email in email_list:
            self.print_error('Email ID already exists. Please log in or Register with new Email ID')            
        else:   
            student.student_id = student.generate_student_id(student_list)
            student.registered_date = datetime.now().strftime('%Y-%m-%d')
            self.database.register_student(student)
            self.print_line("Registered successfully!") 
            

    # TODO UserStory-105, Log in with registered email and password
    # TODO UserStory-106, Display specific error messages for incorrect login details
    def login_student_prompt(self):
        while True:
            self.print_line('Please enter email and password to login.')
            self.email = input("Enter email: ")
            self.password = input("Enter Password: ") 
            if self.email and self.password != '':
                 #Reading data from data_file.json
                self.data = self.database.get_data()
                student_list = self.data['students']
                email_list = [d['email'] for d in student_list]
                if(self.email in email_list):
                    for i in email_list:
                        if(i == self.email):
                            index = email_list.index(i)

                    pwd_list = [d['password'] for d in student_list]
                    pwd = pwd_list[index]

                    if(pwd == self.password):
                        self.print_line('Login Successful')
                        break
                    else:
                        self.print_error('Password incorrect. Try Again.')
                else:
                    self.print_error('User does not exist. Please log in with correct credentials.')
            else:
                self.print_error('Please enter valid values for logging in.')
        while True:
            option = input(
                "(1) View My Enrolments, (2) Enrol in Subject, (3) Withdraw from Subject, (4) Change Password, (99) ExitSubSystem: ")
            if option == "1":
                self.view_my_enrolments_prompt()
            elif option == "2":
                self.enrol_in_subject_prompt()
            elif option == "3":
                self.withdraw_from_subject_prompt()
            elif option == "4":
                self.change_password_prompt()
            elif option == "99":
                self.print_line("Exiting SubSystem")
                break
            else:
                self.print_error("Invalid option")

    # TODO UserStory-301, View list of enrolled subjects
    def view_my_enrolments_prompt(self):
        self.print_line("UserStory-301, View list of enrolled subjects")

    # TODO UserStory-201, Automatically Enrol in subjects
    def enrol_in_subject_prompt(self):
        self.print_line("UserStory-201, Automatically Enrol in subjects")

    # TODO UserStory-302, Remove a subject from enrolment list
    def withdraw_from_subject_prompt(self):
        self.print_line("UserStory-302, Remove a subject from enrolment list")

    # TODO UserStory-205, Change the password
    def change_password_prompt(self):
        self.print_line("UserStory-205, Change the password")


class Register:
    def __init__(self):
        self.email = input("Enter email: ")
        self.password = input("Enter Password: ")
        RegisteredStudents(self.email, self.password).__checkStudent__()


class RegisteredStudents:

    def __init__(self, email, password):
        self.studentList = dict()

        try:
            with open("student_list.json", "r") as s:
                self.studentList = json.loads(s.read())
        except json.decoder.JSONDecodeError:
            pass

        self.email = email
        self.password = password

    def __checkStudent__(self):
        if self.email in self.studentList:
            print("Email ID already exists. Please log in or Register with new Email ID")
        else:
            self.add_student()

    def add_student(self):
        new = {self.email: self.password}

        try:
            with open("student_list.json", "w") as s:
                self.studentList.update(new)
                json.dump(self.studentList, s, indent=4)
        except json.decoder.JSONDecodeError:
            pass


if __name__ == "__main__":
    stu = Student()
    stu.set_name("lol")
    print(stu.name)