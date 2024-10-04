
class subject:
    def __init__(self, subject_name = None, enrolments = [], **kwarg):
        self.subject_id = self._gen_subid()
        self.subject_name = subject_name
        self.enrolments = enrolments


        self.sub_data = dict() # dummy data

    def _gen_subid(self, ):
        # niki 
        # count length of number of subject ids generated in database, and then return 3 digit number in string format
        cur_id = format(len(self.sub_data), '03d')
        self.sub_data[cur_id] = True
        if len(self.sub_data) > 999:
            raise Exception('run out of available subject ids ~~')
        return cur_id
    
    def set_subject_name(self, subject_name):
        self.subject_name = subject_name
        if self.subject_name == subject_name:
            return True
        else:
            return False