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

ADD_BOOK_COOKIE = 'add_book_message'
BOOK_COOKIE = 'book_message'
JOIN_COOKIE = 'join_message'
LOGIN_COOKIE = 'login_message'
EDIT_ACC_COOKIE = 'edit_acc_message'

TOKEN_LIST = ['000000']

# Functions
from author import *
from book import *
from user import *
from librarian import *
from loan import *
from cookies import *


def get_search_results(db, search_query):
    search_queries = search_query.split(' ')
    search_pattern = '%'.join(search_queries)
    search_pattern = '%' + search_pattern + '%'
    search_results = db.execute("""SELECT book.id as book_id, book.title as title,
                                author.first_name as first_name,
                                author.last_name as last_name
                                FROM book
                                INNER JOIN author on author.id = book.author_id
                                WHERE book.title LIKE ?
                                OR author.first_name || ' ' ||
                                author.last_name LIKE ?;""",
                                (search_pattern, search_pattern)).fetchall()

    results = [{'id': b['book_id'], 'title': b['title'],
                'author': b['first_name'] + ' ' + b['last_name']}
               for b in search_results]

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
    message = get_cookie(LOGIN_COOKIE)

    return template('visitor_pages/home', books=books, message=message)


@get('/user/<id>/home')
def user_home(db, id):
    book_requested = request.params.get('book_requested')
    if book_requested is not None:
        book_requested = eval(book_requested)
    else:
        book_requested = False

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, id)

    books = get_book_list(db)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)
    return template('user_pages/user_home', books=books, user=user,
                    book_requested=book_requested)


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


@get('/browse/titles')
def browse_titles(db):
    books = get_title_list(db)

    return template('visitor_pages/visitor_browse_titles', books=books)


@get('/user/<user_id>/browse/titles')
def user_browse_titles(db, user_id):
    books = get_title_list(db)

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, user_id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return template('user_pages/user_browse_titles', books=books,
                    user=user)


@get('/librarian/<user_id>/browse/titles')
def librarian_browse_titles(db, user_id):
    books = get_title_list(db)

    name = get_librarian_name(db, user_id)

    return template('librarian_pages/librarian_browse_titles', books=books,
                    user_id=user_id, name=name)


@get('/browse/authors')
def browse_authors(db):
    authors = get_author_list(db)

    for author in authors:
        author_books = get_books_by_author(db, author['id'])
        author['books'] = author_books

    return template('visitor_pages/visitor_browse_authors', authors=authors)


@get('/user/<user_id>/browse/authors')
def user_browse_authors(db, user_id):
    authors = get_author_list(db)

    for author in authors:
        author_books = get_books_by_author(db, author['id'])
        author['books'] = author_books

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, user_id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans)

    return template('user_pages/user_browse_authors', authors=authors,
                    user=user)


@get('/librarian/<user_id>/browse/authors')
def librarian_browse_authors(db, user_id):
    authors = get_author_list(db)

    for author in authors:
        author_books = get_books_by_author(db, author['id'])
        author['books'] = author_books

    name = get_librarian_name(db, user_id)

    return template('librarian_pages/librarian_browse_authors',
                    authors=authors, name=name, user_id=user_id)


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

    message = get_cookie(BOOK_COOKIE, f'/librarian/{user_id}/')

    loan_list = get_loan_list(db, book_id)
    return template('librarian_pages/librarian_book_page',
                    book_details=book_details,
                    copy_availability_details=copy_availability_details,
                    name=name, user_id=user_id, loan_list=loan_list,
                    message=message)


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

    data = db.execute("""SELECT id, title, author_first_name, author_last_name
                      FROM book_request""").fetchall()
    req_id = [x['id'] for x in data]
    book_title = [x['title'] for x in data]
    book_first_name = [x['author_first_name'] for x in data]
    book_last_name = [x['author_last_name'] for x in data]
    book_author = ["{} {}".format(a_, b_) for a_, b_
                   in zip(book_first_name, book_last_name)]

    return template('librarian_pages/librarian_view_book_requests',
                    name=name, user_id=user_id, book_title=book_title,
                    book_author=book_author, req_id=req_id)


