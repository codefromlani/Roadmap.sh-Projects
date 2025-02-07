import json
import os
from datetime import datetime
import uuid


class TaskTracker():

    VALID_STATUSES = ['todo', 'in-progress', 'done']

    def __init__(self, file_path = 'tasks.json'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):

        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w') as f:
                    json.dump([], f)

            with open(self.file_path, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def save_tasks(self):

        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.tasks, f, indent=4)

        except Exception as e:
            print(f"Error saving tasks: {e}") 


    def add_task(self, description: str, status: str = 'todo') -> None:

        if status not in self.VALID_STATUSES:
            print(f"Invalid status. Valid options are: {self.VALID_STATUSES}")
            return

        date: str = datetime.now().isoformat()
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "description": description,
            "status": status,
            "created_at": date,
            "updated_at": date
        }

        self.tasks.append(new_task)
        self.save_tasks()

        print(f"Task with ID {task_id} created succefully with status '{status}'!")

    def list_tasks(self) -> None:

        if not self.tasks:
            print("No tasks available.")
        
        else:
            print("All Tasks List:")
            for task in self.tasks:
                print(
                    f"ID: {task['id']}, "
                    f"Description: {task['description']}, "
                    f"Status: {task['status']}, "
                    f"Created_at: {task['created_at']}, "
                    f"Updated_at: {task['updated_at']}"
                )


    def update_task(self, task_id: str, description: str) -> None:

        for task in self.tasks:
            if task["id"] == task_id:
                task["description"] = description
                task["updated_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task {task_id} updated to '{description}' with status '{task['status']}'")
                return
        
        print(f"No task found with ID {task_id}")

    def delete_task(self, task_id: str) -> None:

        original_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]

        if len(self.tasks) < original_length:
            self.save_tasks()
            print(f"Task {task_id} deleted")
        else:
            print(f"No task found with ID {task_id}")

    def mark_in_progress(self, task_id: str) -> None:

        for task in self.tasks:
            if task["id"] == task_id:
                if task["status"] == 'in-progress':
                    print(f"Task {task_id} is already in-progress.")
                    return
                
                task["status"] = 'in-progress'
                self.save_tasks()
                print(f"Task {task_id} marked as 'in-progress'.")
                return
            
        print(f"No task found with ID {task_id}.")

    def mark_done(self, task_id: str) -> None:

        for task in self.tasks:
            if task["id"] == task_id:
                if task["status"] == 'done':
                    print(f"Task {task_id} is already done.")
                    return
                
                task["status"] = 'done'
                self.save_tasks()
                print(f"Task {task_id} marked as 'done'.")
                return
            
        print(f"No task found with ID {task_id}.")

    def filter_tasks_by_status(self, status: str = None) -> None:

        if status is None:
            self.list_tasks()
            return

        if status not in self.VALID_STATUSES:
            print(f"Invalid status. Valid options are: {self.VALID_STATUSES}")
            return

        filtered_tasks = [task for task in self.tasks if task["status"] == status]

        if not filtered_tasks:
            print(f"No tasks with status '{status}' found.")
            return
        
        print(f"Tasks with status '{status}':")
        for task in filtered_tasks:
            print(
                f"ID: {task['id']}, "
                f"Description: {task['description']}, "
                f"Status: {task['status']}, "
                f"Created_at: {task['created_at']}, "
                f"Updated_at: {task['updated_at']}"
            )