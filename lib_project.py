# Set Up

from bottle import (get, post, run, debug, install, request, response,
                    redirect, template, static_file)
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
from datetime import datetime as dt
import os

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
                  next_due_back, find_book_id, find_loan_id, insert_copy,
                  get_cover_save_path, check_isbn)
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
     user_loans, user_prof_pic) = get_user_details(db, id)

    books = get_book_list(db)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)
    return template('user_pages/user_home', books=books, user=user)


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
     user_loans, user_prof_pic) = get_user_details(db, id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return template('user_pages/user_search', search_query=search_query,
                    results=results, user=user)


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
    book_details = get_book_details(db, book_id)
    copy_availability_details = check_copies_available(db, book_id)

    return template('visitor_pages/book_page', book_details=book_details,
                    copy_availability_details=copy_availability_details)


@get('/user/<user_id>/book/<book_id>')
def user_book_details(db, user_id, book_id):
    book_details = get_book_details(db, book_id)
    copy_availability_details = check_copies_available(db, book_id)

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, user_id)

    book_loaned, due_date = get_user_book_details(db, user_id, book_id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return template('user_pages/user_book_page', book_details=book_details,
                    user=user, book_loaned=book_loaned, due_date=due_date,
                    copy_availability_details=copy_availability_details)


@get('/librarian/<user_id>/book/<book_id>')
def librarian_book_details(db, user_id, book_id):
    book_details = get_book_details(db, book_id)
    copy_availability_details = check_copies_available(db, book_id)
    name = get_librarian_name(db, user_id)

    return template('librarian_pages/librarian_book_page',
                    book_details=book_details,
                    copy_availability_details=copy_availability_details,
                    name=name, user_id=user_id)


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


@get('/librarian/<user_id>/book_requests')
def view_book_requests(db, user_id):
    name = get_librarian_name(db, user_id)

    data = db.execute("SELECT id, title, author_first_name, author_last_name FROM book_request").fetchall()
    req_id = [x['id'] for x in data]
    book_title = [x['title'] for x in data]
    book_first_name = [x['author_first_name'] for x in data]
    book_last_name = [x['author_last_name'] for x in data]
    book_author = ["{} {}".format(a_, b_) for a_, b_ in zip(book_first_name, book_last_name)]
    
    return template('librarian_pages/librarian_view_book_requests', name=name, user_id=user_id, book_title=book_title, book_author=book_author, req_id=req_id)


@get('/librarian/<user_id>/book_request/remove/<req_id>')
def remove_book_request(db, user_id, req_id):
    db.execute("DELETE FROM book_request WHERE id = ?",(req_id,))
    redirect(f'/librarian/{user_id}/book_requests')


@get('/user/<user_id>/book_request')
def book_request(db, user_id):
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, user_id)
    user_join_date = get_user_join_date(db, user_id)
    user_past_loans = get_user_past_loans(db, user_id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count, 
                loans=user_loans,
                past_loans=user_past_loans,
                join_date=user_join_date)

    return template('user_pages/user_book_request', user=user)


