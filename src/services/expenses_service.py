import shlex
from src.commands.expenses import make_expense, list_expenses, change_expense, delete_expense, expense_log

def lsexpense(arg):
    """List all expenses."""
    list_expenses()

def mkexpense(arg):
    """
    Create a new expense.
    Usage: mkexpense -description <description> -amount <amount> [-date <date>] (optional in format %dd/%mm/%YYYY) -category <category>
    """
    try:
        args = shlex.split(arg)
        description = None
        amount = None
        date = None
        category = None

        if "-description" in args:
            description = args[args.index("-description") + 1]
        if "-amount" in args:
            amount = args[args.index("-amount") + 1]
        if "-date" in args:
            date = args[args.index("-date") + 1]
        if "-category" in args:
            category = args[args.index("-category") + 1]

        if description and amount and category:
            make_expense(description, amount, date, category)
        else:
            print("Error: -description, -amount and -category are required.")
    except (ValueError, IndexError) as e:
        print("Error: Invalid arguments. Usage: mkexpense -description <description> -amount <amount>"
              " [-date <date>] -category <category>")

def chexpense(arg):
    """
           Modify an existing expense.
           Usage: chexpense -id <id> [-description <description>] [-amount <amount>] [-date <date>] [-category <category>]
           """
    try:
        args = shlex.split(arg)
        expense_id = None
        description = None
        amount = None
        date = None
        category = None

        if "-id" in args:
            expense_id = int(args[args.index("-id") + 1])
        if "-description" in args:
            description = args[args.index("-description") + 1]
        if "-amount" in args:
            amount = float(args[args.index("-amount") + 1])
        if "-date" in args:
            date = args[args.index("-date") + 1]
        if "-category" in args:
            category = args[args.index("-category") + 1]

        if expense_id is not None:
            change_expense(expense_id=expense_id, description=description, amount=amount, date=date, category=category)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError) as e:
        print("Error: Invalid arguments. Usage: chexpense -id <id> [-description <description>] "
              "[-amount <amount>] [-date <date>] [-category <category>]")

def rmexpense(arg):
    """
            Remove an expense by ID.
            Usage: rmexpense -id <id>
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
        print("Error: Invalid arguments. Usage: rmexpense -id <id>")

def expenselog(arg):
    """
          Generate an expense log based on filters (start_date, end_date, or category) and optionally export to CSV.
          Usage: expenselog [-start_date <date>] [-end_date <date>] [-category <category>] [-download]
          """
    try:
        args = shlex.split(arg)
        start_date = None
        end_date = None
        category = None
        download = False

        if "-start_date" in args:
            start_date_idx = args.index("-start_date") + 1
            if start_date_idx < len(args):
                start_date = args[start_date_idx]

        if "-end_date" in args:
            end_date_idx = args.index("-end_date") + 1
            if end_date_idx < len(args):
                end_date = args[end_date_idx]

        if "-category" in args:
            category_idx = args.index("-category") + 1
            if category_idx < len(args):
                category = args[category_idx]

        if "-download" in args:
            download = True

        if start_date or end_date or category:
            expense_log(start_date, end_date, category, download)
        else:
            print("Error: At least one filter (-start_date, -end_date, or -category) is required.")

    except (ValueError, IndexError):
        print(
            "Error: Invalid arguments. Usage: expenselog [-start_date <date>] [-end_date <date>] "
            "[-category <category>] [-download]")