import json
import random
import tkinter as tk
import pandas as pd
from tkinter import Listbox, END



def validate_login():
    email = email_entry.get()
    password = password_entry.get()
    if email and password != '':
        try:
            with open("data_file.json", 'r') as s:                      
                data = json.loads(s.read())
        except json.decoder.JSONDecodeError:
            pass
        student_list = data['students']
        email_list = [d['email'] for d in student_list]
        if(email in email_list):
            for i in email_list:
                if(i == email):
                    index = email_list.index(i)
            pwd_list = [d['password'] for d in student_list]
            pwd = pwd_list[index]
            if(pwd == password):
                login_success(email)
                global student_id_cache
                student_id_cache = student_list[index]['student_id']
            else:
                display_error('Password incorrect. Try Again.')
        else:
            display_error('User does not exist. Please log in with correct credentials.')
    else:
        display_error('Please enter valid values for logging in.')
        



def login_success(email):
    clear_widgets()
    
    try:
        with open("data_file.json", 'r') as s:                      
            data = json.loads(s.read())
    except json.decoder.JSONDecodeError:
        pass
    student_list = data['students']
    email_list = [d['email'] for d in student_list]
    for i in email_list:
        if(i == email):
            index = email_list.index(i)

            name_list = [d['name'] for d in student_list]
            name = name_list[index]
    
    success_message = f"Welcome, {name}!"
    welcome_label = tk.Label(frame, text=success_message, fg="#7AC5CD")
    welcome_label.pack()

    subjects_view_button = tk.Button(frame, text="View enrolled subjects", command=on_subjects_view)
    subjects_view_button.pack(pady=10)

    enrol_button = tk.Button(frame, text="Enrol in Subjects", command=enrol_in_subject)
    enrol_button.pack(pady=10)

    logout_button = tk.Button(frame, text="Logout", command=setup_login_widgets)
    logout_button.pack(pady=15)
    global email_cache
    email_cache = email

def display_error(error_msg):
    # Creating a separate pop-up window for the error message
    error_window = tk.Toplevel(root)
    error_window.title("Login Error")
    error_window.geometry("500x150")
    tk.Label(error_window, text=error_msg, fg="red").pack(pady=10)
    tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
    error_window.grab_set()  # Makes the error window modal

def display_enrolment_exception():
    error_window = tk.Toplevel(root)
    error_window.title("Enrolment Error")
    error_window.geometry("600x150")
    tk.Label(error_window, text="You are already enroled in 4 subjects. Enrolment for more than 4 subjects is not allowed.", fg="red").pack(pady=10)
    tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
    error_window.grab_set()

def on_subjects_view():
    
    try:
        with open("data_file.json", 'r') as s:                      
            data = json.loads(s.read())
    except json.decoder.JSONDecodeError:
        pass
    
    def flatten_enrolemnts(stu_info):
        enrol_infos = []
        student_list = data['students']
        id_list = [d['student_id'] for d in stu_info]
        if(student_id_cache in id_list):
            for i in id_list:
                if(i == student_id_cache):
                    index = id_list.index(i)
                    student = student_list.__getitem__(index)

            enrolled_subjects = []
            if student.get('enrolments', []):
                enrolled_subjects.__iadd__(student.get('enrolments', []))
            for enro in enrolled_subjects:
                if enro:
                    enro['student_id'] = student['student_id']
                    enrol_infos.append(enro)
            
        return pd.DataFrame(enrol_infos)


    student_list = data['students']
    enrolment_list = flatten_enrolemnts(student_list)

    subject_list_window = tk.Toplevel(root)
    listbox = Listbox(subject_list_window, width=100, height=20)
    listbox.pack(padx=20, pady=20)
    
    for index, row in enrolment_list.iterrows():
        listbox.insert(END, f"Subject ID: {row['subject_id']}")
        listbox.insert(END, f"Subject Name: {row['subject_name']}")
        listbox.insert(END, f"Mark: {row['mark']}")
        listbox.insert(END, f"Grade: {row['grade']}")
        listbox.insert(END, "")
    if listbox.size() == 0:
        tk.Label(subject_list_window, text="No subjects enrolled.", fg="red").pack(pady=10)
        
    close_button = tk.Button(subject_list_window, text="Close", command=subject_list_window.destroy)
    close_button.pack(pady=5)


