# Book based functions
from datetime import datetime as dt
import os
from models.author import get_author_name_from_id

class Book:
    def __init__(self, db, book_id):
        book_details = Book.get_book_details(db, book_id)
        self.id = book_details['id']
        self.title = book_details['title']
        self.author = book_details['author']
        self.publisher = book_details['publisher']
        self.year = book_details['year']
        self.cover = book_details['cover']
        self.description = book_details['description']
        self.isbn = book_details['isbn']
        self.available = book_details['available']

    @staticmethod
    def get_book_list(db):
        book_id_results = db.execute("""SELECT id
                                    FROM book
                                    ORDER BY title;""").fetchall()

        books = [Book(db, book['id'])
                for book in book_id_results]

        return books

    @staticmethod
    def get_book_details(db, book_id):
        book_info = db.execute("""SELECT book.title as title, book.publisher as publisher,
                            book.year as year, author.first_name as first_name,
                            author.last_name as last_name, book.isbn as isbn,
                            book.description as description, cover
                            FROM book
                            INNER JOIN author ON book.author_id = author.id
                            WHERE book.id = ?""", (book_id,)).fetchone()
        title = book_info['title']
        author = f"{book_info['first_name']} {book_info['last_name']}"
        publisher = book_info['publisher']
        year = book_info['year']
        if book_info['cover']:
            cover = book_info['cover']
        else:
            cover = "/static/images/missing_book_cover.jpg"
        description = book_info['description']
        isbn = book_info['isbn']

        book_details = {'id': book_id, 'title': title, 'author': author,
                        'publisher': publisher, 'year': year,
                        'cover': cover, 'description': description,
                        'isbn': isbn}
        
        copy_availability_details = Book.check_copies_available(db, book_id)
        if copy_availability_details['num_available'] > 0:
            book_details['available'] = 'Available'
        else:
            book_details['available'] = 'Unavailable'

        return book_details

    @staticmethod
    def check_copies_available(db, book_id):
        num_copies = db.execute("""SELECT COUNT (copy.id)
                                FROM copy
                                WHERE book_id = ?;
                                """, (book_id,)).fetchone()[0]
        active_loans = db.execute("""SELECT COUNT(loan.id)
                                FROM copy
                                INNER JOIN loan on loan.copy_id = copy.id
                                WHERE copy.book_id=? AND loan.returned = 0;""",
                                (book_id,)).fetchone()[0]

        copies_available = num_copies - active_loans

        if copies_available == 0:
            next_due = Book.next_due_back(db, book_id)
        else:
            next_due = ''

        copy_availability_details = {'num_copies': num_copies,
                                    'num_loaned': active_loans,
                                    'num_available': copies_available,
                                    'next_due': next_due}

        return copy_availability_details

    @staticmethod
    def next_due_back(db, book_id):
        current_loans = db.execute("""SELECT loan.due_date
                                FROM copy
                                INNER JOIN loan on loan.copy_id = copy.id
                                WHERE copy.book_id=? AND loan.returned = 0;""",
                                (book_id,)).fetchall()

        due_dates = [l['due_date'] for l in current_loans]

        if len(due_dates) == 1:
            next_due_back = due_dates[0]
        else:
            due_dates_conv = [dt.strptime(due_date, "%d/%m/%y")
                            for due_date in due_dates]
            next_due_back = min(due_dates_conv).strftime("%d/%m/%y")

        return next_due_back

    @staticmethod
    def find_book_id(db, title, author_id, isbn, description,
                    publisher, year, cover_save_path):
        book_id = db.execute("""SELECT id FROM book WHERE title=? AND author_id= ?
                            AND isbn=? ;""", (title, author_id, isbn, )
                            ).fetchone()

        if book_id:
            return book_id[0]
        else:
            book_id = db.execute("""INSERT INTO book(title, author_id, isbn,
                                description, publisher, year, cover)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", (title,
                                author_id, isbn,
                                description, publisher, year,
                                cover_save_path)).lastrowid
            return book_id

    @staticmethod
    def find_loan_id(db, user_id, book_id):
        loan = db.execute("""SELECT loan.id FROM loan
                        INNER JOIN copy on copy.id = loan.copy_id
                        WHERE loan.borrower_id = ?
                        AND copy.book_id = ?
                        AND loan.returned = 0;""",
                        (user_id, book_id)).fetchone()

        loan_id = loan['id']

        return loan_id

    @staticmethod
    def insert_copy(db, book_id, hire_period, location):
        db.execute("""INSERT INTO copy(book_id, location, hire_period)
                VALUES (?, ?, ?);""", (book_id, location, hire_period))

        return

    @staticmethod
    def get_cover_save_path(title, author_name):
        stripped_title = "".join(x for x in title if x.isalnum())
        stripped_author_name = "".join(x for x in author_name if x.isalnum())
        cover_save_path = f"""static/images/covers/{stripped_author_name}/{stripped_title}"""

        if not os.path.exists(cover_save_path):
            os.makedirs(cover_save_path)

        return cover_save_path

    @staticmethod
    def check_isbn(db, isbn, title, author_id):
        if len(isbn) == 10:
            check_digit = 11
            alt_sum = 0

            for i in range(0, 9):
                mult = 10 - i
                term = mult * int(isbn[i])

                alt_sum += term

            alt_sum = alt_sum % 11
            check_digit -= alt_sum
            check_digit = check_digit % 11

            if check_digit == 10 and isbn[9] == 'X':
                valid = True
                message = ""
            elif check_digit == int(isbn[9]):
                valid = True
                message = ""
            else:
                valid = False
                message = "Invalid ISBN 10"
        elif len(isbn) == 13:
            check_sum = 0
            for i in range(13):
                if i % 2 == 0:
                    check_sum += int(isbn[i])
                else:
                    check_sum += 3 * int(isbn[i])

            check_sum = check_sum % 10

            if check_sum == 0:
                valid = True
                message = ""
            else:
                valid = False
                message = "Invalid ISBN 13"
        else:
            valid = False
            message = "Invalid ISBN length"

        if valid:
            isbn_results = db.execute("""SELECT title, author_id
                                    FROM book
                                    WHERE isbn = ?;""", (isbn,)).fetchone()

            if isbn_results:
                existing_title = isbn_results['title']
                existing_author_id = isbn_results['author_id']
                if title != existing_title or author_id != existing_author_id:
                    valid = False
                    existing_author = get_author_name_from_id(db,
                                                            existing_author_id)
                    message = f"ISBN already assigned to {existing_title} by {existing_author}"

        return valid, message

    @staticmethod
    def get_title_list(db):
        book_results = db.execute("SELECT id FROM book ORDER BY title;").fetchall()

        books = [Book.get_book_details(db, b['id']) for b in book_results]

        for book in books:
            copy_availability_details = Book.check_copies_available(db, book['id'])

            if copy_availability_details['num_available'] > 0:
                book['available'] = 'Available'
            else:
                book['available'] = 'Unavailable'

        return books

    @staticmethod
    def get_books_by_author(db, author_id):

        book_results = db.execute("""SELECT id, title FROM book
                                WHERE author_id = ? ORDER BY title""",
                                (author_id,)).fetchall()

        author_books = [{'id': b['id'], 'title': b['title']} for b in book_results]

        return author_books
