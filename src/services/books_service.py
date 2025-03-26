import shlex
from src.commands.books import list_books, make_book, change_book, add_rating, add_progress, change_status, delete_book

def lsbooks(arg):
    list_books()

def mkbook(arg):
    try:
        args = shlex.split(arg)
        title = None
        genre = None
        pages = None

        if "-title" in args:
            title = args[args.index("-title") + 1]
        if "-genre" in args:
            genre = args[args.index("-genre") + 1]
        if "-pages" in args:
            pages = args[args.index("-pages") + 1]

        if title and genre and pages:
            make_book(title, genre, pages)
        else:
            print("Error: -title, -genre and -pages are required.")
    except (ValueError, IndexError) as e:
        print("Error: Invalid arguments. Usage: mkbook -title <title> -genre <genre> -pages <pages>.")

def chbook(arg):
    try:
        args = shlex.split(arg)
        book_id = None
        title = None
        genre = None
        pages = None

        if "-id" in args:
            book_id = int(args[args.index("-id") + 1])
        if "-title" in args:
            title = args[args.index("-title") + 1]
        if "-genre" in args:
            genre = args[args.index("-genre") + 1]
        if "-pages" in args:
            pages = args[args.index("-pages") + 1]

        if book_id is not None:
            change_book(book_id, title, genre, pages)
        else:
            print("Error: -id is required.")
    except (ValueError, IndexError) as e:
        print(
            "Error: Invalid arguments. Usage: chbook -id <id> [-title <title>] [-genre <genre>] [-pages <pages>]")

def addbookrating(arg):
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

def chbookstatus(arg):
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

def addbookprogress(arg):
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

def rmbook(arg):
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