@post('/user/<user_id>/book_request')
def add_book_request(db, user_id):
    title = request.forms.get('title').strip()
    author_name = request.forms.get('author_name').strip()

    names = author_name.split(" ", 1)
    first_name = names[0]
    last_name = names[1]

    db.execute("""INSERT INTO book_request(title, author_first_name, author_last_name)
                   VALUES (?,?,?)""", (title, first_name, last_name))

    redirect(f'/user/{user_id}/home')


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

    prof_pic = request.files.get('prof_pic')

    # Save Profile Pic to Directory
    try:
        name, ext = os.path.splitext(prof_pic.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            response.flash('File extension not allowed. Add Book failed')
            redirect('/librarian/<user_id>/add')

        save_path = f"""static/images/prof_pics/{username}"""
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        prof_pic.save(save_path)
        profile_pic_path = '/' + save_path + '/' + prof_pic.filename

    except AttributeError:
        profile_pic_path = '/static/images/unknown-user.jpg'

    # Join Date 
    now = dt.now()
    join_date = now.strftime("%d/%m/%y")

    # Criteria Checking
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

    # Insert into Database
    else:
        db.execute("""INSERT INTO user (first_name, last_name, username,
                   password, type, join_date, prof_pic)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""", (first_name, last_name,
                   username, password, 0, join_date, profile_pic_path))

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
    message = request.get_cookie('book_message', default="")
    if message:
        response.delete_cookie("book_message", path=f"/librarian/{user_id}/")

    return template('librarian_pages/add_books', name=name, user_id=user_id,
                    message=message)


@get('/get_loan_list/<book_id>')
def get_loan_list(db, book_id):
    borrower_list = db.execute("""SELECT first_name, last_name FROM loan
                               JOIN copy on copy_id=copy.id
                               JOIN user on borrower_id=user.id
                               WHERE book_id = ? AND returned = 0""",
                               (book_id,)).fetchall()

    list_of_borrowers = [x['first_name']+' '+x['last_name']
                         for x in borrower_list]

    return {'borrower_names': list_of_borrowers}


@get('/get_book_location/<book_id>')
def get_book_location(db, book_id):

    all_copies_location = db.execute("""SELECT copy.id, location
                                     FROM copy WHERE book_id = ?""",
                                     (book_id,)).fetchall()

    unavailable_copies = db.execute("""SELECT copy.id FROM copy
                                    JOIN loan on copy_id=copy.id
                                    WHERE loan.returned = 0 AND book_id = ?""",
                                    (book_id,)).fetchall()

    list_of_unavailable_copies = [x['id'] for x in unavailable_copies]

    downstairs = 0
    upstairs = 0
    for copy in all_copies_location:
        if copy['id'] not in list_of_unavailable_copies:
            if copy['location'] == 1:
                downstairs += 1
            else:
                upstairs += 1

    return {'downstairs': downstairs, 'upstairs': upstairs}


@post('/librarian/<user_id>/add')
def add_book(db, user_id):
    title = request.forms.get('title').strip()
    author_name = request.forms.get('author_name').strip()
    isbn = request.forms.get('isbn').strip()
    description = request.forms.get('description').strip()
    publisher = request.forms.get('publisher').strip()
    year = request.forms.get('year')
    location = request.forms.get('location')
    hire_period = request.forms.get('hire_period')

    author_id = find_author_id(db, author_name)
    valid_isbn, isbn_message = check_isbn(db, isbn, title, author_id)

    if not valid_isbn:
        response.set_cookie('book_message', f'{isbn_message}. Add Book failed.')
        redirect(f'/librarian/{user_id}/books/add')

    cover = request.files.get('cover')

    try:
        name, ext = os.path.splitext(cover.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            response.set_cookie('book_message', 'File extension not allowed. Add Book failed.')
            redirect('/librarian/<user_id>/add')

        cover_save_path = get_cover_save_path(title, author_name)
        cover_path = cover_save_path + '/' + cover.filename

        if os.path.exists(cover_path):
            os.remove(cover_path)

        cover_path = '/' + cover_path
        cover.save(cover_save_path)

    except AttributeError:
        cover_path = '/static/images/missing_book_cover.jpg'

    book_id = find_book_id(db, title, author_id, isbn, description,
                           publisher, year, cover_path)

    insert_copy(db, book_id, hire_period, location)

    redirect(f'/librarian/{user_id}/book/{book_id}')


@get('/librarian/<user_id>/remove/<book_id>')
def remove_copy(db, user_id, book_id):
    # Find one copy ID to be removed
    all_copies = db.execute("""SELECT id FROM copy where book_id = ?;""",
                            (book_id,)).fetchall()

    unavailable_copies = db.execute("""SELECT copy.id FROM copy
                                    JOIN loan on copy_id=copy.id
                                    WHERE loan.returned = 0
                                    AND book_id = ?""",
                                    (book_id,)).fetchall()

    all_copies_list = [x['id'] for x in all_copies]
    unavailable_copies_list = [x['id'] for x in unavailable_copies]

    available_copies = [x for x in all_copies_list if x not in unavailable_copies_list]

    if len(available_copies)>0:
        copy_id = available_copies[0]

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

    else:
        response.flash("All copies are checked out at the moment!")
        redirect(f'/librarian/{user_id}/book/{book_id}')


@get('/librarian/<user_id>/edit/<book_id>')
def edit_book(db, user_id, book_id):
    name = get_librarian_name(db, user_id)

    book_details = get_book_details(db, book_id)

    return template('librarian_pages/edit_book', user_id=user_id, name=name,
                    book_details=book_details)


@post('/librarian/<user_id>/edit')
def edit_book_details(db, user_id):
    book_id = request.forms.get('book_id')
    title = request.forms.get('title')
    author_name = request.forms.get('author_name')
    description = request.forms.get('description')
    publisher = request.forms.get('publisher')
    year = request.forms.get('year')

    cover = request.files.get('cover')
    if cover:
        name, ext = os.path.splitext(cover.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            response.flash('File extension not allowed. Add Book failed')
            redirect('/librarian/<user_id>/add')

        cover_save_path = get_cover_save_path(title, author_name)
        cover_path = cover_save_path + '/' + cover.filename

        if os.path.exists(cover_path):
            os.remove(cover_path)

        cover_path = '/' + cover_path
        cover.save(cover_save_path)

        db.execute("""UPDATE book SET
                      description = ?,
                      publisher = ?,
                      year = ?,
                      cover = ?
                      WHERE id = ?;""", (description, publisher, year,
                                         cover_path, book_id))
    else:
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
     user_loans, user_prof_pic) = get_user_details(db, user_id)
    user_join_date = get_user_join_date(db, user_id)
    user_past_loans = get_user_past_loans(db, user_id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans,
                prof_pic=user_prof_pic,
                past_loans=user_past_loans,
                join_date=user_join_date)

    return template('user_pages/user_account', user=user)


run(host='localhost', port=8080, debug=True)
