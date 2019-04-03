# System Imports
import os
from datetime import datetime as dt

# Module Function Imports
import models.author
import models.book
import models.user
import services.db_helper
import services.loan
import services.librarian
import services.cookies
import services.tools
from services.cookies import (AUTH_COOKIE, LOGIN_COOKIE, JOIN_COOKIE)
from config import AUTH_COOKIE_SECRET, PWD_KEY, TOKEN_LIST

# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

from config import database_file

# Create Bottle Object
general_app = bottle.Bottle()

# Database Configuration
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
        services.db_helper.redirect_to_home(db)

    books = models.book.get_book_list(db)
    message = services.cookies.get_cookie(LOGIN_COOKIE)

    return bottle.template('visitor_pages/home', books=books, message=message)

@general_app.post('/search')
def search(db):
    search_query = bottle.request.forms.get('search_query')
    results = services.db_helper.get_search_results(db, search_query)

    return bottle.template('visitor_pages/search', search_query=search_query,
                    results=results)

@general_app.get('/book/<book_id>')
def book_details(db, book_id):
    book_details = models.book.get_book_details(db, book_id)
    copy_availability_details = models.book.check_copies_available(db, book_id)

    return bottle.template('visitor_pages/book_page', book_details=book_details,
                    copy_availability_details=copy_availability_details)

@general_app.get('/browse/titles')
def browse_titles(db):
    books = models.book.get_title_list(db)

    return bottle.template('visitor_pages/visitor_browse_titles', books=books)

@general_app.get('/browse/authors')
def browse_authors(db):
    authors = models.author.get_author_list(db)

    for each in authors:
        author_books = models.book.get_books_by_author(db, each['id'])
        each['books'] = author_books

    return bottle.template('visitor_pages/visitor_browse_authors', authors=authors)

@general_app.post('/login')
def login(db):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')

    check_user = db.execute("""SELECT id, password, type FROM user WHERE username = ?;
                            """, (username,)).fetchone()


    if not check_user or check_user['password'] != services.tools.encode(PWD_KEY, password):
        services.cookies.set_cookie(LOGIN_COOKIE, 'Incorrect username or password.')
        bottle.redirect('/')
        
    services.db_helper.check_fines(db, check_user["id"])

    bottle.response.set_cookie(AUTH_COOKIE, str(check_user["id"]), secret=AUTH_COOKIE_SECRET)
    bottle.redirect('/')

@general_app.get('/logout')
def logout(db):
    bottle.response.delete_cookie(AUTH_COOKIE)
    bottle.redirect('/')

@general_app.get('/join')
def join_library(db):
    message = services.cookies.get_cookie(JOIN_COOKIE)
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

    # Join Date
    now = dt.now()
    join_date = now.strftime("%d/%m/%y")

    # Criteria Checking
    username_in_db = db.execute("SELECT id FROM user WHERE username =?",
                                (username,)).fetchall()

    if len(password) < 8:
        services.cookies.set_cookie(JOIN_COOKIE, '''Password must be at least 8 characters.
                   Join library failed.''')
        bottle.redirect('/join')

    if password != conf_password:
        services.cookies.set_cookie(JOIN_COOKIE, '''Your passwords do not match.
                   Join library failed.''')
        bottle.redirect('/join')

    elif username_in_db:
        services.cookies.set_cookie(JOIN_COOKIE, '''This username is already taken.
                   Join library failed.''')
        bottle.redirect('/join')

    elif token is not None and token not in TOKEN_LIST:
        services.cookies.set_cookie(JOIN_COOKIE, '''Librarian token incorrect.
                    Join library failed.''')
        bottle.redirect('/join')


    # Insert into Database
    else:
        # Save Profile Pic to Directory
        try:
            name, ext = os.path.splitext(prof_pic.filename)

            if ext not in ('.png', '.jpg', '.jpeg'):
                services.cookies.set_cookie(JOIN_COOKIE,
                                    'File extension not allowed. Join library failed.')
                bottle.redirect('/join')

            save_path = f"""static/images/prof_pics/{username}"""
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            prof_pic.save(save_path)
            profile_pic_path = '/' + save_path + '/' + prof_pic.filename

        except AttributeError:
            profile_pic_path = '/static/images/unknown-user.jpg'

        password = services.tools.encode(PWD_KEY, password)
        db.execute("""INSERT INTO user (first_name, last_name, username,
                   password, type, join_date, prof_pic)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""", (first_name, last_name,
                   username, password, acc_type, join_date, profile_pic_path))

        user_id = db.execute("SELECT id FROM user WHERE username = ?;",
                             (username,)).fetchone()[0]

        bottle.response.set_cookie(AUTH_COOKIE, str(user_id), secret=AUTH_COOKIE_SECRET)
        services.db_helper.redirect_to_home(db)

