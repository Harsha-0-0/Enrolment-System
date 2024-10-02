from SubSystem import SubSystem

class AdminSubSystem(SubSystem):
    def __init__(self, database):
        super().__init__(database)
    def launch(self):
        print("Welcome to Admin SubSystem ")
        while True:
            option = input("(1) View all Students, (2) Remove Student, (3) View all Subjects, (4) Add Subject, (5) Clear Student Database, (99) ExitSubSystem: ")
            if option == '1':
                print('test 1')
            elif option == '2':
                print('test2')
            elif option == '3':
                print('test3')
            elif option == '4':
                print('test4')
            elif option == '5':
                print('test5')            
            elif option == '99':
                print('Exiting SubSystem')
                break
            else:
                print('Invalid option')    