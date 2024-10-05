import re
from pydantic import BaseModel


class Student(BaseModel):
    def __init__(self, **kwarg) -> None:
        self.student_id = None
        self.name = None
        self.password = None
        self.email = None
        self.registered_date = None
        self.enrolments = None

    def set_name(self, name):
        self.name = name
        if self.name == name:
            return True
        else:
            return False

    def verify_student_email(self, email):
        # if true assign value, else return false
        if email.split('@')[-1] == 'university.com':
            self.email = email
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

        self.password = passwd

    def _gen_sid(self, cur_id):
        # niki TODO
        # count length of number of subject ids generated in database, and then return 3 digit number in string format

        if len(cur_id + 1) > 999999:
            raise Exception('run out of available student ids ~~')

        self.student_id = format(cur_id + 1, '06d')

        return cur_id
