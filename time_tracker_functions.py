import sqlite3
from datetime import datetime

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

def start_task(task_name, category):
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    start_time = datetime.now().isoformat()
    cursor.execute("INSERT INTO tasks (task_name, category, start_time) VALUES (?, ?, ?)",
                   (task_name, category, start_time))
    conn.commit()
    conn.close()
    print(f"Started task: {task_name}")

def stop_task(task_id):
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    end_time = datetime.now().isoformat()
    cursor.execute("UPDATE tasks SET end_time = ? WHERE id = ?", (end_time, task_id))
    conn.commit()
    conn.close()
    print(f"Stopped task with ID: {task_id}")

def view_active_tasks():
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, category, start_time FROM tasks WHERE end_time IS NULL")
    active_tasks = cursor.fetchall()
    conn.close()
    return active_tasks

def view_ended_tasks():
    conn = sqlite3.connect("time_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, category, start_time, end_time FROM tasks WHERE end_time IS NOT NULL")
    ended_tasks = cursor.fetchall()
    conn.close()
    return ended_tasks
