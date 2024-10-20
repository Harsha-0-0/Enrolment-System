import random
import re
from typing import Optional
from pydantic import BaseModel

import Database


class Student(BaseModel):
    student_id: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    registered_date: Optional[str] = None
    enrolments: Optional[str] = None

    def set_name(self, name):
        self.name = name
        if self.name == name:
            return True
        else:
            return False

    def verify_student_email(self, email):
        # if true assign value, else return false
        if re.match(r'^[a-zA-Z]+[.][a-zA-Z]+@university.com$', email):
            self.email = email
            return True
        else:
            return False

    def verify_student_password(self, password):
        # if true assign value, else return false
        if re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', password):
            self.password = password
            return True
        else:
            return False

    def generate_student_id(self, student_list):
        # niki TODO
        # count length of number of subject ids generated in database, and then return 3 digit number in string format

        while True:
            ids = [d['student_id'] for d in student_list]
            uid = str(random.randint(100000, 999999))
            
            if uid not in ids:  
                self.student_id = uid
                return self.student_id
    
