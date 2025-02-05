import json
import os
import datetime
import pandas as pd

HABITS_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'habits.json')


def load_habits():
    """Load habits data from the JSON file."""
    if os.path.exists(HABITS_DATA_FILE):
        with open(HABITS_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_habits(habits):
    """Save habits data to the JSON file."""
    with open(HABITS_DATA_FILE, 'w') as file:
        json.dump(habits, file, indent=4)


def make_habit(name, goal, unit):
    """Create a new habit."""

    if name is None or goal is None or unit is None:
        print("Error: Name, goal and unit are required.")
        return

    habits = load_habits()
    new_id = 1 if not habits else habits[-1]['id'] + 1

    habits.append({
        'id': new_id,
        'name': name,
        'goal': goal,
        'unit': unit,
        'log': []
    })
    save_habits(habits)
    print(f"Habit '{name}' added successfully with ID {new_id}.")


def mark_habit(id):
    """Mark a habit as completed for the day."""
    habits = load_habits()
    today = datetime.datetime.now().strftime('%d/%m/%Y')

    for habit in habits:
        if habit['id'] == id:
            habit['log'].append({'date': today, 'completed': "completed"})
            save_habits(habits)
            print(f"Habit '{habit['name']}' marked as completed.")
            return
    print("Error: Habit not found.")


def list_habits(date=None, id=None):
    """List habits based on filters."""
    habits = load_habits()

    if id:
        habit = next((h for h in habits if h['id'] == id), None)
        if habit:
            print(f"Habit: {habit['name']}")
            for log in habit['log']:
                print(f"{habit['name']}: {habit['goal']} {habit['unit']} - {log['completed']}")
        else:
            print("Habit not found.")
        return

    if date:
        print(f"Habits completed on {date}:")
        for habit in habits:
            for log in habit['log']:
                if log['date'] == date:
                    print(f"{habit['name']}: {habit['goal']} {habit['unit']} - {log['completed']}")
        return

    if not habits:
        print("No habits found.")
        return

    for habit in habits:
        print(f"{habit['id']}. {habit['name']} - Target: {habit['goal']} {habit['unit']}")


def delete_habit(id):
    """Remove a habit by ID."""
    habits = load_habits()
    habits = [habit for habit in habits if habit['id'] != id]
    save_habits(habits)
    print(f"Habit with ID {id} deleted successfully.")


def change_habit(id, name=None, goal=None, unit=None):
    """Modify a habit's properties."""
    habits = load_habits()
    for habit in habits:
        if habit['id'] == id:
            if name:
                habit['name'] = name
            if goal:
                habit['goal'] = goal
            if unit:
                habit['unit'] = unit
            save_habits(habits)
            print(f"Habit ID {id} updated successfully.")
            return
    print("Error: Habit not found.")


def habit_log(id, download=False):
    """Check current and longest streak of a habit."""
    habits = load_habits()
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
        df = pd.DataFrame({'Date': [date.strftime('%d/%m/%Y') for date in log_dates]})
        file_name = f"habit_{id}_log.csv"
        df.to_csv(file_name, index=False)
        print(f"Habit log saved as '{file_name}'")