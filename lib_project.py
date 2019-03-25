
# Configuration
database_file = 'library_project.db'

# Database Seeding
import sqlite3
conn = sqlite3.connect(database_file)
conn.execute("""CREATE TABLE IF NOT EXISTS author(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NULL
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS book (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                author_id INTEGER NOT NULL,
                isbn INTEGER NOT NULL UNIQUE,
                cover VARCHAR(255) NULL,
                description VARCHAR(255) NULL,
                publisher VARCHAR(255) NULL,
                year INTEGER NULL,
                FOREIGN KEY (author_id) REFERENCES author(id)
                );  """)
conn.execute("""CREATE TABLE IF NOT EXISTS copy (
                id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                location INTEGER NULL, -- enumerate possible locations
                hire_period INTEGER NOT NULL, -- number of days
                FOREIGN KEY(book_id) REFERENCES book(id)
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS user (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                type INT NOT NULL -- 0 = borrower, 1 =  librarian
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS loan (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                copy_id INTEGER NOT NULL,
                borrower_id INTEGER NOT NULL,
                due_date VARCHAR(255) NOT NULL,
                returned INTEGER NOT NULL, -- 0 = false, 1 = true
                FOREIGN KEY (copy_id) REFERENCES copy(id),
                FOREIGN KEY (borrower_id) REFERENCES user(id)
                ); """)
conn.commit()

# Backend

# Set Up

from bottle import (get, post, run, debug, install, request, response,
                    redirect, template, static_file)
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
install(message_plugin)
install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# Functions


def get_user_details(db, id):
    user_details = db.execute("""SELECT id, first_name, last_name FROM user
                      WHERE user.id = ?;""", (id,)).fetchone()

    user_loan_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                   author.first_name as first_name,
                                   author.last_name as last_name,
                                   loan.due_date as due_date
                                   FROM loan
                                   INNER JOIN copy on copy.id = loan.copy_id
                                   INNER JOIN book on book.id = copy.book_id
                                   INNER JOIN author on
                                   author.id = book.author_id
                                   WHERE loan.borrower_id = ? AND
                                   loan.returned = 0;""", (id,))

    user_id = user_details['id']
    user_first_name = user_details['first_name']
    user_last_name = user_details['last_name']

    user_loans = [{'book_id': l['book_id'], 'title': l['title'],
                   'author': l['first_name'] + ' ' + l['last_name'],
                   'due_date': l['due_date']} for l in user_loan_results]

    user_loan_count = len(user_loans)

    return (user_id, user_first_name, user_last_name, user_loan_count,
            user_loans)


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


def get_search_results(db, search_query):
    search_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                author.first_name as first_name,
                                author.last_name as last_name
                                FROM book
                                INNER JOIN author on author.id = book.author_id
                                WHERE book.title LIKE ?;""",
                                (search_query,)).fetchall()

    results = [{'id': b['book_id'], 'title': b['title'],
                'author': b['first_name']
                + ' ' + b['last_name']} for b in search_results]

    for book in results:
        num_copies = db.execute("""SELECT COUNT (copy.id)
                                FROM book
                                INNER JOIN copy on copy.book_id = book.id;
                                """).fetchone()[0]

        active_loans = db.execute("""SELECT COUNT(loan.id)
                                  FROM book
                                  INNER JOIN copy on copy.book_id = ?
                                  INNER JOIN loan on loan.copy_id = copy.id
                                  WHERE loan.returned = 0;""",
                                  (book['id'],)).fetchone()[0]
        if num_copies != 0 and num_copies > active_loans:
            book['available'] = 'Available'
        else:
            book['available'] = 'Unvailable'

    return results


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


from datetime import datetime as dt, timedelta


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


def find_author_id(db, author_name):
    names = author_name.split(" ", 1)
    first_name = names[0]
    last_name = names[1]

    author_id = db.execute("""SELECT id FROM author WHERE first_name = ?
                    AND last_name = ?""", (first_name, last_name)).fetchone()

    if author_id:
        return author_id[0]
    else:
        db.execute("""INSERT INTO author(first_name, last_name)
                   VALUES (?,?)""", (first_name, last_name))
        author_id = db.execute("""SELECT id FROM author WHERE first_name = ?
                               AND last_name = ?""",
                               (first_name, last_name)).fetchone()[0]
        return author_id


def find_book_id(db, title, author_id, isbn, description,
                 publisher, year):
    book_id = db.execute("""SELECT id FROM book WHERE title=? AND author_id= ?
                         AND isbn=? ;""", (title, author_id, isbn, )
                         ).fetchall()

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


