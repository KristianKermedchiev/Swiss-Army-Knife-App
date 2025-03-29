from src.utils.file_utils import get_data_file_path
from src.db.db_interface import load_data, save_data

GOAL_DATA_FILE = get_data_file_path('goals.json')

def check_goal(goal_id):
    """Helper function to check whether we ascend towards a goal or descent."""
    goals = load_data(GOAL_DATA_FILE)
    flag = ''

    for goal in goals:
        if goal["id"] == goal_id:
            if int(goal['startingValue']) > int(goal['endValue']):
                flag = 'negative'
            else:
                flag = 'positive'

    return flag


def make_goal(name, unit, starting_value, end_value, category):
    """Create a new goal."""

    if name is None or unit is None or starting_value is None or end_value is None or category is None:
        print("Error: Name, unit, star value, end value and category are required.")
        return

    goals = load_data(GOAL_DATA_FILE)

    new_id = 1 if not goals else goals[-1]['id'] + 1

    goals.append({
        'id': new_id,
        'name': name,
        'unit': unit,
        'startingValue': starting_value,
        'endValue': end_value,
        'status': "In Progress",
        'progress': 0,
        'category': category,
        'archived': False
    })

    save_data(GOAL_DATA_FILE, goals)
    print(f"Goal '{name}' added successfully with ID {new_id}.")


def change_goal(goal_id, name=None, unit=None, starting_value=None, end_value=None, category=None):
    """Update an existing goal."""
    goals = load_data(GOAL_DATA_FILE)

    for goal in goals:
        if goal["id"] == goal_id:
            if name is not None:
                goal["name"] = name
            if unit is not None:
                goal["unit"] = unit
            if starting_value is not None:
                goal["startingValue"] = starting_value
            if end_value is not None:
                goal["endValue"] = end_value
            if category is not None:
                goal["category"] = category

            save_data(GOAL_DATA_FILE, goals)
            print(f"Goal with ID {goal_id} updated successfully.")
            return

    print(f"Error: Goal with ID {goal_id} not found.")


def list_goals():
    """List goals based on filters."""
    goals = load_data(GOAL_DATA_FILE)

    if not goals:
        print("\nNo goals found.")
        return

    for goal in goals:
        try:
            starting_value = float(goal['startingValue'])
        except ValueError:
            print(f"Invalid starting value for goal {goal['id']}: {goal['startingValue']}")
            starting_value = 0

        try:
            end_value = float(goal['endValue'])
        except ValueError:
            print(f"Invalid end value for goal {goal['id']}: {goal['endValue']}")
            end_value = 0

        try:
            progress = float(goal['progress'])
        except ValueError:
            print(f"Invalid progress value for goal {goal['id']}: {goal['progress']}")
            progress = 0

        if check_goal(goal["id"]) == "negative":
            if end_value != starting_value:
                current_value = starting_value - progress
                percent_progress = round(((starting_value - current_value) / (starting_value - end_value)) * 100, 2)
                if percent_progress > 100:
                    percent_progress = 100
            else:
                percent_progress = 0
        elif check_goal(goal["id"]) == "positive":
            if end_value != starting_value:
                current_value = starting_value + progress
                percent_progress = round(((current_value - starting_value) / (end_value - starting_value)) * 100, 2)
                if percent_progress > 100:
                    percent_progress = 100
            else:
                percent_progress = 0
        else:
            percent_progress = 0

        print(
            f"id: {goal['id']} / name: {goal['name']} / category: {goal['category']} / Start: {goal['startingValue']} "
            f"/ Target: {goal['endValue']} / unit: {goal['unit']}, "
            f"Progress: {percent_progress}% / status: {goal['status']} / archived: {goal['archived']}")



def delete_goal(goal_id):
    """Delete a goal by ID."""
    goals = load_data(GOAL_DATA_FILE)

    for goal in goals:
        if goal["id"] == goal_id:
            goals.remove(goal)
            save_data(GOAL_DATA_FILE, goals)
            print(f"Goal with ID {goal_id} deleted successfully.")
            return

    print(f"Error: Goal with ID {goal_id} not found.")


def archive_goal(goal_id):
    """Archive a goal by ID."""
    goals = load_data(GOAL_DATA_FILE)

    for goal in goals:
        if goal["id"] == goal_id:
            goal["archived"] = True
            save_data(GOAL_DATA_FILE, goals)
            print(f"Goal with ID {goal_id} archived successfully.")
            return

    print(f"Error: Goal with ID {goal_id} not found.")


def add_goal_progress(goal_id, value):
    """Add progress to an existing goal and update status if complete."""
    goals = load_data(GOAL_DATA_FILE)

    for goal in goals:
        if goal["id"] == goal_id:
            starting_value = float(goal["startingValue"])
            end_value = float(goal["endValue"])
            value = float(value)

            if check_goal(goal_id) == 'negative':
                goal["progress"] += value
                current_progress = starting_value - goal["progress"]
                percentage = ((starting_value - current_progress) / (starting_value - end_value)) * 100
            else:
                goal["progress"] += value
                current_progress = starting_value + goal["progress"]
                percentage = ((current_progress - starting_value) / (end_value - starting_value)) * 100

            if percentage >= 100:
                goal['status'] = 'Completed'
                goal["progress"] = end_value if check_goal(goal_id) == 'positive' else end_value
                save_data(GOAL_DATA_FILE, goals)
                print(f'Progress towards goal with ID {goal["id"]} added successfully.')
                print(f'Congratulations, you completed the goal "{goal["name"]}"!')
                return
            else:
                save_data(GOAL_DATA_FILE, goals)
                print(f'Progress towards goal with ID {goal["id"]} added successfully. Current progress: {round(percentage, 2)}%.')
                return

    print(f"Error: Goal with ID {goal_id} not found.")