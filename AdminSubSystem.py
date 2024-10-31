import json
from colorama import Fore
import pandas as pd
from tabulate import tabulate
from Database import Database
from SubSystem import SubSystem
from Subject.Subject import Subject


class AdminSubSystem(SubSystem):
    def __init__(self, database: Database):
        super().__init__(database, Fore.BLUE)

    def launch(self):
        self.print_line("Welcome to Admin SubSystem")
        while True:
            option = input(
                "(1) View all Students, (2) Remove Student, (3) View all Subjects, (4) Create Subject, (5) View by Grade, (6) Pass/Fail Partition, (7) Clear Student Database, (99) ExitSubSystem: ")
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
                self.partition_students()
            elif option == "7":
                self.clear_database_prompt()
            elif option == "99":
                self.print_line("Exiting SubSystem")
                break
            else:
                self.print_error("Invalid option")

    # TODO UserStory-401 @Harsha, View list of all registered students
    def view_all_student_prompt(self):
        student_list = self.database.get_student_list()
        # TO show only selected columns, used Pandas, Dataframe
        cols = ['student_id', 'name', 'email']
        df = pd.DataFrame(data=student_list, columns=cols)
        self.print_line(tabulate(df, tablefmt="github", headers=["Student ID", "Student Name", "Email ID"]))

    # TODO UserStory-404, Remove individual students from the system
    def remove_student_prompt(self):

        student_list = self.database.get_student_list()
        cols = ['student_id', 'name', 'email']
        df = pd.DataFrame(data=student_list, columns=cols)
        self.print_line(tabulate(df, tablefmt="github", headers=["Student ID", "Student Name", "Email ID"]))
        student_id = input('Enter the ID of student you want to delete: ')
        id_list = [d['student_id'] for d in student_list]
        if (student_id in id_list):
            index = id_list.index(student_id)
            self.database.remove_student(index)
            self.print_line("Deleted successfully!")

            student_list_after_update = self.database.get_student_list()
            df = pd.DataFrame(data=student_list_after_update, columns=cols)
            self.print_line(tabulate(df, tablefmt="github", headers=["Student ID", "Student Name", "Email ID"]))
        else:
            self.print_error(f"Student ID {student_id} does not exist.")

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
        sub = Subject()
        subject_name = input("Enter Subject Name: ")
        while not sub.set_subject_name(subject_name):
            self.print_error("Invalid, please try again")
            subject_name = input("Enter Subject Name: ")
        sub._gen_subid(self.database.data['subjects'])
        self.database.create_subject(sub)

    # TODO UserStory-402, Organize and view students by grade
    # TODO UserStory-403, Categorize students as PASS or FAIL based on marks
    def view_by_grade_prompt(self):
        def flatten_enrolemnts(stu_info):
            enrol_infos = []
            for stu in stu_info:
                enrolled_subjects = []
                if stu.get('enrolments', []):
                    enrolled_subjects.__iadd__(stu.get('enrolments', []))
                for enro in enrolled_subjects:
                    if enro:
                        enro['student_id'] = stu['student_id']
                        enrol_infos.append(enro)

            return pd.DataFrame(enrol_infos)

        student_list = self.database.get_student_list()
        enrolment_list = flatten_enrolemnts(student_list)

        stu_df = pd.DataFrame(data=student_list, columns=['student_id', 'name'])
        enrol_df = pd.DataFrame(data=enrolment_list, columns=['student_id', 'subject_id', 'grade', 'mark'])
        merge_df = pd.merge(stu_df, enrol_df, on='student_id', how='right')

        for gradegroup in merge_df.groupby('grade'):
            print('{:-^10}'.format(gradegroup[0]))
            self.print_line(tabulate(gradegroup[1], headers=['name', 'student_id',
                            'subject_id', 'grade', 'mark'], tablefmt="pretty"))

    def partition_students(self):
        def flatten_enrolemnts(stu_info):
            enrol_infos = []
            for stu in stu_info:
                enrolled_subjects = []
                if stu.get('enrolments', []):
                    enrolled_subjects.__iadd__(stu.get('enrolments', []))
                for enro in enrolled_subjects:
                    if enro:
                        grade = enro['grade']
                        enro['partition'] = partition(grade)
                        enro['student_id'] = stu['student_id']
                        enrol_infos.append(enro)

            return pd.DataFrame(enrol_infos)

        def partition(grade):
            if grade == 'Z':
                partition = 'FAIL'
            else:
                partition = 'PASS'
            return partition

        student_list = self.database.get_student_list()
        enrolment_list = flatten_enrolemnts(student_list)

        stu_df = pd.DataFrame(data=student_list, columns=['student_id', 'name'])
        enrol_df = pd.DataFrame(data=enrolment_list, columns=[
                                'student_id', 'subject_id', 'subject_name', 'grade', 'mark', 'partition'])
        merge_df = pd.merge(stu_df, enrol_df, on='student_id', how='right')
        for partition_group in merge_df.groupby('partition'):
            print('{:-^10}'.format(partition_group[0]))
            self.print_line(tabulate(partition_group[1], headers=[
                            'Student Id', 'Name', 'Subject Id', 'Subject Name', 'Grade', 'Mark', 'Pass/Fail'], tablefmt="pretty"))

    # TODO UserStory-405, Clear the entire students.data file from the system
    def clear_database_prompt(self):
        self.database.clear_student_file()
