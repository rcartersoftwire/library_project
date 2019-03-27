# Set Up

from bottle import (get, post, run, debug, install, request, response,
                    redirect, template, static_file)
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
from datetime import datetime as dt

# Configuration
import caribou
database_file = 'library_project.db'
migrations_path = 'migrations/'

caribou.upgrade(database_file, migrations_path)

install(message_plugin)
install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# Functions
from author import (find_author_id)
from book import (get_book_list, get_book_details, check_copies_available,
                  next_due_back, find_book_id, find_loan_id, insert_copy)
from user import (get_user_details, get_user_list, get_user_past_loans,
                  get_user_join_date)
from librarian import get_librarian_name
from loan import get_user_book_details, create_loan, end_loan, renew_loan


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

    return template('visitor_pages/home', books=books)


@get('/user/<id>/home')
def user_home(db, id):
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, id)

    books = get_book_list(db)

    return template('user_pages/user_home', books=books, user_id=user_id,
                    user_first_name=user_first_name,
                    user_last_name=user_last_name,
                    user_loan_count=user_loan_count, user_loans=user_loans)


@get('/librarian/<user_id>/home')
def librarian_home(db, user_id):
    name = get_librarian_name(db, user_id)

    books = get_book_list(db)

    return template('librarian_pages/librarian_home', user_id=user_id,
                    books=books, name=name,)


@post('/search')
def search(db):
    search_query = request.forms.get('search_query')
    results = get_search_results(db, search_query)

    return template('visitor_pages/search', search_query=search_query,
                    results=results)


@post('/user/<id>/search')
def user_search(db, id):
    search_query = request.forms.get('search_query')
    results = get_search_results(db, search_query)

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, id)

    return template('user_pages/user_search', search_query=search_query,
                    results=results, user_id=user_id,
                    user_first_name=user_first_name,
                    user_last_name=user_last_name,
                    user_loan_count=user_loan_count, user_loans=user_loans)


