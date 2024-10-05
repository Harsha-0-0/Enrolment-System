from colorama import Fore
from tabulate import tabulate
from Database import Database
from SubSystem import SubSystem
from Subject.Subject import Subject


class AdminSubSystem(SubSystem):
    def __init__(self, database: Database):
        super().__init__(database, Fore.BLUE)

    def launch(self):
        self.print_line("Welcome to Admin SubSystem ")
        while True:
            option = input(
                "(1) View all Students, (2) Remove Student, (3) View all Subjects, (4) Create Subject, (5) View by Grade, (6) Clear Student Database, (99) ExitSubSystem: ")
            if option == "1":
                self.view_all_student_prompt()
            elif option == "2":
                self.remove_student_prompt()
            elif option == "3":
                self.view_all_subjects_prompt()
            elif option == "4":
                self.create_subject_prompt()
            elif option == "5":
                self.view_by_grade_prompt()
            elif option == "6":
                self.clear_database_prompt()
            elif option == "99":
                self.print_line("Exiting SubSystem")
                break
            else:
                self.print_error("Invalid option")

    # TODO UserStory-401 @Harsha, View list of all registered students
    def view_all_student_prompt(self):
        self.print_line("UserStory-401, View list of all registered students")

    # TODO UserStory-404, Remove individual students from the system
    def remove_student_prompt(self):
        self.print_line("UserStory-404, Remove individual students from the system")

    def view_all_subjects_prompt(self):
        subjects = self.database.get_all_subjects()
        # Check if there are subjects to display
        if not subjects:
            self.print_line("No subjects found")
            return

        # Prepare data for tabulation
        subject_list = []
        for subject in subjects:
            subject_list.append([subject.subject_id, subject.subject_name])

        # Print headers and subjects using tabulate
        headers = ["Subject ID", "Subject Name"]
        self.print_line(tabulate(subject_list, headers=headers, tablefmt="pretty"))

    def create_subject_prompt(self):
        subject_id = self.database.create_subject_id()
        sub = Subject(subject_id=subject_id)
        subject_name = input("Enter Subject Name: ")
        if sub.set_subject_name(subject_name):
            self.database.create_subject(sub)
        else:
            self.print_error("Invalid, please try again")

    # TODO UserStory-402, Organize and view students by grade
    # TODO UserStory-403, Categorize students as PASS or FAIL based on marks
    def view_by_grade_prompt(self):
        self.print_line("UserStory-402, Organize and view students by grade")
        self.print_line("UserStory-403, Categorize students as PASS or FAIL based on marks")

    # TODO UserStory-405, Clear the entire students.data file from the system
    def clear_database_prompt(self):
        self.database.clear_student_file()
        self.print_line("Data has been cleared from the file")