def get_user_list(db):
    user_results = db.execute("""SELECT id FROM user WHERE type = 0;
                              """).fetchall()

    user_list = []

    for user in user_results:
        (user_id, user_first_name, user_last_name, user_loan_count,
         user_loans) = get_user_details(db, user['id'])

        user_name = user_first_name + ' ' + user_last_name

        user_list.append({'user_id': user_id, 'name': user_name,
                          'loan_count': user_loan_count,
                          'loans': user_loans})

    return user_list

# Routes


@get('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static')


@get('/')
def home(db):
    books = get_book_list(db)

    return template('home', books=books)


@get('/user/<id>/home')
def user_home(db, id):
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, id)

    books = get_book_list(db)

    return template('user_home', books=books, user_id=user_id,
                    user_first_name=user_first_name,
                    user_last_name=user_last_name,
                    user_loan_count=user_loan_count, user_loans=user_loans)


@get('/librarian/<user_id>/home')
def librarian_home(db, user_id):
    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    books = get_book_list(db)

    return template('librarian_home', user_id=user_id, books=books, name=name,)


@post('/search')
def search(db):
    search_query = request.forms.get('search_query')
    results = get_search_results(db, search_query)

    return template('search', search_query=search_query, results=results)


@post('/user/<id>/search')
def user_search(db, id):
    search_query = request.forms.get('search_query')
    results = get_search_results(db, search_query)

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, id)

    return template('user_search', search_query=search_query, results=results,
                    user_id=user_id, user_first_name=user_first_name,
                    user_last_name=user_last_name,
                    user_loan_count=user_loan_count, user_loans=user_loans)


@post('/librarian/<user_id>/search')
def librarian_search(db, user_id):
    search_query = request.forms.get('search_query')
    results = get_search_results(db, search_query)

    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    return template('librarian_search', search_query=search_query,
                    results=results, name=name, user_id=user_id)


@get('/book/<book_id>')
def book_details(db, book_id):
    (title, author, publisher, year, cover,
     description, isbn) = get_book_details(db, book_id)

    copies, copies_loaned = check_copies_available(db, book_id)
    copies_available = copies - copies_loaned

    if copies_available == 0:
        next_due = next_due_back(db, book_id)
    else:
        next_due = ''

    return template('book_page', title=title, author=author,
                    publisher=publisher, year=year, cover=cover,
                    description=description, isbn=isbn, copies=copies,
                    copies_available=copies_available, next_due=next_due)


@get('/user/<user_id>/book/<book_id>')
def user_book_details(db, user_id, book_id):
    (title, author, publisher, year, cover,
     description, isbn) = get_book_details(db, book_id)
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, user_id)

    book_loan_details = db.execute("""SELECT due_date FROM loan
                                   INNER JOIN copy on copy.id = loan.copy_id
                                   WHERE loan.borrower_id = ?
                                   AND copy.book_id = ?
                                   AND loan.returned = 0
                                   ORDER BY loan.due_date;""",
                                   (user_id, book_id)).fetchone()

    if book_loan_details:
        book_loaned = 1
        due_date = book_loan_details['due_date']
    else:
        book_loaned = 0
        due_date = ''

    copies, copies_loaned = check_copies_available(db, book_id)
    copies_available = copies - copies_loaned

    if copies_available == 0:
        next_due = next_due_back(db, book_id)
    else:
        next_due = ''

    return template('user_book_page', book_id=book_id, title=title,
                    author=author, publisher=publisher, year=year,
                    cover=cover, description=description, isbn=isbn,
                    user_id=user_id,
                    user_first_name=user_first_name,
                    user_last_name=user_last_name,
                    user_loan_count=user_loan_count, user_loans=user_loans,
                    book_loaned=book_loaned, due_date=due_date,
                    copies=copies, copies_available=copies_available,
                    next_due=next_due)


@get('/librarian/<user_id>/book/<book_id>')
def librarian_book_details(db, user_id, book_id):
    (title, author, publisher, year, cover,
     description, isbn) = get_book_details(db, book_id)

    copies, copies_loaned = check_copies_available(db, book_id)
    copies_available = copies - copies_loaned

    if copies_available == 0:
        next_due = next_due_back(db, book_id)
    else:
        next_due = ''

    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    return template('librarian_book_page', title=title, author=author,
                    publisher=publisher, year=year, cover=cover,
                    description=description, isbn=isbn, copies=copies,
                    copies_available=copies_available, next_due=next_due,
                    name=name, user_id=user_id)