@get('/librarian/<user_id>/book_request/remove/<req_id>')
def remove_book_request(db, user_id, req_id):
    db.execute("DELETE FROM book_request WHERE id = ?", (req_id,))
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
    if len(names) == 1:
        last_name = ''
    else:
        last_name = names[1]

    db.execute("""INSERT INTO book_request(title, author_first_name, author_last_name)
                   VALUES (?,?,?)""", (title, first_name, last_name))

    redirect(f'/user/{user_id}/home?book_requested=True')



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
                set_cookie(LOGIN_COOKIE, 'Login failed.')
                redirect('/')
        else:
            set_cookie(LOGIN_COOKIE, 'Incorrect username or password.')
            redirect('/')
    else:
        set_cookie(LOGIN_COOKIE, 'Incorrect username or password.')
        redirect('/')


@get('/logout')
def logout(db):
    redirect('/')


@get('/user/<user_id>/account/edit')
def edit_user_account(db, user_id):
    message = get_cookie(EDIT_ACC_COOKIE)

    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, user_id)
    user_join_date = get_user_join_date(db, user_id)
    user_past_loans = get_user_past_loans(db, user_id)
    (username) = db.execute("SELECT username FROM user WHERE id=?",(user_id,)).fetchone()

    user = dict(id=user_id,
                username=username['username'],
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans,
                prof_pic=user_prof_pic,
                past_loans=user_past_loans,
                join_date=user_join_date)


    return template('user_pages/edit_user_account', message=message, user=user)

@post('/user/<user_id>/account/edit')
def edit_user_account_post(db, user_id):
    first_name = request.forms.get('first_name').capitalize()
    last_name = request.forms.get('last_name').capitalize()
    username = request.forms.get('username')
    old_password = request.forms.get('old_password')
    new_password = request.forms.get('new_password')
    prof_pic = request.files.get('prof_pic')

    db.execute("""UPDATE user SET
                    first_name = ?,
                    last_name = ?,
                    username = ?
                    WHERE id = ?;""", (first_name, last_name, username,
                                        user_id))
    if prof_pic:
        try:
            name, ext = os.path.splitext(prof_pic.filename)

            if ext not in ('.png', '.jpg', '.jpeg'):
                set_cookie(EDIT_ACC_COOKIE,
                        'File extension not allowed. Adding profile pic failed.')
                redirect(f'/user/{user_id}/account')

            save_path = f"""static/images/prof_pics/{username}"""
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            prof_pic.save(save_path)
            profile_pic_path = '/' + save_path + '/' + prof_pic.filename
            db.execute("""UPDATE user SET
                    prof_pic = ?
                    WHERE id = ?;""", (profile_pic_path,
                                        user_id))
        except:
            set_cookie(EDIT_ACC_COOKIE,
                'Profile Pic Update Failed')
            redirect(f'/user/{user_id}/account/edit')

    pwd_verified = False
    if old_password is not None and old_password != '':
        verify_pwd = db.execute("""SELECT password FROM user WHERE user.id=?""",(user_id,)).fetchone()
        print (verify_pwd['password'])
        if old_password == verify_pwd['password']:
            pwd_verified = True
        else:
            set_cookie(EDIT_ACC_COOKIE,
                'Incorrect Password')
            redirect(f'/user/{user_id}/account/edit')

    if pwd_verified:
        db.execute("""UPDATE user SET
                        password = ?
                        WHERE id = ?;""", (new_password,
                                            user_id))


    set_cookie(EDIT_ACC_COOKIE,
                    'Account Updated')
    redirect(f'/user/{user_id}/account/edit')

@get('/join')
def join_library(db):
    message = get_cookie(JOIN_COOKIE)
    return template('visitor_pages/join_library', message=message)


