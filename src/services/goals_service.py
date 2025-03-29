import shlex
from src.commands.goals import list_goals, delete_goal, archive_goal, add_goal_progress, change_goal, make_goal

def lsgoals():
    list_goals()

def mkgoal(arg):
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
        print(
            "Error: Invalid arguments. Usage: mkgoal -name <name> -unit <unit> -startingValue <starting_value> -endingValue <ending_value> -category")

def chgoal(arg):
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

def rmgoal(arg):
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

def archivegoal(arg):
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

def addgoalprogress(arg):
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