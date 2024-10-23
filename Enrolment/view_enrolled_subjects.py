from Database import get_student_by_id
from StudentSubSystem import get_enrolled_subjects

def view_enrolled_subjects(student_id):
    student = get_student_by_id(student_id)  # Fetch student info
    subjects = get_enrolled_subjects(student_id)  # Fetch enrolled subjects

    if subjects:
        print(f"Enrolled subjects for {student['name']}:")
        for subject in subjects:
            print(f"- {subject}")
    else:
        print(f"{student['name']} is not enrolled in any subjects.")
