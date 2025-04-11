import shlex
from commands.todos import make_todo, list_todos, change_todo, delete_todo

def lstodos(arg):
    list_todos()

def mktodo(arg):
    try:
        args = shlex.split(arg)
        description = None
        due_date = None

        if "-description" in args:
            description = args[args.index("-description") + 1]
        if "-duedate" in args:
            due_date = args[args.index("-duedate") + 1]

        if description:
            make_todo(description, due_date)
        else:
            print("Error: -description is required.")
    except (ValueError, IndexError) as e:
        print("Error: Invalid arguments. Usage: mktodo -description <description> [-duedate <due_date>]")

def chtodo(arg):
    try:
        args = shlex.split(arg)
        todo_id = None
        description = None
        due_date = None
        status = None

        if "-id" in args:
            todo_id = int(args[args.index("-id") + 1])
        if "-description" in args:
            description = args[args.index("-description") + 1]
        if "-duedate" in args:
            due_date = args[args.index("-duedate") + 1]
        if "-status" in args:
            status = args[args.index("-status") + 1]

        if todo_id is not None:
            change_todo(todo_id, description, due_date, status)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError) as e:
        print(
            "Error: Invalid arguments. Usage: chtodo -id <id> [-description <description>] [-duedate <due_date>]")

def rmtodo(arg):
    try:
        args = shlex.split(arg)
        todo_id = None

        if "-id" in args:
            todo_id = int(args[args.index("-id") + 1])

        if todo_id is not None:
            delete_todo(todo_id)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError) as e:
        print("Error: Invalid arguments. Usage: rmtodo -id <id>")