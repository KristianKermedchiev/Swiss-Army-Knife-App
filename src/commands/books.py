import json
import os

BOOKS_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'books.json')


def load_books():
    """Load books data from the JSON file."""
    if os.path.exists(BOOKS_DATA_FILE):
        with open(BOOKS_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_books(books):
    """Save books data to the JSON file."""
    with open(BOOKS_DATA_FILE, 'w') as file:
        json.dump(books, file, indent=4)


def list_books():
    """List all books."""
    books = load_books()
    if not books:
        print("\nNo books found.")
        return

    print("\nList of books:")
    for book in books:
        print(f"{book['id']} / {book['title']} / {book['category']} / {book['progress']} / {book['status']} / {book['rating']} ")


def make_book(title, category, pages):
    """Create a new book."""
    if title is None:
        print("Error: Title is required.")
        return

    if category is None:
        print("Error: Category is required.")
        return

    if pages is None:
        print("Error: Pages are required.")
        return

    books = load_books()

    new_id = 1 if not books else books[-1]['id'] + 1

    books.append({
        'id': new_id,
        'title': title,
        'category': category,
        'pages': pages,
        'pages_read': 0,
        'progress': 0,
        'status': "In Progress",
        'rating': 0
    })

    save_books(books)
    print(f"Book '{title}' added successfully with ID {new_id}.")


def add_progress(book_id, pages):
    """Add progress to a book."""
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            book["pages_read"] += int(pages)
            book["progress"] = round((int(book["pages_read"]) / int(book["pages"])) * 100, 2)
            save_books(books)
            print(f'Progress updated successfully for book {book["title"]}, current progress is {book["progress"]}.')
            return

    print(f"Error: Book with ID {book_id} not found.")


def change_status(book_id):
    """Changes the current status of the book to the opposite."""
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            if book["status"] == "In Progress":
                book["status"] = "Completed"
            else:
                book["status"] = "In Progress"
            save_books(books)
            print(f"Book {book['title']}'s status changed to {book['status']}.")
            return

    print(f"Error: Book with ID {book_id} not found.")


def add_rating(book_id, rating):
    """Adds a rating to the book from 1 to 5."""
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            book["rating"] = rating
            save_books(books)
            print(f"Rating updated successfully for book {book['title']}.")
            return

    print(f"Error: Book with ID {book_id} not found.")


def change_book(book_id, title, category, pages):
    """Update an existing book."""
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            if title is not None:
                book["title"] = title
            if category is not None:
                book["category"] = category
            if pages is not None:
                book["pages"] = pages

            save_books(books)
            print(f"Book with ID {book_id} updated successfully.")
            return

    print(f"Error: Book with ID {book_id} not found.")


def delete_book(book_id):
    """Delete a book by ID."""
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books(books)
            print(f"Book with ID {book_id} deleted successfully.")
            return

    print(f"Error: Book with ID {book_id} not found.")