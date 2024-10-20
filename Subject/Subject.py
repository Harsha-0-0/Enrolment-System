from typing import Optional
from pydantic import BaseModel


class Subject(BaseModel):
    subject_id: int
    subject_name: Optional[str] = None

    # def _gen_subid(self, ):
    #     # niki
    #     # count length of number of subject ids generated in database, and then return 3 digit number in string format
    #     cur_id = format(len(self.sub_data), '03d')
    #     self.sub_data[cur_id] = True
    #     if len(self.sub_data) > 999:
    #         raise Exception('run out of available subject ids ~~')
    #     return cur_id

    def set_subject_name(self, subject_name):
        if not subject_name.strip():
            return False
        else:
            self.subject_name = subject_name
            return True