from Database import get_student_by_id
from StudentSubSystem import enrol_in_subject

def enrol_student(student_id, subject):
    student = get_student_by_id(student_id)  # Fetch student info
    
    if len(student['subjects']) >= 4:
        print("Cannot enrol in more than 4 subjects.")
        return False

    enrol_in_subject(student_id, subject)  # Enrol student
    print(f"Successfully enrolled in {subject}.")
    return True
