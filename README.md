# Task-Manager-project

A command-line task management application built in Python. It lets a small team log in, register users, assign tasks, track progress, and generate summary reports, with all data stored in plain text files.

The project was built in three stages, each saved as its own script so you can see how the program evolves from a simple procedural script into a modular, function-based application.

## Project Structure

| File | Stage | Description |
|------|-------|-------------|
| `task_manager.py` | Practical Task 1 | Core functionality: login, register users, add tasks, view all tasks, view my tasks |
| `task_manager_admin.py` | Practical Task 2 | Adds role-based access (admin vs. standard user), completed-task view, and task deletion. Introduces helper functions |
| `task_manager_task_3.py` | Practical Task 3 | Fully refactored into functions with a `main()` entry point. Adds task editing, mark-as-complete, date validation, and report generation |

## Features

### Stage 1: `task_manager.py`
- Login with credentials read from `user.txt`
- Register new users (with duplicate-username and password-confirmation checks)
- Add tasks and assign them to existing users
- View all tasks or only your own

### Stage 2: `task_manager_admin.py`
Everything in Stage 1, plus:
- **Role-based access:** the `admin` user sees an extended menu; standard users see a reduced one
- Admin-only **user registration**
- Admin-only **view completed tasks** (`vc`)
- Admin-only **delete tasks** (`del`)
- Reusable helpers: `print_task()`, `read_tasks()`, `write_tasks()`

### Stage 3: `task_manager_task_3.py`
Everything in Stage 2, plus:
- Code organised into functions (`login`, `reg_user`, `add_task`, `view_all`, `view_mine`, etc.) and run through `main()`
- **Mark tasks as complete** or **edit** the assignee and due date (only while a task is incomplete)
- **Due-date validation** using `datetime.strptime` (format: `DD Mon YYYY`)
- Recursive input validation for task selection (`get_valid_task_number`)
- **Report generation** (`gr`) producing `task_overview.txt` and `user_overview.txt`
- **Display statistics** (`ds`) to print the reports in the terminal (generates them first if missing)

## Requirements

- Python 3.6 or higher
- No external libraries are needed (only the standard library: `datetime`, `os`)

## Getting Started
1. **Download the txt files** to be saved in the same folder as the scripts.
   At minimum you need a `user.txt` containing an `admin` account, 

2. **Run the version you want**
`Default user: admin`
`Password: adm1n`
   python task_manager.py          # Stage 1
   python task_manager_admin.py    # Stage 2
   python task_manager_task_3.py   # Stage 3 (most complete)


## Data File Formats

All data is stored as comma-and-space separated plain text, one record per line.

**`user.txt`**: `username, password`
```
admin, your_password_here
jane, her_password_here
```

**`tasks.txt`**: `assigned_to, title, description, date_assigned, due_date, completed`
```
jane, Prepare report, Compile the monthly sales report, 01 Oct 2026, 15 Oct 2026, No
```

Notes:
- Dates use the format `DD Mon YYYY` (e.g. `01 Jan 2026`).
- The completed field is `Yes` or `No`.
- Because fields are split on `", "`, avoid using a comma followed by a space inside titles or descriptions.
- `tasks.txt` is created automatically in Stages 1 and 3 when the first task is added. In Stage 1, create an empty `tasks.txt` beforehand if you want to view tasks before adding any.

## Usage

After logging in, enter the letter code for the action you want.

**Standard user menu**

| Option | Action |
|--------|--------|
| `a` | Add a task |
| `va` | View all tasks |
| `vm` | View my tasks |
| `e` | Exit |

**Admin menu** (user `admin`; Stage 1 has a smaller menu, see above)

| Option | Action |
|--------|--------|
| `r` | Register a new user |
| `a` | Add a task |
| `va` | View all tasks |
| `vm` | View my tasks (Stage 3: select a task to complete or edit) |
| `vc` | View completed tasks (Stages 2–3) |
| `del` | Delete a task (Stages 2–3) |
| `gr` | Generate reports (Stage 3) |
| `ds` | Display statistics (Stage 3) |
| `e` | Exit |

### Example report output (`task_overview.txt`)

```
==================================================
           TASK OVERVIEW REPORT
==================================================

Total tasks:              10
Completed tasks:          4
Uncompleted tasks:        6
Overdue & incomplete:     2
% Incomplete:             60.0%
% Overdue:                20.0%
```

## Author

**Siboniso Zikhali**

## License

This project is open source and available under the [MIT License](LICENSE).
