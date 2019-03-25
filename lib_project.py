# Set Up

from bottle import (get, post, run, debug, install, request, response,
                    redirect, template, static_file)
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin

# Configuration
import caribou
database_file = 'library_project.db'
migrations_path = 'migrations/'
version = '20190325114200'

caribou.upgrade(database_file, migrations_path)

install(message_plugin)
install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# Functions
from author import (find_author_id)
from book import (get_book_list, get_book_details, check_copies_available,
                  next_due_back, find_book_id, find_loan_id, renew_loan)
from user import get_user_details, get_user_list


def get_search_results(db, search_query):
    search_pattern = '%' + search_query + '%'
    search_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                author.first_name as first_name,
                                author.last_name as last_name
                                FROM book
                                INNER JOIN author on author.id = book.author_id
                                WHERE book.title LIKE ?;""",
                                (search_pattern,)).fetchall()

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
    loan_id = find_loan_id(db, user_id, book_id)

    renew_loan(loan_id)

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

    return template('view_users', name=name, user_id=user_id,
                    user_list=user_list)


run(host='localhost', port=8080, debug=True)
