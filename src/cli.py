import cmd

from src.services.expenses_service import mkexpense, lsexpense, chexpense, rmexpense, expenselog
from src.services.books_service import lsbooks, mkbook, chbook, addbookrating, chbookstatus, addbookprogress, rmbook
from src.services.bills_service import lsbills, mkbill, chbill, rmbill
from src.services.goals_service import lsgoals, mkgoal, chgoal, rmgoal, archivegoal, addgoalprogress
from src.services.habits_service import lshabits, mkhabit, chhabit, rmhabit, habitlog, markhabit
from src.services.studies_service import lsstudies, mkstudy, chstudy, rmstudy, logstudy, markstudycomplete
from src.services.todos_service import lstodos, mktodo, chtodo, rmtodo


class TodoAppCLI(cmd.Cmd):
    intro = "Welcome to the Swiss-Army-Knife App! Type 'help' or '?' to list commands."
    prompt = "(CLI) "

    categories = {
        "Expenses": ["lsexpenses", "mkexpense", "chexpense", "delexpense", "expenselog"],
        "Todo": ["lstodos", "mktodo", "chtodo", "deltodo"],
        "Bills": ["lsbills", "mkbill", "chbill", "delbill"],
        "Books": ["lsbooks", "mkbook", "chbook", "addbookrating", "addbookprogress", "chbookstatus", "rmbook"],
        "Habits": ["lshabits", "mkhabit", "chhabit", "rmhabit", "habitlog", "markhabit"],
        "Goals": ["lsgoals", 'mkgoal', 'chgoal', 'rmgoal', 'archivegoal', 'addgoalprogress'],
        "Studies": ["lsstudies", "mkstudy", "chstudy", "rmstudy", "logstudy", "markstudycomplete"]
    }

    #Expense commands
    def do_lsexpenses(self, arg):
        lsexpense(arg)

    def do_mkexpense(self, arg):
        mkexpense(arg)

    def do_chexpense(self, arg):
       chexpense(arg)

    def do_rmexpense(self, arg):
        rmexpense(arg)

    def do_expenselog(self, arg):
        expenselog(arg)

    #Todo commands
    def do_lstodos(self, arg):
        lstodos(arg)

    def do_mktodo(self, arg):
        mktodo(arg)

    def do_chtodo(self, arg):
        chtodo(arg)

    def do_rmtodo(self, arg):
        rmtodo(arg)

    #Bills commands
    def do_lsbills(self, arg):
        lsbills(arg)

    def do_mkbill(self, arg):
        mkbill(arg)

    def do_chbill(self, arg):
        chbill(arg)

    def do_rmbill(self, arg):
        rmbill(arg)

    #Books commands
    def do_lsbooks(self, arg):
        lsbooks(arg)

    def do_mkbook(self, arg):
        mkbook(arg)

    def do_chbook(self, arg):
        chbook(arg)

    def do_addbookrating(self, arg):
        addbookrating(arg)

    def do_chbookstatus(self, arg):
        chbookstatus(arg)

    def do_addbookprogress(self, arg):
        addbookprogress(arg)

    def do_rmbook(self, arg):
        rmbook(arg)

    # Habit commands
    def do_lshabits(self, arg):
        lshabits(arg)

    def do_mkhabit(self, arg):
        mkhabit(arg)

    def do_chhabit(self, arg):
        chhabit(arg)

    def do_rmhabit(self, arg):
        rmhabit(arg)

    def do_habitlog(self, arg):
        habitlog(arg)

    def do_markhabit(self, arg):
        markhabit(arg)

    # Goal commands
    def do_lsgoals(self, arg):
        lsgoals(arg)

    def do_mkgoal(self, arg):
        mkgoal(arg)

    def do_chgoal(self, arg):
        chgoal(arg)

    def do_rmgoal(self, arg):
        rmgoal(arg)

    def do_archivegoal(self, arg):
        archivegoal(arg)

    def do_addgoalprogress(self, arg):
        addgoalprogress(arg)

    # Study commands
    def do_lsstudies(self, arg):
        lsstudies(arg)

    def do_mkstudy(self, arg):
        mkstudy(arg)

    def do_chstudy(self, arg):
        chstudy(arg)

    def do_rmstudy(self, arg):
        rmstudy(arg)

    def do_logstudy(self, arg):
        logstudy(arg)

    def do_markstudycomplete(self, arg):
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