def enrol_in_subject():
    try:
        with open("data_file.json", 'r') as s:
            data = json.loads(s.read())
        student = next((s for s in data['students'] if s['email'] == email_cache), None)
        enrolled_subjects = student.get('enrolments', [])
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return
    if not enrolled_subjects:
        enrolled_subjects = []     
    if len(enrolled_subjects) >= 4:
        display_enrolment_exception()
        return
    
    subject_selection_window = tk.Toplevel(root)
    subject_selection_window.title("Select Subjects to Enrol")

    subject_listbox = Listbox(subject_selection_window, selectmode='multiple', width=50)
    subject_listbox.pack(pady=20)


    try:
        with open("data_file.json", 'r') as s:
            data = json.loads(s.read())
        
    except json.decoder.JSONDecodeError:
        subject_selection_window.destroy()
        return

    available_subjects = [sub for sub in data.get('subjects', []) if sub['subject_id'] not in [d['subject_id'] for d in enrolled_subjects]]
    if not available_subjects:
        tk.Label(subject_selection_window, text="No available subjects to enrol in.").pack(pady=10)
        return

    for subject in available_subjects:
        subject_listbox.insert(END, f"{subject['subject_name']} (ID: {subject['subject_id']})")

    def confirm_enrolment():
        selected_indices = subject_listbox.curselection()
        for index in selected_indices:
            if len(enrolled_subjects) < 4:
                random_mark = random.randint(25, 100)
                grade = _calculate_grade(random_mark)
                subject_info = available_subjects[index]
                enrolled_subjects.append({
                    'subject_id': subject_info['subject_id'],
                    'subject_name': subject_info['subject_name'],
                    'mark': random_mark,
                    'grade': grade
                })
            else:
                break

        for stu in data['students']:
            if stu['email'] == email_cache:
                stu['enrolments'] = enrolled_subjects
        with open("data_file.json", 'w') as s:
            json.dump(data, s, indent=4)
        subject_selection_window.destroy()

    enrol_button = tk.Button(subject_selection_window, text="Enrol", command=confirm_enrolment)
    enrol_button.pack(pady=10)

    cancel_button = tk.Button(subject_selection_window, text="Cancel", command=subject_selection_window.destroy)
    cancel_button.pack(pady=5)
    
    def _calculate_grade(mark):
        if mark < 50:
            return 'Z'
        elif 50 <= mark < 65:
            return 'P'
        elif 65 <= mark < 75:
            return 'C'
        elif 75 <= mark < 85:
            return 'D'
        else:
            return 'HD'





def clear_widgets():
    for widget in frame.winfo_children():
        widget.destroy()

def setup_login_widgets():
    clear_widgets()
    global login_label
    login_label = tk.Label(frame, text="Login", fg="#7AC5CD").grid(row=0, column=0, columnspan=2)
    # Email
    tk.Label(frame, text="Email:").grid(row=1, column=0)
    global email_entry
    email_entry = tk.Entry(frame, width=25)
    email_entry.grid(row=1, column=1)
    # Password
    tk.Label(frame, text="Password:").grid(row=2, column=0)
    global password_entry
    password_entry = tk.Entry(frame, show="*", width=25)
    password_entry.grid(row=2, column=1)
    # Buttons
    tk.Button(frame, text="Login", command=validate_login).grid(row=3, column=1, sticky="e", padx=25, pady=10)
    tk.Button(frame, text="Cancel", command=root.quit).grid(row=3, column=0, sticky="w", padx=10)

email_cache = None
student_id_cache = None
# Main window
root = tk.Tk()
root.title("Student Enrolment System")
root.geometry("500x500")
root.configure(bg='#7AC5CD')
frame = tk.Frame(root)
frame.pack(expand=True)


setup_login_widgets()

root.mainloop()

