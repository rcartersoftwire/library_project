# System Imports
import os
from datetime import datetime as dt

# Module Function Imports
import db_helper
import author
import book
import user
import loan
import librarian
import cookies
import utils 
from constants import (AUTH_COOKIE, AUTH_COOKIE_SECRET, PWD_KEY, LOGIN_COOKIE, JOIN_COOKIE, TOKEN_LIST)

# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# Create Bottle Object
general_app = bottle.Bottle()

# Database Configuration
database_file = 'library_project.db'
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
general_app.install(message_plugin)
general_app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# ====================================================
# General Routes
@general_app.get('/static/<filename:path>')
def serve_static(filename):
    return bottle.static_file(filename, root='./static')

@general_app.get('/')
def home(db):
    user_id = bottle.request.get_cookie(AUTH_COOKIE, secret=AUTH_COOKIE_SECRET)
    if user_id is not None:
        db_helper.redirect_to_home(db)

    books = book.get_book_list(db)
    message = cookies.get_cookie(LOGIN_COOKIE)

    return bottle.template('visitor_pages/home', books=books, message=message)

@general_app.post('/search')
def search(db):
    search_query = bottle.request.forms.get('search_query')
    results = db_helper.get_search_results(db, search_query)

    return bottle.template('visitor_pages/search', search_query=search_query,
                    results=results)

@general_app.get('/book/<book_id>')
def book_details(db, book_id):
    book_details = book.get_book_details(db, book_id)
    copy_availability_details = book.check_copies_available(db, book_id)

    return bottle.template('visitor_pages/book_page', book_details=book_details,
                    copy_availability_details=copy_availability_details)

@general_app.get('/browse/titles')
def browse_titles(db):
    books = book.get_title_list(db)

    return bottle.template('visitor_pages/visitor_browse_titles', books=books)

@general_app.get('/browse/authors')
def browse_authors(db):
    authors = author.get_author_list(db)

    for each in authors:
        author_books = book.get_books_by_author(db, each['id'])
        each['books'] = author_books

    return bottle.template('visitor_pages/visitor_browse_authors', authors=authors)

@general_app.post('/login')
def login(db):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')

    check_user = db.execute("""SELECT id, password, type FROM user WHERE username = ?;
                            """, (username,)).fetchone()


    if not check_user or check_user['password'] != utils.encode(PWD_KEY, password):
        cookies.set_cookie(LOGIN_COOKIE, 'Incorrect username or password.')
        bottle.redirect('/')
        
    db_helper.check_fines(db, check_user["id"])

    bottle.response.set_cookie(AUTH_COOKIE, str(check_user["id"]), secret=AUTH_COOKIE_SECRET)
    bottle.redirect('/')

@general_app.get('/logout')
def logout(db):
    bottle.response.delete_cookie(AUTH_COOKIE)
    bottle.redirect('/')

@general_app.get('/join')
def join_library(db):
    message = cookies.get_cookie(JOIN_COOKIE)
    return bottle.template('visitor_pages/join_library', message=message)

@general_app.post('/join')
def join(db):
    first_name = bottle.request.forms.get('first_name').capitalize()
    last_name = bottle.request.forms.get('last_name').capitalize()
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    conf_password = bottle.request.forms.get('conf_password')
    acc_type = int(bottle.request.forms.get('acc_type'))
    token = bottle.request.forms.get('token')
        
    prof_pic = bottle.request.files.get('prof_pic')

    # Save Profile Pic to Directory
    try:
        name, ext = os.path.splitext(prof_pic.filename)

        if ext not in ('.png', '.jpg', '.jpeg'):
            cookies.set_cookie(JOIN_COOKIE,
                                'File extension not allowed. Join library failed.')
            bottle.redirect('/join')

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
        cookies.set_cookie(JOIN_COOKIE, '''Password must be at least 8 characters.
                   Join library failed.''')
        bottle.redirect('/join')

    if password != conf_password:
        cookies.set_cookie(JOIN_COOKIE, '''Your passwords do not match.
                   Join library failed.''')
        bottle.redirect('/join')

    elif username_in_db:
        cookies.set_cookie(JOIN_COOKIE, '''This username is already taken.
                   Join library failed.''')
        bottle.redirect('/join')

    elif token is not None and token not in TOKEN_LIST:
        cookies.set_cookie(JOIN_COOKIE, '''Librarian token incorrect.
                    Join library failed.''')
        bottle.redirect('/join')

    # Insert into Database
    else:
        password = utils.encode(PWD_KEY, password)
        db.execute("""INSERT INTO user (first_name, last_name, username,
                   password, type, join_date, prof_pic)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""", (first_name, last_name,
                   username, password, acc_type, join_date, profile_pic_path))

        user_id = db.execute("SELECT id FROM user WHERE username = ?;",
                             (username,)).fetchone()[0]

        bottle.response.set_cookie(AUTH_COOKIE, str(user_id), secret=AUTH_COOKIE_SECRET)
        db_helper.redirect_to_home(db)

