import json
import random
from colorama import Fore
import pandas as pd
from tabulate import tabulate
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

    #Verifying Password criteria
    def verify_student_password(self, password):
        if not password[0].isupper():
            return False

        letter_count = sum(char.isalpha() for char in password)
        digit_count = sum(char.isdigit() for char in password)

        if letter_count < 5 or digit_count < 3:
            return False

        return True


    def register_student_prompt(self):
        while True:
            student = Student()
            self.print_line('Please enter email and password to register')
            self.email = input("Enter email: ")
            self.password = input("Enter Password: ") 
            self.name = input("Enter Name: ")
            
            #verifying the mail and password
            valid_mail = student.verify_student_email(self.email)
            valid_pwd = self.verify_student_password(self.password)
                
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
        

        #Check if student exists. If it is a new email, create generate student id and add to the data_file.json file
        student_list = self.database.get_student_list()
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
                student_list = self.database.get_student_list()
                email_list = [d['email'] for d in student_list]
                if(self.email in email_list):
                    for i in email_list:
                        if(i == self.email):
                            self.index = email_list.index(i)
                    pwd_list = [d['password'] for d in student_list]
                    pwd = pwd_list[self.index]
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
                "(1) View My Enrolments, (2) Enrol in Subject, (3) Withdraw from Subject, (4) Change Password, (99) Exit SubSystem: ")
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


    # UserStory-301, View list of enrolled subjects
    def view_my_enrolments_prompt(self):
        self.print_line("You are currently enrolled in the following subjects:")
        self.view_enrolled_subjects()

    def view_enrolled_subjects(self):
        self.print_line("Viewing enrolled subjects.")
        
        #student has current student data
        student = self.database.get_student(self.index)
        enrolled_subjects = student.get('enrolments',[])

        if not enrolled_subjects:
            self.print_line("No subjects enrolled.")
            return

        self.print_line("You are currently enrolled in the following subjects:")
        cols = ['subject_id', 'subject_name']
        df = pd.DataFrame(data=enrolled_subjects, columns=cols)        
        self.print_line(tabulate(df , tablefmt="github", headers=["Subject ID", "Subject Name"]))


    # UserStory-201, Automatically Enrol in subjects

    def enrol_in_subject_prompt(self):
        self.print_line("Automatically Enrol in subjects is in progress.")

        
        #student has current student data
        student = self.database.get_student(self.index)
         
        enrolled_subjects = []
        subject_id_list = []
        if student.get('enrolments',[]):
            enrolled_subjects.__iadd__(student.get('enrolments',[]))
            
            subject_id_list = [d['subject_id'] for d in enrolled_subjects]
              
        if enrolled_subjects:
            if self.database.countList(enrolled_subjects) >= 4:
                self.print_error("You are already enroled in 4 subjects. Enrolment for more than 4 subjects is not allowed.")
                return
        

        available_subjects = [sub['subject_id'] for sub in self.database.get_data()['subjects'] if sub['subject_id'] not in subject_id_list]

        if not available_subjects:
            self.print_error("No available subjects to enrol in.")
            return

        subjects_to_enrol = random.sample(available_subjects, min(4 - len(enrolled_subjects), len(available_subjects)))

        if subjects_to_enrol:
            for subject_id in subjects_to_enrol:
                self.database.enrol_student(student.get('student_id'), subject_id)
            self.database._save_changes_to_data_file()
            self.print_line("Successfully enrolled in subjects automatically!")
        else:
            self.print_error("Enrolment for more than 4 subjects is not allowed.")    



    # UserStory-302, Remove a subject from enrolment list
    def withdraw_from_subject_prompt(self):
        student = self.database.get_student(self.index)
        self.print_line("Withdrawing a subject from enrolment list.")
        subject_id = input("Enter the subject ID you want to withdraw from: ")
        
        if self.database.unenrol_student(student.get('student_id'), subject_id):
            self.print_line("Successfully withdrawn from the subject.")
        else:
            self.print_error("Failed to withdraw. Please check your subject ID.")



    # UserStory-205, Change the password
    def change_password_prompt(self):
        self.print_line("Change the password")
        
        current_password = input("Enter your current password: ")
        
        #student has current student data
        student = self.database.get_student(self.index)

        if student.get('password') == current_password:
            new_password = input("Enter new password: ")
            
            if self.verify_student_password(new_password):
                if self.database.change_student_pw(student.get('student_id'), new_password):
                    self.database._save_changes_to_data_file() 
                    self.print_line("Password changed successfully!")
                else:
                    self.print_error("Failed to change password.")
            else:
                self.print_error("New password does not meet the criteria.")
        else:
            self.print_error("Invalid current password.")
