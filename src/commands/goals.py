"""2. Goal Manager
Purpose: Store tasks, ideas, goals and personal improvements.
mkgoal - Create a goal, -id, -name, -measuringUnit, -endGoalValue, -startGoalValue, -status, -progress, -category, -archived: True/False
rmgoal - Remove a goal, -id
lsgoals - List goals, optional: -id, -category, -progress, -status, -archived, filtered by archived:False first
archivegoal - Archive a goal by changing the status to archive
chgoal - Modify the goal, -id, -name, -measuringUnit, -endGoalValue, -startGoalValue, -status, -progress, -category, -archived: True/False
addgoalprogress - Add goal progress -id, -value (+=currentValue). check if progress becomes 100% and notify user and change status to Complete
"""


import json
import os

GOAL_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'goals.json')


def load_goals():
    """Load goals data from the JSON file."""
    if os.path.exists(GOAL_DATA_FILE):
        with open(GOAL_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_goals(goals):
    """Save goals data to the JSON file."""
    with open(GOAL_DATA_FILE, 'w') as file:
        json.dump(goals, file, indent=4)


def check_goal(goal_id):
    """Helper function to check whether we ascend towards a goal or descent."""
    goals = load_goals()
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

    goals = load_goals()

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

    save_goals(goals)
    print(f"Goal '{name}' added successfully with ID {new_id}.")


def change_goal(goal_id, name=None, unit=None, starting_value=None, end_value=None, category=None):
    """Update an existing goal."""
    goals = load_goals()

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

            save_goals(goals)
            print(f"Goal with ID {goal_id} updated successfully.")
            return

    print(f"Error: Goal with ID {goal_id} not found.")


def list_goals():
    """List goals based on filters."""
    goals = load_goals()

    if not goals:
        print("\nNo goals found.")
        return

    for goal in goals:
        starting_value = int(goal['startingValue'])
        end_value = int(goal['endValue'])
        progress = int(goal['progress'])

        if check_goal(goal["id"]) == "negative":
            current_value = starting_value - progress
            percent_progress = round(((starting_value - current_value) / (starting_value - end_value)) * 100, 2)
            if percent_progress > 100:
                percent_progress = 100
        elif check_goal(goal["id"]) == "positive":
            current_value = starting_value + progress
            percent_progress = round(((current_value - starting_value) / (end_value - starting_value)) * 100, 2)
            if percent_progress > 100:
                percent_progress = 100
        else:
            percent_progress = 0

        print(f"{goal['id']}. {goal['name']} in category {goal['category']} Start: {goal['startingValue']} - Target: {goal['endValue']} {goal['unit']}, "
              f"Progress: {percent_progress}%, status: {goal['status']}, archived: {goal['archived']}")



def delete_goal(goal_id):
    """Delete a goal by ID."""
    goals = load_goals()

    for goal in goals:
        if goal["id"] == goal_id:
            goals.remove(goal)
            save_goals(goals)
            print(f"Goal with ID {goal_id} deleted successfully.")
            return

    print(f"Error: Goal with ID {goal_id} not found.")


def archive_goal(goal_id):
    """Archive a goal by ID."""
    goals = load_goals()

    for goal in goals:
        if goal["id"] == goal_id:
            goal["archived"] = True
            save_goals(goals)
            print(f"Goal with ID {goal_id} archived successfully.")
            return

    print(f"Error: Goal with ID {goal_id} not found.")


def add_goal_progress(goal_id, value):
    """Add progress to an existing goal and update status if complete."""
    goals = load_goals()

    for goal in goals:
        if goal["id"] == goal_id:
            starting_value = int(goal["startingValue"])
            end_value = int(goal["endValue"])
            value = int(value)

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
                save_goals(goals)
                print(f'Progress towards goal with ID {goal["id"]} added successfully.')
                print(f'Congratulations, you completed the goal "{goal["name"]}"!')
                return
            else:
                save_goals(goals)
                print(f'Progress towards goal with ID {goal["id"]} added successfully. Current progress: {round(percentage, 2)}%.')
                return

    print(f"Error: Goal with ID {goal_id} not found.")