import functions

def menu():
    while True:
        print("1 - Add user")
        print("2 - Search user")
        print("3 - Delete user")
        print("4 - Display all")
        print("5 - Exit")


        choice = input("Enter from the above choices: ")

        if choice.lower() in ['1']:
            functions.add_user()
        elif choice in ['2']:
            functions.search_user()
        elif choice in ['3']:
            function.delete_user()
        elif choice in ['4']:
            functions.show_from_sql('customer')
        elif choice in ['5', 'exit', 'q']:
            print("Application stopped")
            break
        else:
            print("Please enter from the above numbers.")
        
menu()