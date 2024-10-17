import re
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Student(BaseModel):
    student_id : Optional[str] = None
    student_name : Optional[str] = None
    student_password : Optional[str] = None
    student_email : Optional[str] = None
    registered_date : Optional[str] = None

    def set_name(self, name):
        self.student_name = name
        if self.student_name == name:
            return True
        else:
            return False

    def verify_student_email(self, email):
        # if true assign value, else return false
        pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@university.com$'  
        if re.match(pattern, email):
            self.student_email = email
            return True
        else:
            return False

    def verify_student_password(self, passwd):
        # if true assign value, else return false
        if len(''.join(re.findall(r'\d+', passwd))) < 3:
            # less than 3 digits
            return False
        if len(''.join(re.findall(r'[A-Za-z]+', passwd))) < 5:
            # less than five letters
            return False
        if passwd[0].islower():
            return False

        self.student_password = passwd
        return True

    def _gen_sid(self, student_info):
        # niki TODO
        # count length of number of subject ids generated in database, and then return 3 digit number in string format
        existing_ids = {int(student['student_id']) for student in student_info}
        least_available_id = 1 # id start from zero or one ??
        while least_available_id in existing_ids:
            least_available_id += 1

        self.student_id = format(least_available_id, '06d')
        self.registered_date = datetime.today().strftime('%Y-%m-%d') 
        return least_available_id