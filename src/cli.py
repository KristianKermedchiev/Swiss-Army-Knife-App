import cmd
import shlex
from commands.expenses import make_expense, list_expenses, change_expense, delete_expense, expense_log
from commands.todos import make_todo, list_todos, change_todo, delete_todo
from commands.bills import make_bill, list_bills, change_bill, delete_bill
from commands.books import list_books, make_book, change_book, add_rating, add_progress, change_status, delete_book
from commands.habits import make_habit, list_habits, change_habit, delete_habit, habit_log, mark_habit
from commands.goals import list_goals, delete_goal, archive_goal, add_goal_progress, change_goal, make_goal


class TodoAppCLI(cmd.Cmd):
    intro = "Welcome to your CLI To-Do App! Type 'help' or '?' to list commands."
    prompt = "(CLI) "

    categories = {
        "Expenses": ["lsexpense", "mkexpense", "chexpense", "delexpense", "expenselog"],
        "Todo": ["lstodo", "mktodo", "chtodo", "deltodo"],
        "Bills": ["lsbill", "mkbill", "chbill", "delbill"],
        "Books": ["lsbooks", "mkbook", "chbook", "addbookrating", "addbookprogress", "chbookstatus", "rmbook"],
        "Habits": ["lshabits", "mkhabit", "chhabit", "rmhabit", "habitlog", "markhabit"],
        "Goals": ["lshoals", 'mkgoal', 'chgoal', 'rmgoal', 'archivegoal', 'addgoalprogress']
    }

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
    def do_rmexpense(self, arg):
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

    #Todo commands
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
    def do_rmtodo(self, arg):
        """
        Remove a todo by ID.
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
            print("Error: Invalid arguments. Usage: rmtodo -id <id>")

    #Bills commands
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
    def do_rmbill(self, arg):
        """
        Remove a bill by ID.
        Usage: rmbill -id <id>
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
            print("Error: Invalid arguments. Usage: rmbill -id <id>")

    #Books commands
    def do_lsbooks(self, arg):
        """List all books."""
        list_books()
    def do_mkbook(self, arg):
        """
        Create a new book.
        Usage: mkbook -title <title> -category <category> -pages <pages>
        """
        try:
            args = shlex.split(arg)
            title = None
            category = None
            pages = None

            if "-title" in args:
                title = args[args.index("-title") + 1]
            if "-category" in args:
                category = args[args.index("-category") + 1]
            if "-pages" in args:
                pages = args[args.index("-pages") + 1]

            if title and category and pages:
                make_book(title, category, pages)
            else:
                print("Error: -title, -category and -pages are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: mkbook -title <title> -category <category> -pages <pages>.")
    def do_chbook(self, arg):
        """
        Modify an existing book.
        Usage: chbook -id <id> [-title <title>] [-category <category>] [-pages <pages>]
        """
        try:
            args = shlex.split(arg)
            book_id = None
            title = None
            category = None
            pages = None

            if "-id" in args:
                book_id = int(args[args.index("-id") + 1])
            if "-title" in args:
                title = args[args.index("-title") + 1]
            if "-category" in args:
                category = args[args.index("-category") + 1]
            if "-pages" in args:
                pages = args[args.index("-pages") + 1]

            if book_id is not None:
                change_book(book_id, title, category, pages)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print(
                "Error: Invalid arguments. Usage: chbook -id <id> [-title <title>] [-category <category>] [-pages <pages>]")
    def do_addbookrating(self, arg):
        """
        Add rating to an existing book.
        Usage: addbookrating -id <id> -rating (1-5)
        """
        try:
            args = shlex.split(arg)
            book_id = None
            rating = None

            if "-id" in args:
                book_id = int(args[args.index("-id") + 1])
            if "-rating" in args:
                rating = args[args.index("-rating") + 1]

            if book_id is not None:
                add_rating(book_id, rating)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: addbookrating -id <id> -rating (1-5)")
    def do_chbookstatus(self, arg):
        """
        Change the status of an existing book to the opposite one.
        Usage: chbookstatus -id <id>
        """
        try:
            args = shlex.split(arg)
            book_id = None

            if "-id" in args:
                book_id = int(args[args.index("-id") + 1])

            if book_id is not None:
                change_status(book_id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: chbookstatus -id <id>")
    def do_addbookprogress(self, arg):
        """
        Add progress to an existing book.
        Usage: addbookprogress -id <id> -pages <pages>
        """
        try:
            args = shlex.split(arg)
            book_id = None
            pages = None

            if "-id" in args:
                book_id = int(args[args.index("-id") + 1])
            if "-pages" in args:
                pages = args[args.index("-pages") + 1]

            if book_id is not None and pages is not None:
                add_progress(book_id, pages)
            else:
                print("Error: -id and -pages are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: addbookprogress -id <id> -pages <pages>")
    def do_rmbook(self, arg):
        """
        Remove a book by ID.
        Usage: rmbook -id <id>
        """
        try:
            args = shlex.split(arg)
            book_id = None

            if "-id" in args:
                book_id = int(args[args.index("-id") + 1])

            if book_id is not None:
                delete_book(book_id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: rmbook -id <id>")

    # Habit commands
    def do_lshabits(self, arg):
        """
        List all habits, or filter by ID or date.
        Usage: lshabits [-id <id>] [-date <date>]
        """
        try:
            args = shlex.split(arg)
            habit_id = None
            date = None

            if "-id" in args:
                habit_id = int(args[args.index("-id") + 1])
            if "-date" in args:
                date = args[args.index("-date") + 1]

            list_habits(date=date, id=habit_id)

        except (ValueError, IndexError):
            print("Error: Invalid arguments. Usage: lshabits [-id <id>] [-date <dd/mm/yyyy>]")
    def do_mkhabit(self, arg):
        """
        Create a new habit.
        Usage: mkhabit -name <habit_name> -goal <goal> -unit <liters/km/pages>
        """
        try:
            args = shlex.split(arg)
            name = None
            goal = None
            unit = None

            if "-name" in args:
                name = args[args.index("-name") + 1]
            if "-goal" in args:
                goal = args[args.index("-goal") + 1]
            if "-unit" in args:
                unit = args[args.index("-unit") + 1]

            if name and goal and unit:
                make_habit(name, goal, unit)
            else:
                print("Error: -name, -goal, and -unit are required.")
        except (ValueError, IndexError):
            print("Error: Invalid arguments. mkhabit -name <habit_name> -goal <goal> -unit <liters/km/pages>")
    def do_chhabit(self, arg):
        """
        Update an existing habit.
        Usage: chhabit -id <id> [-name <name>] [-goal <goal>] [-unit <liters/km/pages>]
        """
        try:
            args = shlex.split(arg)
            habit_id = None
            name = None
            goal = None
            unit = None

            if "-id" in args:
                habit_id = int(args[args.index("-id") + 1])
            if "-name" in args:
                name = args[args.index("-name") + 1]
            if "-goal" in args:
                goal = args[args.index("-goal") + 1]
            if "-unit" in args:
                unit = args[args.index("-unit") + 1]

            if habit_id is not None:
                change_habit(habit_id, name, goal, unit)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError):
            print("Error: Invalid arguments. chhabit -id <id> [-name <name>] [-goal <goal>] [-unit <liters/km/pages>]")
    def do_rmhabit(self, arg):
        """
        Remove a habit by ID.
        Usage: rmhabit -id <id>
        """
        try:
            args = shlex.split(arg)
            id = None

            if "-id" in args:
                id = int(args[args.index("-id") + 1])

            if id is not None:
                delete_habit(id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError):
            print("Error: Invalid arguments. Usage: rmhabit -id <id>")
    def do_habitlog(self, arg):
        """
        Check the streak of a habit by providing its ID.
        Usage: habitlog -id <id> [-download]
        """
        try:
            args = shlex.split(arg)
            id = None
            download = False

            if "-id" in args:
                id = int(args[args.index("-id") + 1])
            if "-download" in args:
                download = True

            if id is None:
                print("Error: You must specify a habit ID using -id.")
                return

            habit_log(id=id, download=download)

        except (ValueError, IndexError):
            print(
                "Error: Invalid arguments. Usage: habitlog -id <id> [-download]")
    def do_markhabit(self, arg):
        """
        Mark a habit as completed for today.
        Usage: markhabit -id <id>
        """
        try:
            args = shlex.split(arg)
            id = None

            if "-id" in args:
                id = int(args[args.index("-id") + 1])

            if id is not None:
                mark_habit(id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError):
            print("Usage: markhabit -id <id>")

    # Goal commands
    def do_lsgoals(self, arg):
        """List all goals."""
        list_goals()
    def do_mkgoal(self, arg):
        """
        Create a new goal.
        Usage: mkgoal -name <name> -unit <unit> -startingValue <starting_value> -endingValue <ending_value> -category
        """
        try:
            args = shlex.split(arg)
            name = None
            unit = None
            starting_value = None
            ending_value = None
            category = None

            if "-name" in args:
                name = args[args.index("-name") + 1]
            if "-unit" in args:
                unit = args[args.index("-unit") + 1]
            if "-startingValue" in args:
                starting_value = args[args.index("-startingValue") + 1]
            if "-endingValue" in args:
                ending_value = args[args.index("-endingValue") + 1]
            if "-category" in args:
                category = args[args.index("-category") + 1]

            if name and unit and starting_value and ending_value and category:
                make_goal(name, unit, starting_value, ending_value, category)
            else:
                print("Error: -name, -unit, -startingValue, -endingValue and -category are required.")
        except (ValueError, IndexError):
            print("Error: Invalid arguments. Usage: mkgoal -name <name> -unit <unit> -startingValue <starting_value> -endingValue <ending_value> -category")
    def do_chgoal(self, arg):
        """
        Update an existing goal.
        Usage: chgoal -id <id> [-name <name>] [-unit <unit>] [-startingValue <startingValue>] [-endingValue <endingValue>] [-category <category>]
        """
        try:
            args = shlex.split(arg)
            goal_id = None
            name = None
            unit = None
            starting_value = None
            ending_value = None
            category = None

            if "-id" in args:
                goal_id = int(args[args.index("-id") + 1])
            if "-name" in args:
                name = args[args.index("-name") + 1]
            if "-unit" in args:
                unit = args[args.index("-unit") + 1]
            if "-startingValue" in args:
                starting_value = args[args.index("-startingValue") + 1]
            if "-endingValue" in args:
                ending_value = args[args.index("-endingValue") + 1]
            if "-category" in args:
                category = args[args.index("-category") + 1]

            if goal_id is not None:
                change_goal(goal_id, name, unit, starting_value, ending_value, category)
            else:
                print("Error: -id is required.")
        except(ValueError, IndexError):
            print("Error: Invalid arguments. Usage: chgoal -id <id> [-name <name>] [-unit <unit>] "
                    "[-startingValue <startingValue>] [-endingValue <endingValue>] [-category <category>]")
    def do_rmgoal(self, arg):
        """
        Remove a goal by ID.
        Usage: rmgoal -id <id>
        """
        try:
            args = shlex.split(arg)
            id = None

            if "-id" in args:
                id = int(args[args.index("-id") + 1])

            if id is not None:
                delete_goal(id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError):
            print("Error: Invalid arguments. Usage: rmgoal -id <id>")
    def do_archivegoal(self, arg):
        """
        Archive a goal by ID.
        Usage: archivegoal -id <id>
        """
        try:
            args = shlex.split(arg)
            id = None

            if "-id" in args:
                id = int(args[args.index("-id") + 1])

            if id is not None:
                archive_goal(id)
            else:
                print("Error: -id is required.")
        except (ValueError, IndexError):
            print("Error: Invalid arguments. Usage: archivegoal -id <id>")
    def do_addgoalprogress(self, arg):
        """
        Adds progress to an existing goal.
        Usage: addgoalprogress -id <id> -value <value>
        """
        try:
            args = shlex.split(arg)
            goal_id = None
            value = None

            if "-id" in args:
                goal_id = int(args[args.index("-id") + 1])
            if "-value" in args:
                value = args[args.index("-value") + 1]

            if goal_id is not None and value is not None:
                add_goal_progress(goal_id, value)
            else:
                print("Error: -id and -value are required.")
        except (ValueError, IndexError) as e:
            print("Error: Invalid arguments. Usage: addgoalprogress -id <id> -value <value>")

    def do_help(self, arg):
        """Show categorized help menu."""
        if arg:
            return super().do_help(arg)

        print("\nAvailable Commands:\n===============================")
        for category, commands in self.categories.items():
            print(f"{category}:")
            print("  " + "  ".join(commands))
        print("\nType 'help <command>' for detailed usage information.\n")
    def do_exit(self, arg):
        """Exit the program."""
        print("Goodbye!")
        exit()


#cmd Loop
TodoAppCLI().cmdloop()
