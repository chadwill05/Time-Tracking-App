from time_tracker_functions import init_db, start_task, stop_task, view_active_tasks, view_ended_tasks
from datetime import datetime


def main_menu():
    init_db()
    while True:
        print("\nTime Tracker Menu")
        print("1. Start Task")
        print("2. Stop Task")
        print("3. View Active Tasks")
        print("4. View Ended Tasks")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            task_name = input("Task Name: ")
            category = input("Category: ")
            start_task(task_name, category)
        elif choice == "2":
            active_tasks = view_active_tasks()
            if active_tasks:
                print("\nActive Tasks:")
                for task in active_tasks:
                    print(f"ID: {task[0]}, Task: {task[1]}, Category: {task[2]}, Started: {task[3]}")
                task_id = int(input("Enter the ID of the task to stop: "))
                stop_task(task_id)
            else:
                print("\nNo active tasks.")
        elif choice == "3":
            active_tasks = view_active_tasks()
            if active_tasks:
                print("\nActive Tasks:")
                for task in active_tasks:
                    print(f"ID: {task[0]}, Task: {task[1]}, Category: {task[2]}, Started: {task[3]}")
            else:
                print("\nNo active tasks.")
        elif choice == "4":
            ended_tasks = view_ended_tasks()
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
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
