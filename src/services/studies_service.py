import shlex
from src.commands.studies import list_studies, delete_study, make_study, change_study, log_study, mark_study_completed

def lsstudies(arg):
    try:
        args = shlex.split(arg)
        study_id = None

        if "-id" in args:
            study_id = int(args[args.index("-id") + 1])

        list_studies(study_id=study_id)

    except(ValueError, IndexError):
        print("Error: Invalid arguments. Usage: lsstudies [-id <id>]")

def mkstudy(arg):
    try:
        args = shlex.split(arg)
        name = None
        category = None

        if "-name" in args:
            name = args[args.index("-name") + 1]
        if "-category" in args:
            category = args[args.index("-category") + 1]

        if name and category:
            make_study(name, category)
        else:
            print("Error: -name and -category are required.")
    except (ValueError, IndexError):
        print("Error: Invalid arguments. Usage: mkstudy -name <name> -category <category>")

def chstudy(arg):
    try:
        args = shlex.split(arg)
        id = None
        name = None
        category = None
        if "-id" in args:
            id = int(args[args.index("-id") + 1])
        if "-name" in args:
            name = args[args.index("-name") + 1]
        if "-category" in args:
            category = args[args.index("-category") + 1]

        if id is not None:
            change_study(id, name, category)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError):
        print("Error: Invalid arguments. Usage: chstudy -id <id> [-name <name>] [-category <category>]")

def rmstudy(arg):
    try:
        args = shlex.split(arg)
        id = None
        if "-id" in args:
            id = int(args[args.index("-id") + 1])

        if id is not None:
            delete_study(id)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError):
        print("Error: Invalid arguments. Usage: rmstudy -id <id>")

def logstudy(arg):
    try:
        args = shlex.split(arg)
        id = None
        name = None
        date = None
        if "-id" in args:
            id = int(args[args.index("-id") + 1])
        if "-name" in args:
            name = args[args.index("-name") + 1]
        if "-date" in args:
            date = args[args.index("-date") + 1]

        if id and name:
            log_study(id, name, date)
        else:
            print("Error: -id and name are required.")
    except (ValueError, IndexError):
        print("Error: Invalid arguments. Usage: logstudy -id <id> -name <name> [-date <date: dd/mm/YYYY>]")

def markstudycomplete(arg):
    try:
        args = shlex.split(arg)
        id = None
        if "-id" in args:
            id = int(args[args.index("-id") + 1])

        if id is not None:
            mark_study_completed(id)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError):
        print("Error: Invalid arguments. Usage: markstudycomplete -id <id>")