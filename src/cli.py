import cmd
import shlex
from commands.expenses import make_expense, list_expenses, change_expense, delete_expense


class TodoAppCLI(cmd.Cmd):
    intro = "Welcome to your CLI To-Do App! Type 'help' or '?' to list commands."
    prompt = "(CLI) "

    def do_lsexpense(self, arg):
        """List all expenses."""
        list_expenses()

    def do_mkexpense(self, arg):
        """
        Create a new expense.
        Usage: mkexpense -description <description> -amount <amount>
        """
        try:
            args = shlex.split(arg)
            description = None
            amount = None

            if "-description" in args:
                description = args[args.index("-description") + 1]
            if "-amount" in args:
                amount = args[args.index("-amount") + 1]

            if description and amount:
                make_expense(description, amount)
            else:
                print("Error: Both -description and -amount are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: mkexpense -description <description> -amount <amount>")

    def do_chexpense(self, arg):
        """
        Modify an existing expense.
        Usage: chexpense -id <id> [-description <description>] [-amount <amount>]
        """
        try:
            # Parse arguments
            args = shlex.split(arg)
            expense_id = None
            description = None
            amount = None

            if "-id" in args:
                expense_id = int(args[args.index("-id") + 1])
            if "-description" in args:
                description = args[args.index("-description") + 1]
            if "-amount" in args:
                amount = float(args[args.index("-amount") + 1])

            if expense_id is not None:
                change_expense(expense_id=expense_id, description=description, amount=amount)
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


    def do_exit(self, arg):
        """Exit the program."""
        print("Goodbye!")
        exit()
