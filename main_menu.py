from time_tracker_functions import (
    init_db,
    start_task,
    stop_task,
    view_active_tasks,
    view_ended_tasks,
    calculate_durations,
    export_to_csv,
)
from datetime import datetime

def display_active_tasks(active_tasks):
    """Helper function to display active tasks."""
    if active_tasks:
        print("\nActive Tasks:")
        for task in active_tasks:
            print(f"ID: {task[0]}, Task: {task[1]}, Category: {task[2]}, Started: {task[3]}")
    else:
        print("\nNo active tasks.")
    
def display_ended_tasks(ended_tasks):
    """Helper function to display ended tasks with duration."""
    if ended_tasks:
        print("\nEnded Tasks:")
        for task in ended_tasks:
            start_time = datetime.fromisoformat(task[3])
            end_time = datetime.fromisoformat(task[4])
            duration = end_time - start_time
            print(f"ID: {task[0]}, Task: {task[1]}, Category: {task[2]}, "
                  f"Started: {task[3]}, Ended: {task[4]}, Duration: {duration}")
    else:
        print("\nNo ended tasks.")


def main_menu():
    init_db()
    while True:
        print("\nTime Tracker Menu")
        print("1. Start Task")
        print("2. Stop Task")
        print("3. View Active Tasks")
        print("4. View Ended Tasks")
        print("5. Export Tasks to CSV")
        print("6. Calculate Task Durations")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            task_name = input("Task Name: ").strip()
            category = input("Category: ").strip()
            if task_name and category:
                start_task(task_name, category)
                print(f"Task '{task_name}' started in category '{category}'.")
            else:
                print("Task Name and Category cannot be empty.")

        elif choice == "2":
            active_tasks = view_active_tasks()
            display_active_tasks(active_tasks)
            if active_tasks:
                try:
                    task_id = int(input("Enter the ID of the task to stop: "))
                    if any(task[0] == task_id for task in active_tasks):
                        stop_task(task_id)
                        print(f"Task ID {task_id} stopped successfully.")
                    else:
                        print("Invalid Task ID.")
                except ValueError:
                    print("Please enter a valid numeric Task ID.")

        elif choice == "3":
            active_tasks = view_active_tasks()
            display_active_tasks(active_tasks)

        elif choice == "4":
            ended_tasks = view_ended_tasks()
            display_ended_tasks(ended_tasks)

        elif choice == "5":
            filename = input("Enter filename for export (default: tasks.csv): ").strip() or "tasks.csv"
            export_to_csv(filename)

        elif choice == "6":
            calculate_durations()


        elif choice == "7":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()

#commit
