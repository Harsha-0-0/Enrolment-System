from datetime import datetime
import random
from pydantic import BaseModel
from typing import Optional

class Enrolment(BaseModel):

    entrolment_date : Optional[str] = None
    mark : Optional[int] = None
    grade : Optional[str] = None
    subject_id : Optional[str] = None
    student_id : Optional[str] = None

    def __init__(self,):  
            super().__init__()  
            self._assign_marks()
            self._calculate_grade()
            self.entrolment_date = datetime.today().strftime('%Y-%m-%d') 
        
    def _assign_marks(self):
        self.mark = random.randint(25, 100)

    def _calculate_grade(self):
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