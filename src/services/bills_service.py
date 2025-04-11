import shlex
from commands.bills import make_bill, list_bills, change_bill, delete_bill

def lsbills(arg):
    list_bills()

def mkbill(arg):
    try:
        args = shlex.split(arg)
        description = None
        price = None
        date = None

        if "-description" in args:
            description = args[args.index("-description") + 1]
        if "-price" in args:
            price = args[args.index("-price") + 1]
        if "-date" in args:
            date = args[args.index("-date") + 1]

        if description and price and date:
            make_bill(description, price, date)
        else:
            print("Error: -description, -price are required.")
    except (ValueError, IndexError) as e:
        print("Error: Invalid arguments. Usage: mkbill -description <description> -price <price> [-date <date>]")

def chbill(arg):
    try:
        args = shlex.split(arg)
        bill_id = None
        description = None
        price = None
        date = None

        if "-id" in args:
            bill_id = int(args[args.index("-id") + 1])
        if "-description" in args:
            description = args[args.index("-description") + 1]
        if "-price" in args:
            price = args[args.index("-price") + 1]
        if "-date" in args:
            date = args[args.index("-date") + 1]

        if bill_id is not None:
            change_bill(bill_id, description, price, date)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError) as e:
        print(
            "Error: Invalid arguments. Usage: chbill -id <id> [-description <description>] [-price <price>] [-date <date>]")

def rmbill(arg):
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