@get('/user/<user_id>/borrow/<book_id>')
def borrow(db, user_id, book_id):
    copy = db.execute("""SELECT copy.id, copy.hire_period FROM copy WHERE NOT EXISTS
                      (SELECT loan.id FROM loan WHERE loan.copy_id = copy.id
                      AND returned = 0)
                      AND copy.book_id = ?""",
                      (book_id,)).fetchone()

    copy_id = copy['id']
    hire_period = copy['hire_period']

    due_date = (dt.now() + timedelta(days=hire_period)).strftime('%d/%m/%y')

    db.execute("""INSERT INTO loan (copy_id, borrower_id, due_date, returned)
               VALUES (?, ?, ?, ?);""", (copy_id, user_id, due_date, 0))

    redirect(f'/user/{user_id}/book/{book_id}')


@get('/user/<user_id>/return/<book_id>')
def return_book(db, user_id, book_id):
    loan_id = db.execute("""SELECT loan.id
                         FROM loan
                         INNER JOIN copy on copy.id = loan.copy_id
                         WHERE copy.book_id = ?
                         AND loan.borrower_id = ? AND returned = 0""",
                         (book_id, user_id)).fetchone()[0]

    db.execute("""UPDATE loan SET returned = 1 WHERE id=?;""", (loan_id,))

    redirect(f'/user/{user_id}/book/{book_id}')


@get('/user/<user_id>/renew/<book_id>')
def renew_book(db, user_id, book_id):
    loan = db.execute("""SELECT loan.id, loan.due_date, copy.hire_period
                      FROM loan
                      INNER JOIN copy on copy.id = loan.copy_id
                      WHERE copy.book_id = ?
                      AND loan.borrower_id = ? AND returned = 0;""",
                      (book_id, user_id)).fetchone()

    loan_id = loan['id']
    current_due = dt.strptime(loan['due_date'], '%d/%m/%y')
    hire_period = loan['hire_period']
    new_due = current_due + timedelta(days=hire_period)
    new_due_date = new_due.strftime('%d/%m/%y')

    db.execute("""UPDATE loan SET due_date = ? WHERE id = ?;""",
               (new_due_date, loan_id))

    redirect(f'/user/{user_id}/book/{book_id}')


@post('/login')
def login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')

    check_user = db.execute("""SELECT id, password, type FROM user WHERE username = ?;
                            """, (username,)).fetchone()

    if check_user:
        if check_user['password'] == password:
            if check_user['type'] == 0:
                redirect(f'/user/{str(check_user["id"])}/home')
            elif check_user['type'] == 1:
                redirect(f'/librarian/{str(check_user["id"])}/home')
            else:
                redirect('/')
        else:
            redirect('/')
    else:
        redirect('/')


@get('/logout')
def logout(db):
    redirect('/')


@get('/join')
def join_library(db):
    return template('join_library', message=request.message)


@post('/join')
def join(db):
    first_name = request.forms.get('first_name')
    last_name = request.forms.get('last_name')
    username = request.forms.get('username')
    password = request.forms.get('password')
    conf_password = request.forms.get('conf_password')

    username_in_db = db.execute("SELECT id FROM user WHERE username =?",
                                (username,)).fetchall()

    if password != conf_password:
        response.flash("Your passwords do not match")
        redirect('/join')

    elif username_in_db:
        response.flash("This username is already taken")
        redirect('/join')

    else:
        db.execute("""INSERT INTO user (first_name, last_name, username, password, type)
                   VALUES (?, ?, ?, ?, ?);""", (first_name, last_name,
                   username, password, 0))

        user_id = db.execute("SELECT id FROM user WHERE username = ?;",
                             (username,)).fetchone()[0]

        redirect(f'/user/{user_id}/home')


@get('/librarian/<user_id>/books/add')
def add_books(db, user_id):
    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    return template('add_books', name=name, user_id=user_id)


@post('/librarian/<user_id>/add')
def add_book(db, user_id):
    title = request.forms.get('title')
    author_name = request.forms.get('author_name')
    isbn = int(request.forms.get('isbn'))
    description = request.forms.get('description')
    publisher = request.forms.get('publisher')
    year = request.forms.get('year')
    location = request.forms.get('location')
    hire_period = request.forms.get('hire_period')

    author_id = find_author_id(db, author_name)

    book_id = find_book_id(db, title, author_id, isbn, description,
                           publisher, year)

    db.execute("""INSERT INTO copy(book_id, location, hire_period)
               VALUES (?, ?, ?);""", (book_id, location, hire_period))

    redirect(f'/librarian/{user_id}/home')


@get('/librarian/<user_id>/users/view')
def view_users(db, user_id):
    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    user_list = get_user_list(db)

    return template('view_users', name=name, user_id=user_id, user_list=user_list)


run(host='localhost', port=8080, debug=True)
