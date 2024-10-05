# The Database is a service class that runs operations against the InMemoryDatabase and stores the information in a data file and a single one is created by the SubSystem at runtime
import json
import os
import random
from typing import List
from pydantic import BaseModel
from Enrolment.Enrolment import Enrolment
from Student.Student import Student
from Subject.Subject import Subject


class Database:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        # Check if file exists
        if os.path.exists(self.db_file_name):
            # Load the existing data from the JSON file
            with open(self.db_file_name, 'r') as json_file:
                self.data = json.load(json_file)
        else:
            initial_data = self._initialise_data_file()
            with open(self.db_file_name, 'w') as json_file:
                json.dump(initial_data, json_file, indent=4)
            self.data = initial_data

    def clear_student_file(self):
        self.data = self._initialise_data_file()  # Reset the in-memory data
        with open(self.db_file_name, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)  # Write the default data to the file

    def _initialise_data_file(self):
        return {
            "students": [],
            "subjects": []
        }

    def register_student(student: Student) -> bool:
        return False

    # This method is done @Niki, I had to play around with the pydantic python library for saving in memory stuff to the file, from @April
    def create_subject(self, subject):
        self.data['subjects'].append(subject.model_dump())
        self._save_changes_to_data_file()

    def enrol_student(self, student_id: str, subject_id: int) -> bool:
        return False

    def _limit_enrolment(self, current_enrolment_count: int) -> bool:
        return False

    def generate_enrolment_id(self) -> int:
        return 0

    def generate_student_id(self) -> int:
        return 0

    # This method is done @Niki, I had to play around with the pydantic python library for saving in memory stuff to the file, from @April
    def create_subject_id(self) -> int:
        new_subject_id = 0
        # Extract IDs from dictionaries
        existing_ids = {subject['subject_id'] for subject in self.data['subjects']}

        while True:
            # Generate a random number between 1 and 999 #TODO Follow up with tutor about requirement to add leading zeros or start with 100 as min number?
            # randint is inclusive on both ends
            new_subject_id = random.randint(1, 999)

            # Check if the ID is unique
            if new_subject_id not in existing_ids:
                break  # Unique ID found, exit loop

        return new_subject_id

    def view_student_list(self) -> List[Student]:
        return None

    def view_by_grade(self) -> List[Student]:
        return None

    def _categorize_performance(self) -> List:
        return None

    # This method is done @Niki, I had to play around with the pydantic python library for saving in memory stuff to the file, from @April
    def get_all_subjects(self) -> List[Subject]:
        # Convert the list of dictionaries into a list of Subject instances
        subjects = [Subject(**subject) for subject in self.data['subjects']]
        # Sort the subjects by subject_id
        return sorted(subjects, key=lambda subject: subject.subject_id)

    def view_enrolled_subjects(self, excluded_subject_ids: List[int]) -> List[Enrolment]:
        return None

    def get_subject(self, subject_id: int) -> Subject:
        return None

    def login_student(self, email: str, password: str) -> Student:
        return None

    def remove_student(self, student_id: str) -> bool:
        return False

    def change_student_pw(self, student_id: str, new_password: str) -> bool:
        return False

    def view_enrolled_subjects(self, student_id: str) -> List[Enrolment]:
        return None

    def unenrol_student(self, student_id: str) -> bool:
        return False

    # Save the data back to the file
    def _save_changes_to_data_file(self):
        with open(self.db_file_name, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)
