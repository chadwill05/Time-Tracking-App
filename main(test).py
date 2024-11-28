import sqlite3
from datetime import datetime

# initialize database
def init_db():
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task_name TEXT,
            category TEXT,
            start_time TEXT,
            end_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

#start a task
def start_task(task_name, category):
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    start_time = datetime.now().isoformat()
    cursor.execute("INSERT INTO tasks (task_name, category, start_time) VALUES (?, ?, ?)",
                   (task_name, category, start_time))
    conn.commit()
    conn.close()
    print(f"Started task: {task_name}")

# Stop a task
def stop_task(task_id):
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    end_time = datetime.now().isoformat()
    cursor.execute("UPDATE tasks SET end_time = ? WHERE id = ?", (end_time, task_id))
    conn.commit()
    conn.close()
    print(f"Stopped task with ID: {task_id}")

# View active tasks
def view_active_tasks():
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, category, start_time FROM tasks WHERE end_time IS NULL")
    active_tasks = cursor.fetchall()
    conn.close()
    
    if active_tasks:
        print("\nActive Tasks:")
        for task in active_tasks:
            print(f"ID: {task[0]}, Task: {task[1]}, Category: {task[2]}, Started: {task[3]}")
    else:
        print("\nNo active tasks.")

# View ended tasks
def view_ended_tasks():
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, category, start_time, end_time FROM tasks WHERE end_time IS NOT NULL")
    ended_tasks = cursor.fetchall()
    conn.close()
    
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

# Main Menu
def main():
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
            view_active_tasks()
            task_id = int(input("Enter the ID of the task to stop: "))
            stop_task(task_id)
        elif choice == "3":
            view_active_tasks()
        elif choice == "4":
            view_ended_tasks()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()