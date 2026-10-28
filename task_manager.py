# Practical Task 1

# ===== Importing external modules ===========
'''This is the section where modules are being imported'''
from datetime import date

# ==== Login Section ====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and passwords from the user.txt file
    - You can use a list or dictionary to store a list of usernames and
       passwords from the file.
    - Use a while loop to validate your user name and password.
'''

users = {}
with open("user.txt", "r") as file:
    for line in file:
        line = line.strip().split(", ")
        if len(line) == 2:
            users[line[0]] = line[1]

# Validating users credentials
while True:
    username_ = input("Please enter your username").strip()
    password_ = input("Please enter your password").strip()

    if username_ in users and users[username_] == password_:
        print(f"Welcome, {username_}")
        break
    else:
        print("Your username and password do not match, please try again.\n")

while True:
    # Presenting the menu to the user
    menu = input(
        '''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
e - exit
: '''
    ).lower()

    if menu == 'r':
        '''This code block will add a new user to the user.txt file
        - You can use the following steps:
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the same
            - If they are the same, add them to the user.txt file,
              otherwise present a relevant message'''
        new_username = input("Please enter a new username: ")

        # Check if username already exists
        if new_username in users:
            print(
                "Username already exists, please choose a different one.\n")
            continue

        new_password = input("Please enter a password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if new_password == confirm_password:
            users[new_username] = new_password
            with open("user.txt", "a") as file:
                file.write(f"\n{new_username}, {new_password}")
            print(f"User '{new_username}' has been successfully registered.\n")
        else:
            print("Passwords do not match, please try again.\n")

    elif menu == 'a':
        '''This code block will allow a user to add a new task to task.txt file
        - It uses these steps:
            - Prompt a user for the following:
                - the username of the person whom the task is assigned to,
                - the title of the task,
                - the description of the task, and
                - the due date of the task.
            - Then, get the current date.
            - Add the data to the file task.txt
            - Remember to include 'No' to indicate that the task is not
              complete.
        '''
        task_username = input(
            '''Enter the username of the person the task is assigned to: '''
            ).strip()

        # Verifying if the user exits
        if task_username not in users:
            print(
                f"User '{task_username}' does not exist. Please try again.\n")
            continue

        task_title = input("Enter the title of the task: ").strip()
        task_description = input("Enter the description of the task: ").strip()
        task_due_date = input(
            "Enter the due date of the task(e.g 01 Jan 2026: ").strip()
        task_date_added = date.today().strftime("%d %b %Y")

        with open("tasks.txt", "a") as file:
            file.write(
                f"\n{task_username}, {task_title}, {task_description}, "
                f"{task_date_added}, {task_due_date}, No"
            )
        print(f"Task '{task_title}' has been successfully added.\n")

    elif menu == 'va':
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         It does it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 in
              the PDF
            - It is much easier to read a file using a for loop.'''
        print("-" * 60)
        with open("tasks.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(", ")
                if len(parts) == 6:
                    print(f"Task:                  {parts[1]}")
                    print(f"Assigned to:           {parts[0]}")
                    print(f"Date assigned:         {parts[3]}")
                    print(f"Due date:              {parts[4]}")
                    print(f"Task complete?         {parts[5]}")
                    print(f"Task description:      {parts[2]}")
                    print("-" * 60)

    elif menu == 'vm':
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         It does it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the
              username you have read from the file.
            - If they are the same you print the task in the format of Output 2
              shown in the PDF '''
        print("-" * 60)
        found = False
        with open("tasks.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(", ")
                if len(parts) == 6 and parts[0] == username_:
                    found = True
                    print(f"Task:                  {parts[1]}")
                    print(f"Assigned to:           {parts[0]}")
                    print(f"Date assigned:         {parts[3]}")
                    print(f"Due date:              {parts[4]}")
                    print(f"Task complete?         {parts[5]}")
                    print(f"Task description:      {parts[2]}")
                    print("-" * 60)

        if not found:
            print(f"No tasks assigned to '{username_}'.\n")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
