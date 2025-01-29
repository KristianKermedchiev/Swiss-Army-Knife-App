import cmd
import shlex
from commands.expenses import make_expense, list_expenses, change_expense, delete_expense, expense_log
from commands.todos import make_todo, list_todos, change_todo, delete_todo
from commands.bills import make_bill, list_bills, change_bill, delete_bill


class TodoAppCLI(cmd.Cmd):
    intro = "Welcome to your CLI To-Do App! Type 'help' or '?' to list commands."
    prompt = "(CLI) "

    #Expense commands

    def do_lsexpense(self, arg):
        """List all expenses."""
        list_expenses()

    def do_mkexpense(self, arg):
        """
        Create a new expense.
        Usage: mkexpense -description <description> -amount <amount> -date <date> (optional in format %dd/%mm/%YYYY) -category <category>
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
                print("Error: Both -description and -amount are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: mkexpense -description <description> -amount <amount>"
                  " -date <date> -category <category>")

    def do_chexpense(self, arg):
        """
        Modify an existing expense.
        Usage: chexpense -id <id> [-description <description>] [-amount <amount>] [-date <date>] (optional) [-category <category>]
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

    def do_expenselog(self, arg):
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

    def do_lsbill(self, arg):
        """List all bills."""
        list_bills()

    def do_mkbill(self, arg):
        """
        Create a new bill.
        Usage: mkbill -description <description> -price <price>
        """
        try:
            args = shlex.split(arg)
            description = None
            price = None

            if "-description" in args:
                description = args[args.index("-description") + 1]
            if "-price" in args:
                price = args[args.index("-price") + 1]

            if description and price:
                make_bill(description, price)
            else:
                print("Error: -description and -price are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: mktodo -description <description> -price <price>")

    def do_chbill(self, arg):
        """
        Modify an existing bill.
        Usage: chbill -id <id> [-description <description>] [-price <price>]
        """
        try:
            args = shlex.split(arg)
            bill_id = None
            description = None
            price = None

            if "-id" in args:
                bill_id = int(args[args.index("-id") + 1])
            if "-description" in args:
                description = args[args.index("-description") + 1]
            if "-price" in args:
                price = args[args.index("-price") + 1]

            if bill_id is not None:
                change_bill(bill_id, description, price)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print(
                "Error: Invalid arguments. Usage: chbill -id <id> [-description <description>] [-price <price>]")

    def do_delbill(self, arg):
        """
        Delete a bill by ID.
        Usage: delbill -id <id>
        """
        try:
            args = shlex.split(arg)
            bill_id = None

            if "-id" in args:
                bill_id = int(args[args.index("-id") + 1])

            if bill_id is not None:
                delete_bill(bill_id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: delbill -id <id>")

    def do_exit(self, arg):
        """Exit the program."""
        print("Goodbye!")
        exit()


#cmd Loop
TodoAppCLI().cmdloop()