@post('/join')
def join(db):
    first_name = request.forms.get('first_name').capitalize()
    last_name = request.forms.get('last_name').capitalize()
    username = request.forms.get('username')
    password = request.forms.get('password')
    conf_password = request.forms.get('conf_password')
    acc_type = int(request.forms.get('acc_type'))
    token = request.forms.get('token')
        
    prof_pic = request.files.get('prof_pic')

    # Save Profile Pic to Directory
    try:
        name, ext = os.path.splitext(prof_pic.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            set_cookie(JOIN_COOKIE,
                       'File extension not allowed. Join library failed.')
            redirect('/join')

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
        set_cookie(JOIN_COOKIE, '''Password must be at least 8 characters.
                   Join library failed.''')
        redirect('/join')

    if password != conf_password:
        set_cookie(JOIN_COOKIE, '''Your passwords do not match.
                   Join library failed.''')
        redirect('/join')

    elif username_in_db:
        set_cookie(JOIN_COOKIE, '''This username is already taken.
                   Join library failed.''')
        redirect('/join')

    elif token is not None and token not in TOKEN_LIST:
        set_cookie(JOIN_COOKIE, '''Librarian token incorrect.
                    Join library failed.''')
        redirect('/join')

    # Insert into Database
    else:
        db.execute("""INSERT INTO user (first_name, last_name, username,
                   password, type, join_date, prof_pic)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""", (first_name, last_name,
                   username, password, acc_type, join_date, profile_pic_path))

        user_id = db.execute("SELECT id FROM user WHERE username = ?;",
                             (username,)).fetchone()[0]
        if acc_type == 0:
            redirect(f'/user/{user_id}/home')
        else:
            redirect(f'/librarian/{user_id}/home')


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
    message = get_cookie(ADD_BOOK_COOKIE, cookie_path=f"/librarian/{user_id}")

    return template('librarian_pages/add_books', name=name, user_id=user_id,
                    message=message)



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
        set_cookie(ADD_BOOK_COOKIE, f'{isbn_message}. Add Book failed.',
                   f'/librarian/{user_id}')
        redirect(f'/librarian/{user_id}/books/add')

    cover = request.files.get('cover')

    try:
        name, ext = os.path.splitext(cover.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            set_cookie(ADD_BOOK_COOKIE,
                       'File extension not allowed. Add Book failed.')
            redirect(f'/librarian/{user_id}/books/add')

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
def remove_copies(db, user_id, book_id):
    name = get_librarian_name(db, user_id)

    (book_title, first_name, last_name, cover) = db.execute("""SELECT title, first_name, last_name, cover 
                                                        FROM book JOIN author on author.id=author_id 
                                                        WHERE book.id=?""",(book_id,)).fetchone()
    author = first_name + ' ' + last_name

    copies_rows = db.execute("""SELECT copy.id, location, hire_period FROM copy WHERE book_id=?;""",(book_id,)).fetchall()
    checkout_rows = db.execute("""SELECT copy.id, user.first_name, user.last_name FROM loan 
                                    JOIN copy ON copy_id=copy.id 
                                    JOIN user ON user.id=borrower_id
                                    WHERE returned=0 AND book_id=?;""",(book_id,)).fetchall()
    checkout_list = [x['id'] for x in checkout_rows]
    borrower_list = [x['first_name']+' '+x['last_name'] for x in checkout_rows]
    copies_list = [dict(id=x['id'], location=x['location'], hire_period=x['hire_period']) for x in copies_rows]
    for i in range(len(copies_list)):
        if copies_list[i]['location'] == 1:
            copies_list[i]['location'] = 'Downstairs'
        else:
            copies_list[i]['location'] = 'Upstairs'

        copies_list[i]['checkout'] = 'No'
        copies_list[i]['borrower'] = ''

        for j in range(len(checkout_list)):
            if copies_list[i]['id'] == checkout_list[j]:
                copies_list[i]['checkout'] = 'Yes'
                copies_list[i]['borrower'] = borrower_list[j]
                break

    return template('librarian_pages/librarian_remove_copies', 
                        name=name, copies=copies_list, book_id=book_id, 
                        book_title=book_title, book_cover=cover,
                        author=author, user_id=user_id)

@get('/librarian/<user_id>/remove/<book_id>/<copy_id>')
def remove_copy(db, user_id, book_id, copy_id):
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

    redirect(f'/librarian/{user_id}/remove/{book_id}')




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
            set_cookie(BOOK_COOKIE,
                       'File extension not allowed. Failed to edit book.',
                       cookie_path=f"/librarian/{user_id}/")
            redirect(f'/librarian/{user_id}/book/{book_id}')

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
    num_of_copies = int(request.forms.get('num_of_copies'))
    location = request.forms.get('location')

    for i in range(num_of_copies):
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


@get('/librarian/<librarian_id>/users/view/<view_user_profile_id>')
def view_user_profile(db, librarian_id, view_user_profile_id):
    (user_id, user_first_name, user_last_name, user_loan_count,
     user_loans, user_prof_pic) = get_user_details(db, view_user_profile_id)
    user_join_date = get_user_join_date(db, view_user_profile_id)
    user_past_loans = get_user_past_loans(db, view_user_profile_id)

    user = dict(id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                loan_count=user_loan_count,
                loans=user_loans,
                prof_pic=user_prof_pic,
                past_loans=user_past_loans,
                join_date=user_join_date)

    name = get_librarian_name(db, librarian_id)

    return template('librarian_pages/view_user_profile', name=name,
                    user_id=librarian_id, user=user)


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
