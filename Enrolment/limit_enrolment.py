from Database import get_student_by_id

def limit_enrolment(student_id):
    student = get_student_by_id(student_id)  # Fetch student info
    
    if len(student['subjects']) >= 4:
        print(f"{student['name']} has reached the limit of 4 subjects.")
        return False
    return True
