import cmd
from services.expenses_service import mkexpense, lsexpense, chexpense, rmexpense, expenselog
from services.books_service import lsbooks, mkbook, chbook, addbookrating, chbookstatus, addbookprogress, rmbook
from services.bills_service import lsbills, mkbill, chbill, rmbill
from services.goals_service import lsgoals, mkgoal, chgoal, rmgoal, archivegoal, addgoalprogress
from services.habits_service import lshabits, mkhabit, chhabit, rmhabit, habitlog, markhabit
from services.studies_service import lsstudies, mkstudy, chstudy, rmstudy, logstudy, markstudycomplete
from services.todos_service import lstodos, mktodo, chtodo, rmtodo


class TodoAppCLI(cmd.Cmd):
    intro = "Welcome to the Swiss-Army-Knife App! Type 'help' or '?' to list commands."
    prompt = "(CLI) "

    categories = {
        "Bills": ["lsbills", "mkbill", "chbill", "delbill"],
        "Books": ["lsbooks", "mkbook", "chbook", "addbookrating", "addbookprogress", "chbookstatus", "rmbook"],
        "Expenses": ["lsexpenses", "mkexpense", "chexpense", "delexpense", "expenselog"],
        "Goals": ["lsgoals", 'mkgoal', 'chgoal', 'rmgoal', 'archivegoal', 'addgoalprogress'],
        "Habits": ["lshabits", "mkhabit", "chhabit", "rmhabit", "habitlog", "markhabit"],
        "Studies": ["lsstudies", "mkstudy", "chstudy", "rmstudy", "logstudy", "markstudycomplete"],
        "Todo": ["lstodos", "mktodo", "chtodo", "deltodo"],
    }

    #Expense commands
    def do_lsexpenses(self, arg):
        """List all expenses."""
        lsexpense(arg)

    def do_mkexpense(self, arg):
        """
        Create a new expense.
        Usage: mkexpense -description <description> -amount <amount> [-date <date>] (optional in format %dd/%mm/%YYYY) -category <category>
        """
        mkexpense(arg)

    def do_chexpense(self, arg):
        """
        Modify an existing expense.
        Usage: chexpense -id <id> [-description <description>] [-amount <amount>] [-date <date>] [-category <category>]
        """
        chexpense(arg)

    def do_rmexpense(self, arg):
        """
        Remove an expense by ID.
        Usage: rmexpense -id <id>
        """
        rmexpense(arg)

    def do_expenselog(self, arg):
        """
        Generate an expense log based on filters (start_date, end_date, or category) and optionally export to CSV.
        Usage: expenselog [-start_date <date>] [-end_date <date>] [-category <category>] [-download]
        """
        expenselog(arg)

    #Todo commands
    def do_lstodos(self, arg):
        """List all todos."""
        lstodos(arg)

    def do_mktodo(self, arg):
        """
        Create a new todo.
        Usage: mktodo -description <description> [-duedate <due_date>] (format dd/mm/yyyy)
        """
        mktodo(arg)

    def do_chtodo(self, arg):
        """
        Modify an existing todo.
        Usage: chtodo -id <id> [-description <description>] [-duedate <due_date>] (format dd/mm/yyyy) [-status <status>]
        """
        chtodo(arg)

    def do_rmtodo(self, arg):
        """
        Remove a todo by ID.
        Usage: deltodo -id <id>
        """
        rmtodo(arg)

    #Bills commands
    def do_lsbills(self, arg):
        """List all bills."""
        lsbills(arg)

    def do_mkbill(self, arg):
        """
        Create a new bill.
        Usage: mkbill -description <description> -price <price> [-date <date>] (format dd/mm/yyyy)
        """
        mkbill(arg)

    def do_chbill(self, arg):
        """
        Modify an existing bill.
        Usage: chbill -id <id> [-description <description>] [-price <price>] [-date <date>] (format dd/mm/yyyy)
        """
        chbill(arg)

    def do_rmbill(self, arg):
        """
        Remove a bill by ID.
        Usage: rmbill -id <id>
        """
        rmbill(arg)

    #Books commands
    def do_lsbooks(self, arg):
        """List all books."""
        lsbooks(arg)

    def do_mkbook(self, arg):
        """
        Create a new book.
        Usage: mkbook -title <title> -genre <genre> -pages <pages>
        """
        mkbook(arg)

    def do_chbook(self, arg):
        """
        Modify an existing book.
        Usage: chbook -id <id> [-title <title>] [-genre <genre>] [-pages <pages>]
        """
        chbook(arg)

    def do_addbookrating(self, arg):
        """
        Add rating to an existing book.
        Usage: addbookrating -id <id> -rating (1-5)
        """
        addbookrating(arg)

    def do_chbookstatus(self, arg):
        """
        Change the status of an existing book to the opposite one.
        Usage: chbookstatus -id <id>
        """
        chbookstatus(arg)

    def do_addbookprogress(self, arg):
        """
        Add progress to an existing book.
        Usage: addbookprogress -id <id> -pages <pages>
        """
        addbookprogress(arg)

    def do_rmbook(self, arg):
        """
        Remove a book by ID.
        Usage: rmbook -id <id>
        """
        rmbook(arg)

    # Habit commands
    def do_lshabits(self, arg):
        """
        List all habits, or filter by ID or date.
        Usage: lshabits [-id <id>] [-date <date>]
        """
        lshabits(arg)

    def do_mkhabit(self, arg):
        """
        Create a new habit.
        Usage: mkhabit -name <habit_name> -goal <goal> -unit <liters/km/pages>
        """
        mkhabit(arg)

    def do_chhabit(self, arg):
        """
        Update an existing habit.
        Usage: chhabit -id <id> [-name <name>] [-goal <goal>] [-unit <liters/km/pages>]
        """
        chhabit(arg)

    def do_rmhabit(self, arg):
        """
        Remove a habit by ID.
        Usage: rmhabit -id <id>
        """
        rmhabit(arg)

    def do_habitlog(self, arg):
        """
        Check the streak of a habit by providing its ID.
        Usage: habitlog -id <id> [-download]
        """
        habitlog(arg)

    def do_markhabit(self, arg):
        """
        Mark a habit as completed for today.
        Usage: markhabit -id <id>
        """
        markhabit(arg)

    # Goal commands
    def do_lsgoals(self, arg):
        """List all goals."""
        lsgoals()

    def do_mkgoal(self, arg):
        """
        Create a new goal.
        Usage: mkgoal -name <name> -unit <unit> -startingValue <starting_value> -endingValue <ending_value> -category
        """
        mkgoal(arg)

    def do_chgoal(self, arg):
        """
        Update an existing goal.
        Usage: chgoal -id <id> [-name <name>] [-unit <unit>] [-startingValue <startingValue>] [-endingValue <endingValue>] [-category <category>]
        """
        chgoal(arg)

    def do_rmgoal(self, arg):
        """
        Remove a goal by ID.
        Usage: rmgoal -id <id>
        """
        rmgoal(arg)

    def do_archivegoal(self, arg):
        """
        Archive a goal by ID.
        Usage: archivegoal -id <id>
        """
        archivegoal(arg)

    def do_addgoalprogress(self, arg):
        """
        Adds progress to an existing goal.
        Usage: addgoalprogress -id <id> -value <value>
        """
        addgoalprogress(arg)

    # Study commands
    def do_lsstudies(self, arg):
        """
        List all studies.
        Usage: lsstudies [-id <id>]
        """
        lsstudies(arg)

    def do_mkstudy(self, arg):
        """
        Create a new study.
        Usage: mkstudy -name <name> -category <category>
        """
        mkstudy(arg)

    def do_chstudy(self, arg):
        """
        Update an existing study.
        Usage: chstudy -id <id> [-name <name>] [-category <category>]
        """
        chstudy(arg)

    def do_rmstudy(self, arg):
        """
        Remove a study by ID.
        Usage: rmstudy -id <id>
        """
        rmstudy(arg)

    def do_logstudy(self, arg):
        """
        Log a learned topic.
        Usage: logstudy -id <id> -name <name> [-date <date: dd/mm/yyyy>]
        """
        logstudy(arg)

    def do_markstudycomplete(self, arg):
        """
        Mark a study as complete by ID.
        Usage: markstudycomplete -id <id>
        """
        markstudycomplete(arg)

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