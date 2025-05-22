# Task Tracker CLI 

A simple command-line tool to manage tasks. You can add, update, list, delete, and change the status of tasks. This project is built in Python using the `argparse` module for CLI interaction and stores task data in a `JSON` file.

## Features

- **Add a Task**: Create new tasks with a description and a status.
- **List Tasks**: View all tasks 
- **Update Task**: Modify the description of an existing task.
- **Delete Task**: Remove a task by its ID.
- **Mark Task as In-Progress**: Change the status of a task to "in-progress."
- **Mark Task as Done**: Change the status of a task to "done."
- **Filter Tasks by Status**: View tasks filtered by their status (e.g., `todo`, `in-progress`, `done`).

## Requirements

- Python 3.12+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/codefromlani/Roadmap.sh-Projects.git
cd beginner
cd task-tracker
```

## Usage

You can run the application directly from the command line using Python. Below are the available commands:

1. Add a new task:
```bash
python task_cli.py add "Task description" todo
```

2. List all tasks:
```bash
python task_cli.py list
```

3. Update an existing task:
```bash
python task_cli.py update <task_id> "New task description" 
```
<task_id>: The ID of the task you want to update.

4. Delete an existing task:
```bash
python task_cli.py delete <task_id>
```

5. Mark a task as in-progress:
```bash
python task_cli.py mark_in_progress_task <task_id>
```

6. Mark a task as done:
```bash
python task_cli.py mark_done_task <task_id>
```

7. Filter tasks by status:
```bash
python task_cli.py list_task_status <status>
```
<status>: Filter tasks by their current status (todo, in-progress, done).


## Data Storage

The tasks are stored in a tasks.json file. If the file doesn't exist, it will be created when you add the first task.