import json
import os

TODO_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'todos.json')


def load_todos():
    """Load todos data from the JSON file."""
    if os.path.exists(TODO_DATA_FILE):
        with open(TODO_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_todos(todos):
    """Save todos data to the JSON file."""
    with open(TODO_DATA_FILE, 'w') as file:
        json.dump(todos, file, indent=4)


def list_todos():
    """List all todos."""
    todos = load_todos()
    if not todos:
        print("\nNo todos found.")
        return

    print("\nList of todos:")
    for todo in todos:
        print(f"{todo['id']} / {todo['description']} / {todo['due_date']} / {todo['status']}")


def make_todo(description, due_date=None):
    """Create a new todo."""
    if description is None:
        print("Error: Description is required.")
        return

    if due_date is None:
        due_date = "No due date"

    todos = load_todos()

    new_id = 1 if not todos else todos[-1]['id'] + 1

    todos.append({
        'id': new_id,
        'description': description,
        'due_date': due_date,
        'status': "incomplete"
    })

    save_todos(todos)
    print(f"Todo '{description}' added successfully with ID {new_id}.")


def change_todo(todo_id, description=None, due_date=None, status=None):
    """Update an existing todo."""
    todos = load_todos()

    for todo in todos:
        if todo["id"] == todo_id:
            if description is not None:
                todo["description"] = description
            if due_date is not None:
                todo["due_date"] = due_date
            if status is not None:
                todo["status"] = status

            save_todos(todos)
            print(f"Todo with ID {todo_id} updated successfully.")
            return

    print(f"Error: Todo with ID {todo_id} not found.")


def delete_todo(todo_id):
    """Delete a todo by ID."""
    todos = load_todos()

    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            save_todos(todos)
            print(f"Todo with ID {todo_id} deleted successfully.")
            return

    print(f"Error: Todo with ID {todo_id} not found.")