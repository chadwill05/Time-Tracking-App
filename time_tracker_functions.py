import sqlite3
from datetime import datetime

def init_db():
    try:
        conn = sqlite3.connect("time_tracker.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task_name TEXT,
                category TEXT,
                start_time TEXT,
                end_time TEXT,
                duration INTEGER
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

#def update_schema():
#    conn = sqlite3.connect("time_tracker.db")
#    cursor = conn.cursor()
#    # Check if the 'duration' column exists
#    cursor.execute("PRAGMA table_info(tasks)")
#    columns = [col[1] for col in cursor.fetchall()]
#    if "duration" not in columns:
#        # Add the 'duration' column
#        cursor.execute("ALTER TABLE tasks ADD COLUMN duration INTEGER")
#        print("Database schema updated: 'duration' column added.")
#    conn.commit()
#    conn.close()

def start_task(task_name, category):
    """Start a new task by adding it to the database."""
    try:
        conn = sqlite3.connect("time_tracker.db")
        cursor = conn.cursor()
        start_time = datetime.now().isoformat()
        cursor.execute("INSERT INTO tasks (task_name, category, start_time) VALUES (?, ?, ?)",
                       (task_name, category, start_time))
        conn.commit()
        print(f"Started task: {task_name}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def stop_task(task_id):
    """Stop an active task by updating its end_time in the database."""
    try:
        conn = sqlite3.connect("time_tracker.db")
        cursor = conn.cursor()
        end_time = datetime.now().isoformat()
        cursor.execute("UPDATE tasks SET end_time = ? WHERE id = ?", (end_time, task_id))
        if cursor.rowcount == 0:
            print(f"No active task found with ID: {task_id}")
        else:
            print(f"Stopped task with ID: {task_id}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def view_active_tasks():
    """Fetch and return all active tasks (tasks without an end_time)."""
    try:
        conn = sqlite3.connect("time_tracker.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_name, category, start_time FROM tasks WHERE end_time IS NULL")
        active_tasks = cursor.fetchall()
        return active_tasks
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def view_ended_tasks():
    """Fetch and return all ended tasks (tasks with an end_time)."""
    try:
        conn = sqlite3.connect("time_tracker.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_name, category, start_time, end_time FROM tasks WHERE end_time IS NOT NULL")
        ended_tasks = cursor.fetchall()
        return ended_tasks
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def calculate_duration(start_time, end_time):
    """Calculate the duration between start_time and end_time."""
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    duration = end - start
    return duration

def export_to_csv(filename="tasks.csv"):
    """Export all tasks to a CSV file."""
    try:
        import csv
        conn = sqlite3.connect("time_tracker.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_name, category, start_time, end_time FROM tasks")
        tasks = cursor.fetchall()
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Task Name", "Category", "Start Time", "End Time"])
            writer.writerows(tasks)
        print(f"Tasks exported to {filename}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
    finally:
        conn.close()

def calculate_durations():
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    # Update the duration for tasks with an end_time
    cursor.execute("""
        UPDATE tasks
        SET duration = CAST((JULIANDAY(end_time) - JULIANDAY(start_time)) * 24 * 60 AS INTEGER)
        WHERE end_time IS NOT NULL AND duration IS NULL;
    """)
    conn.commit()
    conn.close()
    print("Durations calculated and updated.")
