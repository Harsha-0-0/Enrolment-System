from Database import get_student_by_id
from StudentSubSystem import unenrol_from_subject

def unenrol_student(student_id, subject):
    student = get_student_by_id(student_id)  # Fetch student info
    
    if subject in student['subjects']:
        unenrol_from_subject(student_id, subject)  # Unenrol from subject
        print(f"Successfully unenrolled from {subject}.")
    else:
        print(f"{subject} is not in the enrolment list.")
