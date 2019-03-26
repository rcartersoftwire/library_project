# Book based functions

from datetime import datetime as dt


def get_book_list(db):
    book_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                author.first_name as first_name,
                                author.last_name as last_name
                                FROM book
                                INNER JOIN author on author.id = book.author_id
                                ORDER BY title;""").fetchall()

    books = [{'id': b['book_id'], 'title': b['title'],
              'author': b['first_name']
              + ' ' + b['last_name']} for b in book_results]

    for book in books:
        num_copies, active_loans = check_copies_available(db, book['id'])

        if num_copies != 0 and num_copies > active_loans:
            book['available'] = 'Available'
        else:
            book['available'] = 'Unavailable'

    return books


def get_book_details(db, id):
    book_info = db.execute("""SELECT book.title as title, book.publisher as publisher,
                           book.year as year, author.first_name as first_name,
                           author.last_name as last_name, book.isbn as isbn,
                           book.description as description
                           FROM book
                           INNER JOIN author ON book.author_id = author.id
                           WHERE book.id = ?""", (id,)).fetchone()
    title = book_info['title']
    author = book_info['first_name'] + ' ' + book_info['last_name']
    publisher = book_info['publisher']
    year = book_info['year']
    cover = "/static/images/missing_book_cover.jpg"
    description = book_info['description']
    isbn = book_info['isbn']

    return (title, author, publisher, year, cover, description, isbn)


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

    return num_copies, active_loans


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


def find_book_id(db, title, author_id, isbn, description,
                 publisher, year):
    book_id = db.execute("""SELECT id FROM book WHERE title=? AND author_id= ?
                         AND isbn=? ;""", (title, author_id, isbn, )
                         ).fetchone()

    if book_id:
        return book_id[0]
    else:
        db.execute("""INSERT INTO book(title, author_id, isbn, description, publisher, year)
                   VALUES (?, ?, ?, ?, ?, ?)""", (title, author_id, isbn,
                   description, publisher, year))
        book_id = db.execute("""SELECT id FROM book WHERE title=? AND author_id= ?
                             AND isbn=?;""", (title, author_id, isbn)
                             ).fetchone()[0]
        return book_id


def find_loan_id(db, user_id, book_id):
    loan = db.execute("""SELECT loan.id FROM loan
                      INNER JOIN copy on copy.id = loan.copy_id
                      WHERE loan.borrower_id = ?
                      AND copy.book_id = ?
                      AND loan.returned = 0;""",
                      (user_id, book_id)).fetchone()

    loan_id = loan['id']

    return loan_id
