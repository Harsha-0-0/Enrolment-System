from colorama import Fore
from SubSystem import SubSystem
from Subject.Subject import subject

class AdminSubSystem(SubSystem):
    def __init__(self, database):
        super().__init__(database, Fore.BLUE)
    def launch(self):
        self.print_line("Welcome to Admin SubSystem ")
        while True:
            option = input("(1) View all Students, (2) Remove Student, (3) View all Subjects, (4) Create Subject, (5) View by Grade, (6) Clear Student Database, (99) ExitSubSystem: ")
            if option == '1':
                self.view_all_student_prompt()
            elif option == '2':
                self.remove_student_prompt()
            elif option == '3':
                self.view_all_subjects_prompt()
            elif option == '4':
                self.create_subject_prompt()
            elif option == '5':
                self.view_by_grade_prompt()
            elif option == '6':
                self.clear_database_prompt()            
            elif option == '99':
                self.print_line('Exiting SubSystem')
                break
            else:
               self.print_error('Invalid option')   
    def view_all_student_prompt(self):
        self.print_line('Hello1') 
        # TODO UserStory-401 @Harsha, View list of all registered students
    def remove_student_prompt(self):
        self.print_line('Hello2') 
        # TODO UserStory-404, Remove individual students from the system
    def view_all_subjects_prompt(self):
        self.print_line('Hello3') 
        # TODO @, 
    def create_subject_prompt(self):
        self.print_line('Hello4') 
        # TODO @, 
        sub = subject()
        sub.set_subject_name('any_name')
    def view_by_grade_prompt(self):
        self.print_line('Hello5') 
        # TODO UserStory-402, Organize and view students by grade
        # TODO UserStory-403, Categorize students as PASS or FAIL based on marks
    def clear_database_prompt(self):
        self.print_line("Hello6") 
<<<<<<< HEAD
        # TODO UserStory-405, Clear the entire students.data file from the system
=======
        # TODO UserStory-405, Clear the entire students.data file from the system
>>>>>>> origin/main
