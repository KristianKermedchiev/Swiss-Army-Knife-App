import shlex
from src.commands.habits import make_habit, list_habits, change_habit, delete_habit, habit_log, mark_habit

def lshabits(arg):
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

def mkhabit(arg):
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

def chhabit(arg):
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

def rmhabit(arg):
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

def habitlog(arg):
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

def markhabit(arg):
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