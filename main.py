from flask import Flask, render_template, request, redirect, url_for, flash, session
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
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Initialize database
init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Add your authentication logic here
        # For demonstration, using simple validation
        if email == "admin@example.com" and password == "password":
            session['user_id'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    active_tasks = view_active_tasks()
    ended_tasks = view_ended_tasks()
    return render_template('dashboard.html', 
                         active_tasks=active_tasks, 
                         ended_tasks=ended_tasks)

@app.route('/start_task', methods=['POST'])
@login_required
def start_new_task():
    task_name = request.form.get('task_name')
    category = request.form.get('category')
    if task_name and category:
        start_task(task_name, category)
        flash(f"Task '{task_name}' started in category '{category}'.")
    else:
        flash("Task Name and Category cannot be empty.")
    return redirect(url_for('dashboard'))

@app.route('/stop_task/<int:task_id>')
@login_required
def stop_current_task(task_id):
    active_tasks = view_active_tasks()
    if any(task[0] == task_id for task in active_tasks):
        stop_task(task_id)
        flash(f"Task ID {task_id} stopped successfully.")
    else:
        flash("Invalid Task ID.")
    return redirect(url_for('dashboard'))

@app.route('/export_csv')
@login_required
def export_tasks():
    filename = "tasks.csv"
    try:
        export_to_csv(filename)
        flash(f"Tasks exported to {filename} successfully.")
    except Exception as e:
        flash(f"Error exporting tasks: {str(e)}")
    return redirect(url_for('dashboard'))

@app.route('/calculate_durations')
@login_required
def calc_durations():
    calculate_durations()
    flash("Task durations calculated successfully.")
    return redirect(url_for('dashboard'))

# Template filters
@app.template_filter('format_duration')
def format_duration(start_time, end_time):
    if not end_time:
        return "Active"
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    return str(end - start)

if __name__ == "__main__":
    print("Starting Flask server...")
    try:
        app.run(debug=True, host='127.0.0.1', port=8070)  # Changed to port 8080
        print("Server is running at http://127.0.0.1:8070")
    except Exception as e:
        print(f"Error starting server: {e}")