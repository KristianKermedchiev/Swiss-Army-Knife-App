import cmd
import shlex
from commands.expenses import make_expense, list_expenses, change_expense, delete_expense
from commands.todos import make_todo, list_todos, change_todo, delete_todo


class TodoAppCLI(cmd.Cmd):
    intro = "Welcome to your CLI To-Do App! Type 'help' or '?' to list commands."
    prompt = "(CLI) "


    def do_lsexpense(self, arg):
        """List all expenses."""
        list_expenses()


    def do_mkexpense(self, arg):
        """
        Create a new expense.
        Usage: mkexpense -description <description> -amount <amount> -date <date> (optional)
        """
        try:
            args = shlex.split(arg)
            description = None
            amount = None
            date = None

            if "-description" in args:
                description = args[args.index("-description") + 1]
            if "-amount" in args:
                amount = args[args.index("-amount") + 1]
            if "-date" in args:
                date = args[args.index("-date") + 1]

            if description and amount:
                make_expense(description, amount, date)
            else:
                print("Error: Both -description and -amount are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: mkexpense -description <description> -amount <amount>")

    def do_chexpense(self, arg):
        """
        Modify an existing expense.
        Usage: chexpense -id <id> [-description <description>] [-amount <amount>] [-date <date>] (optional)
        """
        try:
            # Parse arguments
            args = shlex.split(arg)
            expense_id = None
            description = None
            amount = None
            date = None

            if "-id" in args:
                expense_id = int(args[args.index("-id") + 1])
            if "-description" in args:
                description = args[args.index("-description") + 1]
            if "-amount" in args:
                amount = float(args[args.index("-amount") + 1])
            if "-date" in args:
                date = args[args.index("-date") + 1]

            if expense_id is not None:
                change_expense(expense_id=expense_id, description=description, amount=amount, date=date)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: chexpense -id <id> [-description <description>] [-amount <amount>]")

    def do_delexpense(self, arg):
        """
        Delete an expense by ID.
        Usage: delexpense -id <id>
        """
        try:
            args = shlex.split(arg)
            expense_id = None

            if "-id" in args:
                expense_id = int(args[args.index("-id") + 1])

            if expense_id is not None:
                delete_expense(expense_id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: delexpense -id <id>")

        # Todo commands
    def do_lstodo(self, arg):
        """List all todos."""
        list_todos()

    def do_mktodo(self, arg):
        """
        Create a new todo.
        Usage: mktodo -description <description> -duedate <due_date> (optional)
        """
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
            print("Error: Invalid arguments. Usage: mktodo -description <description> -duedate <due_date>")

    def do_chtodo(self, arg):
        """
        Modify an existing todo.
        Usage: chtodo -id <id> [-description <description>] [-duedate <due_date>] [-status <status>]
        """
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

    def do_deltodo(self, arg):
        """
        Delete a todo by ID.
        Usage: deltodo -id <id>
        """
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
            print("Error: Invalid arguments. Usage: deltodo -id <id>")


    def do_exit(self, arg):
        """Exit the program."""
        print("Goodbye!")
        exit()
