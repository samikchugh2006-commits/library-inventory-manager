import sys
from pathlib import Path

# ensure project root is on sys.path so package imports work
project_root = Path(__file__).resolve().parents[1]   # two levels up from cli/main.py
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import logging

# Configure logging for entire application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("library_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("library-cli")

# now import from your package
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

DB_PATH = Path("books.json")



def safe_input(prompt: str) -> str:
    return input(prompt).strip()


def add_book_flow(inv: LibraryInventory):
    print("\n--- Add Book ---")
    title = safe_input("Title: ")
    author = safe_input("Author: ")
    isbn = safe_input("ISBN: ")

    if not (title and author and isbn):
        print("All fields are required.")
        return

    try:
        b = Book(title=title, author=author, isbn=isbn)
        inv.add_book(b)
        print("Book added successfully!")
    except ValueError as e:
        print("Error:", e)


def issue_book_flow(inv: LibraryInventory):
    print("\n--- Issue Book ---")
    isbn = safe_input("Enter ISBN to issue: ")

    try:
        success = inv.issue_book(isbn)
        if success:
            print("Book issued successfully!")
        else:
            print("This book is already issued.")
    except LookupError:
        print("Book not found.")


def return_book_flow(inv: LibraryInventory):
    print("\n--- Return Book ---")
    isbn = safe_input("Enter ISBN to return: ")

    try:
        success = inv.return_book(isbn)
        if success:
            print("Book returned successfully!")
        else:
            print("This book was not issued.")
    except LookupError:
        print("Book not found.")


def view_all_flow(inv: LibraryInventory):
    print("\n--- All Books ---")
    books = inv.display_all()

    if not books:
        print("Catalog is empty.")
        return

    for b in books:
        print(b)


def search_flow(inv: LibraryInventory):
    print("\n--- Search Books ---")
    choice = safe_input("Search by (1) Title or (2) ISBN? [1/2]: ")

    if choice == "1":
        q = safe_input("Enter title/keyword: ")
        results = inv.search_by_title(q)
        if results:
            for b in results:
                print(b)
        else:
            print("No matching books found.")

    elif choice == "2":
        q = safe_input("Enter ISBN: ")
        b = inv.search_by_isbn(q)
        if b:
            print(b)
        else:
            print("No book found with that ISBN.")

    else:
        print("Invalid choice.")


def main_menu():
    inv = LibraryInventory(DB_PATH)

    while True:
        print("\n=== Library Inventory Manager ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Books")
        print("6. Exit")

        choice = safe_input("Choose an option [1-6]: ")

        if choice == "1":
            add_book_flow(inv)
        elif choice == "2":
            issue_book_flow(inv)
        elif choice == "3":
            return_book_flow(inv)
        elif choice == "4":
            view_all_flow(inv)
        elif choice == "5":
            search_flow(inv)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid input, choose between 1–6.")


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        logger.exception("Unhandled exception: %s", e)
        print("An unexpected error occurred. Please check logs.")