@post('/librarian/<user_id>/search')
def librarian_search(db, user_id):
    search_query = request.forms.get('search_query')
    results = get_search_results(db, search_query)

    name = get_librarian_name(db, user_id)

    return template('librarian_pages/librarian_search',
                    search_query=search_query,
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

    return template('visitor_pages/book_page', title=title, author=author,
                    publisher=publisher, year=year, cover=cover,
                    description=description, isbn=isbn, copies=copies,
                    copies_available=copies_available, next_due=next_due)


@get('/user/<user_id>/book/<book_id>')
def user_book_details(db, user_id, book_id):
    (title, author, publisher, year, cover,
     description, isbn) = get_book_details(db, book_id)
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, user_id)

    copies, copies_loaned = check_copies_available(db, book_id)
    copies_available = copies - copies_loaned

    if copies_available == 0:
        next_due = next_due_back(db, book_id)
    else:
        next_due = ''

    book_loaned, due_date = get_user_book_details(db, user_id, book_id)

    return template('user_pages/user_book_page', book_id=book_id, title=title,
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

    name = get_librarian_name(db, user_id)

    return template('librarian_pages/librarian_book_page', title=title,
                    author=author, publisher=publisher, year=year, cover=cover,
                    description=description, isbn=isbn, copies=copies,
                    copies_available=copies_available, next_due=next_due,
                    name=name, user_id=user_id, book_id=book_id)


@get('/user/<user_id>/borrow/<book_id>')
def borrow(db, user_id, book_id):
    create_loan(db, user_id, book_id)

    redirect(f'/user/{user_id}/book/{book_id}')


@get('/user/<user_id>/return/<book_id>')
def return_book(db, user_id, book_id):
    end_loan(db, user_id, book_id)

    redirect(f'/user/{user_id}/book/{book_id}')


@get('/user/<user_id>/renew/<book_id>')
def renew_book(db, user_id, book_id):
    loan_id = find_loan_id(db, user_id, book_id)

    renew_loan(db, loan_id)

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
    return template('visitor_pages/join_library', message=request.message)


@post('/join')
def join(db):
    first_name = request.forms.get('first_name')
    last_name = request.forms.get('last_name')
    username = request.forms.get('username')
    password = request.forms.get('password')
    conf_password = request.forms.get('conf_password')

    now = dt.now()
    join_date = now.strftime("%d/%m/%y")

    username_in_db = db.execute("SELECT id FROM user WHERE username =?",
                                (username,)).fetchall()

    if len(password) < 8:
        response.flash("Password must be at least 8 characters")
        redirect('/join')
        
    if password != conf_password:
        response.flash("Your passwords do not match")
        redirect('/join')

    elif username_in_db:
        response.flash("This username is already taken")
        redirect('/join')

    else:
        db.execute("""INSERT INTO user (first_name, last_name, username,
                   password, type, join_date)
                   VALUES (?, ?, ?, ?, ?, ?);""", (first_name, last_name,
                   username, password, 0, join_date))

        user_id = db.execute("SELECT id FROM user WHERE username = ?;",
                             (username,)).fetchone()[0]

        redirect(f'/user/{user_id}/home')

@get('/get_username_list/<username>')
def get_username_list(db, username):
    username_in_db = db.execute("SELECT id FROM user WHERE username =?",
                                 (username,)).fetchall() 
    if username_in_db:
        return {'nameTaken': True}
    else:
        return {'nameTaken': False}

@get('/librarian/<user_id>/books/add')
def add_books(db, user_id):
    name = get_librarian_name(db, user_id)

    return template('librarian_pages/add_books', name=name, user_id=user_id)



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

    insert_copy(db, book_id, hire_period, location)

    redirect(f'/librarian/{user_id}/home')


@get('/librarian/<user_id>/remove/<book_id>')
def remove_copy(db, user_id, book_id):
    # Find one copy ID to be removed
    result = db.execute("""SELECT id FROM copy where book_id = ?;""", (book_id,)).fetchone()
    copy_id = result['id']

    # Remove associated child loans
    db.execute("""DELETE FROM loan WHERE copy_id = ?;""", (copy_id,))

    # Remove book if last copy
    num_copies = db.execute("""SELECT COUNT (copy.id)
                               FROM copy
                               WHERE book_id = ?;
                               """, (book_id,)).fetchone()[0]

    db.execute("""DELETE FROM copy WHERE id = ?;""", (copy_id,))
    if num_copies == 1:
        db.execute("""DELETE FROM book WHERE id = ?;""", (book_id,))
        redirect(f'/librarian/{user_id}/home')
        return

    redirect(f'/librarian/{user_id}/book/{book_id}')



@get('/librarian/<user_id>/edit/<book_id>')
def edit_book(db, user_id, book_id):
    name = get_librarian_name(db, user_id)

    (title, author, publisher, year, cover, description,
     isbn) = get_book_details(db, book_id)

    return template('librarian_pages/edit_book', user_id=user_id, name=name,
                    title=title, author=author, publisher=publisher, year=year,
                    cover=cover, description=description, isbn=isbn,
                    book_id=book_id)


@post('/librarian/<user_id>/edit')
def edit_book_details(db, user_id):
    book_id = request.forms.get('book_id')
    description = request.forms.get('description')
    publisher = request.forms.get('publisher')
    year = request.forms.get('year')

    db.execute("""UPDATE book SET
               description = ?,
               publisher = ?,
               year = ?
               WHERE id = ?;""", (description, publisher, year, book_id))

    redirect(f'/librarian/{user_id}/book/{book_id}')


@post('/librarian/<user_id>/add_copy')
def add_copy(db, user_id):
    book_id = request.forms.get('book_id')
    hire_period = request.forms.get('hire_period')
    location = request.forms.get('location')

    insert_copy(db, book_id, hire_period, location)
    redirect(f'/librarian/{user_id}/book/{book_id}')

@get('/librarian/<user_id>/users/view')
def view_users(db, user_id):
    libr_names = db.execute("""SELECT first_name, last_name FROM  user
                            WHERE id = ?;""", (user_id,)).fetchone()

    name = libr_names['first_name'] + ' ' + libr_names['last_name']

    user_list = get_user_list(db)

    return template('librarian_pages/view_users', name=name, user_id=user_id,
                    user_list=user_list)


@get('/user/<user_id>/account')
def user_account(db, user_id):
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans) = get_user_details(db, user_id)
    user_join_date = get_user_join_date(db, user_id)
    user_past_loans = get_user_past_loans(db, user_id)

    return template('user_pages/user_account', user_id=user_id,
                    user_first_name=user_first_name,
                    user_last_name=user_last_name,
                    user_loan_count=user_loan_count, user_loans=user_loans,
                    user_past_loans=user_past_loans,
                    user_join_date=user_join_date)


run(host='localhost', port=8080, debug=True)
