from src.utils.file_utils import get_data_file_path
from src.db.db_interface import load_data, save_data

BOOKS_DATA_FILE = get_data_file_path('books.json')

def list_books():
    """List all books."""
    books = load_data(BOOKS_DATA_FILE)
    if not books:
        print("\nNo books found.")
        return

    for book in books:
        print(f"id: {book['id']} / title: {book['title']} / genre: {book['genre']} / progress: {book['progress']}%"
              f" / status: {book['status']} / rating: {book['rating']} ")


def make_book(title, genre, pages):
    """Create a new book."""
    if title is None:
        print("Error: Title is required.")
        return

    if genre is None:
        print("Error: genre is required.")
        return

    if pages is None:
        print("Error: Pages are required.")
        return

    books = load_data(BOOKS_DATA_FILE)

    new_id = 1 if not books else books[-1]['id'] + 1

    books.append({
        'id': new_id,
        'title': title,
        'genre': genre,
        'pages': pages,
        'pages_read': 0,
        'progress': 0,
        'status': "In Progress",
        'rating': 0
    })

    save_data(BOOKS_DATA_FILE, books)
    print(f"Book '{title}' added successfully with ID {new_id}.")


def add_progress(book_id, pages):
    """Add progress to a book."""
    books = load_data(BOOKS_DATA_FILE)

    for book in books:
        if book["id"] == book_id:
            book["pages_read"] += int(pages)
            book["progress"] = round((int(book["pages_read"]) / int(book["pages"])) * 100, 2)
            save_data(BOOKS_DATA_FILE, books)
            print(f'Progress updated successfully for book {book["title"]}, current progress is {book["progress"]}%.')
            return

    print(f"Error: Book with ID {book_id} not found.")


def change_status(book_id):
    """Changes the current status of the book to the opposite."""
    books = load_data(BOOKS_DATA_FILE)

    for book in books:
        if book["id"] == book_id:
            if book["status"] == "In Progress":
                book["status"] = "Completed"
            else:
                book["status"] = "In Progress"
            save_data(BOOKS_DATA_FILE, books)
            print(f"Book {book['title']}'s status changed to {book['status']}.")
            return

    print(f"Error: Book with ID {book_id} not found.")


def add_rating(book_id, rating):
    """Adds a rating to the book from 1 to 5."""
    books = load_data(BOOKS_DATA_FILE)

    if int(rating) < 1 or int(rating) > 5:
        print("Error: Invalid rating. Usage: addbookrating -id <id> -rating (1-5)")

    for book in books:
        if book["id"] == book_id:
            book["rating"] = rating
            save_data(BOOKS_DATA_FILE, books)
            print(f"Rating updated successfully for book {book['title']}.")
            return

    print(f"Error: Book with ID {book_id} not found.")


def change_book(book_id, title, genre, pages):
    """Update an existing book."""
    books = load_data(BOOKS_DATA_FILE)

    for book in books:
        if book["id"] == book_id:
            if title is not None:
                book["title"] = title
            if genre is not None:
                book["genre"] = genre
            if pages is not None:
                book["pages"] = pages

            save_data(BOOKS_DATA_FILE, books)
            print(f"Book with ID {book_id} updated successfully.")
            return

    print(f"Error: Book with ID {book_id} not found.")


def delete_book(book_id):
    """Delete a book by ID."""
    books = load_data(BOOKS_DATA_FILE)

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_data(BOOKS_DATA_FILE, books)
            print(f"Book with ID {book_id} deleted successfully.")
            return

    print(f"Error: Book with ID {book_id} not found.")