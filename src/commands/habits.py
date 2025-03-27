import datetime
import pandas as pd
from src.utils.file_utils import get_data_file_path
from src.db.db_interface import load_data, save_data

HABITS_DATA_FILE = get_data_file_path('habits.json')

def make_habit(name, goal, unit):
    """Create a new habit."""

    if name is None or goal is None or unit is None:
        print("Error: Name, goal and unit are required.")
        return

    habits = load_data(HABITS_DATA_FILE)
    new_id = 1 if not habits else habits[-1]['id'] + 1

    habits.append({
        'id': new_id,
        'name': name,
        'goal': goal,
        'unit': unit,
        'log': []
    })
    save_data(HABITS_DATA_FILE, habits)
    print(f"Habit '{name}' added successfully with ID {new_id}.")


def mark_habit(id):
    """Mark a habit as completed for the day."""
    habits = load_data(HABITS_DATA_FILE)
    today = datetime.datetime.now().strftime('%d/%m/%Y')

    for habit in habits:
        if habit['id'] == id:
            habit['log'].append({'date': today, 'completed': "completed"})
            save_data(HABITS_DATA_FILE, habits)
            print(f"Habit '{habit['name']}' marked as completed.")
            return
    print("Error: Habit not found.")


def list_habits(date=None, id=None):
    """List habits based on filters."""
    habits = load_data(HABITS_DATA_FILE)

    if id:
        habit = next((h for h in habits if h['id'] == id), None)
        if habit:
            print(f"Habit: {habit['name']}")
            for log in habit['log']:
                print(f"name: {habit['name']} / goal: {habit['goal']} / unit: {habit['unit']} / date: {log['date']} / log: {log['completed']}")
        else:
            print("Habit not found.")
        return

    if date:
        print(f"Habits completed on {date}:")
        for habit in habits:
            for log in habit['log']:
                if log['date'] == date:
                    print(f"name: {habit['name']} / goal: {habit['goal']} / unit: {habit['unit']} / log: {log['completed']}")
        return

    if not habits:
        print("No habits found.")
        return

    for habit in habits:
        print(f"name: {habit['name']} / goal: {habit['goal']} / unit: {habit['unit']}")


def delete_habit(id):
    """Remove a habit by ID."""

    if id is None:
        print("Error: Habit ID is required.")
        return

    habits = load_data(HABITS_DATA_FILE)
    habits = [habit for habit in habits if habit['id'] != id]
    save_data(HABITS_DATA_FILE, habits)
    print(f"Habit with ID {id} deleted successfully.")


def change_habit(id, name=None, goal=None, unit=None):
    """Modify a habit's properties."""
    habits = load_data(HABITS_DATA_FILE)
    for habit in habits:
        if habit['id'] == id:
            if name:
                habit['name'] = name
            if goal:
                habit['goal'] = goal
            if unit:
                habit['unit'] = unit
            save_data(HABITS_DATA_FILE, habits)
            print(f"Habit ID {id} updated successfully.")
            return
    print("Error: Habit not found.")


def habit_log(id, download=False):
    """Check current and longest streak of a habit."""
    habits = load_data(HABITS_DATA_FILE)
    habit = next((h for h in habits if h['id'] == id), None)

    if not habit:
        print("Error: Habit not found.")
        return

    log_dates = sorted(
        [datetime.datetime.strptime(log['date'], '%d/%m/%Y') for log in habit['log']],
        key=lambda x: x
    )

    current_streak = 0
    longest_streak = 0
    previous_date = None
    today = datetime.datetime.today()

    for date_obj in log_dates:
        if previous_date and (date_obj - previous_date).days == 1:
            current_streak += 1
        else:
            current_streak = 1
        longest_streak = max(longest_streak, current_streak)
        previous_date = date_obj

    if log_dates and (today - log_dates[-1]).days > 1:
        current_streak = 0

    print(f"Current streak: {current_streak} days")
    print(f"Longest streak: {longest_streak} days")

    if download:
        # Create a list of dictionaries for each log entry, including habit data
        habit_data_for_csv = []
        for log_entry in habit['log']:
            habit_data_for_csv.append({
                'id': habit['id'],
                'name': habit['name'],
                'goal': habit['goal'],
                'unit': habit['unit'],
                'date': log_entry['date'],
                'completed': log_entry['completed']
            })

        # Create the DataFrame
        df = pd.DataFrame(habit_data_for_csv)

        # Save to CSV
        file_name = f"habit_{id}_log.csv"
        df.to_csv(file_name, index=False)
        print(f"Habit log saved as '{file_name}'")