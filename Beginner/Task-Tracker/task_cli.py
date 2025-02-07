import argparse
from task_tracker import TaskTracker


def main():

    parser = argparse.ArgumentParser(
        description="A CLI application to efficiently manage your tasks"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser('add', help="Add a new task")
    add_parser.add_argument('description', help="The Description of the task")
    add_parser.add_argument('status', choices=['todo', 'in-progress', 'done'], default='todo', help="The status of the task")

    subparsers.add_parser('list', help="List all tasks")

    update_parser = subparsers.add_parser('update', help="Update an existing task")
    update_parser.add_argument('task_id', help="The ID of the task to update")
    update_parser.add_argument('new_description', help="The new description of the task")

    delete_parser = subparsers.add_parser('delete', help="Delete an existing task")
    delete_parser.add_argument('task_id', help="The ID of the task to delete")

    in_progress_parser = subparsers.add_parser('mark_in_progress_task', help="Mark a task as 'in-progress'")
    in_progress_parser.add_argument('task_id', help="The ID of the task")

    done_parser = subparsers.add_parser('mark_done_task', help="Mark a task as 'done'")
    done_parser.add_argument('task_id', help="The ID of the task")

    list_status_parser = subparsers.add_parser('list_task_status', help="List tasks filtered by status")
    list_status_parser.add_argument('status', choices=['todo', 'in-progress', 'done'], help="Filter tasks by status")

    args = parser.parse_args()

    my_tasks = TaskTracker()

    if args.command == 'add':
        my_tasks.add_task(args.description)
    
    elif args.command == 'list':
        my_tasks.list_tasks()

    elif args.command == 'update':
        my_tasks.update_task(args.task_id, args.new_description)

    elif args.command == 'delete':
        my_tasks.delete_task(args.task_id)

    elif args.command == 'mark_in_progress_task':
        my_tasks.mark_in_progress(args.task_id)

    elif args.command == 'mark_done_task':
        my_tasks.mark_done(args.task_id)

    elif args.command == 'list_task_status':
        my_tasks.filter_tasks_by_status(args.status)

    else:
        print("Invalid command. Use --help for usage.")

if __name__ == "__main__":
    main()