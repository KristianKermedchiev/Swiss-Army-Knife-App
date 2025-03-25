from src.utils.file_utils import get_data_file_path
from src.db.db_interface import load_data, save_data

TODO_DATA_FILE = get_data_file_path('todos.json')

def list_todos():
    """List all todos."""
    todos = load_data(TODO_DATA_FILE)
    if not todos:
        print("\nNo todos found.")
        return

    print("\nList of todos:")
    for todo in todos:
        print(f"id: {todo['id']} / description: {todo['description']} / due_date: {todo['due_date']} / status: {todo['status']}")


def make_todo(description, due_date=None):
    """Create a new todo."""
    if description is None:
        print("Error: Description is required.")
        return

    if due_date is None:
        due_date = "No due date"

    todos = load_data(TODO_DATA_FILE)

    new_id = 1 if not todos else todos[-1]['id'] + 1

    todos.append({
        'id': new_id,
        'description': description,
        'due_date': due_date,
        'status': "incomplete"
    })

    save_data(TODO_DATA_FILE, todos)
    print(f"Todo '{description}' added successfully with ID {new_id}.")


def change_todo(todo_id, description=None, due_date=None, status=None):
    """Update an existing todo."""
    todos = load_data(TODO_DATA_FILE)

    for todo in todos:
        if todo["id"] == todo_id:
            if description is not None:
                todo["description"] = description
            if due_date is not None:
                todo["due_date"] = due_date
            if status is not None:
                todo["status"] = status

            save_data(TODO_DATA_FILE, todos)
            print(f"Todo with ID {todo_id} updated successfully.")
            return

    print(f"Error: Todo with ID {todo_id} not found.")


def delete_todo(todo_id):
    """Delete a todo by ID."""
    todos = load_data(TODO_DATA_FILE)

    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            save_data(TODO_DATA_FILE, todos)
            print(f"Todo with ID {todo_id} deleted successfully.")
            return

    print(f"Error: Todo with ID {todo_id} not found.")