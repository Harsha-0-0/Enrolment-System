import json
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

    subjects_view_button = tk.Button(frame, text="subjects_view", command=on_subjects_view)
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
    
    def flatten_enrolemnts(stu_info):
        enrol_infos = []
        for stu in stu_info:
            enrolled_subjects = []
            if stu.get('enrolments',[]):
                enrolled_subjects.__iadd__(stu.get('enrolments',[]))
            for enro in enrolled_subjects:
                if enro:
                    enro['student_id'] = stu['student_id']
                    enrol_infos.append(enro)

        return pd.DataFrame(enrol_infos)

    clear_widgets()
    try:
        with open("data_file.json", 'r') as s:                      
            data = json.loads(s.read())
    except json.decoder.JSONDecodeError:
        pass

    student_list = data['students']
    enrolment_list = flatten_enrolemnts(student_list)

    stu_df = pd.DataFrame(data=student_list, columns=['student_id', 'name'])
    enrol_df = pd.DataFrame(data=enrolment_list, columns=['student_id', 'subject_name', 'subject_id', 'grade', 'mark'])
    merge_df = pd.merge(stu_df, enrol_df, on='student_id',how='right')
    merge_df = merge_df[merge_df['student_id'] == student_id_cache]
    
    # subjects_view_button = tk.Button(frame, text="subjects_view", command=on_subjects_view)
    # subjects_view_button.pack(pady=10)
    
    listbox.pack(padx=20, pady=20)

    for grade, group in merge_df.groupby('grade'):
        for index, row in group.iterrows():
            listbox.insert(END, f"Subject ID: {row['subject_id']}")
            listbox.insert(END, f"Subject Name: {row['subject_name']}")
            listbox.insert(END, "")
    if listbox.size() == 0:
        listbox.insert(END, f"No subjects enrolled")

    back2login_button = tk.Button(frame, text="back", command=back2login)
    back2login_button.pack(pady=0)


def enrol_in_subject():
    subject_selection_window = tk.Toplevel(root)
    subject_selection_window.title("Select Subjects to Enrol")

    subject_listbox = Listbox(subject_selection_window, selectmode='multiple', width=50)
    subject_listbox.pack(pady=20)

    try:
        with open("data_file.json", 'r') as s:
            data = json.loads(s.read())
        student = next((s for s in data['students'] if s['email'] == email_cache), None)
        enrolled_subjects = student.get('enrolments', [])
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        subject_selection_window.destroy()
        return

    if not enrolled_subjects:
        enrolled_subjects = []

    if len(enrolled_subjects) >= 4:
        tk.Label(subject_selection_window, text="You have already enrolled in 4 subjects.").pack(pady=10)
        return



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
                subject_info = available_subjects[index]
                enrolled_subjects.append({
                    'subject_id': subject_info['subject_id'],
                    'subject_name': subject_info['subject_name'],
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




def back2login():
    clear_widgets()
    login_success(email_cache)

def clear_widgets():
    for widget in frame.winfo_children():
        widget.destroy()
    if listbox.size() != 0:
        listbox.delete(0, tk.END)

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

listbox = Listbox(root, width=80, height=20)

setup_login_widgets()

root.mainloop()

