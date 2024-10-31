import random
from pydantic import BaseModel


class Enrolment(BaseModel):
    def __init__(self, subject, student) -> None:
        self.entrolment_id = None
        self.entrolment_date = None
        self.mark = None
        self.grade = None
        self.subject = subject
        self.student = student

        self._assign_marks()
        self._calculate_grade()

    def _assign_marks(self):
        self.mark = random.randint(25, 100)

    def _calculate_grade(self, ):
        if self.mark < 50:
            self.grade = 'Z'
        elif self.mark >= 50 and self.mark < 65:
            self.grade = 'P'
        elif self.mark >= 65 and self.mark < 75:
            self.grade = 'C'
        elif self.mark >= 75 and self.mark < 85:
            self.grade = 'D'
        else:
            self.grade = 'HD'
