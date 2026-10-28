# Practical Task 2

# ===== Importing external modules ===========
'''This is the section where modules are being imported'''
from datetime import date

# ==== Login Section ====
# Read all users from file into a dictionary
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and passwords from the user.txt file
    - You can use a list or dictionary to store a list of usernames and
       passwords from the file.
    - Use a while loop to validate your user name and password'''
users = {}
with open("user.txt", "r") as file:
    for line in file:
        line = line.strip().split(", ")
        if len(line) == 2:
            users[line[0]] = line[1]

# Validate login credentials
while True:
    username_ = input("Please enter your username: ").strip()
    password_ = input("Please enter your password: ").strip()

    if username_ in users and users[username_] == password_:
        print(f"Welcome, {username_}!")
        break
    else:
        print("Your username and password do not match, please try again.\n")

is_admin = username_ == "admin"

# ===== Helper Functions =====


def print_task(parts):
    print("-" * 60)  # Printing a line with 60 dashes
    print(f"Task:                 {parts[1]}")
    print(f"Assigned to:          {parts[0]}")
    print(f"Date assigned:        {parts[3]}")
    print(f"Due date:             {parts[4]}")
    print(f"Task complete?        {parts[5]}")
    print(f"Task description:     {parts[2]}")
    print("-" * 60)  # Printing a line with 60 dashes


def read_tasks():
    """
    Read all valid tasks from tasks.txt and return as a list of part-lists.
    """
    tasks = []
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(", ")
                if len(parts) == 6:
                    tasks.append(parts)
    except FileNotFoundError:
        pass
    return tasks


def write_tasks(tasks):
    """Write a list of task part-lists back to tasks.txt."""
    with open("tasks.txt", "w") as file:
        for i, parts in enumerate(tasks):
            line = ", ".join(parts)
            if i < len(tasks) - 1:
                file.write(line + "\n")
            else:
                file.write(line)


# ===== Main Menu Loop =====
while True:
    if is_admin:
        menu = input(
            '''\nPlease select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete tasks
e - exit
: '''
        ).lower().strip()
    else:
        menu = input(
            '''\nPlease select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: '''
        ).lower().strip()

    # Registering users for admin only
    if menu == 'r':
        if not is_admin:
            print("Access denied. Only admin can register new users.\n")
            continue

        new_username = input("Enter a new username: ").strip()
        if new_username in users:
            print('''
                  That username already exists. Please choose a different one.
                  \n''')
            continue

        new_password = input("Enter a new password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if new_password == confirm_password:
            users[new_username] = new_password
            with open("user.txt", "a") as file:
                file.write(f"\n{new_username}, {new_password}")
            print(f"User '{new_username}' has been successfully registered.\n")
        else:
            print("Passwords do not match. Please try again.\n")

    # ── Add task ────────────────────────────────────────────────────────
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
              complete.'''
        task_username = input(
            "Enter the username of the person the task is assigned to: "
            ).strip()

        if task_username not in users:
            print(
                f"User '{task_username}' does not exist. Please try again.\n")
            continue

        task_title = input("Enter the title of the task: ").strip()
        task_description = input("Enter the description of the task: ").strip()
        task_due_date = input(
            "Enter the due date of the task (e.g. 01 Jan 2025): ").strip()
        task_date_added = date.today().strftime("%d %b %Y")

        tasks = read_tasks()
        tasks.append([task_username, task_title, task_description,
                      task_date_added, task_due_date, "No"])
        write_tasks(tasks)
        print(f"Task '{task_title}' has been successfully added.\n")

    # View all tasks
    elif menu == 'va':
        '''This option will view all the tasks for all the usernames'''
        tasks = read_tasks()
        if not tasks:
            print("No tasks found.\n")
        else:
            for parts in tasks:
                print_task(parts)

    # View my tasks
    elif menu == 'vm':
        '''This option will only view the tasks of the logged on username'''
        tasks = read_tasks()
        my_tasks = [p for p in tasks if p[0] == username_]
        if not my_tasks:
            print(f"No tasks assigned to '{username_}'.\n")
        else:
            for parts in my_tasks:
                print_task(parts)

    # View completed tasks (admin only)
    elif menu == 'vc':
        '''This option will view only the tasks which has been marked
        as complete, with a yes on the side'''
        if not is_admin:
            print("You have entered an invalid input. Please try again.\n")
            continue

        tasks = read_tasks()
        completed = [p for p in tasks if p[5].strip().lower() == "yes"]
        if not completed:
            print("No completed tasks found.\n")
        else:
            print(f"\n{len(completed)} completed task(s) found:")
            for parts in completed:
                print_task(parts)

    # Delete tasks (admin only)
    elif menu == 'del':
        '''This option allows admin to delete tasks that are on the list'''
        if not is_admin:
            print("You have entered an invalid input. Please try again.\n")
            continue

        tasks = read_tasks()
        if not tasks:
            print("No tasks found.\n")
            continue

        # Display all tasks with an index number so admin can pick one
        print(f"\n{len(tasks)} task(s) on record:\n")
        for i, parts in enumerate(tasks):
            print(f"  [{i + 1}] {parts[1]} — assigned to {parts[0]} "
                  f"(complete: {parts[5]})")

        try:
            choice = int(input(
                "\nEnter the number of the task to delete (0 to cancel): "
                ).strip())
        except ValueError:
            print("Invalid input. Returning to menu.\n")
            continue

        if choice == 0:
            print("Deletion cancelled.\n")
        elif 1 <= choice <= len(tasks):
            removed = tasks.pop(choice - 1)
            write_tasks(tasks)
            print(f"Task '{removed[1]}' has been successfully deleted.\n")
        else:
            print("Number out of range. No task was deleted.\n")

    # ── Exit ─────────────────────────────────────────────────────────────
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again.\n")
