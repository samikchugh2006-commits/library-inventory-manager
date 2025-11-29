import json
from pathlib import Path
from typing import List, Optional
import logging

from .book import Book  # NOTE: if Python gives import issue, use relative import: from .book import Book

# Actually correct import:
# from .book import Book

# Configure module logger
logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.books: List[Book] = []
        self.load()

    def add_book(self, book: Book):
        if self.search_by_isbn(book.isbn) is not None:
            logger.info("Book with same ISBN already exists. Skipping add.")
            raise ValueError("Book with this ISBN already exists.")
        self.books.append(book)
        logger.info("Added book: %s", book.title)
        self.save()

    def search_by_title(self, title: str) -> List[Book]:
        title_lower = title.strip().lower()
        results = [b for b in self.books if title_lower in b.title.lower()]
        logger.info("Searched by title '%s' -> %d found", title, len(results))
        return results

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn = isbn.strip()
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[Book]:
        logger.info("Displaying all books: %d total", len(self.books))
        return list(self.books)

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if book is None:
            logger.info("Attempt to issue non-existent ISBN: %s", isbn)
            raise LookupError("Book not found")
        if book.issue():
            logger.info("Issued book: %s", book.title)
            self.save()
            return True
        else:
            logger.info("Book already issued: %s", book.title)
            return False

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if book is None:
            logger.info("Attempt to return non-existent ISBN: %s", isbn)
            raise LookupError("Book not found")
        if book.return_book():
            logger.info("Returned book: %s", book.title)
            self.save()
            return True
        else:
            logger.info("Book was not issued: %s", book.title)
            return False

    def save(self):
        data = [b.to_dict() for b in self.books]
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Saved %d books to %s", len(self.books), self.db_path)
        except Exception as e:
            logger.error("Failed to save data: %s", e)
            raise

    def load(self):
        if not self.db_path.exists():
            logger.info("DB file does not exist; starting with empty catalog.")
            self.books = []
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Very defensive: validate data
            self.books = []
            for item in data:
                try:
                    book = Book(
                        title=item["title"],
                        author=item["author"],
                        isbn=item["isbn"],
                        status=item.get("status", "available")
                    )
                    self.books.append(book)
                except KeyError:
                    logger.error("Malformed book entry in JSON, skipping: %s", item)
            logger.info("Loaded %d books from %s", len(self.books), self.db_path)
        except json.JSONDecodeError:
            logger.error("JSON decode error - file may be corrupted. Backing up and starting empty.")
            # back up the corrupted file
            corrupted = self.db_path.with_suffix(".corrupt.json")
            self.db_path.rename(corrupted)
            logger.info("Corrupted file renamed to %s", corrupted)
            self.books = []
        except Exception as e:
            logger.error("Unexpected error when loading DB: %s", e)
            self.books = []
