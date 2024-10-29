# The Database is a service class that runs operations against the InMemoryDatabase and stores the information in a data file and a single one is created by the SubSystem at runtime
import json
import os
import random
from typing import List
from pydantic import BaseModel
from Enrolment.Enrolment import Enrolment
from Student.Student import Student
from Subject.Subject import Subject
import numpy as np

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

    def _save_changes_to_data_file(self):
        with open(self.db_file_name, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)        

    def _initialise_data_file(self):
        return {
            "students": [],
            "subjects": []
        }

    # TODO - Should check if there's already a student with the same StudentId or Email and if there is return false, dont forget to add self._save_changes_to_data_file()
    def register_student(self, student: Student):
        self.data['students'].append(student.model_dump())
        self._save_changes_to_data_file()
    
    # To fetch all the data from data_file.json
    def get_data(self):
        try:
            with open("data_file.json", 'r') as s:                      
                self.studentList = json.loads(s.read())
                return self.studentList
        except json.decoder.JSONDecodeError:
            pass
    # This method is used in Enrolment to check length of enrolments    
    def countList(self, lst):
        count = 0
        for el in lst:
            if type(el) == type({}):
                count += 1
 
        return count

    # TODO - Just match on Email/Password or return null
    def login_student(self, email: str, password: str) -> Student:
        return None


   # Returns false if no match, don't forget to add self._save_changes_to_data_file()
    def change_student_pw(self, student_id: str, new_password: str) -> bool:
        student = next((s for s in self.data['students'] if s['student_id'] == student_id), None)

        if student:
            student['password'] = new_password
            self._save_changes_to_data_file()
            return True  
        else:
            return False  


    # This method is done @Niki, I had to play around with the pydantic python library for saving in memory stuff to the file, from @April
    def create_subject(self, subject):
        self.data['subjects'].append(subject.model_dump()) # serialization
        self._save_changes_to_data_file()

    # Return the Logged in student information
    def get_student(self, index):
        self.data = self.get_data()
        student_list = self.data['students']
        student = student_list.__getitem__(index)
        return student

    # Limit Enrolment
    def _limit_enrolment(self, current_enrolment_count: int) -> bool:
        return current_enrolment_count >= 4

    # Enrol - Find student, find subject, check if the student is already enrolled or not, use _limit_enrolment(), create enrolment, dont forget to add self._save_changes_to_data_file()
    def enrol_student(self, student_id: str, subject_id: int) -> bool:
        student = next((s for s in self.data['students'] if s['student_id'] == student_id), None)
        if not student:
            return False  

        if 'enrolments' not in student or student['enrolments'] is None:
            student['enrolments'] = []

        enrolled_subjects = student['enrolments']

        if subject_id in enrolled_subjects:
            return False  

        if self._limit_enrolment(len(enrolled_subjects)):
            return False  

        available_subjects = [sub['subject_id'] for sub in self.data['subjects'] if sub['subject_id'] not in enrolled_subjects]

        if subject_id not in available_subjects:
            return False  
        
        for sub in self.data['subjects']:
            if sub['subject_id'] == subject_id:
                subject_name = sub['subject_name']
        random_mark = random.randint(25, 100)
        grade = self._calculate_grade(random_mark)

        student['enrolments'].append({
            'subject_id': subject_id,
            'subject_name': subject_name,
            'mark': random_mark,
            'grade': grade
        })

        self._save_changes_to_data_file()
        return True



    def _calculate_grade(self, mark):
        if mark < 50:
            return 'Z'
        elif 50 <= mark < 65:
            return 'P'
        elif 65 <= mark < 75:
            return 'C'
        elif 75 <= mark < 85:
            return 'D'
        else:
            return 'HD'

    

    # Withdraw - Find student, find enrolment with the with subject_id, don't forget to add self._save_changes_to_data_file()
    def unenrol_student(self, student_id: str, subject_id: int) -> bool:
        student = next((s for s in self.data['students'] if s['student_id'] == student_id), None)
        if not student:
            return False  

        if 'enrolments' not in student or student['enrolments'] is None:
            return False  

        enrolled_subjects = student['enrolments']
        for subject in enrolled_subjects:
            if subject['subject_id'] == subject_id:
                enrolled_subjects.remove(subject)  
                self._save_changes_to_data_file() 
                return True  

        return False  


    # TODO - Just make sure it doesn't have duplicates, can be any int, it is possible this field is unnessary
    def generate_enrolment_id(self) -> int:
        return 0

    # TODO - Should get all existing student_ids, maybe convert to int and find the highest number and then pad the leading zero and then ensure there is no duplicate and return
    def generate_student_id(self) -> str:
        
        existing_ids = {student['student_id'] for student in self.data['students']}
        least_available_id = 1 # id start from zero or one ??
        for least_available_id in existing_ids:
            existing_ids += 1
        return least_available_id
    
    # This method is done @Niki, I had to play around with the pydantic python library for saving in memory stuff to the file, from @April
    def create_subject_id(self) -> int:
        # new_subject_id = -1
        # Extract IDs from dictionaries
        existing_ids = {subject['subject_id'] for subject in self.data['subjects']}
        # return the least availble id 
        least_available_id = 1 
        for least_available_id in existing_ids:
            existing_ids += 1
        return least_available_id
    # TODO Follow up with tutor about requirement to add leading zeros or start with 100 as min number?
    # if start from zero, we might need str type for id, for simplicity, 100 is favorable
        # while True:
        #     # Generate a random number between 1 and 999 #
        #     # randint is inclusive on both ends
            
        #     new_subject_id = random.randint(1, 999)
        
        #     # Check if the ID is unique
        #     if new_subject_id not in existing_ids:
        #         break  # Unique ID found, exit loop
        
        # return new_subject_id
    
    # TODO - Maybe return sorted by student_id
    def get_student_list(self):
        self.data = self.get_data()
        student_list = self.data['students']
        return student_list

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


    # TODO - Could be used just to return the particular subject's name
    def get_subject(self, subject_id: int) -> Subject:
        return None


    # TODO - Returns false if no match, don't forget to add self._save_changes_to_data_file()
    def remove_student(self, index) -> bool: 
        if index:
            self.data['students'].pop(index)
            self._save_changes_to_data_file()
            return True
        return False





