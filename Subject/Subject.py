from typing import Optional
from pydantic import BaseModel


class Subject(BaseModel):
    
    subject_id : Optional[str] = None
    subject_name: Optional[str] = None
    # subject_desciption: Optional[str] = None
    def _gen_subid(self, subject_info):
        # niki
        # count length of number of subject ids generated in database, and then return 3 digit number in string format
        existing_ids = {int(subject['subject_id']) for subject in subject_info}
        # return the least availble id 
        least_available_id = 1 
        while least_available_id in existing_ids:
            least_available_id += 1
        self.subject_id = format(least_available_id, '03d')
        return least_available_id


    def set_subject_name(self, subject_name):
        if not subject_name.strip():
            return False
        else:
            self.subject_name = subject_name
            return True