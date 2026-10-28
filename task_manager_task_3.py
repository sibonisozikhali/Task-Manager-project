# Practical task 3

#  Importing external modules
from datetime import date, datetime

#  Helpers


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
        file.write("\n".join(", ".join(parts) for parts in tasks))


def read_users():
    """
    Read all users from user.txt and return as a dict {username: password}.
    """
    users = {}
    try:
        with open("user.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    users[parts[0]] = parts[1]
    except FileNotFoundError:
        pass
    return users


# Display function

def print_task(parts, index=None):
    """Pretty-print a single task. Optionally prefix with an index number."""
    print("-" * 60)
    if index is not None:
        print(f"Task #{index}")
    print(f"Task:                 {parts[1]}")
    print(f"Assigned to:          {parts[0]}")
    print(f"Date assigned:        {parts[3]}")
    print(f"Due date:             {parts[4]}")
    print(f"Task complete?        {parts[5]}")
    print(f"Task description:     {parts[2]}")
    print("-" * 60)


# login function

def login():
    """Prompt for credentials and return (username, is_admin) on success."""
    users = read_users()
    while True:
        username = input("Please enter your username: ").strip()
        password = input("Please enter your password: ").strip()
        if username in users and users[username] == password:
            print(f"\nWelcome, {username}!\n")
            return username, username == "admin"
        print("Your username and password do not match. Please try again.\n")


# functions as per the task document

def reg_user(users):
    """Register a new user. Prevents duplicate usernames."""
    while True:
        new_username = input("Enter a new username: ").strip()
        if new_username in users:
            print(
                "That username already exists. Please choose a different one.\n"
                )
            continue

        new_password = input("Enter a new password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if new_password != confirm_password:
            print("Passwords do not match. Please try again.\n")
            continue

        users[new_username] = new_password
        with open("user.txt", "a") as file:
            file.write(f"\n{new_username}, {new_password}")
        print(f"User '{new_username}' has been successfully registered.\n")
        return


def add_task(users):
    """Add a new task to tasks.txt."""
    task_username = input(
        "Enter the username of the person the task is assigned to: "
    ).strip()
    if task_username not in users:
        print(f"User '{task_username}' does not exist. Please try again.\n")
        return

    task_title = input("Enter the title of the task: ").strip()
    task_description = input("Enter the description of the task: ").strip()

    while True:
        task_due_date = input(
            "Enter the due date of the task (e.g. 01 Jan 2025): "
        ).strip()
        try:
            datetime.strptime(task_due_date, "%d %b %Y")
            break
        except ValueError:
            print(
                "Invalid date format. Please use DD Mon YYYY (e.g. 01 Jan 2025).\n"
                )

    task_date_added = date.today().strftime("%d %b %Y")

    tasks = read_tasks()
    tasks.append([task_username, task_title, task_description,
                  task_date_added, task_due_date, "No"])
    write_tasks(tasks)
    print(f"Task '{task_title}' has been successfully added.\n")


def view_all():
    """Display all tasks from tasks.txt."""
    tasks = read_tasks()
    if not tasks:
        print("No tasks found.\n")
        return
    for parts in tasks:
        print_task(parts)


def get_valid_task_number(my_tasks):
    """
    Recursively prompt the user for a valid task number.
    Base case: user enters -1 to return to the main menu.
    Returns the 0-based index into my_tasks, or -1 to go back.
    """
    raw = input(
        "\nEnter a task number to select it, or -1 to return to the menu: "
    ).strip()

    try:
        choice = int(raw)
    except ValueError:
        print("Invalid input — please enter a number.")
        return get_valid_task_number(my_tasks)

    if choice == -1:
        return -1

    if 1 <= choice <= len(my_tasks):
        return choice - 1          # convert to 0-based index

    print(f"Please enter a number between 1 and {len(my_tasks)}.")
    return get_valid_task_number(my_tasks)


def view_mine(username, users):
    """
    Display tasks assigned to the logged-in user and allow them to:
      - Mark a task as complete
      - Edit the assigned username or due date (only if not yet complete)
    """
    tasks = read_tasks()
    # Build a list of (global_index, parts) for this user's tasks
    my_tasks = [(i, p) for i, p in enumerate(tasks) if p[0] == username]

    if not my_tasks:
        print(f"No tasks assigned to '{username}'.\n")
        return

    print(f"\nTasks assigned to you ({len(my_tasks)} found):\n")
    for display_num, (_, parts) in enumerate(my_tasks, start=1):
        print_task(parts, index=display_num)

    idx = get_valid_task_number(my_tasks)
    if idx == -1:
        return

    global_idx, parts = my_tasks[idx]

    print(f"\nSelected: '{parts[1]}'")
    print("1 - Mark as complete")
    print("2 - Edit task")
    print("0 - Cancel")
    action = input("Choose an action: ").strip()

    if action == "1":
        tasks[global_idx][5] = "Yes"
        write_tasks(tasks)
        print("Task marked as complete.\n")

    elif action == "2":
        if parts[5].strip().lower() == "yes":
            print("This task is already complete and cannot be edited.\n")
            return

        print("\nWhat would you like to edit?")
        print("1 - Assigned username")
        print("2 - Due date")
        print("3 - Both")
        edit_choice = input("Choose an option: ").strip()

        if edit_choice in ("1", "3"):
            new_user = input("Enter the new assigned username: ").strip()
            if new_user not in users:
                print(f"User '{new_user}' does not exist. Edit cancelled.\n")
                return
            tasks[global_idx][0] = new_user

        if edit_choice in ("2", "3"):
            while True:
                new_due = input(
                    "Enter the new due date (e.g. 01 Jan 2025): "
                ).strip()
                try:
                    datetime.strptime(new_due, "%d %b %Y")
                    break
                except ValueError:
                    print("Invalid format. Use DD Mon YYYY.\n")
            tasks[global_idx][4] = new_due

        if edit_choice in ("1", "2", "3"):
            write_tasks(tasks)
            print("Task updated successfully.\n")
        else:
            print("No changes made.\n")

    elif action == "0":
        print("Cancelled.\n")
    else:
        print("Invalid option. Returning to menu.\n")


def view_completed():
    """Display all completed tasks (admin only)."""
    tasks = read_tasks()
    completed = [p for p in tasks if p[5].strip().lower() == "yes"]
    if not completed:
        print("No completed tasks found.\n")
    else:
        print(f"\n{len(completed)} completed task(s) found:")
        for parts in completed:
            print_task(parts)


def delete_task():
    """Allow admin to delete a specific task."""
    tasks = read_tasks()
    if not tasks:
        print("No tasks found.\n")
        return

    print(f"\n{len(tasks)} task(s) on record:\n")
    for i, parts in enumerate(tasks, start=1):
        print(f"  [{i}] {parts[1]} — assigned to {parts[0]} "
              f"(complete: {parts[5]})")

    try:
        choice = int(input(
            "\nEnter the number of the task to delete (0 to cancel): "
        ).strip())
    except ValueError:
        print("Invalid input. Returning to menu.\n")
        return

    if choice == 0:
        print("Deletion cancelled.\n")
    elif 1 <= choice <= len(tasks):
        removed = tasks.pop(choice - 1)
        write_tasks(tasks)
        print(f"Task '{removed[1]}' has been successfully deleted.\n")
    else:
        print("Number out of range. No task was deleted.\n")


# Report Generation

def _is_overdue(due_date_str, complete):
    """Return True if a task is incomplete and its due date has passed."""
    if complete.strip().lower() == "yes":
        return False
    try:
        due = datetime.strptime(due_date_str.strip(), "%d %b %Y").date()
        return due < date.today()
    except ValueError:
        return False


def generate_reports():
    """
    Generate task_overview.txt and user_overview.txt with summary statistics.
    """
    tasks = read_tasks()
    users = read_users()

    total_tasks = len(tasks)
    completed = sum(1 for p in tasks if p[5].strip().lower() == "yes")
    uncompleted = total_tasks - completed
    overdue = sum(1 for p in tasks if _is_overdue(p[4], p[5]))

    pct_incomplete = (uncompleted / total_tasks * 100) if total_tasks else 0
    pct_overdue = (overdue / total_tasks * 100) if total_tasks else 0

    # Task_overview.txt
    with open("task_overview.txt", "w") as f:
        f.write("=" * 50 + "\n")
        f.write("           TASK OVERVIEW REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total tasks:              {total_tasks}\n")
        f.write(f"Completed tasks:          {completed}\n")
        f.write(f"Uncompleted tasks:        {uncompleted}\n")
        f.write(f"Overdue & incomplete:     {overdue}\n")
        f.write(f"% Incomplete:             {pct_incomplete:.1f}%\n")
        f.write(f"% Overdue:                {pct_overdue:.1f}%\n")

    # user_overview.txt
    with open("user_overview.txt", "w") as f:
        f.write("=" * 50 + "\n")
        f.write("           USER OVERVIEW REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total registered users:   {len(users)}\n")
        f.write(f"Total tasks:              {total_tasks}\n\n")

        for user in users:
            user_tasks = [p for p in tasks if p[0] == user]
            u_total = len(user_tasks)
            u_completed = sum(
                1 for p in user_tasks if p[5].strip().lower() == "yes"
            )
            u_incomplete = u_total - u_completed
            u_overdue = sum(
                1 for p in user_tasks if _is_overdue(p[4], p[5])
            )

            pct_of_total = (u_total / total_tasks * 100) if total_tasks else 0
            pct_done = (u_completed / u_total * 100) if u_total else 0
            pct_todo = (u_incomplete / u_total * 100) if u_total else 0
            pct_u_overdue = (u_overdue / u_total * 100) if u_total else 0

            f.write(f"--- {user} ---\n")
            f.write(f"  Tasks assigned:         {u_total}\n")
            f.write(f"  % of all tasks:         {pct_of_total:.1f}%\n")
            f.write(f"  % completed:            {pct_done:.1f}%\n")
            f.write(f"  % still to complete:    {pct_todo:.1f}%\n")
            f.write(f"  % overdue & incomplete: {pct_u_overdue:.1f}%\n\n")

    print("Reports generated: task_overview.txt and user_overview.txt\n")


#  Display Statistics

def display_statistics():
    """
    Display the contents of the report files.
    Generates them first if they don't exist yet.
    """
    import os
    if not os.path.exists("task_overview.txt") \
            or not os.path.exists("user_overview.txt"):
        print("Report files not found — generating now...\n")
        generate_reports()

    for filename in ("task_overview.txt", "user_overview.txt"):
        with open(filename, "r") as f:
            print(f.read())


#  Main

def main():
    username, is_admin = login()
    users = read_users()

    while True:
        if is_admin:
            menu = input(
                '''\nPlease select one of the following options:
r  - register user
a  - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete a task
ds - display statistics
gr - generate reports
e  - exit
: '''
            ).lower().strip()
        else:
            menu = input(
                '''\nPlease select one of the following options:
a  - add task
va - view all tasks
vm - view my tasks
e  - exit
: '''
            ).lower().strip()

        if menu == 'r':
            if not is_admin:
                print("Access denied. Only admin can register users.\n")
            else:
                reg_user(users)
                users = read_users()   # refresh after adding a new user

        elif menu == 'a':
            add_task(users)

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(username, users)

        elif menu == 'vc':
            if not is_admin:
                print("Access denied.\n")
            else:
                view_completed()

        elif menu == 'del':
            if not is_admin:
                print("Access denied.\n")
            else:
                delete_task()

        elif menu == 'gr':
            if not is_admin:
                print("Access denied.\n")
            else:
                generate_reports()

        elif menu == 'ds':
            if not is_admin:
                print("Access denied.\n")
            else:
                display_statistics()

        elif menu == 'e':
            print('Goodbye!!!')
            break

        else:
            print("Invalid input. Please try again.\n")


if __name__ == "__main__":
    main()
