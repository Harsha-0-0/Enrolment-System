from colorama import Fore, Style
from AdminSubSystem import AdminSubSystem
from Database import Database
from StudentSubSystem import StudentSubSystem

# This is the entry of the program, it will initially prompt the user to select Student or Admin subsystem, it should be in a loop unless exited
if __name__ == "__main__":
    while True:
        database = Database("data_file.json")
        option = input(Style.RESET_ALL + "Enter 's' for student or 'a' for or 'e' for exit: ")
        if option == "s":
            student_console = StudentSubSystem(database)
            student_console.launch()
        elif option == "a":
            admin_console = AdminSubSystem(database)
            admin_console.launch()
        elif option == "e":
            print("Exiting System")
            break
        else:
            print(Fore.RED + "Invalid option")
